# Reddit Data Handling Policy

This document describes the data lifecycle for the Reddit connector in this repository.

## Scope

The integration is limited to recent public submissions from the following public subreddits:

- r/Forex
- r/Daytrading
- r/stocks
- r/investing
- r/StockMarket

Only the `new` listing is implemented in the initial connector.

## Fields retained temporarily

The local cache may contain only:

- Reddit submission ID;
- subreddit;
- title;
- creation timestamp;
- Reddit permalink;
- public score;
- cache timestamp.

The connector deliberately excludes author identity and submission body from the record that is persisted.

## Fields not collected by the initial connector

The initial implementation does not collect or persist:

- comment bodies;
- private messages;
- chats;
- user profiles;
- user histories;
- email addresses;
- IP addresses;
- private-community content;
- moderator-only data;
- subscriber lists;
- inferred sensitive user attributes.

## Retention

The local cache has a maximum TTL of 24 hours.

Expired records are deleted automatically by `retention.py` whenever the cache is read or updated. The cache can also be cleared manually.

The integration is not intended to create a historical Reddit archive.

If a cached submission is known to have been deleted or otherwise made unavailable on Reddit before the TTL expires, the application can remove it immediately by submission ID.

## AI and machine learning

Reddit content retrieved by this connector must not be:

- used to train or fine-tune a model;
- used to benchmark or evaluate a model;
- added to an embeddings or vector database;
- sent to a third-party LLM service;
- used to build user-level behavioral or political profiles.

The Reddit connector is separated from KAIRO AI/ML pipelines that operate on other independently authorized data sources.

## Sharing and redistribution

Reddit content retrieved through this connector is for the local single-user reading view only.

It is not:

- sold;
- licensed;
- redistributed as a dataset;
- exposed through a public API;
- provided as a bulk export;
- mirrored as an independent Reddit archive.

The original Reddit permalink is retained so the user can open the source discussion on Reddit.

## Rate limiting

The connector enforces an application-level maximum of 5 requests per minute and a planned daily budget below 1,000 requests.

It does not use multiple accounts, proxies, credential rotation, or other techniques to circumvent Reddit limits.

## Failure behavior

If official Reddit API authorization is unavailable, revoked, or disabled, the connector stops collecting Reddit data.

There is no HTML-scraping fallback.

## Credentials

Credentials are supplied only through environment variables. Secrets must never be committed to this repository, logs, screenshots, or bug reports.

## Changes to scope

Any material expansion of the Reddit integration — including comments, additional communities, higher request volume, user-level data, commercial use, AI/ML processing, or redistribution — requires a new compliance review and, where required, additional Reddit authorization before implementation.
