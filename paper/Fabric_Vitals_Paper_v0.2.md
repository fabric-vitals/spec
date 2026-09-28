# Fabric Vitals: a vendor-neutral health score for AI data-center fabrics, measured against a declared design

**Shankar Gopidas, Founder & CEO, datacenternetwork.ai**

*Fabric Vitals v0.2 (draft) — a technical proposal for discussion. Not a standard. Rulebook values not yet set.*

---

## Summary

The networks that connect GPUs in AI data centers are watched through dozens of separate signals, but there is no shared answer to the question operators, owners and customers keep asking: *is this AI fabric healthy?* This paper proposes **Fabric Vitals**, a vendor-neutral method that produces one number, the **Vitals Score**, readable at a glance like a credit score.

The method works like the rating of a car's range. Every car is measured by the same official test procedure, but each car has its own rated range. In Fabric Vitals, a **Rulebook** that is identical for every fabric says how fabrics are measured and judged, and a **Fabric Spec Sheet**, declared by the owner before measurement, says what this fabric promises. The Vitals Score confirms whether the fabric keeps its promises. Four design choices make that confirmation credible:
- **Seven vitals** are measured from network evidence only.
- **The headline is the weakest vital,** capped by named critical conditions, so one collapsed area cannot be averaged away.
- **Unmeasured parts of the fabric count as unknown, not healthy,** so hiding telemetry cannot improve the score.
- **Every rule and every promise is fixed and published before measurement.**

The method is defined here. The Rulebook's values are not: they are to be set through an open validation programme.

---

## 1. The problem

Operators of AI fabrics watch link states, drops, ECN marks, PFC pauses, buffer occupancy, retransmissions, latency tails, forward-error-correction statistics, optics readings, routing state and synthetic collective tests. Each signal is useful. None answers "is this fabric healthy?", and today that question is answered in four incompatible ways:
- **pass/fail gates**, such as node and switch health checks and acceptance tests [1, 2, 3];
- **each operator's own thresholds**, for example Meta's PFC watchdog above 200 ms and buffer alarms above 80% [4];
- **deviation from a baseline or from peers** [5, 6, 7];
- **vendor dashboard scores** whose inputs and weights are only partly documented [8, 9, 10].

These answers share three weaknesses.

**They are not comparable.** Each operator's thresholds and baselines are its own. A baseline-relative "healthy" means "unchanged", not "built and running as designed". A fabric that has been degraded since day one becomes its own normal.

**Averages hide failures.** Several vendor scores average their inputs [9, 11]. Take a fabric with four areas at 100 and one collapsed to 10. Its arithmetic mean is 82, exactly the score of a fabric that is uniformly mediocre at 82. The OECD/JRC handbook on composite indicators shows the same full compensation with its (21, 1, 1, 1) versus (6, 6, 6, 6) example [12].

**They do not say what the network was supposed to be.** Losing one uplink is routine in a fabric designed to tolerate two link failures, and serious in a single-homed one. In one 256-GPU testbed, training "cannot recover" when a single-homed link's repair takes more than two minutes, while a dual-homed design saw 6.25% degradation [13]. In a multi-plane design with packet spraying, the job continues through a lost NIC-to-switch link [14]. The same physical event means different things depending on design and transport.

---

## 2. Why AI fabrics need their own health measure

A characteristic of AI fabrics justifies a dedicated measure only if it changes **what is measured, how it is normalized or how it is aggregated**. Six do.

1. **Synchronized collectives are gated by the slowest transfer** [13, 14, 15]. A single bad link can slow a whole training step, so the aggregation must be tail-dominated and non-compensatory.
2. **Congestion behaviour depends on the transport.**
   - Lossless RDMA over Ethernet brings PFC head-of-line blocking, pause storms and deadlock [16, 17, 18].
   - The available signals depend on the congestion-control mode. Without DCQCN, Meta monitors NIC pause duration instead of congestion-notification counts [4].
   - The same loss rate means different health under different transports. In a two-server test, 0.4% deterministic loss gave zero goodput under go-back-0 retransmission [16], while a multipath spraying transport with selective retransmission rides out tier-to-tier link flaps [14].
3. **Low-entropy elephant flows and bursts.**
   - ECMP hash collisions limited RDMA to 60% utilization in one Microsoft experiment across two podsets of a new data center [16].
   - Bursts saturate 400G NICs for seconds [13].
   - At four-minute polling, utilization barely predicted drops (r = 0.098, in a general data-center study) [19].

   Capacity evidence must therefore be burst-aware, and load-imbalance metrics apply only to flow-hash fabrics.
4. **Gray failures are hidden by redundancy.**
   - In one production job on about 75,000 GPUs, a switch that stayed "up" but stopped forwarding dropped about 580,000 packets without device state showing it [14].
   - Silent drops and black holes appear only to active probing [5].
   - Standalone stress tests catch degradation that monitoring of running workloads misses [1].
5. **Rail, multi-plane and rail-only topologies.**
   - Rail-only fabrics are *meant* to lack any-to-any paths [20].
   - In one published design comparison, losing a single tier-to-tier link removes 3% of a node's capacity in an 800G plane but 0.4% in a 100G plane (design arithmetic, not measurement) [14].
   - A vendor reference design already prescribes dual planes at 256 GPUs [21].

   Health must therefore be normalized to capacity share and to the declared design.
6. **Training and inference differ.** Collective tail and throughput dominate training [13, 15]. Time-to-first-token, time-per-output-token and KV-cache transfer dominate disaggregated inference [22, 23].

Everything else is shared with generic network health. That is where existing standards are reused rather than replaced (Section 7).

---

## 3. Design principles

**Principle 1: measured against a declared reference.** A health score is a confirmation of conformance to an agreed standard. An AI fabric is designed to a level of resilience and recovery, and the score confirms whether it meets that level. Every metric and threshold either comes from an agreed standard or best practice, or is explicitly defined, with documented reasoning, **before** anything is measured. How fabrics are judged is fixed in the Rulebook; what each fabric promises is fixed on its spec sheet. No value is tuned after the fact.

**Principle 2: simple at the top, deep underneath.** One number, always shown with its spec sheet and class, its range, the reason it has its value, and the full set of vitals.

**Principle 3: no false health.** One catastrophic condition cannot be concealed by several excellent ones.

**Principle 4: unknown is not healthy.** Unmeasured capacity lowers the *confirmed* score. It never raises it.

**Principle 5: no false precision.** Integers only. Colour bands are a display rule, published only once calibrated. Every parameter without evidence is marked "value not set".

**Principle 6: vendor-neutral.** The method describes behaviour, not products. Where vendor-neutral telemetry does not exist yet, the dependency is stated.

**Principle 7: deterministic.** The same telemetry, spec sheet and Rulebook always produce the same score. Language models may explain a score but never compute it.

---

## 4. How Fabric Vitals works

### 4.1 Two inputs: the Rulebook and the Fabric Spec Sheet

Every car's range is measured by the same official test procedure, but each car has its own rated range, printed on its spec sheet. Nobody expects a small city car and a long-distance saloon to have the same range; everybody expects both to be measured the same way. Fabric Vitals makes the same separation.

**The Rulebook (identical for every fabric).** The Rulebook (called the reference profile in v0.1) says how to measure and how to judge: the metric definitions and measurement procedures; the coverage floor; the blast-radius threshold; the grace period; the critical-condition definitions and cap; the rules for UNSCORABLE; the temporal windows; the score band edges; and the versioning rules. It is published and frozen before measurement, and it is the same for every fabric.

