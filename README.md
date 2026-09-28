# Fabric Vitals

**A vendor-neutral health score for AI data-center fabrics: the back-end networks that connect GPUs and other accelerators for training and inference.**

> **Status: Fabric Vitals v0.2 (draft) — a technical proposal for discussion. Not a standard. Rulebook values not yet set.**

The networks that connect accelerators in AI data centers are monitored through dozens of separate signals, but there is no shared answer to "is this AI fabric healthy?". Fabric Vitals is an open method that produces one number, the **Vitals Score** (0–100, or UNSCORABLE), readable at a glance like a credit score. Underneath it sit seven **vitals** (D1–D7) and a full explanation.

**How it works, in one picture.** Every car's range is measured by the same official test procedure, but each car has its own rated range. Fabric Vitals works the same way:
- **The Rulebook** ([`RULEBOOK.md`](RULEBOOK.md)) is the test procedure. It says how every fabric is measured and judged, and it is identical for every fabric.
- **The Fabric Spec Sheet** ([`SPEC_SHEET.md`](SPEC_SHEET.md)) is the rated range. The owner declares, before measurement, what this fabric promises: its purpose, its build, the failures it rides through, how fast it recovers, how often it should be healthy, and its performance envelope.
- **Class presets** are the standard models: published spec sheets that fabrics can adopt, so that fabrics on the same preset can be compared. There are three, ordered by redundancy, not by quality: **R1** rail-optimized, single-homed; **R2** dual-homed; **R3** multi-plane, sprayed, tested.

**What makes it different:**
- **Measured against a declared promise.** Every vital is the fraction of its declared promise being delivered, from 0 to 100, judged by a Rulebook fixed and published before measurement. A score is always shown with its class: "Vitals Score N, class Rx (spec sheet version)".
- **Scored where jobs run.** Each declared scoring scope (a pod or scalable unit) gets its own score; large fabrics are reported as a set of scope scores with the lowest named, never as one blended number.
- **The weakest vital sets the score.** Critical conditions cap it. Four vitals at 100 and one at 10 score **10**, not the 82 an average would give.
- **Unknown is not healthy.** The Vitals Score is the *confirmed* score. Unmeasured capacity counts as worst, and the upper bound is shown beside it. If coverage is too low, the result is UNSCORABLE, with a list of exactly which telemetry is missing and where.
- **Every score explains itself.** The record gives the binding vital or condition, ordered contributors, and full lineage to raw counters. Language models may explain a score but never compute it.
- **Vendor-neutral and open.** The method describes behaviour, not products.

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

**Start on day one.** The Day-One Set ([`SPEC.md`](SPEC.md) §13) lists the smallest set of vitals, counters and probes that yields a valid Vitals Score from telemetry most platforms already export.

**Out of scope in v0.x, and on the roadmap** as candidate future profiles, in order of likely demand: front-end and inference-serving networks; storage and checkpoint traffic; scale-up interconnects (NVLink-class, including Ethernet-based scale-up); multi-tenant isolation. Security is excluded.

**How to take part** ([`CONTRIBUTING.md`](CONTRIBUTING.md)):
- critique the method, the Rulebook split and the class presets;
- report which telemetry your platforms export by default;
- offer lab or production fabrics for validation, especially mid-sized clusters of about 32–2,000 GPUs.

Start with the questions in [`SEED_ISSUES.md`](SEED_ISSUES.md).

**Steward:** datacenternetwork.ai (initially; see [`GOVERNANCE.md`](GOVERNANCE.md)). **Disclosure:** the author organization develops network software. The proposal is written to be implementable by any vendor or operator. The method, its Rulebook and its class presets are vendor-neutral and are offered for open discussion.

*Fabric Vitals is not affiliated with, or endorsed by, any other organization that uses the word "vitals". "Fabric Vitals" and "Vitals Score" are claimed as marks of datacenternetwork.ai; see [`TRADEMARK.md`](TRADEMARK.md).*
