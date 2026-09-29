# Fabric Vitals FAQ

**Sep 29, 2026 · Shankar Gopidas**

Plain-language answers about Fabric Vitals, the Vitals Score and the simulator, for readers who are not network engineers. Everything here follows the v0.2 proposal; where the proposal has not set a value yet, this FAQ says so.

## Status and claims

**What is the status of Fabric Vitals?**

Fabric Vitals v0.2 is an **open technical proposal** for discussion, critique and validation.

It is not a finished standard, certification or procurement benchmark. Most Rulebook values remain unset, and the score model and proposed class presets are being offered for industry validation.

Vendor-neutrality is the design goal, but complete cross-vendor telemetry and score equivalence have not yet been demonstrated.

The Vitals Score is a conformance reading against a declared Fabric Spec Sheet and common Rulebook. It is not a probability of failure, a reliability percentage or a percentile ranking.

## What does an AI data center do, and what is the "fabric"?

**Are training and inference the two workload profiles?**

Fabric Vitals v0.2 scores the **back-end scale-out fabric**: the high-speed network carrying accelerator-to-accelerator traffic.

That back-end fabric can use one of three workload profiles: **TRAINING, INFERENCE or GENERAL**. The profile changes some measurement details, such as the relevant delay statistic and test traffic.

Separate front-end networks, inference-serving network domains, storage/checkpoint networks, scale-up interconnects and multi-tenant isolation remain outside v0.x.

Training is teaching a model. Thousands of accelerators can work on one job for days or weeks and repeatedly exchange partial results. Every participant can end up waiting for the slowest exchange, so the back-end network can directly affect how fast the job proceeds.

Inference is using a trained model. Some inference systems also create accelerator-to-accelerator back-end traffic, but their latency, burst and communication characteristics can differ from training. The workload profile tells the Rulebook which back-end behavior is being judged.

**What is the fabric?** The dedicated, very fast network that connects accelerators to each other for scale-out communication. It is separate from the ordinary front-end network that connects services and users, and separate from storage. When engineers say "the back-end network" or "the scale-out fabric", they mean this network domain.

## What is Fabric Vitals, and what is the Vitals Score?

Fabric Vitals is a **proposed health score for AI data-center back-end scale-out fabrics**.

It measures how well a fabric is keeping the promises on its **Fabric Spec Sheet**, under a common **Rulebook**.

The Vitals Score is the headline result, from 0 to 100, or UNSCORABLE when there is not enough required evidence.

Think of the credit-score analogy only as: **one number at a glance, with the reasons underneath**.

Where does the name come from? A patient has vital signs: pulse, temperature, blood pressure. Each answers a different question. Fabric Vitals gives the network several vital signs and then provides a headline reading with the underlying reasons still visible.

Who computes it? A fixed, repeatable method that any conforming implementation can reproduce from the same telemetry, Spec Sheet and Rulebook. AI language models may help explain a result in words; they do not calculate it.

## What does "vendor-neutral" mean here?

The method is designed to describe network behavior rather than one vendor's product.

Some measurements already use common models. Others require vendor- or platform-specific adapters, especially some NIC, PFC, buffer and transport counters. The validation programme checks whether equivalent conditions produce equivalent evidence and scores across platforms.

## Who is this for?

The intended audience is anyone who owns, runs, designs or pays for an AI back-end fabric and needs a common way to discuss whether the network is keeping its declared promises.

| Who | What they own | What the score can give them |
|---|---|---|
| Operators of AI clusters | The fabric and the people who run it | One headline reading with the reasons underneath, plus history and evidence |
| Buyers of GPU capacity | A contract and an expected service level | A common technical framework for discussing whether the declared network promise was kept |
| Equipment and software vendors | Switches, NICs, NOS, telemetry and assurance tools | An open method they can implement, critique and help validate |
| Designers and consultants | Reference designs and architectures | A Spec Sheet that declares what a fabric is expected to deliver before measurement starts |

Three people can read the same score differently. The on-call engineer reads the current number and binding reason. The operations lead reads the score over a reporting period. The reliability engineer reads the trend and the underlying vitals to see deterioration before it becomes an incident.

Does it only fit the very largest clusters? No, but the public evidence is strongest at hyperscale. Mid-sized fabrics, roughly 32 to 2,000 GPUs, are an important validation gap and a priority for validation partners.

**Important current-use limit:** v0.2 is for technical discussion, experimentation and validation. It is not yet a certified benchmark, contractual acceptance test or procurement ranking.

## Why propose another layer if dashboards and assurance systems already exist?

Dashboards, health indexes, intent/assurance systems, alarms and test traffic are already useful. Fabric Vitals is meant to sit **above** them as a common measurement contract, not replace them.

v0.2 uses the lowest required vital as its headline because that prevents compensation by construction.

But validation does not assume that this is the final answer. In the simple example, four 100s and one 10 produce an arithmetic mean of 82 and a minimum of 10. That shows how the two aggregators behave differently.

E4 and E5 compare the current minimum, a calibrated minimum, an arithmetic-average comparator and other serious alternatives. The question is which model best preserves severe faults, tracks network-attributable operational impact, remains explainable and behaves robustly under uncertainty.