**The Fabric Spec Sheet (declared per fabric, before measurement).** The owner fills in a standard template with 23 fields:
- **purpose and workload profile:** training, inference or mixed;
- **scoring scope:** the unit within which jobs run, a pod or scalable unit, which is scored as one (Section 4.10);
- **build:** topology, host attachment, uplinks and subscription ratio, planes, transport (flow hashing or packet spraying), the lossless-transport configuration, and physical diversity;
- **resilience promise:** the failures the fabric rides through without capacity loss, and its recovery objective, including routing convergence time;
- **availability target:** the share of time the Vitals Score stays in the healthy band (Section 4.8);
- **performance envelope:** bandwidth per accelerator, collective bandwidth reference, tail-delay budget, loss and pause budgets, and physical-layer budgets;
- **required tests:** whether synthetic collectives are required, and the telemetry the fabric exports;
- **declared class** (a preset or custom, Section 4.2) and spec-sheet version.

**Each vital checks spec-sheet fields.**

| Vital | Spec-sheet fields it checks |
|---|---|
| D1 Reachability | Scope and inventory; topology; host attachment |
| D2 Resilience | Host attachment; uplinks and subscription; planes; failures ridden through; recovery objective, including convergence time |
| D3 Congestion and loss | Transport; lossless-transport configuration; loss budget; pause budget |
| D4 Delay and tail | Workload profile; tail-delay budget |
| D5 Physical link integrity | Physical-layer budgets |
| D6 Effective capacity | Uplinks and subscription; transport (hashing or spraying); bandwidth per accelerator |
| D7 AI communication | Collective bandwidth reference; required tests |

**The register split.** Every parameter in the register is labelled Rulebook or Spec sheet. Parameters that are really per-fabric promises (the pause budget, NIC retransmission budget, early-warning margin for bit errors, residual capacity after failures, recovery objectives, the class values themselves, and the physical-layer budgets as a standard floor) move to the spec sheet, with the status **VALUE DECLARED BY OWNER**. The tail-delay budget and the collective bandwidth reference keep their measurement method in the Rulebook and take their value from the spec sheet. Everything that decides *how we judge* (coverage floor, grace period, blast-radius threshold, the coupling rule between them, the cap, event definitions, band edges) stays in the Rulebook. Of 40 parameters, **31 are Rulebook, 7 spec sheet and 2 both**.

The spec sheet can promise less, but it cannot hide what it promises. The declaration is public in the score record, and comparisons are allowed only between fabrics on the same class or identical spec sheets (Section 4.9).

### 4.2 Class presets and the conformance check

**Class presets are the standard models.** Most owners should not have to write a spec sheet from scratch. Fabric Vitals publishes three **class presets**: complete spec sheets, each with its **structural predicates** (the build a fabric of that class must have) *and* its **promise fields** (what it promises). **Classes are design patterns ordered by redundancy, not quality tiers.** A fabric that keeps the promises of its class is healthy, whichever class it is.

| Class | Name | What it is |
|---|---|---|
| **R1** | Rail-optimized, single-homed | The most common training design in published reference designs today. Each accelerator NIC attaches to one leaf of its rail; recovery from a leaf failure is by checkpoint restart. |
| **R2** | Dual-homed | Rides through a leaf failure, or a bounded number of uplink failures per rail, without losing capacity. |
| **R3** | Multi-plane, sprayed, tested | Independent planes, packet spraying across them, and continuous synthetic collective tests. |

The patterns are all in use. In one vendor's validated design, "rail Nth connects all GPUs in position Nth on all the servers, to leaf node Nth" [24], and another vendor's reference compute fabric "is rail-optimized" [25]; Alibaba describes single-ToR attachment as "widely used in the majority of current cloud providers" [13]. Alibaba's own production design "connects two ports of each NIC to different ToRs in an active-active way", so that "if one ToR (or a port) is down, the other can still work" [13]. Multi-plane designs with packet spraying ride through tier-to-tier link failures [14].

An owner may instead declare a custom spec sheet; comparability then holds only between fabrics on identical spec sheets. The preset's name fixes its pattern; **all numeric preset values are proposed and not set,** except the physical-layer budgets, where the IEEE budget applies (Section 4.3).

**Why failure consequence, not path counts.** Facility standards count distribution paths [26, 27]. Rail-optimized AI designs, however, attach each NIC to a single rail switch by design, and one open reference design states that "no redundancy is assumed or required" [28]. AI resilience comes instead from planes and spraying [14], dual top-of-rack attachment [13] or designed spare capacity. In one AI zone, Meta chose an under-subscription ratio "to allow for buffer for up to two link failures" [4]. Presets are therefore stated as *failure consequence*.

**The borrowed ideas and the proposal.** Four ideas come from data-center facility practice:
- owner declaration before design, from business impact [29];
- rating by the weakest subsystem: "The site's Tier rating is the lowest of the individual subsystem ratings" [30];
- no fractional ratings [30];
- outcome-based confirmation tests [30].

The preset scheme itself is the author's proposal, derived from public sources, and offered for critique.

**The build is checked against the fabric as built.** The **verified class** is the most redundant preset whose structural predicates all hold. It is checked three ways: by static comparison of the declared build with the discovered topology and running configuration; by a residual-capacity computation under the declared tolerated failures; and by periodic controlled-failure tests measured with synthetic collectives, which also measure recovery and convergence time against the recovery objective. The **conformance status** is CONFORMANT, NON-CONFORMANT (with the failed predicates listed) or NOT ASSESSED.

**The score is computed against the declared spec sheet, and over-claiming is visible.** Redundancy that was declared but never built counts as absent:
- the resilience vital counts it as absent, so a complete over-claim scores 0 on D2 by the common-currency definition (Section 4.4), and a partial shortfall scores the fraction actually delivered;
- the single-point-of-failure condition fires where the spec sheet promised none.

The record and any display must show the counterfactual: **"declared Rx, built as Ry; as Ry it would score N"**, tagged DESIGN SHORTFALL, with re-declaration as the remedy. An honest, versioned new spec sheet starts a new score series. This penalizes only over-promising, because the spec sheet is the owner's own choice (worked example in Section 5).

A permanent shortfall can pin the headline for as long as it lasts. To keep operational faults visible during that time:
- every binding reason is tagged DESIGN SHORTFALL, OPERATIONAL or PLANNED (Section 4.8);
- a breadth indicator and the full set of vitals keep moving even while the headline cannot (Section 4.5).

### 4.3 The Rulebook, fixed before measurement

Every score is computed against a named, versioned Rulebook. The first, RB-0.2, lists 40 parameters (T1–T40). The basis of each Rulebook value, or of each preset value, is one of four reference categories:
- **(a) Standard exists.** The IEEE 802.3 physical-layer budgets are the only case. The complete-PHY post-FEC frame loss ratio is 6.2×10⁻¹¹ for 64-octet frames at 200G and above, and 6.2×10⁻¹⁰ at 100G, derived from the bit-error-ratio objectives of the IEEE 802.3 projects [31, 32, 33, 34, 35, 36]. The Ultra Ethernet specification reproduces them [37, 38]. They are used as distance to budget, not as alarm levels. On a spec sheet they are a floor: an owner may promise better, never worse.
- **(b) Best practice exists, graded by authority**, for example the Ultra Ethernet method for estimating link reliability from FEC statistics [37]. A single vendor's or single operator's value is usable only as a declared reference for its own technology.
- **(c) Must be defined by Fabric Vitals.** The value is set only by named validation experiments, and frozen before use.
- **(d) Method only.** No universal number can exist. ECN marking, for example, depends on configured thresholds [4, 17]. The Rulebook then standardizes the procedure: declared configuration, a measurement definition, a commissioning measurement under a standard test suite, the declared value and any preset acceptance criterion, and versioned re-registration on any change. Operators already work this way: one 800-GPU cluster fixed its ECN and PFC parameters after a vendor-validated sweep and left them unchanged [39].

