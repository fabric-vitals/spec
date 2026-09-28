# Changelog

## v0.2 (draft) — 2026-09-28

**Design change: the Rulebook and the spec sheet are separate.**
- The parameter register (the list of every parameter the method uses) is renamed the **Rulebook**, version RB-0.2, and is identical for every fabric. It replaces `REFERENCE_PROFILE.md`. See [`RULEBOOK.md`](RULEBOOK.md).
- New **Fabric Spec Sheet**, the form on which an owner declares what a fabric promises: fields S1–S23, declared for each fabric before measurement (purpose, build, resilience promise, availability target, performance envelope, required tests, class); a normative mapping that says which fields each vital is judged against; and a fillable template ([`templates/fabric-spec-sheet.yaml`](templates/fabric-spec-sheet.yaml)). See [`SPEC_SHEET.md`](SPEC_SHEET.md).
- The register gains a "Rulebook / Spec sheet" column saying which side each parameter belongs to. Per-fabric promises move to the spec sheet with status VALUE DECLARED BY OWNER (T3, T4, T5, T12, T32, T33; T37 stays BUDGET CITED as a standard floor); T10 and T26 keep their method in the Rulebook and take their value from the spec sheet. Every T-ID (parameter number) is kept. Result: 31 Rulebook, 7 spec sheet, 2 both.
- Design classes become **class presets**: published, ready-made spec sheets with structural predicates (yes-or-no tests of how a fabric is built) and promise fields. All preset values are PROPOSED and not set, except the physical-layer budgets taken from IEEE standards (the Institute of Electrical and Electronics Engineers, publisher of the Ethernet standards). Comparability holds within a preset or between identical spec sheets.
- **Availability** is defined as the share of measurement windows in the healthy band with no critical condition active. No targets are set. See [`SPEC.md`](SPEC.md) §9.2.

**Score bands.** New Rulebook parameter **T40, score band edges** (status VALUE NOT SET). Bands are a display rule, the colour a score is shown in: green, amber, red; any active critical condition displays red; UNSCORABLE displays grey. Bands are published only once they have been calibrated against evidence; until then any displayed bands are illustrative and labelled so. T22 is now the band calibration method and labels; T15 must lie below the lower edge.

**Two named gaps.**
- **Lossless-transport configuration consistency**: whether the PFC priorities, ECN, the DSCP-to-class mapping and the MTU are configured consistently across switches and NICs. (PFC is Priority Flow Control, which pauses a traffic class rather than dropping packets; ECN is Explicit Congestion Notification, a mark that tells senders to slow down; DSCP is the Differentiated Services Code Point, the packet field that names a traffic class; MTU is the maximum transmission unit, the largest packet a link carries; a NIC is a network interface card, the adapter that connects a server to the network.) Added as spec-sheet field S8, conformance predicate P-CFG (a yes-or-no check), and metric M43 as evidence for vital D3.
- **Routing stability and convergence time** (how stable the routes are, and how long the network takes to settle on new routes after a change): metric M44 as evidence for vital D1, and metric M45 as recovery-objective evidence for vital D2; scenario 18 in [`SCENARIOS.md`](SCENARIOS.md); new validation experiment E12.
- Deliberate exclusions (security, scale-up, front-end and storage networks) are now stated explicitly; storage and checkpoint traffic is named as a candidate second profile (a variant of the method for another kind of network).

**Positioning.** New section "Why not a metric checklist?" in [`RELATED_WORK.md`](RELATED_WORK.md) §6.

**Governance and community.** New [`TRADEMARK.md`](TRADEMARK.md) (draft policy on use of the names); [`GOVERNANCE.md`](GOVERNANCE.md) adds the commitment to transfer the marks and stewardship to a neutral body, and the pre-registration rule for experiments (an experiment is described before its data is collected); new issue templates and [`SEED_ISSUES.md`](SEED_ISSUES.md), the list of open questions.

**Editorial.** One reference style across all files; duplicate references merged; formatting fixes (table headers in SCENARIOS.md, stray punctuation).

**Further changes after review (also in v0.2).**
- **Common currency:** every vital is expressed as the fraction of the declared promise being delivered, 0–100, so that all vitals are on the same scale; this is the design intent of T25 and T31. See SPEC.md §4.1 and §5.
- **Scoring scope:** new spec-sheet field S23; one score per pod or scalable unit (the building block a fabric is grown by); fabrics with several scopes are reported as a set of scope scores with the lowest named, never blended into one number; blast radius (how much of the fabric one failure can take out) and coverage are evaluated within the scope. See SPEC.md §2.6.
- **Planned maintenance:** maintenance windows are declared in advance and versioned; a PLANNED origin tag (a label marking the cause of an event as planned); the spec sheet says whether such windows count against availability; there is no undeclared maintenance mode; scenario 19. See SPEC.md §9.3.
- **D7 footprint:** the cost of running vital D7's synthetic tests (their duration, the nodes reserved or the gaps scheduled for them, and how often they run) is bounded as a method (T26, values not set); D7 corroborates the other vitals unless the class requires it to count.
- **Presentation:** a score is never shown without its class, in the form "Vitals Score N, class Rx (spec sheet version)" (MUST, the strongest requirement level).
- **Over-claim rule:** redundancy that is declared on the spec sheet but not actually built counts as absent (a complete over-claim gives D2 = 0); the record shows "declared Rx, built as Ry; as Ry it would score N"; experiment E10 is extended to cover this.
- **Classes named R1–R3** as design patterns ordered by redundancy, not quality tiers: R1 rail-optimized, single-homed; R2 dual-homed; R3 multi-plane, sprayed, tested.
- **Day-One Set:** the minimum set of vitals, counters and probes that yields a valid Vitals Score. See SPEC.md §13.
- **Roadmap of excluded areas:** front-end and inference-serving networks; storage and checkpoint traffic; scale-up (NVLink-class, including Ethernet-based scale-up); multi-tenant isolation.

**Status:** a technical proposal for discussion. Not a standard. Rulebook values not yet set.

## v0.1 — 2026-09-23

Initial public proposal:
- the specification (SPEC.md): design classes and how a fabric declares one, the conformance check, the vitals D1–D7, reference-first normalization (each measurement is expressed relative to its declared reference), weakest-vital aggregation, critical conditions CC1–CC6, the confirmed score and its range, the grace period, the coverage-floor / blast-radius constraint, UNSCORABLE with a list of the missing telemetry, temporal behaviour (how the score behaves over time), profiles, the explanation record, versioning;
- the parameter register RP-0.1 (skeleton): 39 parameters. Status: 37 VALUE NOT SET, 1 BUDGET CITED (T37), 1 CONSTRAINT DEFINED (T39);
- metric definitions M01–M42;
- the validation programme (experiments E1–E11, small-cluster targets V-S1–V-S6);
- scenarios and the scoring-formula comparison (SCENARIOS.md): the masking example (where an average hides a failing vital) across eight aggregation-formula families, and a 17-scenario failure table;
- related work, governance, contributing guide.
