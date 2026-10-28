# Proposed architecture

## Design principles

1. **Policy before persona.** System safety, user authorization, and organizational permissions cannot be overwritten by behavioral traits.
2. **Episodes over lore.** Every stored lesson links to an actual simulated or real observed event and its provenance.
3. **Behavior over adjectives.** A trait is meaningful only when it predicts an action on unseen cases.
4. **Separation of training and testing.** Held-out scenarios cannot enter memory, retrieval, or reflection during training.
5. **Reversibility.** Learned preferences are versioned, inspectable, and can be rolled back; critical permissions are not learned.

## Components

| Component | Responsibility | Critical boundary |
| --- | --- | --- |
| Role specification | Job objectives, KPIs, permitted tools | Authority never inferred from personality |
| Scenario bank | Disjoint situation families and hidden tests | Prevent train/test leakage |
| Action policy | Selects a response or tool action | Hard constraints enforced externally |
| Environment | Resolves effects and consequences | Distinguish deterministic rules from LLM speculation |
| Evaluator | Scores task success and policy compliance | Independent of actor where possible |
| Episode store | Records evidence, outcomes, feedback | Tenant isolation and provenance |
| Reflection engine | Proposes behavioral principles and contradictions | Reflection is a hypothesis, not ground truth |
| Profile store | Holds compact, versioned Decision DNA | Human review for consequential changes |
| Retrieval layer | Selects relevant lessons at runtime | Scope, recency, confidence, and token limits |
| Audit and rollback | Reproduces a decision and its context | Immutable versions of critical changes |

## Example data contracts (illustrative)

### Episode

```json
{
  "episode_id": "ep-001",
  "source": "synthetic_simulation",
  "role": "sales_representative",
  "scenario_family": "discount_authority",
  "observation": "Customer asks for a discount beyond the approved limit.",
  "action": "offer_authorized_alternatives",
  "outcome": {"customer_retained": true, "policy_violation": false},
  "evaluator": {"type": "rule_based", "version": "0.1"},
  "lesson": "Negotiate within authority and escalate only when justified.",
  "confidence": 0.8
}
```

The sample outcome is fictitious and does not represent observed performance.

### Versioned behavioral profile

```json
{
  "profile_version": "0.1.0",
  "role": "sales_representative",
  "foundation_model": "model-identifier-recorded-separately",
  "traits": [
    {
      "name": "negotiation_within_authority",
      "description": "Offers permitted alternatives before escalating.",
      "supporting_episodes": ["ep-001"],
      "confidence": 0.8
    }
  ],
  "known_failure_cases": [],
  "approval_status": "research_only"
}
```

The numbers are schema examples, not psychometrically validated trait scores.

## Runtime decision sequence

1. Parse task and current context.
2. Resolve permitted scope and governing constraints.
3. Retrieve a small set of relevant episodes with provenance.
4. Include validated behavioral principles and known exceptions.
5. Propose an action and calibrate uncertainty.
6. Check permission and policy constraints before any external side effect.
7. Execute or ask for approval, then capture actual outcome and feedback.
8. Queue candidate updates; do not silently let a single interaction rewrite the identity.

## Memory lifecycle

- **Write:** preserve important events with outcomes, source types, timestamps, consent, and confidence.
- **Consolidate:** identify recurring rules and exceptions; do not collapse contradictory evidence into a neat fiction.
- **Retrieve:** rank by task relevance, evidential reliability, novelty, and recency.
- **Decay:** lower retrieval priority for weak or obsolete experiences, without erasing critical compliance and failure evidence.
- **Correct:** support explicit feedback, appeal, rollback, and tenant-scoped deletion.

## Main failure modes

- **Self-confirming simulation:** one model generates an action, its consequence, and its reward.
- **Persona collapse:** agents with distinct history return to the same default policy on unseen tasks.
- **Reward hacking:** the agent optimizes score instead of the real organizational objective.
- **Authority drift:** an agent treats synthetic success as permission to act.
- **Context confounding:** longer prompts, not experiences, explain an apparent gain.
- **Memory contamination:** test scenarios or private customer information leak into training.
- **Unbounded cost:** multiple model calls per simulated step make the economics unattractive.

An effective implementation must measure these failure modes rather than hide them.