**Baselines become anomaly evidence.** Rolling baselines and peer comparisons still run, but they only produce findings and trigger investigation. They never move a score. A learned baseline turns whatever a fabric *is* into what it *should be*.
- One cloud validation system learns its criteria from the fleet's own results with "no ground-truth on which nodes are defective" [1]. The inference that a uniformly degraded fleet would then set its own criteria is ours; the paper does not test it.
- Peer comparison across planes is valid only where the transport keeps planes equally loaded [14].

In RB-0.2, **1 parameter has a standard behind it, 4 rest on graded best practice, 26 must be defined through experiments, and 9 are methods.** Only one value is set: the IEEE budget. The Rulebook is a skeleton until validation fills it.

### 4.4 The seven vitals

**A common currency.** Every vital is measured on one scale: **the fraction of the declared promise being delivered**, from 0 (none of it) to 100 (all of it), judged against the spec sheet. A resilience vital of 75 means three quarters of the declared resilience is available now; a congestion vital of 75 means three quarters of the promised loss and pause envelope is being kept. This is what makes the weakest-vital rule meaningful (Section 4.5): the headline is the promise that is least kept. It is the design intent of the Rulebook's value functions and their anchors (parameters T25 and T31), whose shapes remain to be calibrated.

| Vital | Question it answers | Main evidence |
|---|---|---|
| **D1 Reachability** | Can every endpoint that should reach every other get packets through? | Control-plane state compared with intent, including routing stability, *and* data-plane probes (the only way to see black holes) |
| **D2 Resilience** | If the next tolerated failure happens, will the fabric still do its job? | Remaining redundancy and residual capacity relative to the spec sheet; measured recovery and convergence time against the recovery objective |
| **D3 Congestion and loss** | Is traffic getting through without harmful loss, pausing or congestion spread? | Loss by cause, PFC pause time, storms and deadlock, buffer stress, ECN against its registered reference, NIC transport anomalies, lossless-configuration consistency |
| **D4 Delay and tail** | Is the network adding more delay than it should, at the tail? | Probe delay per path class against the tail-delay budget |
| **D5 Physical link integrity** | Are the links, optics and PHYs healthy? | Distance to the physical-layer budgets, link reliability from FEC statistics, errors, flaps, optics |
| **D6 Effective capacity** | Is there enough usable bandwidth where traffic goes, spread well? | Peak utilization in communication phases against declared capacity; imbalance on flow-hash fabrics |
| **D7 AI communication** | Tested the way AI jobs use it, does the fabric perform as promised? | Synthetic collectives and RDMA pair scans on known-good hosts |

**What is in scope.** Only network-attributable evidence is scored: signals from switches, NIC ports and transport counters, running configuration, or active measurements that exercise the network independently of tenants' compute. Raw job signals are excluded because they mix in non-network causes:
- one collective-library error code covers GPU crashes, network disconnection, out-of-memory and user code [40];
- a host PCIe downgrade surfaced as a surge in PFC pauses [41].

Job signals enter only after attribution to a network element [7, 40].

**Two named gaps, now explicit.**
- **Lossless-transport configuration consistency.** Lossless RDMA needs PFC priorities, ECN marking, the DSCP-to-traffic-class mapping and MTU to agree across switches and NICs. Misconfiguration is a documented failure cause: in Meta's lossless fabrics, congestion drops were "uncommon and observed mostly due to misconfiguration" [4], and Microsoft traced one production incident to "the buffer misconfiguration of a newly introduced switch type" and runs a service that checks running against desired configuration on switches and servers [16]. The declared configuration is a spec-sheet field and a conformance check; a live mismatch is D3 evidence. It is not a new critical condition, because its harmful consequences are already capped by the loss, storm and black-hole conditions.
- **Routing stability and convergence time.** Session flaps and route churn are named D1 control-plane evidence. Routing convergence time is part of the recovery objective and is judged by D2, measured in controlled-failure tests and, where probes allow, on real events. The IETF AI-fabric benchmarking draft already lists FIB and route convergence time, the time to converge routing after a topology change, among its fabric health indicators [42].

**The D7 exception.** D7 is corroborating unless the class requires it; of the presets, only R3 does. Its cost is bounded by method: short runs, a small reserved set of nodes or scheduled gaps between jobs, and a frequency bound, with the values not yet set. This avoids a perverse incentive: if D7 simply joined the minimum whenever it was run, a fabric that tests itself could only ever score the same or lower than one that does not.

**Deliberate exclusions.** Security is excluded. Front-end and inference-serving networks, storage and checkpoint traffic, scale-up interconnects and multi-tenant isolation are out of scope in v0.x and are candidate future profiles (Section 8).

**Vendor-neutral telemetry is uneven.**
- Physical-layer counters are well covered by IEEE and OpenConfig models [43, 44].
- PFC counters and buffer watermarks exist in the SAI switch interface but not in OpenConfig, and the IEEE 802.3.2 PFC counters are deprecated [43, 44, 45]. PFC configuration has no OpenConfig model either [46].
- RDMA NIC counters have no vendor-neutral set; their names and meanings differ by driver [47].

The congestion vital therefore depends on work outside this proposal. The dependency is stated, not hidden.

### 4.5 The weakest-vital headline and critical conditions

**The Vitals Score is the minimum across the vitals the spec sheet requires.** No weights are used. Precedents:
- the IETF Quality of Outcome draft scores by the minimum over its sub-scores [48];
- ITU-T M.3042 takes a minimum across network-element types inside 8 of its 21 third-level indexes [49];
- US bridge-condition rules rate each bridge by its minimum component rating [50];
- facility tiers rate a site by its lowest subsystem [30].

**The minimum is not assumption-free.** It assumes the vitals are commensurable: a 60 in physical integrity must mean as bad as a 60 in congestion. The common currency makes equal values mean the same share of each promise delivered *by definition*. Whether that also means equal operational impact is an open empirical question, tested by experiment. The minimum also ignores non-binding vitals. So every headline is printed with:
- a **breadth indicator** ("k of 7 vitals not delivering their full promise");
- the **next-binding vital**;
- trends on the full set of vitals.

**Critical conditions cap the score whatever the vitals show.** Each names itself as the reason:

| Condition | Why it matters |
|---|---|
| CC1 Partition or black hole | Black holes and silent drops are invisible to device state [5, 14] |
| CC2 PFC storm or deadlock | "a single malfunctioning NIC may block the entire network" [16] |
| CC3 Sustained loss on a lossless class | "normally no RDMA packets should be dropped" [16] |
| CC4 Single point of failure on job-bearing capacity | Applies only where the spec sheet promises none [13] |
| CC5 Redundancy exhausted | In one testbed, all-reduce regressed once more than half of a switch's *redundant* uplinks were down [1] |
| CC6 Uncorrectable errors beyond the IEEE budget | The physical-layer budget above, measured as a link reliability ratio [37] |

A condition caps the score only when the job-bearing capacity it affects reaches a **blast-radius threshold** (T16). The cap value (T15), the persistence time and the blast-radius threshold are Rulebook parameters, all "value not set".

### 4.6 Confirmed score and range

**Unmeasured capacity is treated as unknown.** Each vital is computed twice over the *declared* inventory:
- once with every unmeasured entity or time slice at 0, giving the **lower bound**;
- once with every unmeasured entity or time slice at 100, giving the **upper bound**.

The **Vitals Score is the confirmed lower bound**, printed with the upper bound and the coverage. Critical conditions count unmeasured capacity as affected. Once raised, a condition clears only when it is observed to have cleared, never because telemetry stopped.

