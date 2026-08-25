"""Restricted read-only Reddit Data API connector for KAIRO.

This module intentionally implements only the approved initial scope documented
in README.md and DATA_HANDLING.md.

Important boundaries:
- disabled by default;
- public submissions only;
- fixed subreddit allowlist;
- no comments, profiles, messaging, voting, moderation, or write actions;
- no HTML scraping fallback;
- application-level maximum of 5 requests/minute;
- output schema excludes author identity and post body;
- Reddit records returned here are for the local reading/discovery view only.
"""

from __future__ import annotations

import asyncio
import os
import time
from collections import deque
from dataclasses import dataclass
from typing import Any, Deque

import httpx


REDDIT_API_BASE = "https://oauth.reddit.com"
REDDIT_TOKEN_URL = "https://www.reddit.com/api/v1/access_token"

ALLOWED_SUBREDDITS = frozenset(
    {
        "Forex",
        "Daytrading",
        "stocks",
        "investing",
        "StockMarket",
    }
)

MAX_REQUESTS_PER_MINUTE = 5
MAX_POSTS_PER_REQUEST = 25
REQUEST_TIMEOUT_SECONDS = 15.0


class RedditConnectorError(RuntimeError):
    """Raised when the restricted Reddit connector cannot complete a request."""


@dataclass(frozen=True, slots=True)
class RedditDisplayPost:
    """Minimal Reddit record permitted to leave this connector.

    Deliberately omitted: author, selftext/body, user profile data, comments,
    flair text that could contain user-entered personal data, and any inferred
    user attributes.
    """

    post_id: str
    subreddit: str
    title: str
    created_utc: float
    permalink: str
    score: int

    @property
    def canonical_url(self) -> str:
        return f"https://www.reddit.com{self.permalink}"


class SlidingWindowRateLimiter:
    """Simple process-local sliding-window limiter."""

    def __init__(self, max_calls: int, window_seconds: float = 60.0) -> None:
        if max_calls < 1:
            raise ValueError("max_calls must be >= 1")
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self._calls: Deque[float] = deque()
        self._lock = asyncio.Lock()

    async def acquire(self) -> None:
        async with self._lock:
            while True:
                now = time.monotonic()
                cutoff = now - self.window_seconds
                while self._calls and self._calls[0] <= cutoff:
                    self._calls.popleft()

                if len(self._calls) < self.max_calls:
                    self._calls.append(now)
                    return

                sleep_for = self.window_seconds - (now - self._calls[0])
                await asyncio.sleep(max(sleep_for, 0.05))


class RedditReadOnlyConnector:
    """Narrow OAuth connector for recent public submissions only."""

    def __init__(self) -> None:
        self.enabled = os.getenv("REDDIT_API_ENABLED", "false").lower() == "true"
        self.client_id = os.getenv("REDDIT_CLIENT_ID", "").strip()
        self.client_secret = os.getenv("REDDIT_CLIENT_SECRET", "").strip()
        self.user_agent = os.getenv("REDDIT_USER_AGENT", "").strip()

        self._access_token: str | None = None
        self._token_expires_at = 0.0
        self._rate_limiter = SlidingWindowRateLimiter(MAX_REQUESTS_PER_MINUTE)

    def _validate_configuration(self) -> None:
        if not self.enabled:
            raise RedditConnectorError(
                "Reddit API integration is disabled. Set REDDIT_API_ENABLED=true "
                "only after official Reddit authorization is granted."
            )
        if not self.client_id or not self.client_secret or not self.user_agent:
            raise RedditConnectorError(
                "REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, and REDDIT_USER_AGENT are required."
            )
        if len(self.user_agent) < 8:
            raise RedditConnectorError("REDDIT_USER_AGENT must be descriptive.")

    @staticmethod
    def _validate_subreddit(subreddit: str) -> str:
        clean = subreddit.removeprefix("r/").strip()
        if clean not in ALLOWED_SUBREDDITS:
            raise RedditConnectorError(
                f"Subreddit r/{clean} is outside the approved initial allowlist."
            )
        return clean

    async def _get_access_token(self, client: httpx.AsyncClient) -> str:
        now = time.time()
        if self._access_token and now < self._token_expires_at - 60:
            return self._access_token

        await self._rate_limiter.acquire()
        response = await client.post(
            REDDIT_TOKEN_URL,
            auth=(self.client_id, self.client_secret),
            data={"grant_type": "client_credentials"},
            headers={"User-Agent": self.user_agent},
        )
        if response.status_code >= 400:
            raise RedditConnectorError(
                f"Reddit OAuth failed with HTTP {response.status_code}; no fallback scraping will be attempted."
            )

        payload = response.json()
        token = payload.get("access_token")
        if not token:
            raise RedditConnectorError("Reddit OAuth response did not include an access token.")

        expires_in = int(payload.get("expires_in", 3600))
        self._access_token = str(token)
        self._token_expires_at = now + max(expires_in, 60)
        return self._access_token

    async def fetch_new_posts(
        self,
        subreddit: str,
        *,
        limit: int = 25,
    ) -> list[RedditDisplayPost]:
        """Fetch recent public submissions from one approved subreddit.

        Only the `/new` listing is implemented. The method returns a minimal
        display schema and intentionally discards author identity and post body.
        """

        self._validate_configuration()
        clean_subreddit = self._validate_subreddit(subreddit)
        safe_limit = max(1, min(int(limit), MAX_POSTS_PER_REQUEST))

        async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT_SECONDS) as client:
            token = await self._get_access_token(client)
            await self._rate_limiter.acquire()
            response = await client.get(
                f"{REDDIT_API_BASE}/r/{clean_subreddit}/new",
                params={"limit": safe_limit, "raw_json": 1},
                headers={
                    "Authorization": f"Bearer {token}",
                    "User-Agent": self.user_agent,
                },
            )

        if response.status_code == 429:
            raise RedditConnectorError("Reddit rate limit reached; request stopped.")
        if response.status_code >= 400:
            raise RedditConnectorError(
                f"Reddit API request failed with HTTP {response.status_code}; no scraping fallback will be attempted."
            )

        return self._parse_listing(response.json(), expected_subreddit=clean_subreddit)

    @staticmethod
    def _parse_listing(payload: dict[str, Any], *, expected_subreddit: str) -> list[RedditDisplayPost]:
        posts: list[RedditDisplayPost] = []
        children = payload.get("data", {}).get("children", [])

        for child in children:
            data = child.get("data", {}) if isinstance(child, dict) else {}
            subreddit = str(data.get("subreddit", ""))
            if subreddit != expected_subreddit:
                continue

            post_id = str(data.get("id", "")).strip()
            title = str(data.get("title", "")).strip()
            permalink = str(data.get("permalink", "")).strip()
            if not post_id or not title or not permalink.startswith("/r/"):
                continue

            posts.append(
                RedditDisplayPost(
                    post_id=post_id,
                    subreddit=subreddit,
                    title=title,
                    created_utc=float(data.get("created_utc", 0.0) or 0.0),
                    permalink=permalink,
                    score=int(data.get("score", 0) or 0),
                )
            )

        return posts


async def example() -> None:
    """Manual example. This does nothing while access is disabled."""

    connector = RedditReadOnlyConnector()
    posts = await connector.fetch_new_posts("Forex", limit=10)
    for post in posts:
        print(post.title, post.canonical_url)


if __name__ == "__main__":
    asyncio.run(example())
