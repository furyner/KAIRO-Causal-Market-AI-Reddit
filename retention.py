"""Temporary local cache for the restricted Reddit connector.

The cache has a hard maximum TTL of 24 hours and stores only the minimal display
schema emitted by reddit_connector.RedditDisplayPost.
"""

from __future__ import annotations

import sqlite3
import time
from pathlib import Path
from typing import Iterable

from reddit_connector import RedditDisplayPost


CACHE_TTL_SECONDS = 24 * 60 * 60


class RedditTemporaryCache:
    def __init__(self, path: str | Path = "reddit_cache.sqlite3") -> None:
        self.path = Path(path)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        return connection

    def _init_db(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS reddit_posts (
                    post_id TEXT PRIMARY KEY,
                    subreddit TEXT NOT NULL,
                    title TEXT NOT NULL,
                    created_utc REAL NOT NULL,
                    permalink TEXT NOT NULL,
                    score INTEGER NOT NULL,
                    cached_at REAL NOT NULL
                )
                """
            )
            connection.execute(
                "CREATE INDEX IF NOT EXISTS idx_reddit_posts_cached_at ON reddit_posts(cached_at)"
            )

    def purge_expired(self, *, now: float | None = None) -> int:
        current = time.time() if now is None else float(now)
        cutoff = current - CACHE_TTL_SECONDS
        with self._connect() as connection:
            cursor = connection.execute(
                "DELETE FROM reddit_posts WHERE cached_at <= ?",
                (cutoff,),
            )
            return int(cursor.rowcount or 0)

    def upsert(self, posts: Iterable[RedditDisplayPost]) -> int:
        """Store minimal records and immediately enforce the 24-hour TTL."""

        self.purge_expired()
        cached_at = time.time()
        rows = [
            (
                post.post_id,
                post.subreddit,
                post.title,
                post.created_utc,
                post.permalink,
                post.score,
                cached_at,
            )
            for post in posts
        ]
        if not rows:
            return 0

        with self._connect() as connection:
            connection.executemany(
                """
                INSERT INTO reddit_posts (
                    post_id, subreddit, title, created_utc, permalink, score, cached_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(post_id) DO UPDATE SET
                    subreddit = excluded.subreddit,
                    title = excluded.title,
                    created_utc = excluded.created_utc,
                    permalink = excluded.permalink,
                    score = excluded.score,
                    cached_at = excluded.cached_at
                """,
                rows,
            )
        return len(rows)

    def list_recent(self, *, subreddit: str | None = None) -> list[RedditDisplayPost]:
        self.purge_expired()
        query = (
            "SELECT post_id, subreddit, title, created_utc, permalink, score "
            "FROM reddit_posts"
        )
        params: tuple[object, ...] = ()
        if subreddit:
            query += " WHERE subreddit = ?"
            params = (subreddit.removeprefix("r/").strip(),)
        query += " ORDER BY created_utc DESC"

        with self._connect() as connection:
            rows = connection.execute(query, params).fetchall()

        return [
            RedditDisplayPost(
                post_id=row["post_id"],
                subreddit=row["subreddit"],
                title=row["title"],
                created_utc=float(row["created_utc"]),
                permalink=row["permalink"],
                score=int(row["score"]),
            )
            for row in rows
        ]

    def delete_post(self, post_id: str) -> bool:
        """Delete a known record immediately, for example after deletion is detected."""

        with self._connect() as connection:
            cursor = connection.execute(
                "DELETE FROM reddit_posts WHERE post_id = ?",
                (post_id,),
            )
            return bool(cursor.rowcount)

    def clear(self) -> int:
        """Delete all locally cached Reddit records."""

        with self._connect() as connection:
            cursor = connection.execute("DELETE FROM reddit_posts")
            return int(cursor.rowcount or 0)