**Removing telemetry cannot raise the score.** Removing telemetry can only lower each lower bound, can only increase the affected share for each condition, and the minimum is monotone. A simpler rule that excludes unmeasured areas fails this test. In an illustrative case, hiding three bad switch groups *raises* the score from 69 to 80 (Section 5).

**Two refinements.**
1. **Grace period.** Collector restarts and missed polls are not fabric events. A sample therefore becomes "unmeasured" only after it is older than its declared sampling interval plus a **grace period G** (parameter T30). During the grace period, counters use their last completed interval and gauges carry their last value forward. The price is bounded: removing telemetry can never raise the score above what full telemetry would have shown at some moment within the preceding G. G = 0 restores the strict property. The value of G per metric type is to be set by an experiment that measures false drops caused purely by telemetry gaps.
2. **Coupling the coverage floor and the blast radius.** Below a **coverage floor F** (parameter T29) the result is UNSCORABLE. Could a fabric that passes the floor still be capped "critical" purely because some capacity is unmeasured? Unmeasured share u satisfies u ≤ 1 − F, and it alone reaches the blast-radius threshold only if u ≥ T16. Both hold together exactly when F + T16 ≤ 1. So, by default, **every critical condition must satisfy F + T16 > 1**, with both shares measured on the same capacity base (constraint T39). A Rulebook may relax this for a specific condition only with a written rationale.

   The consequence is intended. Hiding a region large enough to trigger a condition forces coverage below the floor, so the fabric becomes UNSCORABLE instead of escaping the cap. Fabrics with thin telemetry, including many small clusters, will be UNSCORABLE for affected conditions until their telemetry improves.

**Evidence-quality confidence** is reported separately. It covers sample age within the grace period, resolution, platform capability, counter integrity [51] and comparability of counter meanings across vendors [47]. It never changes the number.

### 4.7 UNSCORABLE, with a missing-telemetry list

When coverage falls below the floor, the result is **UNSCORABLE**, meaning "conformance not confirmed". It ranks below every numeric score and is never shown as a pass. This follows the IETF service-assurance convention that −1 means "no value could be computed" [52], and the practice of declaring thin credit files unscorable [53].

An UNSCORABLE result **must list exactly which required telemetry is missing, and where**: vital or condition, entity, metric, capacity share, and whether each item is missing, stale beyond grace, or unsupported by the platform. The result is an instruction to the operator, not a dead end.

### 4.8 Availability and score bands

**Availability.** Owners and customers often ask a time question: "how much of the time was the fabric healthy?" Fabric Vitals answers it with one definition. Over a period, divided into scoring windows, **availability is the share of windows in which the Vitals Score is in the healthy band and no critical condition is active.** "Healthy X% of the time" means exactly that. UNSCORABLE windows count as not healthy, because unknown is not healthy, and their share is reported beside the figure. The owner declares an availability target on the spec sheet; availability is reported against it as met or not met. Availability accompanies the score and never changes it. No target values are proposed.

**Score bands.** Bands are a **display rule**, not part of the score. The Rulebook parameter T40 holds two band edges (value not set):
- **green** at or above the upper edge;
- **amber** between the edges;
- **red** below the lower edge;
- **red, regardless of the number,** while any critical condition is active;
- **grey** for UNSCORABLE.

The cap value lies below the lower edge, so a capped score is red by number as well as by rule. Bands are part of the Rulebook and are published only once calibrated against measured impact. Until then, any displayed bands are illustrative and must be labelled so; demonstrations of the method use illustrative edges. Voice-quality bands that look similar belong to a different scale and must not be borrowed [54].

**Planned maintenance.** Maintenance reduces the resilience a fabric actually has, so the score reflects it. When a maintenance window was declared in advance (declarations are versioned, like the spec sheet), the affected contributors are tagged **PLANNED**. The spec sheet states whether declared windows count against the availability target. There is no undeclared "maintenance mode": nothing suspends scoring.

### 4.9 Every score explains itself

- **The top-level explanation is exact.** Under the minimum, the score equals a named vital or a named critical condition.
- **Contributors follow.** Below the top level, contributors are listed in order, following the credit-score practice of listing the factors with "the most influence first" [55]. This also satisfies the IETF rule that "a non-maximal score must always be explained by one or more symptoms" [52].
- **Full lineage.** Every value links to the raw counters, the value-function version, the Rulebook entry and the spec-sheet field it was judged against.
- **Presentation.** A score is never shown without its class. The unit of presentation is "Vitals Score N, class Rx (spec sheet version)"; a bare number is non-conformant. Scores are integers, shown with their band.
- **Language models** may turn the structured result into prose. They never compute or change it.

Scores are comparable for the same fabric over time (under the same spec-sheet version), and between fabrics on the **same class preset, or on identical spec sheets, under the same Rulebook version**. A score for one class is not a ranking against another: it confirms conformance to its own spec sheet.

### 4.10 Scoring scope and large fabrics

A job runs inside a pod or scalable unit, and it is gated by the slowest transfer there [13, 14]. A Vitals Score therefore applies to a declared **scoring scope**: that unit, stated on the spec sheet. A fabric with many pods is reported as a **set of scope scores**, with their distribution and the lowest scope named, never as one capacity-blended number; a blended figure would let one failing pod disappear into a large healthy fabric, which is the averaging problem again. Coverage floors and blast-radius thresholds are evaluated within the scope.

### 4.11 Starting on day one

An operator can start with the **Day-One Set**: the smallest set of vitals, counters and probes that yields a valid Vitals Score, drawn from telemetry most platforms already export. It covers every vital with standard counters: interface state, routing sessions, cabling checks and a probe mesh for reachability, resilience and delay; drops, switch-side ECN marks and, on lossless fabrics, PFC pause time for congestion; FEC, CRC and flap counters for the physical layer; and interface octets for capacity. A score computed from it is a Vitals Score like any other, under the same Rulebook. Richer telemetry (NIC transport counters, buffer watermarks, in-band telemetry, optics) is optional: where it is not observed, it is listed as unscorable at the metric level and reflected in evidence-quality confidence, never in the score.

---

## 5. A worked example

*Every number in this section is ILLUSTRATIVE.*

**The masking example.** Four vitals are at 100 and one is at 10. The arithmetic mean is 82. So is the result of any scheme that sums across areas, including M.3042's two-stage form, which takes minimums inside areas but sums across them. The Vitals Score is **10**, with the binding reason named.

**A fabric under stress.**
- The vitals are D1 100, D2 90, D4 85, D5 97, D6 80.
- For congestion (D3), the fabric has ten leaf groups, each carrying 10% of the relevant capacity. Seven are at 95. Three are under PFC stress at 10 and are in an active pause storm (CC2).
- Using a simple capacity-weighted mean for illustration, D3 = 69.5.
- The storm affects 30% of capacity. Against an illustrative blast-radius threshold of 25%, the condition fires, so the score is capped and names CC2.

**The operator hides the three stressed groups.**

| Rule | What happens |
|---|---|
| Excluding unmeasured areas (the rejected design) | The groups vanish, D3 becomes 95, and the headline *rises* to 80 |
| Fabric Vitals, coverage floor 80% | D3 coverage falls to 70%, below the floor: the result is **UNSCORABLE**, listing the three leaf groups and their missing congestion counters |
| Fabric Vitals, coverage floor 65% (the illustrative F + T16 = 0.90 breaks the coupling rule) | The confirmed D3 is 66.5 and the unmeasured 30% still triggers CC2, so the operator gains nothing. But in this configuration, three merely *unmonitored* healthy groups would also cap the score, which is why the default Rulebook forbids it |

**A collector restart.** All congestion telemetry arrives 40 seconds late, with a 10-second sampling interval.
- With no grace period, coverage collapses and the fabric falsely becomes UNSCORABLE.
- With a 60-second grace period, nothing changes.

