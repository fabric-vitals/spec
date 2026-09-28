# Seed issues: the open questions

**Status:** Fabric Vitals v0.2 (draft) — a technical proposal for discussion. Not a standard. Rulebook values not yet set.

These are the questions we most want the community to answer. Each will be opened as an issue on the first day, using the templates in [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE/). Evidence is more useful than opinion: please cite a standard, a paper or operational data, and state its scope (lab or production; scale).

## 1. Lossless-transport configuration consistency

**Summary.** Configuration errors are a documented cause of failure in lossless RDMA fabrics, so v0.2 names a consistency check (PFC priorities, ECN, DSCP-to-class mapping, MTU across switches and NICs) as spec-sheet field S8 and metric M43 ([`SPEC_SHEET.md`](SPEC_SHEET.md) §3). PFC configuration has no OpenConfig model, and NIC-side configuration is driver-specific.

**Question.** Which configuration items does your platform expose through a vendor-neutral model, and should a live mismatch be a critical condition rather than D3 evidence? *Template: telemetry availability or method critique. Label: `method`, `telemetry`.*

## 2. Routing stability and convergence time

**Summary.** v0.2 names routing stability as D1 control-plane evidence (M44) and routing convergence time as part of the recovery objective checked by D2 (M45, S11). Convergence time has no standard counter; it is measured in outcome tests and, where probes allow, on real events.

**Question.** How do you measure convergence time in production AI fabrics today, and at what resolution? *Template: telemetry availability. Label: `telemetry`.*

## 3. The commensurability assumption

**Summary.** The Vitals Score is the minimum across vitals. That assumes a value of 60 in one vital means as bad as 60 in another. The Rulebook makes this true by definition relative to each reference; whether it also holds for operational impact is untested (experiment E4, [`VALIDATION.md`](VALIDATION.md)).

**Question.** Do you have evidence, from incidents or experiments, that equal distances from reference in different vitals have similar or very different impact on AI jobs? *Template: method critique. Label: `method`.*

## 4. The role of D7 (AI communication)

**Summary.** D7 (synthetic collectives on known-good hosts) enters the minimum only where the spec sheet requires it; otherwise it corroborates the other vitals. This avoids penalizing fabrics that test themselves ([`SPEC.md`](SPEC.md) §4.3).

**Question.** Should synthetic collectives be required for some class presets, and how often can operators run them without disturbing tenants? *Template: method critique. Label: `method`.*

## 5. The class-preset proposal

**Summary.** Class presets R1 (rail-optimized, single-homed), R2 (dual-homed) and R3 (multi-plane, sprayed, tested) are published spec sheets with structural predicates and promise fields: design patterns ordered by redundancy, not quality tiers, stated as failure consequence rather than path counts ([`SPEC_SHEET.md`](SPEC_SHEET.md) §5). The scheme is the author's proposal and all preset values are unset.

**Question.** Are these three patterns the right ones for real AI fabrics, and are the predicate families and promise fields right for each? *Template: method critique. Label: `method`, `presets`.*

## 6. Evidence from mid-sized clusters

**Summary.** Most public evidence on normal ranges and failure rates comes from a few hyperscale operators. For clusters of about 32 to 2,000 GPUs, public operational evidence is thin, and every value carried over from hyperscale is marked "not validated at this scale".

**Question.** Can you share per-link flap, bit-error and pause rates, or telemetry availability, from a mid-sized cluster, or run the shadow-mode experiment V-S2? *Template: validation offer. Label: `validation`.*

## 7. Band calibration

**Summary.** Score bands (green, amber, red; grey for UNSCORABLE) are a display rule with edges T40, published only once calibrated against attributed communication impact (experiment E6). Until then, any displayed bands are illustrative and labelled so.

**Question.** What outcome data would convince you that a band edge is in the right place, and can you help collect it? *Template: validation offer or method critique. Label: `validation`, `method`.*
