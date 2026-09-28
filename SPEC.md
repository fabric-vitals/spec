# Fabric Vitals — Specification v0.2

**Status:** Fabric Vitals v0.2 (draft) — a technical proposal for discussion. Not a standard. Rulebook values not yet set.

Fabric Vitals is a method for measuring and scoring the health of the network fabric inside an AI (artificial intelligence) data center: the switches, links and network-adapter ports that carry traffic between the accelerators, the chips that run the AI jobs. The result is one headline number for each fabric, the Vitals Score, together with the evidence that explains it. It is written for the people who own or run such a fabric, and for anyone who writes software to compute the score. To use the method, the owner of a fabric first writes down what that fabric promises, on a Fabric Spec Sheet; the fabric is then measured against that promise using the rules in the Rulebook, which are the same for every fabric. This document is the specification of the method. It describes the method precisely enough that two independent implementations, given the same data, produce identical results, once a Rulebook with values exists. The method has two inputs:
- the **Rulebook**: the single set of rules that says how every fabric is measured and judged. It is identical for all fabrics, and its adjustable values are the parameters T1–T40. See [`RULEBOOK.md`](RULEBOOK.md).
- the **Fabric Spec Sheet**: the written declaration of what one particular fabric promises, made by its owner before any measurement starts. Its fields are S1–S23. An owner can adopt a published **class preset**, a ready-made spec sheet for a common design, or write a custom sheet. See [`SPEC_SHEET.md`](SPEC_SHEET.md).

The individual measurements the method uses are called metrics. Each has an identifier (ID) from M01 to M45, and each is defined in [`METRICS.md`](METRICS.md). This document summarizes the reasoning and evidence behind each rule. How Fabric Vitals relates to other standards and published work is described in [`RELATED_WORK.md`](RELATED_WORK.md).

## 0. Conventions

Requirement words written in capitals have a fixed meaning taken from a published Internet standard, so that readers and implementers agree on what is compulsory, what is advised and what is left open. The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY" and "OPTIONAL" in this document are to be interpreted as described in BCP 14 (RFC 2119, RFC 8174) when, and only when, they appear in all capitals, as shown here. "BCP" stands for best current practice, a kind of document published by the IETF, the Internet Engineering Task Force, which publishes Internet standards; RFC stands for "Request for Comments", the name given to each IETF document.

Terms used throughout:
- **Numbers.** Some numbers in this document are made up purely to show how a mechanism works. These are marked ILLUSTRATIVE and are not proposed values. A Rulebook parameter whose value has not yet been decided is marked "VALUE NOT SET". A spec-sheet parameter, whose value comes from the fabric owner rather than from the Rulebook, is marked "VALUE DECLARED BY OWNER".
- **Implementation.** The software that computes Vitals Scores from the fabric's telemetry (the counters and measurements the network exports) and its spec sheet.
- **Operator.** The organisation or team that runs the fabric day to day.
- **Owner.** The organisation or team that declares the fabric's spec sheet, that is, states what the fabric promises. The owner may be the same as the operator, but need not be.

## 1. Terminology

| Term | Definition |
|---|---|
| **Fabric Vitals (FV)** | The method specified in this document. "FV" is its short form. |
| **Vitals Score** | The headline number for one fabric: a whole number from 0 to 100, or the word UNSCORABLE when there is not enough evidence to give a number. "FV score" is an acceptable short form. |
| **Vital** | One of the seven aspects of fabric health that the method measures, numbered D1–D7, such as reachability or resilience. Each vital has a value from 0 to 100, which is the fraction of the declared promise that is being delivered. See §4. |
| **Rulebook** | The single, versioned register of how every fabric is measured and judged. It is pre-registered, meaning it is published before any fabric is scored against it. A version is named like RB-0.2. |
| **Fabric Spec Sheet** | The versioned document in which an owner declares what one fabric promises. It covers the fabric's purpose, how it is built, which failures it promises to ride through, how available it aims to be, what performance it promises, which tests it requires, and its class. See §2. |
| **Class preset** | A ready-made, published spec sheet for a common fabric design. There are three, named R1, R2 and R3. Each has structural predicates (checks on how the fabric is built that must all hold for it to belong to that class) and promise fields (the values the class promises). Classes are design patterns ordered by how much redundancy they have; they are not quality tiers. See §2.2. |
| **Custom spec sheet** | A spec sheet that is not a preset used unchanged. Any edit to a preset makes it a custom sheet. |
| **Fabric scope** | The set of switches, links and NIC ports (a NIC, network interface card, is the network adapter in each server) that one spec sheet covers. The owner declares it together with its inventory in field S1. In v0.2 the scope is a back-end scale-out fabric, the network that carries traffic between accelerators. See §2.5. |
| **Scoring scope** | The unit within which jobs run, such as a pod or a scalable unit (a block of servers and switches that is built and grown as one piece). It is declared on the spec sheet in field S23. Each scoring scope receives its own Vitals Score. See §2.6. |
| **Verified class** | The class the fabric actually qualifies for: the most redundant class preset whose structural predicates all hold on the fabric as it was really built, whatever class was declared. See §3. |
| **Conformance status** | The outcome of checking the fabric as built against its declared spec sheet. It is one of CONFORMANT, NON-CONFORMANT (with the failed predicates listed), or NOT ASSESSED. See §3. |
| **Confirmed score** | The Vitals Score computed with every part of the fabric that could not be measured treated as if it were in the worst state. It is the lower bound of the score, and it is the number that is published. |
| **Upper bound** | The same computation with every unmeasured part treated as if it were in the best state. The confirmed score and the upper bound together form the score's range. |
| **Coverage** | How much of the fabric was actually measured. For a vital, or for the evidence set of a critical condition, coverage is the share of the *declared* capacity for which the required telemetry arrived within the grace period (the allowed delay before a measurement is treated as missing). |
| **Critical condition** | One of six named states, CC1–CC6, so serious that while one is present the Vitals Score is held down to a cap value, however good everything else is. See §7. |
| **Binding reason** | The one vital or critical condition that is setting the Vitals Score at its current value. It is tagged DESIGN SHORTFALL, OPERATIONAL or PLANNED to say where the problem comes from. See §7. |
| **Declared maintenance window** | A period of planned maintenance that the owner has declared before it starts, recorded as a versioned event. See §9.3. |
| **Day-One Set** | The smallest set of vitals, counters and probes from which a valid Vitals Score can be computed. It is the starting point for a new implementation. See §13. |
| **UNSCORABLE** | The result given instead of a number when too little of the fabric was measured, that is, when coverage is below the coverage floor. It means "conformance not confirmed". See §8.4. |
| **Score band** | The colour in which a result is displayed: green, amber, red or grey. Which colour applies is set by the band edges, Rulebook parameter T40. See §11.2. |
| **Availability** | Over a chosen period, the share of scoring windows (the fixed time slices the period is divided into) in which the fabric was healthy. See §9.2. |

## 2. The Fabric Spec Sheet

### 2.1 Fields