**Over-claiming.** An owner declares class R2 (dual-homed) for a 256-NIC scoring scope.
- *Complete over-claim:* every NIC is in fact single-homed, so the fabric is built as R1. None of the declared second attachments exists, so D2 delivers none of its declared promise: **D2 = 0**, and the Vitals Score is 0, class R2, tagged DESIGN SHORTFALL. The record adds: "declared R2, built as R1; as R1 it would score 91". The remedy is to build the second attachments or re-declare as R1.
- *Partial shortfall:* 64 of the 256 NICs are single-homed. Three quarters of the declared dual-homing exists, so the attachment part of D2 is 75. Because the 25% of single-homed capacity reaches the illustrative blast-radius threshold, the single-point-of-failure condition also fires, which is the state in the record below.

**The explanation record** for that capped state, with illustrative band edges of 80 and 60:

```
Vitals Score 41, class R2 (spec sheet v2) · confirmed; ≤ 44 if unmeasured capacity is healthy · RED (illustrative band edges 80/60)
Scope: pod-3 · fabric scope scores 41 / 83 / 88 / 90 (lowest: pod-3) · Rulebook RB-0.3 (hypothetical) · 15-minute window
Class: declared R2 · verified R1 · NON-CONFORMANT (64 NICs single-homed; spec sheet declares dual-homing)
Counterfactual: declared R2, built as R1; as R1 it would score 58 [DESIGN SHORTFALL]
Breadth: 3 of 7 not delivering their full promise · next-binding D3 = 58 · evidence-quality confidence 90%
Binding: CC4 single point of failure [DESIGN SHORTFALL]
  1. D3 PFC pause-time on leaf-12/13 spine ports exceeds the pause budget   [OPERATIONAL]
  2. D3 NIC out-of-sequence rate behind leaf-12 exceeds the loss budget      [OPERATIONAL]
  3. D2 spine-2 drained in declared maintenance window MW-7                 [PLANNED]
  Anomaly evidence: ECN ratio 4× its registered commissioning value
Availability, last 30 days: healthy in 96% of windows (0.5% UNSCORABLE) · declared target 99% (declared maintenance counts: no) · NOT MET
Remedy: restore dual-homing, or re-declare as R1 (versioned; new score series)
```

---

## 6. Why not a metric checklist?

A common way to describe AI-fabric health is a checklist: NIC speed, bisection bandwidth, oversubscription, tail latency, loss, ECN and PFC activity, utilization, job completion time and, for inference, tokens per second. The IETF benchmarking drafts express this view for the lab: the back-end fabric "determines Job Completion Time (JCT), training throughput, and accelerator utilization" [42], and for inference serving it determines time to first token, inter-token latency "and aggregate throughput in tokens per second (TPS)" [56]. Fabric Vitals uses many of these metrics as inputs. A checklist on its own, however, falls short in five ways.
- **It gives no verdict.** A list of numbers does not say whether the fabric is healthy; the benchmarking drafts explicitly leave "acceptance criteria or performance requirements" out of scope [42]. Fabric Vitals gives one verdict and explains it.
- **It mixes build with operation.** NIC speed, bisection and oversubscription describe the build; loss, pauses and delay describe operation. Fabric Vitals puts the build on the spec sheet, checks it once by conformance, and scores operation continuously.
- **It judges design choices universally.** A checklist implies that more bisection or less oversubscription is always healthier. Rail-only fabrics are designed without any-to-any paths [20]. Fabric Vitals judges each fabric against its own declared promises.
- **It counts workload performance.** Job completion time and tokens per second depend on accelerators, software, models and schedulers as well as the network, and job-level signals mix causes: one collective-library error code covers GPU crashes, network disconnection, out-of-memory and user code [40]. Fabric Vitals scores only network-attributable evidence, and uses job metrics for validation.
- **It has no rule for missing data.** Unmonitored links silently drop out of a checklist. In Fabric Vitals they count as unknown, and below the coverage floor the result is UNSCORABLE, with a list of what is missing.

---

## 7. Relationship to existing work

**ITU-T M.3042** (2025) is the principal prior work. It is the ITU-T framework for communication network health, and it defines a network health index as "a single summary indicator expressed in quantitative terms indicating the degree of communication network health" [49].
- **Structure.** Four levels: an overall index; four dimensions (availability, reliability, security and maintainability); 21 third-level indexes; and scenario-specific indexes.
- **Aggregation.** The top two levels are weighted sums, with weights "outside the scope of this Recommendation". Inside 8 of the 21 third-level indexes, M.3042 already applies the weakest-element rule: it takes the minimum across network-element types.
- **Where Fabric Vitals differs.** It applies that minimum *across* its dimensions, adds critical conditions, scores against a declared spec sheet and a pre-registered Rulebook rather than operator-chosen weights, and uses AI-fabric inputs. It also excludes security, which M.3042 includes, to stay focused on fabric health.

The two are complementary. Fabric Vitals could be described to ITU-T readers level by level against M.3042.

**IETF AI-fabric benchmarking drafts** [42, 56, 57]. These individual drafts define *Fabric Health Indicators* for lab benchmarking, and they explicitly leave acceptance criteria out of scope. Their indicators map naturally onto Fabric Vitals inputs: PFC events and storms, ECN ratio, loss, buffer occupancy, retransmission, link flaps, CRC and FEC errors, and route convergence time. Their benchmark methodology is a candidate basis for the commissioning test suite.

**The IETF Link Quality Score draft** [58] is the closest published score for AI fabrics found. It defines a vendor-agnostic, per-link, 0–255 composite built from utilization, queue depth, ECN, PFC pause and drops. It feeds adaptive routing, and "the computation of LQS from hardware signals is EXPLICITLY implementation-defined".
- **What it is not.** It scores individual links for congestion; it is not a fabric-wide health measure.
- **How Fabric Vitals can use it.** It is a possible input to the congestion and capacity vitals. Its monotonicity requirement matches ours, and its caution that two conforming implementations may disagree is the problem a pre-registered Rulebook addresses. Its "healthy" range is not adopted as a reference.

**IETF service assurance (SAIN) and Quality of Outcome.** SAIN standardizes a 0–100 health score with −1 for "no value could be computed", and requires symptoms for any non-maximal score [52, 59]. Fabric Vitals conforms to both conventions, and its vitals could be carried as SAIN subservices. The IETF Quality of Outcome draft scores by the minimum with application profiles [48]. Fabric Vitals follows it.

**Facility tier practice.**
- **Uptime Institute's Tier Standard: Topology** explicitly excludes IT and the network. It rates a site by its lowest subsystem, with no partial tiers, confirmed by outcome-based tests [30].
- **ANSI/BICSI 002** defines network infrastructure classes that the owner declares before design [29].
- **ANSI/TIA-942** and **EN 50600** class cabling infrastructure [26, 27].

Fabric Vitals borrows the ideas of declaration, weakest-subsystem rating and outcome testing. It does not claim to implement those standards' requirement texts, which the author has not consulted.

---

## 8. Limitations and what is not yet known

**No values yet.** Of the 40 parameters, one has a standard behind it (the IEEE budget). Twenty-six must be defined by experiment, and nine are methods. The class presets carry no promise values yet. Until validation runs, a Vitals Score is for discussion and experimentation, not for acceptance decisions.

**The evidence is concentrated.**
- Mechanisms are well evidenced.
- "Normal" ranges and failure rates are evidenced almost only at hyperscale. Most of the empirical evidence comes from a few hyperscale operators, and one heavily cited source is a preprint whose results depend on its multipath transport [14].
- At 32 to 2,000 GPUs, where many readers operate, public evidence is thin. The two operational reports found cover 504 and 800 GPUs, and neither collected fabric congestion counters [39, 60]. Vendor validation results at those scales are private [24, 61].
- Every value carried over from hyperscale is marked "not validated at this scale".

