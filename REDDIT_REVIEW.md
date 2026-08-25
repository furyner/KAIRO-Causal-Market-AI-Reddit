# Reddit Review Summary

This page is a concise reviewer-oriented summary of the requested integration.

## Applicant use case

KAIRO Causal Market AI is a local Python desktop application. The requested Reddit integration is a single-user, non-commercial, read-only connector used to discover recent public market-related submissions and open the original discussions on Reddit.

## Requested access

The initial connector requests only authenticated read access to recent public submissions from:

- r/Forex
- r/Daytrading
- r/stocks
- r/investing
- r/StockMarket

The connector implements only the `new` listing for those communities.

## What the connector does not do

It does not:

- create posts or comments;
- vote;
- send messages or chats;
- perform moderation actions;
- access private communities;
- retrieve user profile histories;
- persist usernames;
- collect comments in the initial scope;
- crawl arbitrary communities;
- create historical archives;
- use unauthorized HTML scraping;
- circumvent Reddit rate limits;
- use multiple accounts to increase collection volume.

## Minimal data schema

The local display/cache schema contains only:

- post ID;
- subreddit;
- title;
- creation time;
- Reddit permalink;
- public score;
- local cache timestamp.

Author identity and post body are deliberately excluded from the persisted schema.

## Retention

Maximum local retention is 24 hours.

Expired records are automatically deleted. The application can also remove a known post immediately if deletion/unavailability is detected.

## AI / ML boundary

Reddit content retrieved by this connector is not used for model training, fine-tuning, benchmarking, evaluation, embeddings, vector storage, or third-party LLM processing.

The Reddit reading connector is separated from KAIRO analytical pipelines that operate on other independently authorized sources.

## Data budget

- maximum application-level rate: 5 requests/minute;
- planned total: less than 1,000 Reddit API requests/day;
- no historical bulk crawling;
- no dataset export.

## Redditor benefit

The integration helps a Reddit user organize recent public financial-market discussions from communities they already follow and preserves a direct permalink to the original Reddit discussion for context and participation on Reddit.

## Why the application is external

KAIRO is an existing local desktop application built with Python/PySide6 and a local backend. It is not a subreddit application, moderation tool, interactive Reddit post, or Reddit-hosted experience. The requested access is therefore limited authenticated read access for the existing external local application.

## Authorization behavior

The Reddit connector ships disabled by default. If official Reddit API authorization is not available, it remains disabled and no scraping fallback is used.
