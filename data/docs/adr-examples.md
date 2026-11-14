# Architecture Decision Records: examples

An Architecture Decision Record (ADR) captures one significant decision, its context and its consequences. Keep ADRs short, numbered and immutable: if a decision changes, write a new ADR that supersedes the old one.

## Template

```
# ADR-000: Title
Status: Proposed | Accepted | Superseded by ADR-xxx
Date: YYYY-MM-DD
Context: forces and constraints
Decision: what we chose
Consequences: benefits, costs, risks
```

## ADR-001: Use plain JavaScript and CSS for blocks

**Status:** Accepted

**Context:** The team needs fast pages and low maintenance. Authors work in documents, and developers want minimal tooling.

**Decision:** Build blocks with native JavaScript modules and CSS, without a framework or a mandatory build step.

**Consequences:** Smaller payloads and simpler onboarding. Complex interactive widgets need extra care, and some developers may miss framework conveniences.

## ADR-002: Load analytics only after consent

**Status:** Accepted

**Context:** Legal requirements and brand trust demand that non-essential tracking waits for the visitor's choice.

**Decision:** Load the consent platform first. Analytics and personalization libraries are loaded in the delayed phase and only when the matching category is granted.

**Consequences:** Some early-session data is lost, and reporting must account for it. Compliance risk and Core Web Vitals impact drop.

## ADR-003: Group-based access to content with a simple hierarchy in the lab

**Status:** Accepted for the lab

**Context:** The lab needs to demonstrate that retrieval respects who is asking. Each document has a minimum group in its metadata.

**Decision:** Use a linear hierarchy `public < partner < internal`. A user can retrieve a document when their group is greater than or equal to the document's `min_group`. Filtering happens before generation, at retrieval time.

**Consequences:** Easy to explain and test. It cannot express overlapping teams or exceptions. In production, replace it with real ACLs per group, synchronized with the identity provider.

## ADR-004: Personalize by audience metadata, not by guessing

**Status:** Accepted

**Context:** Content should fit developers and marketers, but inferring role from behavior is unreliable and raises privacy concerns.

**Decision:** Use an explicit `audience` attribute (`developer`, `marketer`, `all`) on content and an explicit role chosen or provided by the user.

**Consequences:** Predictable and auditable personalization. Users who do not set a role receive neutral content.

## Writing good ADRs

- Record alternatives you rejected and why.
- State the status and date.
- Link to related ADRs.
- Review ADRs in pull requests like code.
- Keep them in the repository, near the code they affect.