**Telemetry gaps.**
- The congestion vital depends on vendor-neutral PFC, buffer and NIC counter definitions that do not yet exist.
- The lossless-configuration check can read switch-side MTU, DSCP classification and ECN enablement through vendor-neutral models, but not PFC configuration or NIC-side settings.
- Because the coverage rule is strict, many small fabrics will be UNSCORABLE for affected conditions at first. They will receive a list of what to add.

**Standards texts.** The requirement texts of several facility and cabling standards, and the normative IEEE 802.3 clause text, were not consulted. The physical-layer budget is cited from the IEEE project objectives and the Ultra Ethernet specification.

**Design risks to test.**
- The minimum's commensurability assumption may fail.
- The grace period trades false drops for bounded staleness.
- Scoring against the declared spec sheet can pin the headline during a design shortfall.
- Custom spec sheets can promise little; their scores are then honest but not comparable, which is why presets matter.
- Method-only references can lock in a fabric that was already bad at commissioning, wherever no declared value or acceptance criterion exists.

**Roadmap of excluded areas.** Out of scope in v0.x, and candidate future profiles, in order of likely demand: front-end and inference-serving networks; storage and checkpoint traffic; scale-up interconnects (NVLink-class, including Ethernet-based scale-up); and multi-tenant isolation. Security is excluded.

**The field is moving.** The closest prior art appeared in July 2026. Related work must be re-checked before any submission.

**How validation will proceed.**
1. **Expert critique** of the class presets and the spec-sheet template, in public.
2. **Without GPUs, in a container-based emulated fabric.** Tests of the scoring machinery run on replayed or emulated telemetry: anti-gaming under telemetry removal, false drops from telemetry gaps, determinism, monotonicity, and detection of configuration mismatches and convergence time. They set the first Rulebook values: the coverage floor, the grace period, the coupling-rule values and the event definitions. An emulated fabric cannot reproduce switch-chip buffers, PFC or ECN at line rate, FEC and optics, or GPU collectives, so those values wait.
3. **With GPUs and hardware.** Lab experiments at 32 to 256 GPUs follow, including a test of whether equal vital values mean equal impact, the calibration of band edges, and the preset promise values. Shadow deployments on mid-sized production fabrics come after that.

---

## 9. How to take part

The method, the Rulebook skeleton, the spec-sheet template and class presets, the metric definitions and the validation programme are published as an open specification at **https://github.com/fabric-vitals/spec**. The questions we most want answered are listed there as seed issues: the two named gaps, the commensurability assumption, the role of D7, the class-preset proposal, evidence from mid-sized clusters, and band calibration. Three kinds of contribution are invited through its issue tracker:
- **Method critique:** the Rulebook / spec-sheet split, the class presets, the aggregation rule, the coverage rules.
- **Telemetry availability:** which counters and configuration your platforms export by default, and at what resolution.
- **Validation partnership:** lab or production fabrics, especially mid-sized clusters, that can help set the Rulebook and preset values.

Rulebook values will be fixed before measurement, through an open, versioned change process, and never tuned after the fact. "Fabric Vitals" and "Vitals Score" are claimed as marks of datacenternetwork.ai so that the names always mean the published method; anyone may state that a product implements Fabric Vitals when it follows the published Rulebook and spec-sheet rules, and the marks will move with stewardship if it passes to a neutral body.

---

## 10. Disclosure

The author organization develops network software. The proposal is written to be implementable by any vendor or operator. The method, its Rulebook and its class presets are vendor-neutral and are offered for open discussion.

---

## References

