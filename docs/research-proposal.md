# Research proposal: Decision DNA

**Working title:** Experience-Conditioned Identity for Autonomous AI Employees  
**Status:** Pre-experiment protocol draft, 29 October 2026

## Abstract

Foundation-model agents can be given verbal personas, but such descriptions may not produce stable behavior across contexts or work tasks. We propose **Decision DNA**, an agent architecture that records simulated decisions, modeled consequences, explicit feedback, and behavioral reflections, then selectively conditions future decisions on the resulting experience history. We propose a controlled comparison against role-only and static-persona agents using held-out professional dilemmas in sales, support, and operations. The primary outcome is task success under organizational constraints; secondary outcomes include policy violations, decision consistency, escalation quality, cost, latency, and cross-model transfer. This document specifies hypotheses and methodology only. It contains no empirical findings.

## Motivation

Writing "be proactive and empathetic" does not ensure appropriate choices under conflicting objectives. A durable agent identity might instead be expressed as a compact, evidence-linked behavioral policy learned from prior situations. Crucially, **stored simulated episodes are not real experience**, and repeated API calls do not update model parameters unless an explicit training or memory-conditioning mechanism is used.

## Hypotheses

- **H1 (useful generalization):** A consequence-conditioned experience history improves held-out task success over an equally detailed static persona with the same model and tool budget.
- **H2 (consistency):** The experience-conditioned agent applies the same organizational principles more consistently across paraphrased and adversarial situations.
- **H3 (differentiation):** Distinct curated professional histories induce measurably differentiated decision policies while preserving safety constraints.
- **H4 (transfer):** Reusing a history with a different foundation model retains some measurable advantage over the new model's corresponding static baseline.

All hypotheses are prospective and may be disproved.

## Experimental protocol

### Conditions

1. **Role-only**: job description, objectives, tools, constraints.
2. **Static persona**: role-only plus a detailed profile of disposition and preferences, approximately matched to the length of C's compacted profile.
3. **Decision DNA**: role-only plus relevant retrieved simulated episodes, versioned reflections, and behavioral preferences.

Hold the base model, temperature, tool access, latency budget, authority boundaries, and evaluator rules fixed within each comparison. A fourth ablation can include unevaluated synthetic episodes to isolate the benefit of consequences and feedback.

### Data

- Start with **300 training scenarios** across professional roles and **100 unseen held-out scenarios**, as provisional sample sizes.
- Partition by **scenario family**, not merely paraphrase, to reduce leakage.
- Include dilemma classes such as conflicting KPIs, discount authority, customer confidentiality, misleading claims, uncertain evidence, delegation, service recovery, time pressure, and escalation.
- Include paired paraphrases and counterfactuals with the same governing principle but different incidental details.
- Make relevant constraints machine-readable and auditable.
- Review scenario quality and scoring criteria before agent outputs are generated.

### Simulation loop

1. Present an observation and available authorized actions.
2. Record action, confidence, and concise user-facing justification.
3. Apply environment rules and optionally a separately configured simulator to generate plausible outcomes.
4. Score against independent policy and task-success criteria; flag ambiguities rather than inventing certainty.
5. Write an episode with source, outcome, feedback, and evaluator provenance.
6. Produce candidate behavioral reflections from multiple episodes.
7. Validate and version the compacted profile; retain contradictory cases and known failures.
8. At inference time, retrieve only relevant episodes and principles, preserving the hard policy boundary.

### Evaluation

**Primary:** held-out task success under explicit constraints.  
**Safety:** unauthorized action rate and severe policy violations.  
**Behavior:** principle consistency, escalation precision/recall, and calibration on ambiguous cases.  
**Operational:** tokens, dollars, wall-clock latency, memory size, and retrieval failure rate.  
**Transfer:** change in outcomes when the same experience profile is applied to another model.

Use independent judgments for ambiguous results. Blind raters to experimental arm when feasible. Report counts, per-domain effects, confidence intervals, adverse cases, and failure modes. Consider at least five independent seeds or histories per arm for a first study, with sample size revised based on variance.

### Interpretation

An improvement over A alone does not establish the effect of *experience*: B is necessary to test whether a detailed persona would suffice. An improvement over B might still be due to longer context, extra examples, or stronger feedback. Therefore include token-budget controls and ablations. Synthetic feedback from the same model may create self-confirming errors. Significant claims require independent outcome checks.

## Falsification conditions

- C performs no better than B on family-level held-out cases.
- Any gain disappears under equalized context or retrieval controls.
- Different histories produce cosmetic speech differences but no meaningful action differences.
- Higher task success is accompanied by unacceptable rule violations.
- Cross-model transfer collapses or operating cost exceeds justified value.

## Ethical and deployment constraints

Always disclose that this is synthetic history. Distinguish performance evidence from fictional biography. Isolate tenant data. Preserve provenance, consent, retention/deletion controls, role permissions, and a human override. Behavioral adaptation must not silently broaden authority or create deceptive human impersonation. High-stakes uses need domain-specific evaluation and oversight.

## Deliverables required for a research claim

- Preregistered scenario specification and frozen test split
- Reproducible runner with pinned model settings
- Independent scoring rubric and human-rating instructions
- Baseline, ablation, and transfer comparisons
- Statistical summary, cost accounting, and negative results
- Limitations and public versioned artifacts where privacy permits

Until those exist, describe this work as a **research proposal**.

