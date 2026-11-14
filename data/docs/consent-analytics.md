# Consent and analytics basics

## Why consent comes first

Analytics and personalization tools process personal data, such as identifiers, IP addresses and behavioral events. In the EU and UK, the ePrivacy rules and the GDPR generally require informed, prior consent before non-essential cookies or similar technologies are set. Other regions have their own rules, so confirm requirements with legal counsel.

## Categories of tracking

- **Strictly necessary:** session handling, load balancing, security. No consent needed.
- **Preferences:** language or layout choices.
- **Analytics:** measuring traffic and behavior.
- **Marketing:** advertising, retargeting and cross-site profiles.

Map each tag on your site to one of these categories and document the purpose.

## A consent management platform (CMP)

A CMP shows the banner, stores the visitor's choices and exposes them to your code. Good practice:

- Make "Reject" as easy as "Accept".
- Do not preselect optional categories.
- Store a timestamp and a policy version with each decision.
- Let visitors change their choice at any time through a persistent link.

## Gating tags

The rule is simple: no consent, no tag. Implement it with a tag manager or an event-driven approach:

1. Load only the CMP and essential code initially.
2. Listen for the consent event.
3. When the analytics category is granted, load the analytics library.
4. When it is revoked, stop sending events and clear related cookies where possible.

On performance-focused platforms, load the CMP early enough to avoid a flash of unconsented tracking, but keep analytics in the delayed phase to protect Core Web Vitals.

## Consent Mode and modeled data

Some analytics tools support signalling consent state and use aggregated or modeled data when consent is denied. This can reduce reporting gaps, but it does not replace the need to respect the visitor's choice. Check the vendor's current documentation.

## Measurement design

- Define a measurement plan with business questions first, then events.
- Use a consistent naming convention, for example `object_action` such as `form_submit`.
- Keep a data layer or event schema documented and versioned.
- Avoid sending personal data (emails, names) as event parameters.

## Data minimization and retention

Collect only what you need. Set retention periods in the analytics tool, anonymize IP addresses where supported, and review access regularly.

## Server-side considerations

Moving tags server-side can improve control and performance, but it does not remove the legal need for consent. Treat it as an architecture choice, not a compliance shortcut.

## Testing checklist

- Visit the site in a clean browser profile and confirm no analytics requests before consent.
- Accept, then verify events fire as expected.
- Reject or withdraw, then verify requests stop.
- Test on mobile and with ad blockers enabled.
- Re-test after every banner or tag change.
