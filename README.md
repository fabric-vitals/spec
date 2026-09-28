# Fabric Vitals

**A vendor-neutral health score for AI data-center fabrics: the back-end networks that connect GPUs and other accelerators for training and inference.**

In plain words: AI stands for artificial intelligence. A GPU is a graphics processing unit, the kind of chip that does most of the computation when an AI model is trained or run, and "accelerator" is the general word for any chip built for that job. Inside an AI data center, the accelerators are wired together by a dedicated network so that they can work on one model at the same time. That network is the fabric. "Vendor-neutral" means the method is not tied to any one equipment maker: it describes how a fabric behaves, not whose products it is built from. This page is written for the people who build, run or buy these networks (network engineers, operators and equipment vendors) and for anyone who wants to test or challenge the method.

> **Status: Fabric Vitals v0.2 (draft) — a technical proposal for discussion. Not a standard. Rulebook values not yet set.**

The networks that connect accelerators in AI data centers are monitored through dozens of separate signals, but there is no shared answer to the question "is this AI fabric healthy?". Fabric Vitals is an open method that answers it with one number, the Vitals Score. The score runs from 0 to 100 and is meant to be read at a glance, like a credit score. When a fabric cannot be measured well enough to score, the result is UNSCORABLE, a word that means "no number can honestly be given", rather than a misleading number. Underneath the score sit seven vitals, numbered D1–D7. A vital is one measured aspect of the fabric's health, in the way that a patient's vital signs each measure one aspect of the patient's health. Every score comes with a full explanation of how it was reached. If you are new here, read this page to the end and then go to the open questions in the file SEED_ISSUES.md, listed in the table below.

**How it works, in one picture.** Every car's range is measured by the same official test procedure, but each car has its own rated range. Fabric Vitals works the same way:
- **The Rulebook** is the test procedure. It is one document that says how every fabric is measured and how the measurements are judged, and it is the same for every fabric. It is the file RULEBOOK.md, listed in the table below.
- **The Fabric Spec Sheet** is the rated range. It is a short form that the owner of a fabric fills in before any measurement takes place, declaring what this particular fabric promises: what it is for, how it is built, which failures it is designed to keep working through, how fast it recovers from them, how often it should be healthy, and the performance envelope it is expected to stay within. It is the file SPEC_SHEET.md.
- **Class presets** are the standard models. A class preset is a ready-made spec sheet, published with the method, that a fabric owner can adopt instead of writing one from scratch. Fabrics that adopt the same preset can be compared with each other. There are three presets, named R1, R2 and R3. They are ordered by how much redundancy the design carries (how many spare paths it keeps), not by quality: R1 is rail-optimized, a common wiring layout for AI fabrics, and single-homed, meaning one connection into the fabric for each endpoint; R2 is dual-homed, meaning two connections; R3 is multi-plane, sprayed and tested, meaning the fabric is built as several parallel planes, traffic is spread across them, and the design is proven by tests.

**What makes it different:**
- **Measured against a declared promise.** Every vital is reported as the fraction of its declared promise that is actually being delivered, from 0 to 100. The judging is done by a Rulebook that was fixed and published before the measurement started, so the rules are known before the result is. A score is always shown together with its class, in the form "Vitals Score N, class Rx (spec sheet version)", where N stands for the number and Rx for the preset (R1, R2 or R3) that the fabric declared.
- **Scored where jobs run.** A fabric owner declares one or more scoring scopes. A scoring scope is the part of the fabric that a training or inference job actually runs on, usually a pod or a scalable unit (the building block a fabric is grown by). Each scope gets its own score. A large fabric is reported as a set of scope scores with the lowest one named, never as one blended number.
- **The weakest vital sets the score.** The Vitals Score is the lowest of the seven vitals, not their average, and a critical condition (one of a short list of faults that are serious in their own right) caps the score while it is present. If four vitals score 100 and one scores 10, the fabric scores 10, not the 82 that an average would give.
- **Unknown is not healthy.** The Vitals Score is the confirmed score: it counts only what has actually been measured. Any capacity that was not measured is counted as if it were in its worst state, and the highest score the fabric could have had, if the unmeasured parts were healthy, is shown beside it as an upper bound. Coverage means how much of the fabric the telemetry (the measurement data that switches and network adapters export) actually reaches. If coverage is too low, the result is UNSCORABLE, together with a list of exactly which telemetry is missing and where.
- **Every score explains itself.** The score record names the binding vital or condition, the one that set the score; lists the contributors in order; and carries a full lineage, a trail from the score back to the raw counters it was computed from. Language models may explain a score to a reader, but they never compute it.
- **Vendor-neutral and open.** The method describes behaviour, not products, so it applies to any maker's equipment.

**Files:**