A number without a reason is not enough. Every Vitals Score names the area or critical condition that set it, lists the main contributors and preserves lineage back to the evidence, the Rulebook and the declared promise.

## What are the Rulebook and the Fabric Spec Sheet?

Think of how a car's range is rated. Every car is measured by the same official test procedure, but each car has its own rated range on its spec sheet.

- **The Rulebook** is the common test procedure. It says how fabrics are measured and judged: measurement methods, coverage rules, critical-condition logic, score bands once calibrated, versioning and other shared rules. It is published and fixed before measurement.
- **The Fabric Spec Sheet** is the declaration for one fabric. The owner states the in-scope back-end fabric, workload profile, topology and attachment model, resilience and recovery promises, performance envelope, required tests, telemetry profile and class or CUSTOM identity.

Why split them? Because "healthy" only has meaning relative to a promise. A fabric with one connection per accelerator is not unhealthy merely because it has one connection; it is unhealthy against a declaration that promised two.

What if the owner promises more than was built? The declared build is checked against the fabric as actually built. Missing redundancy counts as absent, the shortfall is visible, and the record can show what the score would be under the class actually built. A new Spec Sheet starts a new score series; it does not erase the old result.

Are the Rulebook's values set? Not yet. v0.2 defines the method and leaves most numerical values to the validation programme.

## What are R1, R2 and R3?

They are three **proposed class presets**: ready-made Fabric Spec Sheets offered as candidate reference profiles.

They are ordered by redundancy, not quality.

**R1** reflects a rail-optimized, single-homed training pattern documented in multiple current reference designs and operator reports. Each accelerator NIC attaches to one leaf on its rail.

**R2** is dual-homed: each NIC attaches to two leaves so the design can ride through the loss of one attachment within its declared limits.

**R3** is multi-plane, sprayed and tested: several independent planes, packet spraying across them, and required synthetic collective testing.

**The attributes below are the simulator's fictional declaration. Every numerical value is illustrative; the final preset values remain part of the validation programme.**

| Promise | R1 | R2 | R3 |
|---|---|---|---|
| Host attachment | One connection per accelerator NIC | Two connections | Multiple independent planes |
| Traffic distribution | Flow hashing | Flow hashing | Packet spraying |
| Resilience idea | Recovery may depend on restart/checkpoint | Dual attachment and spare capacity | Independent planes plus spraying and required testing |
| AI-style test traffic | Optional | Optional | Required by the current proposal |
| Typical use | **Example rail-optimized training design** | Example dual-homed design | Example multi-plane design with continuous assurance |

Which class should a customer pick? The one that actually matches what was built and what the owner is prepared to promise. Declaring a more redundant class without building it produces a visible design shortfall, not a better score.

## What are the seven vitals?

Each vital answers one question about the fabric. The current v0.2 proposal uses seven.

| Vital | Question it answers | Examples of evidence |
|---|---|---|
| D1 Reachability | Can endpoints that should communicate actually get packets through? | Interface/routing state and active probes |
| D2 Resilience | If the next tolerated failure happens, will the fabric still do its job? | Remaining redundancy, residual capacity, recovery and convergence |
| D3 Congestion and loss | Is traffic getting through without harmful loss, pausing or congestion spread? | Loss, PFC, ECN, buffers, NIC transport anomalies, configuration consistency |
| D4 Delay and tail | Is the network adding more delay than promised, especially at the tail? | Active probe delay against the declared budget |
| D5 Physical link integrity | Are links, optics and PHYs healthy? | FEC, CRC, errors, flaps, optics and distance to physical-layer budgets |
| D6 Effective capacity | Is enough usable bandwidth available where traffic goes? | Utilization, declared capacity and imbalance where applicable |
| D7 AI communication | Tested the way AI jobs use it, does the fabric perform as promised? | Synthetic collectives and related active tests |

Why is D7 different? It requires active AI-style test traffic, so in the current presets it is binding only where the Spec Sheet requires it. Otherwise it corroborates the other evidence.

## Why does v0.2 use the weakest vital?

The design goal is to stop one serious shortfall from being hidden by strong results elsewhere, so the current v0.2 computation uses the lowest required vital.

That is a testable proposal, not a predetermined final answer. E4 tests whether different vitals can be calibrated onto a sufficiently comparable impact scale. E5 then compares the current minimum, a calibrated minimum, an arithmetic average and other aggregation models. If another model performs better on the pre-registered criteria, a later normative version can change the aggregation method.

## What are critical conditions?

Six named situations can cap the score while active. A vital measures distance from a reference; a critical condition represents a serious state that should not be hidden by otherwise healthy readings.

| Condition | Plain meaning |
|---|---|
| CC1 Partition or black hole | Traffic enters part of the network and silently disappears |
| CC2 PFC storm or deadlock | Pause behavior spreads until traffic stalls |
| CC3 Sustained loss on a lossless class | A class that promises lossless behavior is persistently dropping packets |
| CC4 Single point of failure | Applies where the Spec Sheet promised no such single point |
| CC5 Redundancy exhausted | The spare capacity or failure tolerance promised by the design has been used up |
| CC6 Uncorrectable errors beyond budget | Physical errors exceed the declared/standard budget |

