# DXP and CRM integration

## Goal

Connecting a digital experience platform (DXP) to a customer relationship management (CRM) system lets the website capture leads, recognize known customers and show relevant content. The challenge is doing this with clean data, clear ownership and respect for consent.

## Common integration patterns

1. **Form to CRM:** a website form posts to a middleware endpoint that validates the data and creates or updates a lead or contact.
2. **Webhook or event-driven:** the CRM emits events (for example, lead status changed), and the DXP reacts by updating content or triggering workflows.
3. **Batch sync:** scheduled exports move audience lists between systems. Simple, but data can be stale.
4. **Real-time lookup:** the site queries a profile service at request time. Powerful, but latency and availability become critical.

## Use middleware

Avoid connecting the browser directly to the CRM. A small serverless or edge function can:

- Hide credentials and API keys.
- Validate and sanitize inputs.
- Add rate limiting and bot protection.
- Map website fields to CRM fields.
- Retry failed requests and log errors.

## Data mapping

Create a mapping table before writing code:

| Website field | CRM field | Required | Notes |
| --- | --- | --- | --- |
| email | Email | yes | Lowercase and trim |
| company | Account name | no | Free text |
| consent_marketing | Opt-in flag | yes | Store timestamp and policy version |
| utm_campaign | Campaign source | no | Captured from URL |

Agree on identifiers. Email is common, but a stable customer ID is better once a user is authenticated.

## Consent and privacy

Store what the visitor agreed to, when and where. Do not use data for purposes the visitor did not consent to. Support deletion and access requests across both systems.

## Deduplication and quality

- Match on a normalized email before creating new records.
- Define which system wins for each field.
- Validate formats at the edge, not only in the CRM.
- Monitor bounce rates and sync errors.

## Authentication and security

Use OAuth or scoped API tokens, rotate secrets regularly and keep them in a secret store. Apply least privilege: the integration should only create and update the objects it needs.

## Reliability

- Make operations idempotent so retries do not create duplicates.
- Queue submissions if the CRM is unavailable.
- Alert on error rates, not only on total failures.
- Provide a manual recovery path for lost leads.

## Operating model

Name an owner on both the marketing and the technical side. Version the field mapping, test changes in a sandbox, and document the flow with a sequence diagram so new team members understand it quickly.
