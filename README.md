# Fabric Vitals

**A proposed vendor-neutral health score for AI data-center back-end scale-out fabrics.**

> **Status: Fabric Vitals v0.2 (draft) — a technical proposal for discussion. Not a standard. Rulebook values not yet set.**

Operators already use health dashboards, intent/assurance systems and many separate signals. What is not widely adopted is a common vendor-neutral AI-fabric operational conformance method built around a shared measurement contract and a pre-declared fabric promise. Fabric Vitals proposes such a method. Its Vitals Score is a number from 0 to 100 intended to be read at a glance, with the reasons underneath. It measures how well a fabric is currently keeping the promises on its Fabric Spec Sheet under the common Rulebook. It is not an absolute network-quality rating, a probability of failure, a reliability percentage or a percentile ranking. When too little of the fabric has been measured to give an honest number, the result is UNSCORABLE instead.

This repository is for the engineers who build and run these fabrics, the buyers who pay for them, and the vendors whose equipment they run on. If you are new here, read this page, then start with the open questions in SEED_ISSUES.md.

**How it works, in one picture.** Every car's range is measured by the same official test procedure, but each car has its own rated range. Fabric Vitals works the same way:
- **The Rulebook** (RULEBOOK.md) is the test procedure. It says how every fabric is measured and judged, and it is identical for every fabric.
- **The Fabric Spec Sheet** (SPEC_SHEET.md) is the rated range. The owner declares, before measurement, what this fabric promises: its purpose, its build, the failures it rides through, how fast it recovers, how often it should be healthy, and its performance envelope.
- **Proposed class presets** are candidate reference profiles: published spec sheets offered as starting points for industry critique. There are three, ordered by redundancy, not by quality: **R1** rail-optimized, single-homed (one connection per endpoint); **R2** dual-homed (two connections); **R3** multi-plane, sprayed, tested (several parallel planes, traffic spread across them, proven by tests). They are not claimed as an established universal taxonomy.

**What makes it different:**
- **Measured against a declared promise.** Every vital is the fraction of its declared promise being delivered, from 0 to 100, judged by a Rulebook fixed and published before measurement. A score is always shown with its class: "Vitals Score N, class Rx (spec sheet version)".
- **Scored where jobs run.** Each declared scoring scope (the pod or scalable unit a job runs on) gets its own score; large fabrics are reported as a set of scope scores with the lowest named, never as one blended number.
- **The weakest vital sets the score in the v0.2 proposal.** Critical conditions cap it. Four vitals at 100 and one at 10 score **10**, not the 82 an average would give. This minimum rule is a hypothesis to validate: the open question is whether heterogeneous vitals can be normalized well enough that equal scores have sufficiently comparable operational meaning.
- **Unknown is not healthy.** The Vitals Score is the *confirmed* score: only what was measured counts. Unmeasured capacity counts as worst, and the upper bound (the score if the unmeasured parts were healthy) is shown beside it. If coverage, the share of the fabric the telemetry (the equipment's exported measurements) reaches, is too low, the result is UNSCORABLE, with a list of exactly which telemetry is missing and where.
- **Every score explains itself.** The record gives the binding vital or condition (the one that set it), ordered contributors, and full lineage to raw counters. Language models may explain a score but never compute it.
- **Designed to be vendor-neutral and open.** The method describes behaviour, not products. Some measurements already have common models, others require vendor/platform adapters, and some counter semantics still need validation. Complete cross-vendor score equivalence has not yet been demonstrated.

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