How big must a fault be to count as critical? It must reach the Rulebook's blast-radius rule within the scoring scope. The numerical threshold is not yet set.

When does a condition clear? Only when it is positively observed to have cleared; missing telemetry does not silently clear it.

Contributors can be tagged OPERATIONAL, DESIGN SHORTFALL or PLANNED so the same headline can still explain what kind of problem produced it.

## What happens when data is missing?

Anything not measured counts as unknown, never as healthy. The score is computed over the declared inventory and is shown with an upper bound representing the best case if the missing evidence were healthy.

Can hiding a problem raise the confirmed score? The method is specifically designed to prevent that. Removing telemetry reduces what the evidence can confirm and can make the result UNSCORABLE.

What is UNSCORABLE? When required coverage is below the Rulebook's coverage floor, Fabric Vitals gives no numeric score and lists what evidence is missing and where.

**Won't fabrics with thin monitoring be UNSCORABLE?**

Some may be. The proposal includes a **Day-One Set**, the proposed minimum starting set of counters and probes needed to compute a score.

It prefers common data models where they exist and uses platform adapters where necessary. Validation will determine how portable and equivalent that minimum is across vendors.

What about a brief data-collection hiccup? The proposal includes a bounded grace period so a short collector restart does not automatically look like a fabric failure. The final grace values are part of validation.

## The score changes over time. How do I read it?

A score is a reading, not a verdict. The current number and reason matter now; availability over a period shows how often the fabric met its declared healthy condition; the time series shows direction and slow decay.

The history view shows score readings, the upper-bound band, critical-condition intervals, UNSCORABLE gaps and Spec Sheet/class changes. It is not smoothed, so a serious event is not averaged away.

Annotations are derived from the score record itself. Operators may add notes, but notes do not create or erase score events.

## How do systems do this today?

There is substantial prior art. IETF SAIN defines service-health conventions and explanatory symptoms. ITU-T M.3042 defines a communication-network health-index framework. IETF Quality of Outcome uses requirement-relative sub-scores and minimum aggregation. Vendors also provide health, assurance and intent-validation systems, and facility standards provide resilience/rating precedents.

Fabric Vitals builds on those ideas. Its proposed contribution is the combination of a pre-declared fabric promise, a common Rulebook, AI-fabric evidence, deterministic scoring, explicit missing-data treatment, critical conditions, evidence lineage and open pre-registered validation.

## How do I use the simulator?

The simulator runs the **actual proposed v0.2 scoring mechanics** on a fictional 256-GPU pod, using **illustrative Rulebook values**.

You set the conditions and watch how the method reacts. The point is to make the proposal easy to challenge: introduce failures, remove telemetry or change the illustrative Rulebook and see what happens.

The simulator lets you declare R1/R2/R3, compare the declared design with the fictional build, inspect the Vitals Score and seven vitals, view a synthetic history, and introduce conditions such as a PFC storm, tail delay, a black hole, exhausted redundancy, an over-claimed class, hidden telemetry or a collector restart.

Are the colours official? No. The bands shown in the simulator are illustrative until calibrated against measured impact.

## What is not done yet?

The numerical Rulebook values are not set, and validation still has to resolve the final aggregation method, cross-vital calibration, exact thresholds, band edges, coverage rules, D7 calibration, mid-scale calibration and cross-vendor measurement equivalence.

The simulator demonstrates the proposed mechanics; it does not validate those values or choices.

How will values be set? Through the validation programme: emulation/replay for scoring mechanics first, then hardware/GPU experiments and production shadow scoring where needed.

What can the score be used for today? Discussion, experimentation and design review - not certification, contractual acceptance or procurement ranking.

Where is the evidence thin? Especially mid-sized fabrics, roughly 32 to 2,000 GPUs, and some cross-vendor telemetry semantics.

Can a fabric score 100 today? The simulator can show 100 using illustrative values. A production-grade real-world score requires a Rulebook whose relevant values have been established through the validation process.

## How do I get involved?

Three kinds of help are especially useful:

- **Expert review:** challenge the method, proposed class presets, Rulebook / Spec Sheet split and aggregation model.
- **Validation partners:** offer lab or production fabrics, especially mid-sized clusters, to help test assumptions and set evidence-backed values.
- **Standards and telemetry input:** help identify which switch and NIC measurements are genuinely equivalent across vendors and where common definitions are still needed.

Where everything lives:

- Simulator and public explanation: datacenternetwork.ai/fabric-vitals
- Specification, Rulebook skeleton, Spec Sheet, metrics, scenarios and open questions: github.com/fabric-vitals/spec
- Contact: hello@datacenternetwork.ai

## Who is behind it?

Fabric Vitals is authored and currently stewarded by datacenternetwork.ai, a company that develops network software.

Governance today is author-stewarded and open to contribution. The governance document commits to transferring the specification, Rulebook, class presets and the “Fabric Vitals” / “Vitals Score” marks to an open multi-party body if the community chooses that path.
