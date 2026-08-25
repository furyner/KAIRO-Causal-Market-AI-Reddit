# KAIRO Causal Market AI — Reddit API Integration

This repository contains public documentation for the planned Reddit Data API integration used by **KAIRO Causal Market AI**.

The production application is maintained separately. This public repository exists to document how Reddit data will be accessed, processed, and used.

## About the project

**KAIRO Causal Market AI** is a local Python desktop application for evidence-based market intelligence and causal analysis.

The application combines information from several independent data sources and tries to answer questions in the following form:

```text
WHAT HAPPENED
    ↓
WHY IT MAY MATTER
    ↓
MARKET REACTION
    ↓
POSSIBLE CAUSAL MECHANISM
    ↓
ALTERNATIVE EXPLANATIONS
    ↓
WHAT WOULD INVALIDATE THE INTERPRETATION
```

The project is designed for market research and monitoring. It does not place real financial-market orders.

## Application architecture

KAIRO is primarily a Python application built around:

- PySide6 desktop UI;
- local FastAPI backend;
- asynchronous external-data connectors;
- SQLite/WAL local persistence;
- source provenance tracking;
- news quality and deduplication;
- event extraction;
- market-data quality validation;
- event-reaction analysis;
- causal graph analysis;
- evidence retrieval and analytical reporting.

The application processes market and macroeconomic information from supported APIs and machine-readable feeds. Existing source categories include official government and central-bank publications, economic-data APIs, financial-market data, news indexes, YouTube Data API, and Telegram's official API.

Reddit is planned as an additional public social-discussion source.

## Purpose of the Reddit integration

The Reddit integration will be used to retrieve relevant **public discussions about financial markets, macroeconomics, commodities, and geopolitical events that may affect markets**.

Reddit content will be treated as a social signal and discussion source, not as an authoritative source of factual information.

Example topics include:

- Federal Reserve decisions;
- inflation and CPI releases;
- employment and NFP reports;
- Treasury yields;
- foreign exchange markets;
- gold and precious metals;
- crude oil and energy markets;
- stock indices and equities;
- geopolitical events affecting financial markets;
- changes in public market sentiment.

Public Reddit discussions may be displayed and analyzed together with independent market, economic, official, and news data.

## Intended subreddits

Initial public communities may include:

- `r/Forex`
- `r/Daytrading`
- `r/stocks`
- `r/investing`
- `r/StockMarket`

Additional public communities may be added when they are relevant to the same market-research purpose.

## Reddit data that may be accessed

The application intends to use Reddit's official OAuth/Data API to retrieve publicly available information such as:

- subreddit name;
- post ID;
- post title;
- public post body;
- post creation timestamp;
- permalink or canonical Reddit URL;
- public score and engagement metadata;
- public comments relevant to a selected discussion;
- comment timestamps;
- public identifiers required to process the API response.

Only information made available through officially authorized Reddit API endpoints will be used.

## Read-only usage

The initial Reddit integration is intended to operate in **read-only mode**.

The application is not designed to automatically:

- create posts;
- create comments;
- send private messages or chat messages;
- upvote or downvote content;
- manipulate engagement;
- mass-follow Reddit users;
- perform automated moderation actions;
- bypass subreddit restrictions;
- bypass Reddit authentication;
- scrape private information;
- use unauthorized HTML scraping as a substitute for the Reddit API.

## Example processing flow

```mermaid
flowchart LR
    A[Reddit Data API] --> B[Read-only Reddit Connector]
    B --> C[Normalization]
    C --> D[Market Relevance Filtering]
    D --> E[Deduplication]
    E --> F[Local Storage]
    F --> G[Evidence and Event Analysis]
    G --> H[KAIRO Desktop Interface]
```

A Reddit post or comment by itself is not treated as proof that an external event occurred.

## Source provenance

KAIRO is designed to preserve source provenance for information used in analysis.

Where applicable, a Reddit observation will retain the corresponding Reddit URL or public identifier so the original public discussion can be referenced.

Social-media observations remain distinguishable from primary official sources and established news sources. A social-media claim is not automatically converted into a verified fact.

## How Reddit data will be processed

Reddit data may be used to:

1. identify market-related public discussions;
2. filter irrelevant content from the analytical pipeline;
3. detect duplicated or substantially overlapping discussions;
4. associate discussions with relevant financial assets or macroeconomic topics;
5. compare public discussion with independent news, economic, official, and market data;
6. display relevant evidence in the local KAIRO desktop interface.

The purpose is market research and information organization.

## User profiling and private data

The Reddit integration is not intended to build personal profiles of individual Reddit users.

The analytical focus is on public market discussions and events, not on identifying sensitive attributes of Reddit users.

Private Reddit data is not required for this use case.

## No unauthorized Reddit scraping

KAIRO will not use unauthorized HTML scraping as a replacement for official Reddit API access.

The integration is specifically intended to use Reddit's authorized API and comply with applicable API access restrictions and rate limits.

If authorized API access is unavailable, Reddit ingestion will remain disabled.

## Why Devvit is not suitable for this application

KAIRO Causal Market AI is a standalone desktop application whose main processing environment operates outside Reddit.

The application needs to combine Reddit observations with independent external datasets, including:

- financial-market data;
- economic statistics;
- official government and central-bank publications;
- financial news and news indexes;
- other authorized social and media APIs.

The ingestion pipeline, local database, analytical engines, causal graph, and user interface all operate in the external Python application.

KAIRO is therefore not an embedded Reddit experience, subreddit application, or moderation tool.

External OAuth/Data API access is required so the local backend can retrieve authorized public Reddit data and process it together with the application's other evidence sources.

## API credentials

Reddit credentials will be provided to the application through environment variables:

```env
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=
```

Credentials and other secrets are not committed to source control.

## Current status

The Reddit connector is currently **planned and disabled pending official Reddit API authorization**.

The application does not attempt to bypass the requirement for approved API access.

After authorization, the connector will be implemented using Reddit's officially supported authentication and API mechanisms.

## Project summary

- **Application:** KAIRO Causal Market AI
- **Repository purpose:** Public documentation for Reddit API integration
- **Platform:** Local desktop application
- **Primary language:** Python
- **Backend:** FastAPI
- **Reddit access model:** OAuth / official Reddit Data API
- **Initial access:** Read-only
- **Primary use case:** Financial-market and macroeconomic research
