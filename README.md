# KAIRO Causal Market AI — Reddit Read-Only Integration

This repository contains the public, auditable implementation and data-handling documentation for the planned Reddit Data API connector used by **KAIRO Causal Market AI**.

The Reddit connector is intentionally narrow. It is designed for a **single-user, non-commercial, local desktop application** and is disabled unless official Reddit API authorization has been granted.

## Purpose

KAIRO Causal Market AI is a local Python desktop application used to organize financial-market and macroeconomic information from multiple independently authorized sources.

The Reddit integration has one limited purpose: **show recent public market-related submissions from a small predefined set of public subreddits so the user can discover and open the original discussion on Reddit.**

Reddit content is not treated as authoritative evidence of an external event.

## Initial Reddit scope

The connector is restricted to these public communities:

- `r/Forex`
- `r/Daytrading`
- `r/stocks`
- `r/investing`
- `r/StockMarket`

The initial implementation retrieves only recent public submissions from the `new` listing.

It does **not** crawl arbitrary subreddits or perform historical bulk collection.

## Data accessed

The connector requests only the fields required for a small local reading/discovery view:

- submission ID;
- subreddit name;
- submission title;
- creation timestamp;
- Reddit permalink;
- public score/engagement count required for display.

The initial connector does **not** retrieve or persist:

- private Reddit data;
- private messages or chats;
- user profile data;
- user history;
- email addresses;
- IP addresses;
- moderator-only information;
- subscriber lists;
- comment bodies;
- submission author profiles;
- sensitive user attributes.

## Read-only behavior

The connector does not:

- create posts;
- create comments;
- vote;
- send messages;
- follow users;
- perform moderation actions;
- automate engagement;
- access private communities;
- bypass authentication;
- bypass rate limits;
- use HTML scraping as a substitute for the authorized Reddit API.

## No user profiling

The Reddit integration does not build profiles of Reddit users.

It does not attempt to infer or classify an individual's:

- political beliefs;
- financial condition;
- health information;
- race or ethnicity;
- religion;
- sexual orientation;
- other sensitive personal characteristics.

The analytical focus is on public market topics, not on individual Redditors.

## AI / machine-learning restriction

Reddit content retrieved by this connector is **not used to train, fine-tune, benchmark, or evaluate AI or machine-learning models**.

The connector also does not send stored Reddit content to third-party LLM services and does not place Reddit content into an embeddings or vector database.

The implementation exposes a deliberately limited display record for the local Reddit reading view and the original Reddit permalink.

KAIRO may use AI functionality with other independently licensed or authorized data sources, but this Reddit connector is separated from those pipelines.

## Local retention

Reddit data is stored only in a temporary local cache.

- maximum cache TTL: **24 hours**;
- expired records are removed automatically;
- the connector does not create a historical Reddit archive;
- source provenance is preserved using the Reddit submission ID and permalink;
- if Reddit access is disabled, no new Reddit content is collected.

See [DATA_HANDLING.md](DATA_HANDLING.md) and [PRIVACY.md](PRIVACY.md).

## Rate limits and data budget

This implementation deliberately applies limits below Reddit's published platform limits:

- application limit: **5 requests per minute**;
- planned daily budget: **less than 1,000 Reddit API requests per day**;
- no bulk exports;
- no historical crawling;
- no multi-account sharding or rate-limit circumvention.

The connector also respects Reddit API responses and rate-limit errors.

## Reddit attribution

Every displayed record retains a Reddit permalink so the user can open the original discussion on Reddit.

Reddit remains clearly identified as the source. The application does not present Reddit content as its own publication.

## Why Devvit is not the requested execution environment

KAIRO is an existing standalone Python desktop program built around a local PySide6 interface and local backend. Its user interface, local cache, and non-Reddit data connectors execute on the user's computer.

It is not a subreddit application, interactive Reddit post, moderation tool, or Reddit-hosted experience.

The requested integration therefore requires narrowly scoped, authenticated, read-only access for an external local application. If Reddit determines that a different developer product is required, the connector will remain disabled until the appropriate authorization is available.

## Security

Credentials are supplied through environment variables and are never committed to source control.

```env
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=
REDDIT_USER_AGENT=
REDDIT_API_ENABLED=false
```

`REDDIT_API_ENABLED` defaults to `false`.

## Repository files

- `reddit_connector.py` — read-only OAuth connector with subreddit allowlist and application-level rate limiting;
- `retention.py` — temporary SQLite cache with a hard 24-hour TTL;
- `.env.example` — example configuration with access disabled by default;
- `DATA_HANDLING.md` — exact data lifecycle and restrictions;
- `PRIVACY.md` — privacy commitments for the Reddit integration;
- `requirements.txt` — minimal Python dependency list.

## Example flow

```text
Authorized Reddit Data API
        |
        v
Read-only connector
        |
        v
Fixed subreddit allowlist
        |
        v
Minimal field extraction
        |
        v
24-hour local cache
        |
        v
Local Reddit reading view
        |
        +----> Original Reddit permalink
```

There is no Reddit-to-LLM, Reddit-to-training, Reddit-to-embeddings, automated posting, or user-profiling path in this connector.

## Current status

The connector is **disabled pending official Reddit API authorization**.

If authorization is not granted, Reddit ingestion remains disabled. The project does not attempt to replace denied API access with unauthorized scraping or another circumvention method.

## Project summary

- **Application:** KAIRO Causal Market AI
- **Integration:** Reddit read-only public-submission discovery
- **Platform:** local Python desktop application
- **Access model:** official Reddit OAuth / Data API only
- **Users:** single user
- **Commercial status of this integration:** non-commercial
- **Writes to Reddit:** none
- **User profiling:** none
- **Comments:** not accessed in the initial scope
- **Cache TTL:** 24 hours
- **Application rate limit:** 5 requests/minute
- **Planned daily budget:** <1,000 requests/day
- **AI training/fine-tuning with Reddit data:** prohibited
- **Third-party LLM processing of Reddit data:** prohibited