The spec sheet has the fields S1–S23, which are listed in full in the Spec Sheet template, `SPEC_SHEET.md` §2. They fall into seven parts:
- **identity:** which fabric this is: its scope and inventory (S1), its purpose and workload profile (S2), and its scoring scope (S23);
- **build:** how the fabric is put together: its topology (S3); how hosts attach to it (S4); its uplinks and subscription ratio, the ratio between the traffic that can enter a switch from below and what can leave it upward (S5); its planes, separate parallel copies of the network (S6); its transport and load distribution, how traffic is carried and spread across paths (S7); its lossless-transport configuration, the settings meant to stop packets being dropped under congestion (S8); and its physical diversity, whether paths share the same cables, racks or power (S9);
- **resilience promise:** which failures the fabric promises to ride through without losing capacity (S10); and its recovery objective, how quickly it promises to recover, including the routing convergence time, the time the network takes to settle on new paths after a change (S11);
- **availability target:** how much of the time the fabric promises to be healthy (S12);
- **performance envelope:** the performance the fabric promises: bandwidth per accelerator (S13); the collective bandwidth reference, the throughput expected when many accelerators exchange data at once (S14); the tail-delay budget, the delay allowed for the slowest packets (S15); the loss budget (S16); the pause budget (S17); and the physical-layer budgets, the error limits for cables and optics (S18);
- **required tests and telemetry:** the synthetic collective tests and conformance tests the fabric runs (S19), and the telemetry profile, the list of measurements it exports (S20);
- **class and version:** the declared class (S21) and the spec-sheet version (S22).

Every vital checks one or more of these fields. The mapping from vitals to fields is normative, meaning implementations follow it exactly, and it is given in `SPEC_SHEET.md` §4.

### 2.2 Class presets

1. **Status.** The class scheme is proposed and open for critique. It is derived from public sources on data-center facility tiers and availability classes [1, 2, 3, 4, 5, 6] and from published AI-fabric designs [7, 8, 9]. It is not derived from the requirement tables of any standard that sits behind a paywall.
2. **Shape.** There are three presets. Each is a complete spec sheet: its structural predicates are the build fields S3–S9 and the test and telemetry fields S19 and S20, and its promise fields are S10–S18. The presets are design patterns ordered by redundancy, not quality tiers. A fabric that keeps the promises of its class is healthy, whichever class that is:
   - **R1 Rail-optimized, single-homed:** each NIC attaches to a single rail leaf switch, so there is no second path if that switch fails. This is the most common training design in published reference designs today, and it recovers from a failure by restarting the job from a checkpoint [8, 10, 11];
   - **R2 Dual-homed:** each NIC attaches to two leaf switches, so the fabric rides through the failure of one leaf, or of a bounded number of uplinks per rail, without losing capacity [8];
   - **R3 Multi-plane, sprayed, tested:** the fabric is built as several independent planes (parallel copies of the network), traffic is sprayed packet by packet across all of them, and synthetic collective tests run continuously to confirm it performs as promised [9].

   The evidence for each pattern is given in `SPEC_SHEET.md` §5.
3. **Values.** A preset's name fixes its structural pattern: single-homed, dual-homed, or multi-plane with spraying and with the communication vital D7 required. Its numeric values live in the Rulebook: parameter T32 and the preset columns of T3, T4, T5, T10, T12, T26 and T33. Those values are PROPOSED and not yet set. The one exception is the physical-layer budgets in field S18, where the budget published by the IEEE (the Institute of Electrical and Electronics Engineers, the body that writes the Ethernet standards) applies, as parameter T37.
4. **Why failure consequence rather than path counts.** Presets are expressed as failure consequence, that is, what the fabric promises to ride through, rather than as a count of redundant paths. Some AI designs attach each NIC to a single rail leaf by design [10, 11]. One open design states that "no redundancy is assumed or required" [12]. In AI fabrics, resilience comes instead from planes, dual attachment and spare capacity built in by design [7, 8, 9].
5. **Custom sheets.** An owner **MAY** declare a custom spec sheet instead of adopting a preset. A custom sheet **MUST NOT** carry a preset's name. See §12.
6. **Standards floors.** Where a published standard already sets a limit for a field (today only the physical-layer budgets, S18), the value the owner declares **MAY** be stricter than the standard and **MUST NOT** be laxer than it.

### 2.3 Lossless-transport configuration consistency

Lossless transport means the fabric is configured to pause traffic rather than drop packets when a queue fills. It only works when the switches and the NICs use the same settings, so this section checks that they do.

