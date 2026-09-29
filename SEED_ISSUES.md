# Seed issues: the open questions

**Status:** Fabric Vitals v0.2 (draft) — a technical proposal for discussion. Not a standard. Rulebook values not yet set.

These are the questions we most want the community to answer. Each will be opened as an issue on the first day, using the templates in [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE/). Evidence is more useful than opinion: please cite a standard, a paper or operational data, and state its scope (lab or production; scale).

## 1. Lossless-transport configuration consistency

**Summary.** Configuration errors are a documented cause of failure in lossless RDMA fabrics, so v0.2 names a consistency check as spec-sheet field S8 and metric M43 ([`SPEC_SHEET.md`](SPEC_SHEET.md) §3). The check covers PFC priorities (Priority Flow Control, which pauses a traffic class instead of dropping packets), ECN (Explicit Congestion Notification, a mark that tells senders to slow down), DSCP-to-class mapping and MTU across switches and NICs. PFC configuration has no OpenConfig model, and NIC-side configuration is driver-specific.

**Question.** Which configuration items does your platform expose through a vendor-neutral model, and should a live mismatch be a critical condition (a fault that caps the score on its own) rather than evidence for vital D3 (a vital is one of the seven measured dimensions of fabric health)? *Template: telemetry availability or method critique. Label: `method`, `telemetry`.*

## 2. Routing stability and convergence time

**Summary.** v0.2 names routing stability as D1 control-plane evidence (M44) and routing convergence time as part of the recovery objective checked by D2 (M45, S11). Convergence time has no standard counter; it is measured in outcome tests and, where probes allow, on real events.

**Question.** How do you measure convergence time in production AI fabrics today, and at what resolution? *Template: telemetry availability. Label: `telemetry`.*

## 3. The commensurability assumption

**Summary.** The Vitals Score (the single health score) is the minimum across vitals: the lowest vital sets the score. That assumes the vitals are commensurable, so that a value of 60 in one vital means as bad as 60 in another. The Rulebook (the one set of rules that applies to every fabric) makes this true by definition relative to each reference; whether it also holds for operational impact is untested (experiment E4, [`VALIDATION.md`](VALIDATION.md)).

**Question.** Do you have evidence, from incidents or experiments, that equal distances from reference in different vitals have similar or very different impact on AI jobs? *Template: method critique. Label: `method`.*

## 4. Cross-vendor measurement equivalence

**Summary.** Fabric Vitals is designed to be vendor-neutral, but the metric inventory distinguishes measurements with common models from those that need vendor/platform adapters or have unresolved counter semantics. Cross-vendor score equivalence is therefore a validation question, not an established property of v0.2.

**Question.** For the metrics you operate, which switch and NIC counters have genuinely equivalent semantics across vendors today, where are adapters sufficient, and where would two conforming implementations still risk producing different evidence from the same fabric condition? *Template: telemetry availability or method critique. Label: `telemetry`, `method`.*

## 5. The role of D7 (AI communication)

**Summary.** D7 (synthetic collectives on known-good hosts: test runs of the group communication patterns AI training uses) enters the minimum only where the spec sheet requires it; otherwise it corroborates the other vitals. This avoids penalizing fabrics that test themselves ([`SPEC.md`](SPEC.md) §4.3).

**Question.** Should synthetic collectives be required for some class presets (the published, ready-made spec sheets a fabric can adopt), and how often can operators run them without disturbing tenants? *Template: method critique. Label: `method`.*

## 6. The class-preset proposal

**Summary.** The proposed class presets R1 (rail-optimized, a documented wiring pattern, and single-homed, meaning one connection into the fabric for each endpoint), R2 (dual-homed, meaning two connections) and R3 (multi-plane, sprayed, tested, meaning several parallel network planes with traffic spread across them and the design proven by tests) are candidate reference profiles with structural predicates (yes-or-no tests of how the fabric is built) and promise fields: design patterns ordered by redundancy, not quality tiers, stated as failure consequence rather than path counts ([`SPEC_SHEET.md`](SPEC_SHEET.md) §5). The scheme is the author's proposal, not an established universal taxonomy, and all preset values are unset.

**Question.** Are these three patterns the right ones for real AI fabrics, and are the predicate families and promise fields right for each? *Template: method critique. Label: `method`, `presets`.*

## 7. Evidence from mid-sized clusters

**Summary.** Most public evidence on normal ranges and failure rates comes from a few hyperscale operators. For clusters of about 32 to 2,000 GPUs, public operational evidence is thin, and every value carried over from hyperscale is marked "not validated at this scale".

**Question.** Can you share per-link flap, bit-error and pause rates, or telemetry availability (which measurement data your equipment exports), from a mid-sized cluster, or run the shadow-mode experiment V-S2, in which a fabric is scored in the background while it runs its normal work? *Template: validation offer. Label: `validation`.*

## 8. Band calibration

**Summary.** Score bands (green, amber, red; grey for UNSCORABLE, meaning no valid score can be given) are a display rule with edges T40, published only once calibrated against attributed communication impact (experiment E6). Until then, any displayed bands are illustrative and labelled so.

**Question.** What outcome data would convince you that a band edge is in the right place, and can you help collect it? *Template: validation offer or method critique. Label: `validation`, `method`.*
