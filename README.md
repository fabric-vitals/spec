# Fabric Vitals

**A proposed health score for AI data-center back-end scale-out fabrics.**

Fabric Vitals is a proposed health score for AI data-center fabrics. In v0.2, it scores the **back-end scale-out fabric**. It measures how well the fabric is keeping the promises on its Fabric Spec Sheet, under a common Rulebook. The Vitals Score gives one number at a glance, with the reasons underneath.

## Status and claims

- **v0.2 is an open technical proposal** for discussion, critique and validation. It is not a standard, certification or procurement benchmark.
- **Most Rulebook values remain unset.** The score model and proposed class presets are being offered for validation and industry critique.
- **Vendor-neutrality is the design goal.** Complete cross-vendor telemetry and score equivalence have not yet been demonstrated.
- **The score is a conformance reading, not an absolute rating.** It is not a probability of failure, a reliability percentage or a percentile ranking.

This repository is for the engineers who build and run these fabrics, the buyers who pay for them, and the vendors whose equipment they run on. If you are new here, read this page, then start with the open questions in SEED_ISSUES.md.

**How it works, in one picture.** Every car's range is measured by the same official test procedure, but each car has its own rated range. Fabric Vitals works the same way:
- **The Rulebook** (RULEBOOK.md) is the test procedure. It says how every fabric is measured and judged, and it is identical for every fabric.
- **The Fabric Spec Sheet** (SPEC_SHEET.md) is the rated range. The owner declares, before measurement, what this fabric promises: its purpose, its build, the failures it rides through, how fast it recovers, how often it should be healthy, and its performance envelope.
- **Class presets** are proposed ready-made Spec Sheets. **R1** reflects a rail-optimized, single-homed training pattern documented in multiple current reference designs and operator reports; **R2** is dual-homed; **R3** is multi-plane, sprayed and tested. They are ordered by redundancy, not quality, and are starting points for critique and validation.

**What makes it different:**
- **Measured against a declared promise.** Every vital is the fraction of its declared promise being delivered, from 0 to 100, judged by a Rulebook fixed and published before measurement. A score is always shown with its class: "Vitals Score N, class Rx (spec sheet version)".
- **Scored where jobs run.** Each declared scoring scope (the pod or scalable unit a job runs on) gets its own score; large fabrics are reported as a set of scope scores with the lowest named, never as one blended number.
- **The v0.2 headline uses the weakest vital.** Critical conditions cap it. Four vitals at 100 and one at 10 score **10**. Validation experiments E4 and E5 test whether this minimum, a calibrated minimum, an arithmetic average or other serious alternatives best preserve severe faults and track attributed operational impact.
- **Unknown is not healthy.** The Vitals Score is the *confirmed* score: only what was measured counts. Unmeasured capacity counts as worst, and the upper bound (the score if the unmeasured parts were healthy) is shown beside it. If coverage, the share of the fabric the telemetry (the equipment's exported measurements) reaches, is too low, the result is UNSCORABLE, with a list of exactly which telemetry is missing and where.
- **Every score explains itself.** The record gives the binding vital or condition (the one that set it), ordered contributors, and full lineage to raw counters. Language models may explain a score but never compute it.
- **Designed for vendor-neutral implementation.** The method describes behaviour, not products. `METRICS.md` identifies where common models exist, where vendor/platform adapters are needed and where counter semantics still need validation.

**Files:**

| File | What it contains |
|---|---|
| [`SPEC.md`](SPEC.md) | The method, with implementer requirements (BCP 14 keywords) |
| [`RULEBOOK.md`](RULEBOOK.md) | Rulebook RB-0.2 (skeleton): all 40 parameters, whether each belongs to the Rulebook or the spec sheet, and their status. Only one value is set (an IEEE budget). |
| [`SPEC_SHEET.md`](SPEC_SHEET.md) | The Fabric Spec Sheet template (S1–S23), the lossless-configuration check, the vital-to-field mapping, and the class presets |
| [`templates/fabric-spec-sheet.yaml`](templates/fabric-spec-sheet.yaml) | A fillable copy of the spec-sheet template |
| [`METRICS.md`](METRICS.md) | Metric definitions M01–M45 and vendor-neutral model availability |
| [`SCENARIOS.md`](SCENARIOS.md) | The scoring-formula comparison behind the weakest-vital rule, and the 19-scenario failure and event table |
| [`VALIDATION.md`](VALIDATION.md) | The validation programme that will set the Rulebook values and preset values. States what an emulated fabric can and cannot validate, and which experiments need GPUs. |
| [`RELATED_WORK.md`](RELATED_WORK.md) | Positioning against ITU-T M.3042, IETF drafts, SAIN, QoO, facility tier practice and the metric-checklist view |
| [`SEED_ISSUES.md`](SEED_ISSUES.md) | The open questions we most want answered |
| [`GOVERNANCE.md`](GOVERNANCE.md) | Stewardship, versioning, the pre-registration rule, and the commitment to a neutral body |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How to open issues and propose changes |
| [`TRADEMARK.md`](TRADEMARK.md) | How the names "Fabric Vitals" and "Vitals Score" may be used (draft policy) |
| [`CHANGELOG.md`](CHANGELOG.md) | Version history |
| [`CITATION.cff`](CITATION.cff) | How to cite this specification |
| [`LICENSE`](LICENSE) | CC BY 4.0 |

Print versions: [paper (PDF)](paper/Fabric_Vitals_Paper_v0.2.pdf) · [summary (PDF)](paper/Fabric_Vitals_Summary_v0.2.pdf)

**Start on day one.** The Day-One Set (SPEC.md §13) is the smallest set of vitals, counters and probes that yields a valid Vitals Score from telemetry most platforms already export.

**Scope in v0.x:** Fabric Vitals scores the back-end scale-out fabric. That back-end fabric may use the TRAINING, INFERENCE or GENERAL workload profile. Separate front-end networks, inference-serving network domains, storage/checkpoint networks, scale-up interconnects (NVLink-class, including Ethernet-based scale-up) and multi-tenant isolation remain out of scope and are candidates for later profiles. Security is excluded.

**How to take part** (CONTRIBUTING.md):
- critique the method, the Rulebook split and the class presets;
- report which telemetry your platforms export by default;
- offer lab or production fabrics for validation, especially mid-sized clusters of about 32–2,000 GPUs.

Start with the questions in SEED_ISSUES.md.

**Governance:** Fabric Vitals is currently author-stewarded by datacenternetwork.ai and open to contribution; it does not yet have neutral institutional governance. See [`GOVERNANCE.md`](GOVERNANCE.md) for the commitment to transfer stewardship and the marks to an open multi-party body if the community chooses that path. **Disclosure:** the author organization develops network software. The proposal is designed to be implementable across vendors and is offered for open discussion and validation.

*Fabric Vitals is not affiliated with, or endorsed by, any other organization that uses the word "vitals". "Fabric Vitals" and "Vitals Score" are claimed as marks of datacenternetwork.ai; see [`TRADEMARK.md`](TRADEMARK.md).*
