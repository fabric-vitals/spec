# Fabric Vitals: a health score for AI data-center fabrics — two-page summary

**Shankar Gopidas, Founder & CEO, datacenternetwork.ai**

*Fabric Vitals v0.2 (draft) — a technical proposal for discussion. Not a standard. Rulebook values not yet set.*

**Fabric Vitals is a proposed health score for AI data-center back-end scale-out fabrics. It measures how well a fabric is keeping the promises on its Fabric Spec Sheet, under a common Rulebook.**

## The problem

AI data centers connect accelerators through dedicated high-speed networks, the "fabric". Operators already use dashboards, health indexes, intent/assurance systems and many separate signals. What is not widely adopted is a common vendor-neutral AI-fabric operational conformance method built around a shared measurement contract and a pre-declared fabric promise. Fabric Vitals proposes one such method. It does not replace the underlying telemetry or assurance systems; it tries to put a common, explainable contract above them.

## The idea

The **Vitals Score** is the headline number: one number at a glance, with reasons underneath. It is a conformance reading against the declared Spec Sheet and Rulebook, not an absolute quality or risk ranking. If a fabric is built to survive two link failures without disrupting training, the score checks that it still can. It does not ask whether the fabric merely looks "normal" compared with last week.

Think of how a car's range is rated. Every car is measured by the same official test procedure, but each car has its own rated range on its spec sheet. Fabric Vitals works the same way: one **Rulebook** says how every fabric is measured and judged, and each fabric has its own **Fabric Spec Sheet** saying what it promises.

## How it works

**1. The owner fills in a spec sheet.** Before anything is measured, the owner declares the in-scope back-end scale-out fabric, the workload profile it carries (TRAINING, INFERENCE or GENERAL), how it is built, which failures it rides through, how quickly it recovers, how much of the time it should be healthy, and the performance it promises. R1, R2 and R3 are proposed class presets: **R1** reflects a rail-optimized, single-homed training pattern documented in multiple current reference designs and operator reports; **R2** is dual-homed; **R3** is multi-plane, sprayed and tested. They are ordered by redundancy, not quality, and are offered as candidate reference profiles for critique and validation. Large fabrics are scored pod by pod, with the weakest pod named, rather than blended into one number. The build the owner declared is checked against the fabric as actually built. If the owner promises more than was built, the missing redundancy counts as absent, and the score says what it would be under the class actually built. The honest fix is a new, versioned spec sheet.

**2. The Rulebook is fixed before measurement.** Every measurement is judged by a published Rulebook, set in advance and versioned, and identical for every fabric. Where an industry standard exists, it is used. Where none exists, the rule is either defined with documented reasoning or set by a standard test procedure. The rules are never tuned after the fact to make a result look better.

**3. The v0.2 headline uses the weakest area, and severe problems cap it.** The fabric is scored in seven proposed areas, called **vitals**: reachability, resilience, congestion and loss, delay, physical link quality, usable capacity and, where the spec sheet requires it, performance under AI-style test traffic. The v0.2 headline is the lowest required vital, subject to named critical-condition caps. In the simple masking example, four 100s and one 10 produce an arithmetic mean of 82 and a minimum of 10; that illustrates different compensation behavior, not a predetermined winner. E4 and E5 compare the current minimum, a calibrated minimum, an arithmetic-average comparator and other serious alternatives against measured network-attributable impact, explainability and robustness.

**4. Missing data never makes the score look better.** Parts of the fabric that are not being measured count as unknown, not as healthy. The headline is the health the evidence actually confirms, and it is shown beside the best case if the unmeasured parts turned out to be fine. If too much is unmeasured, the result is "unscorable", together with a list of exactly which measurements are missing and where. Hiding telemetry, the readings the equipment reports about itself, therefore cannot raise the score. The only exception is a short, bounded allowance for momentary gaps in data collection, so that a restarting collector (the software that gathers those readings) does not look like a failing network.