1. Y. Xiong, Y. Jiang, Z. Yang, L. Qu et al. (Microsoft). "SuperBench: Improving Cloud AI Infrastructure Reliability with Proactive Validation". USENIX ATC 2024, July 2024. https://www.usenix.org/system/files/atc24-xiong.pdf (accessed 2026-09-23).
2. A. Kokolis, M. Kuchnik, J. Hoffman et al. (FAIR at Meta). "Revisiting Reliability in Large-Scale Machine Learning Research Clusters". IEEE HPCA 2025, February 2025. https://arxiv.org/pdf/2410.21680 (accessed 2026-09-23).
3. R. Lucchese, N. Birkner, Y. Hagai, V. Adams. "A practitioner's guide to testing and running large GPU clusters for training generative AI models". Together AI blog, August 2024. Single-operator practice. https://www.together.ai/blog/a-practitioners-guide-to-testing-and-running-large-gpu-clusters-for-training-generative-ai-models (accessed 2026-09-23).
4. A. Gangidi, R. Miao, S. Zheng et al. (Meta). "RDMA over Ethernet for Distributed AI Training at Meta Scale". ACM SIGCOMM 2024, August 2024. Single operator. https://engineering.fb.com/wp-content/uploads/2024/08/sigcomm24-final246.pdf (accessed 2026-09-28).
5. C. Guo, L. Yuan, D. Xiang et al. (Microsoft). "Pingmesh: A Large-Scale System for Data Center Network Latency Measurement and Analysis". ACM SIGCOMM 2015, August 2015. https://conferences.sigcomm.org/sigcomm/2015/pdf/papers/p139.pdf (accessed 2026-09-23).
6. Z. Jiang, H. Lin, Y. Zhong et al. (ByteDance, Peking University). "MegaScale: Scaling Large Language Model Training to More Than 10,000 GPUs". USENIX NSDI 2024, April 2024. https://www.usenix.org/system/files/nsdi24-jiang-ziheng.pdf (accessed 2026-09-23).
7. Z. Yao, P. Hu, C. Miao et al. (Fudan University, Tencent, University of Chicago). "Holmes: Localizing Irregularities in LLM Training with Mega-scale GPU Clusters". USENIX NSDI 2025, April 2025. https://www.usenix.org/system/files/nsdi25-yao.pdf (accessed 2026-09-23).
8. Cisco. "Monitor and Troubleshoot Network Health". Cisco Catalyst Assurance User Guide 3.1.x, December 2025. Vendor documentation. https://www.cisco.com/c/en/us/td/docs/cloud-systems-management/network-automation-and-management/catalyst-center-assurance/3-1-x/b_cisco_catalyst_assurance_3_1_x_ug/b_cisco_catalyst_assurance_3_1_x_ug_chapter_0110.html (accessed 2026-09-23).
9. NVIDIA. "Validate Overall Network Health". Cumulus NetQ 4.11 documentation, 2026. Vendor documentation. https://docs.nvidia.com/networking-ethernet-software/cumulus-netq-411/Validate-Operations/Validate-Overall-Network-Health (accessed 2026-09-23).
10. Nokia. "Units of automation". Nokia EDA documentation, release 25.8. Vendor documentation. https://docs.eda.dev/25.8/getting-started/units-of-automation/ (accessed 2026-09-23).
11. Dell Technologies. "Monitoring SFM and the SONiC switches". SmartFabric Manager for SONiC User Guide, release 1.0.0. Vendor documentation. https://www.dell.com/support/manuals/en-us/smartfabric-manager-for-sonic/sfm-100-user-guide-pub/monitoring-sfm-and-the-sonic-switches?guid=guid-2f01bcd7-0e79-49c3-ac38-d4da8018bd13&lang=en-us (accessed 2026-09-23).
12. OECD and European Commission Joint Research Centre (M. Nardo, M. Saisana, A. Saltelli, S. Tarantola, A. Hoffmann, E. Giovannini). "Handbook on Constructing Composite Indicators: Methodology and User Guide". OECD Publishing, 2008. https://www.oecd.org/content/dam/oecd/en/publications/reports/2008/08/handbook-on-constructing-composite-indicators-methodology-and-user-guide_g1gh9301/9789264043466-en.pdf (accessed 2026-09-23).
13. K. Qian et al. (Alibaba Cloud). "Alibaba HPN: A Data Center Network for Large Language Model Training". ACM SIGCOMM 2024, August 2024. Single operator. https://ennanzhai.github.io/pub/sigcomm24-hpn.pdf (accessed 2026-09-23).
14. J. Araujo, A. Chow, M. Handley, J. Padhye et al. (49 authors; OpenAI, Microsoft, AMD, Broadcom, NVIDIA). "Resilient AI Supercomputer Networking using MRC and SRv6". arXiv 2605.04333v1, May 2026. Preprint; results depend on its multipath transport. https://arxiv.org/abs/2605.04333 (accessed 2026-09-23).
15. Ultra Ethernet Consortium. "Overview of and Motivation for the Forthcoming Ultra Ethernet Consortium Specification". White paper, July 2023. https://ultraethernet.org/wp-content/uploads/sites/20/2023/10/23.07.12-UEC-1.0-Overview-FINAL-WITH-LOGO.pdf (accessed 2026-09-23).
16. C. Guo, H. Wu, Z. Deng, G. Soni, J. Ye, J. Padhye, M. Lipshteyn (Microsoft). "RDMA over Commodity Ethernet at Scale". ACM SIGCOMM 2016, August 2016. Single operator. https://www.microsoft.com/en-us/research/wp-content/uploads/2016/11/rdma_sigcomm2016.pdf (accessed 2026-09-23).
17. Y. Zhu, H. Eran, D. Firestone, C. Guo et al. "Congestion Control for Large-Scale RDMA Deployments". ACM SIGCOMM 2015, August 2015. https://conferences.sigcomm.org/sigcomm/2015/pdf/papers/p523.pdf (accessed 2026-09-23).
18. Y. Li, R. Miao, H. H. Liu et al. "HPCC: High Precision Congestion Control". ACM SIGCOMM 2019, August 2019. https://liyuliang001.github.io/publications/hpcc.pdf (accessed 2026-09-23).
19. Q. Zhang, V. Liu, H. Zeng, A. Krishnamurthy. "High-Resolution Measurement of Data Center Microbursts". ACM IMC 2017, November 2017. General data-center traffic, not AI-specific. https://conferences.sigcomm.org/imc/2017/papers/imc17-final60.pdf (accessed 2026-09-23).
20. W. Wang, M. Ghobadi, K. Shakeri, Y. Zhang, N. Hasani. "Rail-only: A Low-Cost High-Performance Network for Training LLMs with Trillion Parameters". arXiv 2307.12169v5, July 2023 (v5 September 2024). Preprint. https://arxiv.org/abs/2307.12169 (accessed 2026-09-23).
21. NVIDIA. "NVIDIA HGX AI Factory Enterprise Reference Architecture: Networking Logical Architecture". NVIDIA documentation (latest edition, undated). Single-vendor reference design. https://docs.nvidia.com/enterprise-reference-architectures/hgx-ai-factory/latest/network-logical-architecture.html (accessed 2026-09-23).
22. Y. Zhong, S. Liu, J. Chen et al. "DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving". USENIX OSDI 2024, July 2024. https://www.usenix.org/system/files/osdi24-zhong-yinmin.pdf (accessed 2026-09-23).
23. R. Qin et al. (Moonshot AI, Tsinghua University). "Mooncake: Trading More Storage for Less Computation — A KVCache-centric Architecture for Serving LLM Chatbot". USENIX FAST 2025, February 2025. https://www.usenix.org/system/files/fast25-qin.pdf (accessed 2026-09-23).
24. Juniper Networks. "AI Data Center Network with Juniper Apstra, NVIDIA GPUs, ConnectX NIC, and WEKA Storage — Juniper Validated Design" (JVD-AICLUSTERDC-AIML-02-10). August 2026. Single-vendor validated design. https://www.juniper.net/documentation/us/en/software/jvd/jvd-ai-dc-apstra-nvidia-weka/jvd-ai-dc-apstra-nvidia-weka.pdf (accessed 2026-09-28).
25. NVIDIA. "NVIDIA DGX SuperPOD (B300/XDR): Key Components". NVIDIA reference architecture documentation, last updated September 2026. Single-vendor reference design. https://docs.nvidia.com/dgx-superpod/reference-architecture/scalable-infrastructure-b300-xdr/latest/dgx-superpod-components.html (accessed 2026-09-28).
26. TIA. "ANSI/TIA-942: The Global Data Center Standard" (brochure describing TIA-942-C). Telecommunications Industry Association, April 2024. Brochure, not the standard text. https://tiaonline.org/wp-content/uploads/2024/05/Data-Centers-Brochure_040124.pdf (accessed 2026-09-23).
27. ISO/IEC JTC 1. "ISO/IEC TS 22237-5:2018 Data centre facilities and infrastructures — Part 5: Telecommunications cabling infrastructure". ISO/IEC, May 2018. Public preview only. https://cdn.standards.iteh.ai/samples/73012/f90c18a9cfdf49e2aa38e45fec4e420d/ISO-IEC-TS-22237-5-2018.pdf (accessed 2026-09-23).
28. L. D. Lamb, L. Staley, J. Mora, A. Raman. "Open Pod Group for M xPUs (OPG-M) System Architecture". Open Compute Project, January 2026. Contributor document. https://www.opencompute.org/documents/opg-m-system-architecture-final-14-january-2026-pdf (accessed 2026-09-23).
29. BICSI. "An Overview of the ANSI/BICSI 002-2019 Data Center Availability Class Methodology". BICSI, 2019. Public overview, not the standard text. https://www.bicsi.org/docs/default-source/publications/002-2019-methodology.pdf (accessed 2026-09-23).
30. Uptime Institute. "Data Center Site Infrastructure Tier Standard: Topology". Uptime Institute, 2018 (effective October 2018). https://www.gpxglobal.net/wp-content/uploads/2018/11/Uptime-Tier-Standard-Topology.pdf (accessed 2026-09-23).
31. IEEE 802.3 Working Group. "IEEE P802.3bs Project Objectives". IEEE, March 2016. Adopted objectives. https://www.ieee802.org/3/bs/Objectives_16_0317.pdf (accessed 2026-09-23).
32. IEEE 802.3 Working Group. "IEEE P802.3cd Objectives" (v4). IEEE. Adopted objectives. https://www.ieee802.org/3/cd/P802d3cd_objectives_v4.pdf (accessed 2026-09-23).
33. IEEE 802.3 Working Group. "IEEE P802.3ck Objectives". IEEE, March 2018. Adopted objectives. https://www.ieee802.org/3/ck/P802_3ck_Objectives_2018mar.pdf (accessed 2026-09-23).
34. IEEE 802.3 Working Group. "IEEE P802.3db Adopted Objectives". IEEE, November 2020. Adopted objectives. https://www.ieee802.org/3/db/P802d3db_Updated_Objectives_Approved_November_2020.pdf (accessed 2026-09-23).
35. IEEE 802.3 Working Group. "Adopted IEEE P802.3df Objectives". IEEE, November 2022. Adopted objectives. https://www.ieee802.org/3/df/proj_doc/objectives_P802d3df_221117.pdf (accessed 2026-09-23).
36. IEEE 802.3 Working Group. "Adopted IEEE P802.3dj Objectives". IEEE, March 2024. Adopted objectives for a project in development. https://www.ieee802.org/3/dj/projdoc/objectives_P802d3dj_240314.pdf (accessed 2026-09-23).
37. Ultra Ethernet Consortium. "Ultra Ethernet Specification", version 1.0.2. UEC, January 2026. https://ultraethernet.org/wp-content/uploads/sites/20/2026/01/UE-Specification-1.0.2-1.pdf (accessed 2026-09-23).
38. Ultra Ethernet Consortium. "Ultra Ethernet Specification", version 1.0.3. UEC, July 2026. https://ultraethernet.org/wp-content/uploads/sites/20/2026/08/UE-Specification-1.0.3.pdf (accessed 2026-09-23).
39. F. Konishi, Y. Tsubouchi, H. Tsuruta et al. (SAKURA internet Research Center). "SAKURAONE: An Open Ethernet-Based AI HPC System and Its Observed Workload Dynamics in a Single-Tenant LLM Development Environment". arXiv 2604.13600v2, April 2026. Preprint; single 800-GPU cluster. https://arxiv.org/abs/2604.13600 (accessed 2026-09-23).
40. J. Dong, B. Luo, J. Zhang et al. (Alibaba, HKUST). "Enhancing Large-Scale AI Training Efficiency: The C4 Solution for Real-Time Anomaly Detection and Communication Optimization". IEEE HPCA 2025, March 2025. https://arxiv.org/abs/2406.04594 (accessed 2026-09-23).
41. Y. Deng, X. Shi, Z. Jiang et al. "Minder: Faulty Machine Detection for Large-scale Distributed Model Training". USENIX NSDI 2025, April 2025. https://www.usenix.org/system/files/nsdi25-deng.pdf (accessed 2026-09-23).
42. F. Calabria, C. Pignataro, Q. Wu, G. Fioccola, S. Reddy. "Benchmarking Methodology for AI Training Network Fabrics" (draft-calabria-bmwg-ai-fabric-training-bench-04). IETF, August 2026. Individual Internet-Draft, not adopted by a working group; work in progress. https://datatracker.ietf.org/doc/draft-calabria-bmwg-ai-fabric-training-bench/ (accessed 2026-09-28).
43. IEEE 802.3 Working Group. "IEEE Std 802.3.2-2025, Ethernet YANG Data Model Definitions". IEEE, approved September 2025. https://standards.ieee.org/ieee/802.3.2/11245/ (accessed 2026-09-23).
44. OpenConfig. "openconfig/public: YANG models" (release/models; openconfig-qos revision 2026-04-30). GitHub, September 2026. https://github.com/openconfig/public (accessed 2026-09-28).
45. Open Compute Project SAI project. "Switch Abstraction Interface headers" (saiport.h, saiqueue.h, saibuffer.h), API version 1.19.0. GitHub, September 2026. https://github.com/opencomputeproject/SAI/tree/master/inc (accessed 2026-09-23).
46. OpenConfig. "Ethernet flow-control config" (issue #1044, open since February 2024). GitHub. https://github.com/openconfig/public/issues/1044 (accessed 2026-09-28).
47. Linux kernel. RDMA driver sources (mlx5 counters.c, bnxt_re hw_counters.c, irdma verbs.c, ionic ionic_hw_stats.c). Linux source tree, master branch (July 2026). https://github.com/torvalds/linux/tree/master/drivers/infiniband/hw (accessed 2026-09-23).
48. B. I. T. Monclair, M. Olden, I. Kunze (Ed.). "Quality of Outcome (QoO)" (draft-ietf-ippm-qoo-11). IETF IPPM Working Group, May 2026. Working-group Internet-Draft in the RFC Editor queue; not yet an RFC. https://datatracker.ietf.org/doc/draft-ietf-ippm-qoo/ (accessed 2026-09-23).
49. ITU-T Study Group 2. "Recommendation ITU-T M.3042: Framework of communication network health evaluation". ITU-T, March 2025. https://www.itu.int/rec/T-REC-M.3042 (accessed 2026-09-23).
50. US Federal Highway Administration. "23 CFR 490.409: Calculation of National performance management measures for assessing bridge condition". US Code of Federal Regulations (current text via the Legal Information Institute). https://www.law.cornell.edu/cfr/text/23/490.409 (accessed 2026-09-23).
51. M. Bjorklund. "A YANG Data Model for Interface Management" (RFC 8343). IETF, March 2018. Proposed Standard. https://www.rfc-editor.org/rfc/rfc8343 (accessed 2026-09-23).
52. B. Claise, J. Quilbeuf, D. Lopez, D. Voyer, T. Arumugam. "Service Assurance for Intent-Based Networking Architecture" (RFC 9417). IETF, July 2023. Informational. https://www.rfc-editor.org/rfc/rfc9417 (accessed 2026-09-23).
53. J. Gaskin. "FICO Fact: Does FICO's Minimum Scoring Criteria Limit Consumers' Access to Credit?". FICO, October 2021. Score owner's own publication. https://www.fico.com/blogs/fico-fact-does-ficos-minimum-scoring-criteria-limit-consumers-access-credit (accessed 2026-09-23).
54. ITU-T. "Recommendation ITU-T G.109: Definition of categories of speech transmission quality". ITU-T, September 1999 (Amendment 1, January 2007). https://www.itu.int/rec/T-REC-G.109 (accessed 2026-09-23).
55. L. DeNicola. "What Are Credit Score Reason Codes?". myFICO, undated. Score owner's own publication. https://www.myfico.com/credit-education/blog/reason-codes (accessed 2026-09-23).
56. F. Calabria, C. Pignataro, Q. Wu, G. Fioccola, S. Reddy. "Benchmarking Methodology for AI Inference Serving Network Fabrics" (draft-calabria-bmwg-ai-fabric-inference-bench-04). IETF, August 2026. Individual Internet-Draft, not adopted by a working group; work in progress. https://datatracker.ietf.org/doc/draft-calabria-bmwg-ai-fabric-inference-bench/ (accessed 2026-09-28).
57. F. Calabria, C. Pignataro, Q. Wu, G. Fioccola, S. Reddy. "Benchmarking Terminology for AI Network Fabrics" (draft-calabria-bmwg-ai-fabric-terminology-04). IETF, August 2026. Individual Internet-Draft, not adopted by a working group; work in progress. https://datatracker.ietf.org/doc/draft-calabria-bmwg-ai-fabric-terminology/ (accessed 2026-09-28).
58. S. P. K. Pasalapudi, V. P. Beeram. "A YANG Data Model for Link Quality Telemetry in CLOS Data Center Fabrics" (draft-praveen-fann-lq-telemetry-info-00). IETF, July 2026. Individual Internet-Draft; work in progress. https://datatracker.ietf.org/doc/draft-praveen-fann-lq-telemetry-info/ (accessed 2026-09-23).
59. B. Claise, J. Quilbeuf, P. Lucente, P. Fasano, T. Arumugam. "A YANG Data Model for Service Assurance" (RFC 9418). IETF, July 2023. Proposed Standard. https://www.rfc-editor.org/rfc/rfc9418 (accessed 2026-09-23).
60. Lablup Inc. "From Detection to Recovery: Operational Analysis on LLM Pre-training with 504 GPUs". arXiv 2605.09370v5, June 2026. Preprint (technical report); single 504-GPU cluster. https://arxiv.org/abs/2605.09370 (accessed 2026-09-23).
61. Juniper Networks. "AI Data Center Network with Juniper Apstra, AMD GPUs, Broadcom Thor2 — Juniper Validated Design" (JVD-AICLUSTERDC-AIML-AMD-03-04). July 2026. Single-vendor validated design. https://www.juniper.net/documentation/us/en/software/jvd/jvd-ai-dc-apstra-amd/jvd-ai-dc-apstra-amd.pdf (accessed 2026-09-23).