| File | What it contains |
|---|---|
| [`SPEC.md`](SPEC.md) | The method itself, with the requirements an implementer has to meet. Those requirements use the BCP 14 keywords (BCP stands for Best Current Practice, a series of internet-standards documents; this one fixes the meaning of capitalised words such as "must", "should" and "may") |
| [`RULEBOOK.md`](RULEBOOK.md) | The Rulebook, version RB-0.2, as a skeleton: the structure is complete but almost none of the values are filled in yet. It lists all 40 parameters, says for each whether it belongs to the Rulebook or to the spec sheet, and gives its status. Only one value is set so far: a physical-layer budget taken from an IEEE standard (IEEE is the Institute of Electrical and Electronics Engineers, the body that publishes the Ethernet standards). |
| [`SPEC_SHEET.md`](SPEC_SHEET.md) | The Fabric Spec Sheet template, with its fields numbered S1–S23; the lossless-configuration check (a lossless fabric is one configured so that packets are paused rather than dropped, and the check confirms that this configuration is consistent everywhere); the mapping that says which spec-sheet fields each vital is judged against; and the three class presets |
| [`templates/fabric-spec-sheet.yaml`](templates/fabric-spec-sheet.yaml) | A fillable copy of the spec-sheet template, as a plain-text file an owner can complete |
| [`METRICS.md`](METRICS.md) | The definitions of the metrics, numbered M01–M45, and whether each one is available through a vendor-neutral data model |
| [`SCENARIOS.md`](SCENARIOS.md) | The comparison of scoring formulas that led to the weakest-vital rule, and a table of 19 failure and event scenarios |
| [`VALIDATION.md`](VALIDATION.md) | The validation programme: the planned experiments that will set the Rulebook values and the preset values. It states what an emulated fabric (one simulated in software, without real hardware) can and cannot validate, and which experiments need real GPUs. |
| [`RELATED_WORK.md`](RELATED_WORK.md) | How Fabric Vitals relates to existing work: ITU-T M.3042 (a recommendation from the telecommunication standardization sector of the International Telecommunication Union), IETF drafts (from the Internet Engineering Task Force, the body that publishes internet standards), SAIN (Service Assurance for Intent-based Networking), QoO (Quality of Outcome), data-center facility tier practice, and the metric-checklist view (judging health by a checklist of separate metrics) |
| [`SEED_ISSUES.md`](SEED_ISSUES.md) | The open questions we most want answered |
| [`GOVERNANCE.md`](GOVERNANCE.md) | Who stewards the method, how versions work, the pre-registration rule (values are fixed and published before measurement, never adjusted afterwards), and the commitment to hand the method to a neutral body |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | How to open issues and propose changes |
| [`TRADEMARK.md`](TRADEMARK.md) | How the names "Fabric Vitals" and "Vitals Score" may be used (draft policy) |
| [`CHANGELOG.md`](CHANGELOG.md) | Version history |
| [`CITATION.cff`](CITATION.cff) | How to cite this specification |
| [`LICENSE`](LICENSE) | The CC BY 4.0 licence (Creative Commons Attribution), which lets anyone copy, share and adapt the text as long as they credit the source |

**Start on day one.** The Day-One Set is the smallest set of vitals, counters and probes (a probe is test traffic sent across the fabric on purpose, to measure it) that still yields a valid Vitals Score, chosen so that it can be fed from the telemetry most platforms already export. See SPEC.md §13.

**Out of scope in v0.x, and on the roadmap.** The following are not covered in v0.x but are candidates for future profiles (a profile is a variant of the method adapted to a different kind of network), listed in order of likely demand: front-end and inference-serving networks; storage and checkpoint traffic; scale-up interconnects, the links that join accelerators inside one server or rack (NVLink-class, including Ethernet-based scale-up); and multi-tenant isolation, keeping the traffic of different tenants apart. Security is excluded.

**How to take part.** The file CONTRIBUTING.md explains how. The three things we most need now are:
- critique of the method, of the split between what the Rulebook fixes and what the spec sheet declares, and of the class presets;
- reports of which telemetry your platforms export by default;
- offers of lab or production fabrics for validation, especially mid-sized clusters of about 32–2,000 GPUs.

Start with the questions in SEED_ISSUES.md.

**Steward:** datacenternetwork.ai is the steward, the organization that maintains the method, initially; how that may change is described in GOVERNANCE.md. **Disclosure:** the author organization develops network software. The proposal is written to be implementable by any vendor or operator. The method, its Rulebook and its class presets are vendor-neutral and are offered for open discussion.

*Fabric Vitals is not affiliated with, or endorsed by, any other organization that uses the word "vitals". "Fabric Vitals" and "Vitals Score" are claimed as marks of datacenternetwork.ai; see TRADEMARK.md.*