1. For every lossless traffic class, the spec sheet **MUST** declare, in field S8, the settings that switches and NICs are expected to share: which priorities have PFC enabled (PFC, priority flow control, is the pause signal a switch sends when a queue fills); the ECN marking configuration (ECN, explicit congestion notification, is a mark set on a packet to tell the sender to slow down before packets are dropped); the mapping from DSCP values to traffic classes (DSCP, the differentiated services code point, is the field in each packet header that says which class of service the packet belongs to); and the MTU (maximum transmission unit, the largest packet size allowed).
2. The conformance check **MUST** evaluate the predicate named P-CFG. It holds when, on every path that carries job traffic, the running configuration of every switch along the path and of the NICs at both ends matches what S8 declares. See §3.
3. Where the running configuration can be read while the fabric is in operation, a mismatch **MUST** be reported as evidence for the congestion-and-loss vital D3, as metric M43, and as a mandatory finding tagged OPERATIONAL. It lowers D3 for the affected capacity through the value function, Rulebook parameter T25.
4. **Rationale.** Configuration errors are a documented cause of failure in lossless RDMA fabrics (RDMA, remote direct memory access, lets one server write straight into another server's memory across the network, and it depends on the network not dropping packets): Meta reports congestion drops "observed mostly due to misconfiguration" [7], and Microsoft checks "if the running configurations of the switches and the servers are the same as their desired configurations" after an incident caused by a buffer misconfiguration [13]. Lossless operation needs NICs and switches to agree on how traffic is classified [13]. A mismatch is not made a critical condition in v0.2, because its harmful consequences are already capped by the critical conditions CC1–CC3. See §7.

### 2.4 Declaration

1. The owner **MUST** declare a spec sheet before any measurement window can count toward a score. The promise comes first; the measurement follows.
2. The choice of class **SHOULD** come from an assessment of what downtime would cost and how much disruption each kind of failure may be allowed to cause, following the public practice of BICSI (a standards association for information and communications technology infrastructure) and of ISO 22301 (the International Organization for Standardization's business-continuity standard) [4, 5].
3. The spec sheet **MUST** be signed, dated and given a version number, recorded in field S22, and it **MUST** name the Rulebook version it is declared against.
4. Any change to any field **MUST** create a new spec-sheet version. Scores computed under different spec-sheet versions form separate series. See §12.

### 2.5 Scope and deliberate exclusions

1. v0.2 covers back-end scale-out fabrics: the networks that carry traffic between accelerators across many servers.
2. **Security** is deliberately excluded. The ITU-T recommendation M.3042 (ITU-T is the telecommunication standardization arm of the International Telecommunication Union) includes it; Fabric Vitals keeps to fabric health.
3. **Roadmap of excluded areas.** The following are out of scope in every v0.x release. They are candidates for future profiles, listed in the order in which demand for them is expected:
   1. front-end networks and the networks that serve inference (running a trained model to answer requests);
   2. storage and checkpoint traffic;
   3. scale-up interconnects, the very short-range links that join the accelerators inside one server or rack, such as NVLink and Ethernet-based equivalents;
   4. multi-tenant isolation, keeping the traffic of different customers or teams on a shared fabric apart.

### 2.6 Scoring scope

1. The spec sheet **MUST** declare one or more scoring scopes in field S23. A scoring scope is the unit within which jobs run, such as a pod or a scalable unit.
2. Every vital, every coverage figure and every critical-condition threshold **MUST** be computed within one scoring scope at a time. This includes the blast-radius threshold, parameter T16 (how much of the capacity a condition has to affect before it caps the score), and the coverage floor, parameter T29 (how much of the capacity has to be measured for a score to be given at all).
3. A fabric with more than one scoring scope **MUST** be reported as the set of scope scores, showing how they are distributed and naming the lowest-scoring scope. An implementation **MUST NOT** publish one Vitals Score for several scopes blended together in proportion to their capacity.
4. **Rationale.** A job runs only as fast as the slowest transfer inside the unit it runs in [8, 9]. Blending a failed pod into a large, healthy fabric would hide it in an average, which is exactly the averaging the method rejects. See §6.

## 3. Conformance check

The conformance check compares the fabric as it was actually built with the class it claims to be.

1. An implementation **MUST** compute the verified class as the most redundant preset whose structural predicates all hold on the fabric as built. This is the lowest-predicate rule: a single failed predicate is enough to exclude a class, following the practice used for data-center facility tiers [2]. Fractional classes, such as "almost R2", **MUST NOT** be reported.
2. The check **MUST** include:
   - (a) a static evaluation: the declared build, fields S3–S9, is compared with the topology actually discovered (for example through LLDP, the Link Layer Discovery Protocol, by which switches announce themselves to their neighbours), with the inventory, and with the running configuration, including the configuration predicate P-CFG. See §2.3.
   - (b) a computed evaluation: the capacity that would remain after each of the failures the fabric promises to tolerate, field S10, is worked out from the build.
3. The check **SHOULD** also include (c) outcome-based tests: a failure is caused deliberately, or a device is drained of traffic, and the fabric's behaviour is measured with the D7 method, parameter T26. The measured recovery time and routing convergence time are compared with the recovery objective in field S11. These tests **SHOULD** run when the fabric is commissioned and again at the declared cadence, the interval `K_conf` in field S19. They follow outcome-based confirmation practice, in which resilience is confirmed by observing what actually happens [2, 6].
4. The conformance status **MUST** be one of CONFORMANT, NON-CONFORMANT (with every failed predicate listed), or NOT ASSESSED.
5. **Scoring uses the declared spec sheet.** Vitals and critical conditions **MUST** be evaluated against the spec sheet the owner declared, not against the verified class. The verified class and the conformance status **MUST** be reported beside the score. See §11.
6. **Over-claim rule.** Redundancy that was declared but never built **MUST** count as absent. Because every vital measures the fraction of the promise delivered, a fabric that claimed redundancy it does not have at all scores 0 on the resilience vital D2, and a fabric that has only part of it scores the fraction it has. The binding reason is tagged DESIGN SHORTFALL. See §4.1.
7. **Counterfactual.** Whenever the declared class differs from the verified class, the record and any display **MUST** show the sentence "declared Rx, built as Ry; as Ry it would score N", where N is the score recomputed using the promises of the verified class's preset, and **MUST** name re-declaring the spec sheet as the remedy. This counterfactual is information only; the Vitals Score remains the score against the declared spec sheet.

## 4. Vitals

### 4.1 Common currency and definitions

1. Every vital is on one scale: the fraction of the declared promise being delivered, from 0 (none of it) to 100 (all of it). The promise is what the spec sheet declares or, where the Rulebook sets the reference, the Rulebook reference for the declared class.
2. This shared scale, the common currency, is what makes the weakest-vital rule meaningful: a value of the same size in two different vitals means the same share of each promise is being delivered. See §6.
3. It is the design intent behind the value functions (the formulas that turn a raw measurement into a value on this scale, parameter T25) and their anchors (the fixed points those formulas pass through, parameter T31). The shapes of the value functions between the anchors remain to be calibrated, in experiment E4. See §5.5.

| ID | Vital | Question | Definition | Metrics | Spec-sheet fields checked |
|---|---|---|---|---|---|
| D1 | **Reachability** | Can every endpoint that should reach every other get packets through? | The share of declared endpoint-to-endpoint paths, weighted by capacity, that are correct in the control plane (the links and routing sessions are up and stable, and both the FIB, the forwarding table each switch actually uses, and the cabling match the intended design) and are also verified in the data plane by active probes, test packets sent across the path. The control-plane evidence includes routing stability, meaning session flaps and route churn, metric M44. | M01–M06, M44 | S1, S3, S4 |
| D2 | **Resilience** | If the next tolerated failure happens, will the fabric still do its job? | The fraction of the declared resilience promise that is available right now: how much redundancy remains and how much capacity would be left, with redundancy that was declared but never built counted as absent, and the measured recovery compared with the recovery objective, including routing convergence time, metric M45. See §3. | M07–M09, M45 | S4, S5, S6, S10, S11 |
| D3 | **Congestion and loss** | Is traffic getting through without harmful loss, pausing or congestion spread? | Packet loss, broken down by cause and by traffic class, against the loss budget; the fraction of time spent paused by PFC against the pause budget; pause storms and deadlock; buffer stress; ECN marks and CNPs (congestion notification packets, the messages a receiving NIC sends back to make a sender slow down) against the references registered at commissioning; anomalies in the NIC's transport counters; and consistency of the lossless-transport configuration | M10–M22, M43 | S7, S8, S16, S17 |
| D4 | **Delay and tail** | Is the network adding more delay than it should, at the tail? | The delay of probe packets on each class of path, both when the fabric is loaded and when it is idle, summarised by the tail statistic the workload profile selects (a statistic that describes the slowest packets rather than the average), against the declared tail-delay budget; and the high-water marks of queue delay | M23–M26 | S2, S15 |
| D5 | **Physical link integrity** | Are the links, optics and PHYs (the physical-layer transmitter and receiver circuits at each end of a link) healthy? | How far each link is from the physical-layer budgets (the IEEE budget, parameter T37, and any extra margin the owner declares, parameter T5); link reliability worked out from FEC statistics (FEC, forward error correction, is the coding that lets a receiver repair corrupted bits, and its counters show how much repair is happening), parameter T38; the tail of the FEC histogram; CRC errors (frames whose check value shows they were corrupted in transit) and symbol errors; link flaps (links going down and coming back up); and optical modules against their own thresholds | M27–M34 | S18 |
| D6 | **Effective capacity** | Is there enough usable bandwidth where traffic goes, spread well? | Utilization measured as a peak or a percentile within the phases when accelerators are communicating, against the declared capacity in field S13; imbalance between links on fabrics that place each flow on one path by hashing; and imbalance between planes on fabrics that spray packets | M35–M37 | S5, S7, S13 |
| D7 | **AI communication** | Tested the way AI jobs use it, does the fabric perform as promised? | The bus bandwidth achieved by synthetic collective tests (test runs that imitate the group data exchanges of an AI job) and by RDMA scans between every pair of known-good hosts, against the declared collective bandwidth reference | M38, M39 | S14, S19 |

### 4.2 Evidence scope

1. Only evidence that can be attributed to the network is in scope:
   - (a) signals that originate in switches, NIC ports, NIC transport counters or optics;
   - (b) active measurements that exercise the network on their own, without depending on the tenants' compute jobs;
   - (c) the running configuration of switches and NICs, used for the consistency check. See §2.3.
2. Signals that come from the jobs themselves, such as training step time, job completion, or errors from the collective-communication library inside a tenant's job, **MUST NOT** enter a vital unless a declared attribution method has traced them to a specific network element [14, 15]. Raw job signals mix network causes with causes that have nothing to do with the network [15, 16].
3. A symptom seen on a single NIC **MUST NOT** lower a fabric-wide vital unless it is correlated across hosts or attributed to a network element. Causes inside the host or inside the NIC itself show up as PFC and ECN symptoms [13, 16].

### 4.3 D7 rules

The AI-communication vital D7 normally serves to corroborate the other vitals, that is, to confirm what they show, and it enters the score only when the class requires it. Of the presets, only R3 requires it. A custom spec sheet may require it, in field S19.

1. Where the spec sheet requires communication testing, through field S19 and the predicate P-D7, D7 **MUST** be included in the minimum that sets the score and **MUST** follow the method in parameter T26. If D7 is not run, it counts as unobserved. See §6 and §8.
2. Where the spec sheet does not require it, D7 **MUST NOT** enter the minimum. In that case:
   - a D7 result that agrees with what D1–D6 show **SHOULD** raise the evidence-quality confidence;
   - a D7 result below its reference while D1–D6 all meet theirs **MUST** produce the finding "unexplained communication regression" and **SHOULD** start an attribution investigation;
   - once the cause has been attributed to a network element, that evidence lowers the vital that covers the element.
3. **Footprint.** Synthetic collective tests **MUST** stay within the footprint (the amount of the fabric's time and nodes they take up) that the Rulebook fixes as part of the method M-D7, parameter T26. Its values are not yet set:
   - a short duration for each run, the parameter `K_d7dur`;
   - a small set of nodes reserved for testing, the parameter `K_d7nodes`, or scheduled gaps between tenant jobs;
   - an upper limit on how often tests run, the cadence `K_cad`.

   The spec sheet declares the footprint actually used, within those bounds, in field S19.

## 5. Normalization

Normalization means turning every raw measurement into a value on the common scale by comparing it with a reference.

1. Every metric **MUST** be judged against a reference that is either registered in the Rulebook or declared on the spec sheet. Which of the two applies to each metric is stated in the register column headed "Rulebook / Spec sheet", in `RULEBOOK.md` §2. Rulebook references fall into one of four categories:
   - (a) a published standard exists and sets the reference;
   - (b) a best practice exists but no standard. Best practices are graded by authority, from strongest to weakest: a consortium specification, then multi-vendor community practice, then a single operator's practice, then a single vendor's reference design, then marketing material;
   - (c) no standard or practice exists, so Fabric Vitals must define the reference itself;
   - (d) method only: the Rulebook fixes how the reference is measured, and the number itself comes from each fabric.
2. A category (b) value that comes from a single vendor or a single operator **MAY** be used only as a declared reference for that vendor's or operator's own technology.
3. For category (d), the reference is produced separately for each fabric by the method registered in the Rulebook, which has these parts:
   - (i) the declared configuration;
   - (ii) a measurement definition;
   - (iii) a measurement taken when the fabric is commissioned, using the standard test suite, parameter T34, after the burn-in period, parameter T36, has passed;
   - (iv) the value declared on the spec sheet, and the preset's acceptance criterion where the preset has one;
   - (v) re-registration of the reference, as a versioned event, whenever the configuration or the design changes.
4. Rolling baselines (references learned from the fabric's own recent history) and peer comparisons (comparing one entity with similar ones), parameter T27, **MAY** be computed. They **MUST NOT** change a vital's value. What they produce is anomaly findings, triggers for attribution, and flags on evidence-quality confidence. The reason is that a learned baseline turns whatever state the fabric is in now into its reference [17]. Comparing planes with each other, on the expectation that they should look alike, is valid only where the transport forces equal load onto every plane [9].
5. **Value functions.** Each metric **MUST** pass through a value function that maps it onto the common currency. See §4.1. The function is anchored so that the same states map to the same values in every vital, using the anchors in parameter T31:
   - 100 means the declared promise, or the Rulebook reference for the class, is fully delivered;
   - values in between mean the fraction of the promise delivered, for example the share of the capacity that meets it;
   - 0 means none of the promise is delivered; capacity under a critical condition is at 0.

   The shape of each function between its anchors is parameter T25, which is VALUE NOT SET. Value functions **MUST** be monotone: a worse input never yields a higher value.
6. **Utilization** **MUST NOT** be scored as an average over time. It is scored as a peak or a percentile within the phases when accelerators are communicating, against the declared capacity and the current failure state [18].
7. **Physical-layer budgets.** These are category (a) references, parameter T37, taken from the IEEE Ethernet standards. They are used to measure how far a link is from its budget, not as alarm levels:
   - the frame loss ratio for the complete PHY after FEC has made its repairs: 6.2×10⁻¹¹ for 64-octet frames at 200 Gb/s and above, and 6.2×10⁻¹⁰ at 100 Gb/s [19, 20, 21, 22, 23, 24, 25, 26];
   - the bit error ratio (BER) allowed before FEC correction at the PMD (the physical medium dependent sublayer, the part of the PHY that drives the cable or fibre): 2.4×10⁻⁴ for PHYs that use the RS(544,514) Reed–Solomon code at 50/100G per lane [27, 28].

## 6. Aggregation

Aggregation is how many measurements become one vital value, and how the vital values become one Vitals Score.

1. **Within a vital:**
   - quantities **MUST** be intensive, meaning expressed as rates or fractions that do not grow with the size of the fabric, such as per link-hour, per GB (gigabyte) or as a fraction of time;
   - entities (switches, links, ports) **MUST** be weighted by their share of the capacity in the declared inventory;
   - the single worst entity **MUST** be reported alongside the vital value;
   - the exact rule for combining entities within a vital is part of the value-function definition, parameter T25.
2. **Across vitals:** the Vitals Score **MUST** be the minimum, that is, the lowest, of the confirmed (lower-bound) values of the vitals the spec sheet requires, capped by any active critical condition. No weights are used: no vital counts for more than another. See §7.
3. **Companions.** With every Vitals Score an implementation **MUST** also report:
   - the breadth indicator: how many of the required vitals are not delivering their full promise, that is, are below 100, out of the number required;
   - the next-binding vital, the one that would set the score if the current weakest were fixed, and its value;
   - the full list of all the vital values.
4. **Why the minimum.** Different ways of combining vitals were compared on a masking example, in which four vitals are at 100 and one has collapsed to 10; the comparison is in [`SCENARIOS.md`](SCENARIOS.md) §1. Only the rules that let the collapsed vital decide the score pass that test, and among those the minimum is the only one that needs no weights and no cap constants.
5. **Commensurability.** Taking the minimum assumes that the vitals are commensurable, that is, that a given value means the same degree of trouble in every vital. Implementations and Rulebooks **SHOULD** treat this assumption as unvalidated until experiment E4 reports. The experiment is described in [`VALIDATION.md`](VALIDATION.md).

## 7. Critical conditions

A critical condition is a state so serious that the score is capped while it lasts. The table names the six conditions, the evidence that shows each one, and where each one applies.

| ID | Condition | Evidence | Applies where |
|---|---|---|---|
| CC1 | Partition or black hole: part of the fabric cannot reach the rest, or packets are silently discarded | Verified by probes, metric M04, with the interface, session and route metrics M01–M03 | Always |
| CC2 | PFC storm or deadlock: pause signals spread out of control, or paused queues wait on each other so that none can ever drain | The storm and pause metrics M14 and M13 | Only where lossless transport is declared, field S7 |
| CC3 | Sustained loss on a lossless class | The loss metrics M10 and M17; how long counts as "sustained" is parameter T14 | Only where lossless transport is declared, field S7; the details depend on the transport mode |
| CC4 | A single point of failure on capacity that carries jobs: one device or link whose failure alone would take that capacity out | The interface status metric M01 together with the declared build | Only where the spec sheet promises that there is no single point of failure, fields S4 and S10 |
| CC5 | Redundancy exhausted: the spare paths the fabric promised have all been used up | For a class of job-bearing paths, the resilience metrics M07–M09 | Measured against the failures the fabric declared it tolerates, field S10 |
| CC6 | Uncorrectable errors beyond the IEEE budget: bit errors that FEC could not repair, more of them than the standard allows | On job-bearing links, the error metrics M28 and M30, judged against parameters T37 and T38 | The budget depends on the PHY type, field S18 |

1. A condition **MUST** cap the Vitals Score at the cap value, parameter T15, only when the share of job-bearing capacity it affects is at least the blast-radius threshold, parameter T16. How long a condition has to persist before it counts, and how long it is held afterwards, are parameter T17.
2. The affected share **MUST** be computed as the share observed to be in the condition plus the share of that condition's evidence set that could not be observed at all. Unmeasured capacity counts as affected.
3. Once raised, a condition **MUST** remain raised until the fabric is positively observed to be clear of it. Losing the telemetry that showed it **MUST NOT** clear it.
4. A condition that is capping the score **MUST** be reported as the binding reason, with a tag saying where it comes from: DESIGN SHORTFALL when it is a failed predicate against the declared spec sheet, PLANNED when it falls inside a declared maintenance window, or OPERATIONAL otherwise. See §9.3.
5. The expected behaviour for nineteen representative failures and events, showing which vitals move, when a condition caps the score, and how long recovery takes, is tabulated in `SCENARIOS.md` §2. That table is informative, not normative: it illustrates the rules but does not add to them.

## 8. Coverage, confirmed score and range

This section says what happens when some of the telemetry is missing.

### 8.1 Telemetry profile

The telemetry profile, declared in field S20, is the list of what the fabric exports. It has one row for each combination of entity class (such as switch port or NIC port), vital and metric. It **MUST** cover at least the minimum the Rulebook sets for the declared class, parameter T35. Each row gives:
- the metric ID;
- where the value comes from: the path in the data model, or the mapping used for each driver;
- the metric type: a counter (a running total), a gauge (a current value), a watermark (a high or low point reached), an event or a histogram;
- the declared sampling interval, written Δ (how often a value is collected), and the resolution requirement, parameter T20;
- the grace period, written G (how late a sample may be before it counts as missing), parameter T30;
- whether the metric is required for coverage;
- which critical conditions' evidence sets it belongs to.

A metric that a predicate declares NOT APPLICABLE to this fabric (for example CNP counts on a fabric that does not run DCQCN, the data-center congestion-control scheme that uses those packets) is removed from the coverage denominator, the total against which coverage is measured. Simply failing to export a metric **MUST NOT** remove it from the denominator; it counts as missing.

### 8.2 Grace period

For each pair of entity and metric, let *a* be the age of the most recent valid sample at the moment the score is computed.
1. If a ≤ Δ + G, that is, the sample is no older than one sampling interval plus the grace period, the slice is observed:
   - cumulative counters use the rate over the last completed interval;
   - gauges and watermarks carry their last value forward;
   - event and state streams use the last state reported, provided a heartbeat or a full synchronisation arrived within Δ + G.
2. If a > Δ + G, the slice is unobserved from the moment t_last + Δ + G onward, where t_last is the time of that last sample.
3. Carrying a value forward **MUST NOT** clear a raised critical condition.
4. A score that has been published **MUST NOT** be revised when late data arrives. Recomputing with a later data cut-off produces a new score record instead. Counter discontinuities (a counter resetting or jumping, for example after a reboot) are handled as RFC 8343 defines with its `discontinuity-time` field [29].
5. **Property.** These rules guarantee that removing telemetry can never raise the confirmed score above the value that full telemetry would have produced at some moment within the preceding grace period G. G = 0 gives the strict form of this property.

### 8.3 Bounded values and the confirmed score

1. For each vital, the implementation **MUST** compute:
   - a lower bound, in which every unobserved entity or time slice is set to 0, the worst value;
   - an upper bound, in which every unobserved entity or time slice is set to 100, the best value.
2. The Vitals Score is the confirmed score: the minimum of the lower bounds, capped by critical conditions. It **MUST** be displayed together with the upper bound (the same calculation done with the upper bounds) and the coverage of each vital.

### 8.4 Coverage floor and UNSCORABLE

1. If any required vital, or the evidence set of any critical condition, has coverage below the coverage floor F, parameter T29, the result **MUST** be UNSCORABLE, recorded as the value −1.
2. Wherever scores are used to judge conformance, UNSCORABLE **MUST** rank below every numeric score, and it **MUST NOT** be displayed as a pass. The −1 value follows the IETF's service-assurance practice [30].
3. **Missing-telemetry list.** An UNSCORABLE result **MUST** say exactly which required telemetry is missing and where: for each vital or condition, the entity IDs, the metric IDs, the share of capacity below the floor, and for each item whether it is *missing*, *stale beyond grace* or *unsupported by the platform*.

### 8.5 Coupling constraint (T39)

1. For every critical condition *k*, take its coverage floor F_k and its blast-radius threshold T16_k, both defined over the same denominator, namely the job-bearing capacity of the condition's evidence set. The Rulebook **MUST** set them so that F_k + T16_k > 1.
2. A Rulebook **MAY** relax this constraint for one specific condition only by setting the flag `unobserved_capacity_can_be_critical = true` for that condition, and only with a written rationale recorded in the Rulebook.
3. **Why.** A fabric can be scored only if its unobserved share u ≤ 1 − F_k, that is, only if no more is missing than the floor allows. Unobserved capacity on its own reaches the blast-radius threshold only if u ≥ T16_k. Both can be true at the same time exactly when F_k + T16_k ≤ 1, which is the case the constraint rules out.
4. **Consequences:**
   - Under the constraint, hiding a region of the fabric large enough to trigger condition *k* pushes coverage below F_k, so the result becomes UNSCORABLE instead of escaping the cap.
   - If the coverage floor is measured over a denominator D that is larger than the denominator J used by the condition's gate, the constraint becomes T16_k > (1 − F_k)·|D|/|J|.
   - Fabrics that export little telemetry will be UNSCORABLE for the conditions affected. The missing-telemetry list tells the operator what to add.

### 8.6 Evidence-quality confidence

Implementations **MUST** report evidence-quality confidence, a statement of how far the evidence behind each vital, and behind the overall score, can be trusted. It covers:
- freshness: whether samples arrived within the grace period;
- resolution: whether samples are fine-grained enough;
- capability: whether the platform can export every required metric (a required metric the platform does not support also counts as unobserved);
- counter integrity: whether the counters themselves are sound;
- semantic trust: whether a metric means the same thing on every device, since some counters have driver-specific or device-specific meanings [31, 32];
- corroboration by D7, the AI-communication vital.

Confidence **MUST NOT** change the Vitals Score. The level at which a flag is raised, and the rule for combining the parts, are parameter T23.

## 9. Temporal behaviour

### 9.1 Windows and trends

1. Within a scoring window, vitals **SHOULD** score the share of the time, or of the samples, that was in a good state.
2. Implementations **SHOULD** publish three labelled views of the score: current, rolling and daily. The length of each window is parameter T19.
3. Short catastrophes, failures that are over quickly but serious, **MUST** still register: through the critical conditions, and through pairing a short window with a long one.
4. How quickly a condition's effect decays after it clears, and the hysteresis that stops a condition flickering on and off, are set for each class of condition in parameter T18.
5. Trends **MUST** be reported on the full list of vital values and on the breadth indicator, not on the headline number alone.
6. A trend against the fabric's own history is descriptive only; it **MUST NOT** be used to re-base any reference.

### 9.2 Availability

1. **Definition.** Take a reporting period P and divide it into scoring windows, each as long as the current view, parameter T19. The fabric's availability over P is the share of those windows in which all of the following hold:
   - the result is numeric (not UNSCORABLE);
   - the Vitals Score is at or above the upper band edge, parameter T40, that is, it is in the healthy band; and
   - no critical condition is active.

   A statement such as "Healthy X% of the time" means that availability over P was X%.
2. UNSCORABLE windows **MUST** count as not healthy, following the rule that unknown is not the same as healthy. Implementations **MUST** report the share of windows that were UNSCORABLE beside the availability figure.
3. Availability **MUST** be reported against the target the owner declared on the spec sheet, field S12, as MET or NOT MET for the period, with the period stated.
4. Availability is a companion figure to the Vitals Score, not an input to it. It **MUST NOT** change any vital or the headline number.
5. The Rulebook sets no availability targets; the target is the owner's. Until the band edges, parameter T40, are set, availability can be computed only with made-up edges, and any such figure **MUST** be labelled ILLUSTRATIVE.

### 9.3 Planned maintenance

1. Maintenance reduces the resilience that is actually available while it is going on, and the score **MUST** reflect that: vitals and critical conditions are computed exactly as for any other window.
2. A maintenance window **MAY** be declared in advance, giving its scope, the entities affected, and its start and end times. Declarations are versioned events, like the spec sheet itself, and **MUST** be made before the window starts.
3. Contributors and binding reasons that occur inside a declared window, on the entities that were declared, **MUST** be tagged PLANNED.
4. The spec sheet, in field S12, states whether windows that fall inside declared maintenance count against the availability target. The availability report **MUST** state which rule was applied.
5. There is no undeclared maintenance mode. Nothing suspends scoring, and an intervention that was not declared in advance is tagged OPERATIONAL.

## 10. Workload profiles

A workload profile describes what kind of work the fabric is used for, and it adjusts a few details of how the fabric is judged. The profiles are TRAINING, INFERENCE and GENERAL.
- **What a profile selects:** which tail statistic the delay vital D4 uses, what "headroom" means for the capacity vital D6, which value functions the congestion vital D3 uses, and which test suites are run for D7 and at commissioning.
- **What it does not change:** the set of vitals, the way they are aggregated, the set of critical conditions, or the coverage rules.
- **Mixed fabrics:** a fabric whose declared purpose, field S2, is a mix of workloads **MUST** declare the one profile it is scored under.
- **Candidate profiles:** the excluded areas listed in §2.5 item 3, namely front-end and inference-serving networks, storage and checkpoint traffic, scale-up interconnects and multi-tenant isolation, are candidates for later profiles, in that order.

The evidence for splitting the profiles this way is in [8, 33, 34, 35].

## 11. Explanation record and presentation

### 11.1 The record

The explanation record is the full account that goes with every score. Every score record **MUST** contain the following.

**Identity:**
- the Rulebook ID and version;
- the spec-sheet version, and the class preset it adopts, or CUSTOM if it adopts none;
- the scoring scope ID and, for a fabric with several scopes, the full set of scope scores with their distribution and the lowest scope;
- the declared maintenance windows in force;
- the declared class, the verified class, the conformance status and the date of the last conformance check;
- the commissioning references registered and in force;
- the versions of the metric definitions and of the aggregation rules.

**Context:**
- the workload profile;
- the fabric scope ID;
- the window scored;
- the data cut-off time and the time of computation.

**Result:**
- the Vitals Score (the confirmed score) and the upper bound, with the coverage of each vital; or UNSCORABLE together with the missing-telemetry list;
- the score band, marked ILLUSTRATIVE where the band edges have not been calibrated. See §11.2.
- the breadth indicator, the next-binding vital and the full list of vital values;
- the evidence-quality confidence;
- the binding reason with its origin tag (DESIGN SHORTFALL, OPERATIONAL or PLANNED);
- where the declared class differs from the verified class, the counterfactual "declared Rx, built as Ry; as Ry it would score N" and the remedy. See §3.
- the contributors, listed in order [36], and the mandatory findings;
- availability over the reporting period against the declared target, where it is reported. See §9.2.

The record **MUST** satisfy the rule that "a non-maximal score must always be explained by one or more symptoms" [30]: a score below the maximum is never left unexplained.

### 11.2 Score bands

1. Bands are a display rule: they decide the colour a score is shown in. They never change the Vitals Score.
2. The band edges are Rulebook parameter T40, which has an upper edge and a lower edge; both are VALUE NOT SET. The display is:
   - **green** for a score at or above the upper edge;
   - **amber** for a score at or above the lower edge and below the upper edge;
   - **red** for a score below the lower edge;
   - **red**, whatever the number, while any critical condition is active;
   - **grey** for UNSCORABLE.
3. Bands are part of the Rulebook and are published only once they have been calibrated, in experiment E6 using the method in parameter T22. Until then, any bands that are displayed are made-up and **MUST** be labelled ILLUSTRATIVE wherever they appear. Demonstrations of the method published before calibration use illustrative edges.
4. The cap value, parameter T15, **MUST** lie below the lower edge, so that a capped score shows red by its number as well as by the critical-condition rule.

### 11.3 Presentation rules

- **A score is never shown without its class.** The unit of presentation is the phrase "Vitals Score N, class Rx (spec sheet version)", with CUSTOM in place of Rx for a custom sheet. Showing a bare number is non-conformant presentation.
- Scores **MUST** be displayed as whole numbers.
- Language models (AI text generators) **MAY** be used to write explanations from the record in plain prose. They **MUST NOT** compute or change any value in it.

## 12. Comparability and versioning

1. Two scores can be compared only when all of the following are the same for both:
   - the fabric itself, compared over time; or, for different fabrics, the same class preset or identical spec sheets;
   - the Rulebook version;
   - the workload profile;
   - the kind of scoring scope: a scope score is compared with other scope scores, never with a figure blended across a whole fabric.
2. While the presets' promise values are not yet set, fabrics that adopt the same preset structure but declare their own promise values are comparable on structure only, not on the numbers, and the record **MUST** say so.
3. Scores of different classes, or of different custom spec sheets, **MUST NOT** be ranked against each other. A score confirms conformance to the fabric's own spec sheet, nothing more.
4. A score **MUST NOT** be compared across different Rulebook versions, spec-sheet versions or re-registrations of references unless it is recomputed first.
5. **Rulebook versions:** written RB-<major>.<minor>. A new major version changes the structure or the methods; a new minor version sets or revises values, including preset values. Once set, values are frozen at their freeze point. See [`GOVERNANCE.md`](GOVERNANCE.md).
6. **Determinism.** The same telemetry, the same spec sheet and the same Rulebook version **MUST** produce a score record that is identical bit for bit, whoever computes it.

## 13. Minimum implementation: the Day-One Set

1. **Purpose.** An operator should be able to compute a valid Vitals Score on the first day, using only telemetry that most platforms already export. The Day-One Set is the smallest set of vitals, counters and probes that makes this possible. A score computed from it is a Vitals Score like any other: the same Rulebook, the same rules and the same meaning.
2. **Contents.** The set below is PROPOSED. It becomes the common core of the minimum telemetry profile, parameter T35, for every class:

| Vital or condition | Counters and probes | Vendor-neutral data model, as listed in `METRICS.md` |
|---|---|---|
| D1 Reachability | Whether each interface is operationally up (M01); the state of each BGP session (BGP, the Border Gateway Protocol, is the routing protocol these fabrics use to exchange routes) (M02); LLDP neighbour data checked against the intended cabling (M06); an active probe mesh, test packets sent between endpoints (M04, using the method M-PRB) | OpenConfig (a vendor-neutral data model for network devices); the metric definitions in RFC 7679/7680 |
| D2 Resilience | How much path diversity remains and how much capacity would be left (M07–M09), worked out from M01, M06 and the declared inventory | Derived |
| D3 Congestion and loss | Packets dropped at queues and at interfaces (M10, M11); ECN marks applied by switches (M15); on lossless classes, how long PFC pauses last and storm events (M13, M14) | OpenConfig; SAI (the Switch Abstraction Interface, a common programming interface to switch chips) for M13 and M14 |
| D4 Delay and tail | Delay measured by the same probe mesh (M23) | RFC 7679 |
| D5 Physical link integrity | FEC codewords that were corrected and codewords that could not be corrected (M27, M28); FCS errors (FCS, the frame check sequence, is the checksum at the end of each Ethernet frame) (M31); link flaps (M32) | OpenConfig; IEEE |
| D6 Effective capacity | Bytes carried by each interface, taken as the peak within each sampling interval (M35) | OpenConfig |
| D7 AI communication | Only where the class requires it, which among the presets is R3: synthetic collective tests (M38) | — |
| Critical conditions | The evidence sets of the critical conditions, drawn from the rows above. See §7. | — |

3. **Everything else is optional in the Day-One Set:** the NIC's transport counters (M16–M18), buffer and queue watermarks (M19, M20, M24), in-band telemetry, which is measurement data carried inside the packets themselves (M25, M26), FEC histograms (M29), optical-module readings (M33), link-level retry counts (M34), configuration reads beyond the switch side (M43), and measurements of routing churn and convergence (M44, M45). An optional metric that is not observed is listed in the record as UNSCORABLE at the level of that metric, with the reason (missing, stale or unsupported). It does not enter the coverage denominator, and it is reflected in the evidence-quality confidence, never in the score. See §8.6.
4. A class's minimum telemetry profile, parameter T35, **MUST** include the Day-One Set and **MAY** require more.

## References

1. TIA. "ANSI/TIA-942: The Global Data Center Standard" (brochure describing TIA-942-C). Telecommunications Industry Association, April 2024. Brochure, not the standard text. https://tiaonline.org/wp-content/uploads/2024/05/Data-Centers-Brochure_040124.pdf (accessed 2026-09-23).
2. Uptime Institute. "Data Center Site Infrastructure Tier Standard: Topology". Uptime Institute, 2018 (effective October 2018). https://www.gpxglobal.net/wp-content/uploads/2018/11/Uptime-Tier-Standard-Topology.pdf (accessed 2026-09-23).
3. ISO/IEC JTC 1. "ISO/IEC TS 22237-5:2018 Data centre facilities and infrastructures — Part 5: Telecommunications cabling infrastructure". ISO/IEC, May 2018. Public preview only. https://cdn.standards.iteh.ai/samples/73012/f90c18a9cfdf49e2aa38e45fec4e420d/ISO-IEC-TS-22237-5-2018.pdf (accessed 2026-09-23).
4. BICSI. "An Overview of the ANSI/BICSI 002-2019 Data Center Availability Class Methodology". BICSI, 2019. Public overview, not the standard text. https://www.bicsi.org/docs/default-source/publications/002-2019-methodology.pdf (accessed 2026-09-23).
5. ISO/TC 292. "ISO 22301:2019 Security and resilience — Business continuity management systems — Requirements". ISO, October 2019. Public preview only. https://cdn.standards.iteh.ai/samples/75106/5e083fd428f54407a6aae14cb574019c/ISO-22301-2019.pdf (accessed 2026-09-23).
6. ISO/IEC JTC 1/SC 27. "ISO/IEC 27031:2025 Cybersecurity — ICT readiness for business continuity". ISO/IEC, 2025. Public preview only. https://cdn.standards.iteh.ai/samples/80975/8e844992be7e4ec88c4c364d22e73a4f/ISO-IEC-27031-2025.pdf (accessed 2026-09-23).
7. A. Gangidi, R. Miao, S. Zheng et al. (Meta). "RDMA over Ethernet for Distributed AI Training at Meta Scale". ACM SIGCOMM 2024, August 2024. Single operator. https://engineering.fb.com/wp-content/uploads/2024/08/sigcomm24-final246.pdf (accessed 2026-09-28).
8. K. Qian et al. (Alibaba Cloud). "Alibaba HPN: A Data Center Network for Large Language Model Training". ACM SIGCOMM 2024, August 2024. Single operator. https://ennanzhai.github.io/pub/sigcomm24-hpn.pdf (accessed 2026-09-23).
9. J. Araujo, A. Chow, M. Handley, J. Padhye et al. (49 authors; OpenAI, Microsoft, AMD, Broadcom, NVIDIA). "Resilient AI Supercomputer Networking using MRC and SRv6". arXiv 2605.04333v1, May 2026. Preprint; results depend on its multipath transport. https://arxiv.org/abs/2605.04333 (accessed 2026-09-23).
10. Juniper Networks. "AI Data Center Network with Juniper Apstra, NVIDIA GPUs, ConnectX NIC, and WEKA Storage — Juniper Validated Design" (JVD-AICLUSTERDC-AIML-02-10). August 2026. Single-vendor validated design. https://www.juniper.net/documentation/us/en/software/jvd/jvd-ai-dc-apstra-nvidia-weka/jvd-ai-dc-apstra-nvidia-weka.pdf (accessed 2026-09-28).
11. NVIDIA. "NVIDIA DGX SuperPOD (B300/XDR): Key Components". NVIDIA reference architecture documentation, last updated September 2026. Single-vendor reference design. https://docs.nvidia.com/dgx-superpod/reference-architecture/scalable-infrastructure-b300-xdr/latest/dgx-superpod-components.html (accessed 2026-09-28).
12. L. D. Lamb, L. Staley, J. Mora, A. Raman. "Open Pod Group for M xPUs (OPG-M) System Architecture". Open Compute Project, January 2026. Contributor document. https://www.opencompute.org/documents/opg-m-system-architecture-final-14-january-2026-pdf (accessed 2026-09-23).
13. C. Guo, H. Wu, Z. Deng, G. Soni, J. Ye, J. Padhye, M. Lipshteyn (Microsoft). "RDMA over Commodity Ethernet at Scale". ACM SIGCOMM 2016, August 2016. Single operator. https://www.microsoft.com/en-us/research/wp-content/uploads/2016/11/rdma_sigcomm2016.pdf (accessed 2026-09-23).
14. Z. Yao, P. Hu, C. Miao et al. (Fudan University, Tencent, University of Chicago). "Holmes: Localizing Irregularities in LLM Training with Mega-scale GPU Clusters". USENIX NSDI 2025, April 2025. https://www.usenix.org/system/files/nsdi25-yao.pdf (accessed 2026-09-23).
15. J. Dong, B. Luo, J. Zhang et al. (Alibaba, HKUST). "Enhancing Large-Scale AI Training Efficiency: The C4 Solution for Real-Time Anomaly Detection and Communication Optimization". IEEE HPCA 2025, March 2025. https://arxiv.org/abs/2406.04594 (accessed 2026-09-23).
16. Y. Deng, X. Shi, Z. Jiang et al. "Minder: Faulty Machine Detection for Large-scale Distributed Model Training". USENIX NSDI 2025, April 2025. https://www.usenix.org/system/files/nsdi25-deng.pdf (accessed 2026-09-23).
17. Y. Xiong, Y. Jiang, Z. Yang, L. Qu et al. (Microsoft). "SuperBench: Improving Cloud AI Infrastructure Reliability with Proactive Validation". USENIX ATC 2024, July 2024. https://www.usenix.org/system/files/atc24-xiong.pdf (accessed 2026-09-23).
18. Q. Zhang, V. Liu, H. Zeng, A. Krishnamurthy. "High-Resolution Measurement of Data Center Microbursts". ACM IMC 2017, November 2017. General data-center traffic, not AI-specific. https://conferences.sigcomm.org/imc/2017/papers/imc17-final60.pdf (accessed 2026-09-23).
19. IEEE 802.3 Working Group. "IEEE P802.3bs Project Objectives". IEEE, March 2016. Adopted objectives. https://www.ieee802.org/3/bs/Objectives_16_0317.pdf (accessed 2026-09-23).
20. IEEE 802.3 Working Group. "IEEE P802.3cd Objectives" (v4). IEEE. Adopted objectives. https://www.ieee802.org/3/cd/P802d3cd_objectives_v4.pdf (accessed 2026-09-23).
21. IEEE 802.3 Working Group. "IEEE P802.3ck Objectives". IEEE, March 2018. Adopted objectives. https://www.ieee802.org/3/ck/P802_3ck_Objectives_2018mar.pdf (accessed 2026-09-23).
22. IEEE 802.3 Working Group. "IEEE P802.3db Adopted Objectives". IEEE, November 2020. Adopted objectives. https://www.ieee802.org/3/db/P802d3db_Updated_Objectives_Approved_November_2020.pdf (accessed 2026-09-23).
23. IEEE 802.3 Working Group. "Adopted IEEE P802.3df Objectives". IEEE, November 2022. Adopted objectives. https://www.ieee802.org/3/df/proj_doc/objectives_P802d3df_221117.pdf (accessed 2026-09-23).
24. IEEE 802.3 Working Group. "Adopted IEEE P802.3dj Objectives". IEEE, March 2024. Adopted objectives for a project in development. https://www.ieee802.org/3/dj/projdoc/objectives_P802d3dj_240314.pdf (accessed 2026-09-23).
25. Ultra Ethernet Consortium. "Ultra Ethernet Specification", version 1.0.2. UEC, January 2026. https://ultraethernet.org/wp-content/uploads/sites/20/2026/01/UE-Specification-1.0.2-1.pdf (accessed 2026-09-23).
26. Ultra Ethernet Consortium. "Ultra Ethernet Specification", version 1.0.3. UEC, July 2026. https://ultraethernet.org/wp-content/uploads/sites/20/2026/08/UE-Specification-1.0.3.pdf (accessed 2026-09-23).
27. M. Gustlin. "802.3bj FEC Overview and Status". IEEE 802.3 100 Gb/s Wavelength Short Reach PHYs Study Group contribution, January 2020. Quotes IEEE 802.3 text. https://grouper.ieee.org/groups/802/3/100GSR/public/Jan20/gustlin_100GSR_01a_0120.pdf (accessed 2026-09-23).
28. X. Wang, X. He, H. Ren. "BER objective for Beyond 400GbE". IEEE 802.3 Beyond 400 Gb/s Ethernet Study Group contribution, March 2021. https://grouper.ieee.org/groups/802/3/B400G/public/21_03/wang_b400g_01a_210315.pdf (accessed 2026-09-23).
29. M. Bjorklund. "A YANG Data Model for Interface Management" (RFC 8343). IETF, March 2018. Proposed Standard. https://www.rfc-editor.org/rfc/rfc8343 (accessed 2026-09-23).
30. B. Claise, J. Quilbeuf, D. Lopez, D. Voyer, T. Arumugam. "Service Assurance for Intent-Based Networking Architecture" (RFC 9417). IETF, July 2023. Informational. https://www.rfc-editor.org/rfc/rfc9417 (accessed 2026-09-23).
31. Linux kernel. RDMA driver sources (mlx5 counters.c, bnxt_re hw_counters.c, irdma verbs.c, ionic ionic_hw_stats.c). Linux source tree, master branch (July 2026). https://github.com/torvalds/linux/tree/master/drivers/infiniband/hw (accessed 2026-09-23).
32. P4.org Applications Working Group. "In-band Network Telemetry (INT) Dataplane Specification", version 2.1. P4.org, November 2020. https://p4.org/wp-content/uploads/sites/53/p4-spec/docs/INT_v2_1.pdf (accessed 2026-09-23).
33. Ultra Ethernet Consortium. "Overview of and Motivation for the Forthcoming Ultra Ethernet Consortium Specification". White paper, July 2023. https://ultraethernet.org/wp-content/uploads/sites/20/2023/10/23.07.12-UEC-1.0-Overview-FINAL-WITH-LOGO.pdf (accessed 2026-09-23).
34. Y. Zhong, S. Liu, J. Chen et al. "DistServe: Disaggregating Prefill and Decoding for Goodput-optimized Large Language Model Serving". USENIX OSDI 2024, July 2024. https://www.usenix.org/system/files/osdi24-zhong-yinmin.pdf (accessed 2026-09-23).
35. R. Qin et al. (Moonshot AI, Tsinghua University). "Mooncake: Trading More Storage for Less Computation — A KVCache-centric Architecture for Serving LLM Chatbot". USENIX FAST 2025, February 2025. https://www.usenix.org/system/files/fast25-qin.pdf (accessed 2026-09-23).
36. L. DeNicola. "What Are Credit Score Reason Codes?". myFICO, undated. Score owner's own publication. https://www.myfico.com/credit-education/blog/reason-codes (accessed 2026-09-23).
