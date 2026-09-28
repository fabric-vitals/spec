# Changelog

## v0.2 (draft) — 2026-09-28

**Design change: the Rulebook and the spec sheet are separate.**
- The parameter register is renamed the **Rulebook** ([`RULEBOOK.md`](RULEBOOK.md), RB-0.2), identical for every fabric. It replaces `REFERENCE_PROFILE.md`.
- New **Fabric Spec Sheet** ([`SPEC_SHEET.md`](SPEC_SHEET.md)), on which an owner declares what a fabric promises: fields S1–S23 declared per fabric before measurement (purpose, build, resilience promise, availability target, performance envelope, required tests, class), a normative mapping from each vital (the seven measured dimensions of fabric health) to the fields it is judged against, and a fillable template ([`templates/fabric-spec-sheet.yaml`](templates/fabric-spec-sheet.yaml)).
- The register gains a **"Rulebook / Spec sheet"** column. Per-fabric promises move to the spec sheet with status VALUE DECLARED BY OWNER (T3, T4, T5, T12, T32, T33; T37 stays BUDGET CITED as a standard floor); T10 and T26 keep their method in the Rulebook and take their value from the spec sheet. Every T-ID is kept. Result: 31 Rulebook, 7 spec sheet, 2 both.
- Design classes become **class presets**: published, ready-made spec sheets with structural predicates and promise fields. All preset values are PROPOSED and not set, except the IEEE physical-layer budgets. Comparability holds within a preset or between identical spec sheets.
- **Availability** defined as the share of windows in the healthy band with no critical condition active ([`SPEC.md`](SPEC.md) §9.2). No targets set.

**Score bands.** New Rulebook parameter **T40, score band edges** (VALUE NOT SET). Bands are a display rule: green, amber, red; any active critical condition displays red; UNSCORABLE (no valid score can be given) displays grey. Bands are published only once calibrated; until then any displayed bands are illustrative and labelled so. T22 is now the band calibration method and labels; T15 must lie below the lower edge.

**Two named gaps.**
- **Lossless-transport configuration consistency** (PFC priorities, ECN, DSCP-to-class mapping, MTU across switches and NICs; PFC is Priority Flow Control, which pauses a traffic class instead of dropping packets, and ECN is Explicit Congestion Notification, a mark that tells senders to slow down): spec-sheet field S8, conformance predicate P-CFG, and D3 evidence metric M43.
- **Routing stability and convergence time:** D1 evidence M44 and D2 recovery-objective evidence M45; scenario 18 in [`SCENARIOS.md`](SCENARIOS.md); new validation experiment E12.
- Deliberate exclusions (security, scale-up, front-end and storage networks) stated explicitly; storage and checkpoint traffic named as a candidate second profile.

**Positioning.** New section "Why not a metric checklist?" in [`RELATED_WORK.md`](RELATED_WORK.md) §6.

**Governance and community.** New [`TRADEMARK.md`](TRADEMARK.md) (draft policy); [`GOVERNANCE.md`](GOVERNANCE.md) adds the commitment to transfer the marks and stewardship to a neutral body and the pre-registration rule for experiments; new issue templates and [`SEED_ISSUES.md`](SEED_ISSUES.md).

**Editorial.** One reference style across all files; duplicate references merged; formatting fixes (table headers in [`SCENARIOS.md`](SCENARIOS.md), stray punctuation).

**Further changes after review (also in v0.2).**
- **Common currency:** every vital is the fraction of the declared promise being delivered, 0–100; the design intent of T25/T31 ([`SPEC.md`](SPEC.md) §4.1, §5).
- **Scoring scope** (the part of a fabric one score covers): new spec-sheet field S23; one score per pod or scalable unit; multi-scope fabrics reported as a set of scope scores with the lowest named, never blended; blast radius (how much of the fabric one failure can take out) and coverage (the share of the scope that telemetry, the exported counters and measurements, observes) evaluated within the scope ([`SPEC.md`](SPEC.md) §2.6).
- **Planned maintenance:** declared, versioned maintenance windows; PLANNED origin tag; the spec sheet says whether windows count against availability; no undeclared maintenance mode ([`SPEC.md`](SPEC.md) §9.3); scenario 19.
- **D7 footprint:** duration, reserved nodes or scheduled gaps, and frequency bound as method (T26, values not set); D7 corroborating unless the class requires it.
- **Presentation:** a score is never shown without its class: "Vitals Score N, class Rx (spec sheet version)" (MUST).
- **Over-claim rule:** declared-but-unbuilt redundancy counts as absent (complete over-claim: D2 = 0); the record shows "declared Rx, built as Ry; as Ry it would score N"; experiment E10 extended.
- **Classes named R1–R3** as design patterns ordered by redundancy, not quality tiers: R1 rail-optimized, single-homed; R2 dual-homed; R3 multi-plane, sprayed, tested.
- **Day-One Set:** the minimum set of vitals, counters and probes that yields a valid Vitals Score, the single health score ([`SPEC.md`](SPEC.md) §13).
- **Roadmap of excluded areas:** front-end and inference-serving networks; storage and checkpoint traffic; scale-up (NVLink-class, including Ethernet-based scale-up); multi-tenant isolation.

**Status:** a technical proposal for discussion. Not a standard. Rulebook values not yet set.

## v0.1 — 2026-09-23

Initial public proposal:
- the specification ([`SPEC.md`](SPEC.md)): design classes and declaration, conformance check, vitals D1–D7, reference-first normalization, weakest-vital aggregation, critical conditions CC1–CC6, confirmed score (the score counting only what telemetry observed) and range, grace period (how long a telemetry lapse is tolerated), the coverage-floor / blast-radius constraint, UNSCORABLE with a missing-telemetry list, temporal behaviour, profiles, the explanation record, versioning;
- the parameter register RP-0.1 (skeleton): 39 parameters. Status: 37 VALUE NOT SET, 1 BUDGET CITED (T37), 1 CONSTRAINT DEFINED (T39);
- metric definitions M01–M42;
- the validation programme (experiments E1–E11, small-cluster targets V-S1–V-S6);
- scenarios and scoring-formula comparison ([`SCENARIOS.md`](SCENARIOS.md)): the masking example across eight aggregation-formula families, and a 17-scenario failure table;
- related work, governance, contributing guide.
