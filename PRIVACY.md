# Privacy Policy — Reddit Integration

This privacy notice applies only to the Reddit connector contained in this repository.

## Purpose

The connector exists to let a single local user discover recent public financial-market discussions from a small predefined set of public Reddit communities and open the original discussion on Reddit.

## Data minimization

The connector is designed to collect the minimum information needed for that reading view.

It may temporarily retain:

- Reddit submission ID;
- subreddit name;
- submission title;
- creation timestamp;
- Reddit permalink;
- public score;
- local cache timestamp.

It does not intentionally collect or retain Reddit usernames, user profile histories, private messages, chats, private-community data, email addresses, IP addresses, or other private user information.

## Sensitive profiling

The connector does not build personal profiles of Redditors and does not attempt to infer an individual's political beliefs, financial condition, health information, religion, race or ethnicity, sexual orientation, or other sensitive attributes.

## Retention

Reddit records are stored only in a temporary local cache for a maximum of 24 hours and are automatically purged.

The connector is not designed to maintain a historical Reddit archive.

## AI processing

Reddit content retrieved by this connector is not used for AI or machine-learning training, fine-tuning, benchmarking, or evaluation.

It is not sent to third-party LLM providers and is not stored in an embeddings or vector database.

## Disclosure and sale

Reddit data collected by this connector is not sold, licensed, or redistributed as a dataset and is not exposed through a public API.

The integration is intended for a single-user local desktop application.

## Reddit source attribution

The original Reddit permalink is retained so the user can return to Reddit for the source discussion.

## Security

Reddit API credentials are loaded from environment variables and must not be committed to source control.

The connector is disabled by default and should be enabled only after official Reddit API authorization has been granted.

## Access changes

If Reddit authorization is unavailable or revoked, data collection stops. The connector does not use unauthorized scraping as a substitute.

## Scope changes

Any future change involving broader data access, comments, user-level data, commercial redistribution, AI/ML processing, or substantially higher request volume must be reviewed separately before deployment.
