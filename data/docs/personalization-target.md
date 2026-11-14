# Personalization with Adobe Target

## Purpose

Personalization adapts content to the visitor's context, while experimentation measures whether the change helps. Adobe Target supports both: A/B tests, experience targeting (XT), automated personalization and recommendations.

## Core concepts

- **Activity:** the test or personalization campaign.
- **Experience:** a variant shown to a segment of visitors.
- **Audience:** rules that define who qualifies, such as device, geography or a profile attribute.
- **Mbox / decision scope:** a named location where Target decides what to show.
- **Metric:** the goal, such as clicks, form submissions or revenue.

## Client-side and server-side delivery

With the Web SDK or at.js, Target can modify the page in the browser. This is flexible but risks flicker if the page renders before the decision arrives. Server-side or edge-based decisioning avoids flicker and fits well with fast static delivery, at the cost of more engineering.

Prefer decisions that return structured content (JSON) rather than raw HTML. Your code then renders the offer using approved components.

## Avoiding flicker and performance loss

- Apply the decision to content below the fold whenever possible.
- Do not personalize the largest contentful element unless you must.
- Use a short timeout and fall back to default content.
- Keep the personalization script out of the critical path.

## Audiences that work

Start simple:

1. New versus returning visitors.
2. Traffic source or campaign parameter.
3. Logged-in status or account tier supplied by your own systems.
4. Role or interest, inferred from explicit choices rather than guesses.

More complex, behavior-based models need enough traffic and clean data.

## Experiment hygiene

- Write a hypothesis: "Changing X for Y will improve Z because..."
- Pick one primary metric before launching.
- Calculate sample size and run for full business cycles, usually at least two weeks.
- Do not stop early because of a promising trend.
- Document the outcome, including failed tests.

## Consent and privacy

Personalization based on identifiers or behavior generally requires consent. When consent is missing, show the default experience. Do not store sensitive attributes in profiles or send them to Target.

## Governance

Create a naming convention for activities and audiences, assign owners and retire old activities. A quarterly review keeps the library clean and avoids conflicting experiences.

## Quick start checklist

- Consent signal available before Target runs.
- Default content defined for every personalized location.
- Metrics and audiences agreed with stakeholders.
- QA performed on all variants and devices.
- Rollback procedure documented.
