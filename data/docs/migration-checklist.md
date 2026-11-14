# CMS migration checklist

A migration succeeds or fails on preparation. Use this checklist as a starting point and adapt it to your platform, content volume and governance model.

## 1. Discovery and inventory

- Export a full URL list from the current CMS, sitemap and analytics.
- Classify pages by template, traffic, last-modified date and owner.
- Identify content that is duplicated, outdated or legally required.
- Record integrations: search, forms, commerce, CRM, consent, analytics and SSO.

## 2. Content strategy

- Decide what to migrate, what to rewrite and what to retire.
- A common rule of thumb: retire anything with no traffic and no business purpose for twelve months.
- Define the target content model: page types, reusable blocks and metadata fields.
- Agree on naming, folder structure and URL conventions.

## 3. URL and SEO plan

- Map every old URL to a new URL or an explicit 410.
- Prepare a redirect file and test it in bulk before go-live.
- Preserve titles, descriptions, canonical tags and structured data.
- Keep hreflang annotations consistent across language versions.
- Plan a new XML sitemap and submit it after launch.

## 4. Technical migration

- Choose an import approach: scripted conversion, manual copy for key pages, or a hybrid.
- Normalize HTML: remove inline styles, deprecated tags and tracking leftovers.
- Move media to the new DAM or content store and keep alt text.
- Validate that internal links point to the new structure rather than the legacy domain.

## 5. Governance and people

- Name a content owner for every section.
- Train authors on the new authoring experience before cutover.
- Define publishing workflows, approvals and roles.
- Document escalation paths for launch week.

## 6. Quality assurance

- Compare a sample of pages visually and structurally against the original.
- Run link, accessibility and performance checks automatically.
- Verify forms, search and integrations end to end.
- Test consent banners and analytics tags on the new pages.

## 7. Cutover

- Freeze content changes in the legacy CMS for an agreed window.
- Lower DNS TTL in advance, and keep a rollback plan.
- Launch during a low-traffic period with the team on call.
- Monitor errors, 404s and Core Web Vitals in the first 72 hours.

## 8. Post-launch

- Review 404 reports weekly and add missing redirects.
- Compare organic traffic and conversions with the baseline.
- Decommission the legacy system only after a defined stabilization period.
- Run a retrospective and update this checklist.

## Typical risks

| Risk | Mitigation |
| --- | --- |
| Lost SEO equity | Complete redirect map, early crawl tests |
| Scope creep | Fixed template list and change control |
| Author resistance | Early training and quick wins |
| Hidden integrations | Inventory based on network traces, not only documentation |