**5. Every score explains itself.** Each score names the area or condition that set it. It lists the main contributors in order, and links every number back to the raw measurements, the rule that was applied and the promise it was judged against. It also shows how many areas fall short, so that broad deterioration is visible even when the headline has not moved. The score can be shown in green, amber or red, with any critical condition shown red; those colour bands will be published only once they are calibrated, and until then any colours shown are illustrative. "Healthy 99% of the time" gets a precise meaning: the share of time the score was green with no critical condition active. A score is always shown with its class, in the form "Vitals Score N, class R2 (spec sheet version)". A score is a reading, not a verdict: it is also shown over time, with the upper bound, critical conditions, unscorable gaps and spec-sheet changes marked, and never smoothed. Scores are always computed by a fixed, repeatable method. AI language models may help explain a result, but they never calculate it.

## What makes it different

Fabric Vitals is designed to be vendor-neutral and open, and it builds on substantial prior art rather than claiming those ideas as new:
- **IETF SAIN / RFC 9417–9418** provides 0–100 service-health conventions, an unavailable value and explanatory symptoms.
- **ITU-T M.3042** defines a communication-network health-index framework and uses minimum aggregation inside some lower-level indexes.
- **IETF Quality of Outcome** uses requirement-relative 0–100 sub-scores and minimum aggregation.
- **IETF AI-fabric benchmarking drafts** define health indicators and methods that can feed Fabric Vitals.
- **Vendor assurance/health systems** and **facility resilience/rating models** provide additional operational and classification precedents.

The potentially distinctive contribution is the combination: **pre-declared fabric promise + common Rulebook + AI-fabric evidence + deterministic scoring + explicit missing-data treatment + critical conditions + evidence lineage + open pre-registered validation**. The class presets themselves are the author's proposed candidate reference profiles, drawn from public sources and open for critique.

## What is not done yet

The method is defined, but the Rulebook's values are not, and the class presets carry no promise values yet. Most thresholds have no industry standard behind them, so they will be set through open validation experiments. The first round needs no GPUs: it runs on an emulated network with replayed data and tests the scoring machinery itself. Its results produce the first Rulebook with values, which will be published openly. Tests that need real hardware and GPUs come later. Until then, scores are for discussion and experimentation, not for acceptance decisions.

The available evidence is strongest for the very largest AI clusters and thinnest for mid-sized ones, roughly 32 to 2,000 GPUs, which is where many readers operate. Some requirement texts of paid industry standards were not consulted. Fabrics with limited monitoring may be "unscorable" at first, and they will be told what to add; the proposed Day-One Set still requires validation across vendors and platforms. v0.2 scores the **back-end scale-out fabric** under a TRAINING, INFERENCE or GENERAL workload profile. Separate front-end networks, inference-serving network domains, storage/checkpoint networks, scale-up interconnects and multi-tenant isolation are out of scope and are on the roadmap.

## How to get involved

We are asking for three things:
- **Expert review:** critique of the method, the Rulebook and spec-sheet split, and the class presets, through the specification repository's issue tracker.
- **Validation partners:** access to lab or production fabrics, including mid-sized clusters, to help set the Rulebook's values.
- **Standards and community input:** in particular on vendor-neutral definitions of network-card and congestion counters, and of lossless-network configuration.

Specification and issues: https://github.com/fabric-vitals/spec · Contact: hello@datacenternetwork.ai

## Disclosure

The author organization develops network software. Fabric Vitals is currently author-stewarded by datacenternetwork.ai and open to contribution; it does not yet have neutral institutional governance. The proposal is designed for implementation across vendors and operators, while complete cross-vendor equivalence remains part of validation. The method, its Rulebook and its proposed class presets are offered for open discussion.

---

Full paper: *Fabric Vitals: a vendor-neutral health score for AI data-center fabrics, measured against a declared design* (v0.2) · Specification: https://github.com/fabric-vitals/spec
