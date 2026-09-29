# Fabric Vitals — Fabric Spec Sheet and class presets (v0.2)

**Status:** Fabric Vitals v0.2 (draft) — a technical proposal for discussion. Not a standard. Rulebook values not yet set.

Fabric Vitals is a method for scoring the health of an AI data-center fabric: the network of switches, links and server network adapters that carries traffic between the accelerators of a cluster. The method produces one headline number, the Vitals Score, which says how well the fabric is keeping the promises made for it. This document is about those promises. It is written for the fabric's owner, the party accountable for the fabric, who is often also the operator that runs it, and for anyone who reads or checks an owner's declaration.

Fabric Vitals separates two things that the earlier draft, v0.1, kept together in a single register, one list of parameters:
- **The Rulebook** says how every fabric is measured and judged. It is identical for every fabric. It is the file [`RULEBOOK.md`](RULEBOOK.md).
- **The Fabric Spec Sheet** (this file) says what this fabric promises. The owner fills it in before measurement starts, and the Vitals Score then confirms whether the fabric keeps those promises.

The model is the car. Every car's range is measured by the same official test procedure, but each car has its own rated range. The test procedure is the Rulebook, and the rated range is on the car's spec sheet. The standard models in a maker's range are the **class presets**: ready-made, complete spec sheets for common fabric designs, which an owner can adopt instead of writing a custom one. Presets are different designs for different jobs, not better and worse versions of one design. See §5.

What to do with this file: read the rules in §1, then fill in every field of the template in §2 before any measurement starts. A fillable copy of the template is the file [`templates/fabric-spec-sheet.yaml`](templates/fabric-spec-sheet.yaml). The main specification, the file [`SPEC.md`](SPEC.md), holds the binding requirements for declaring a spec sheet and for checking a fabric against it. This file holds the template itself, the mapping that says which measurement checks which field, and the presets. See SPEC.md §2 and §3.

## 1. Rules for a spec sheet

1. **Declared before measurement.** No measurement window counts toward a Vitals Score until a spec sheet is in force. See SPEC.md §2.
2. **Signed, dated and versioned.** A change to any field creates a new spec-sheet version, and scores under different versions form separate series. See SPEC.md §12.
3. **Preset or custom.** The owner either adopts a class preset unchanged, or declares a custom spec sheet. A custom sheet must not carry a preset's class name. See §5.
4. **No laxer than a standard.** Where a field has a standard behind it (today only the physical-layer budgets, S18), the owner may declare a stricter value but never a laxer one.
5. **Checked two ways.** The build fields are checked by the conformance check, which compares the fabric as built with what the sheet declares. The promise fields are checked continuously by the vitals (the seven measured dimensions of fabric health, D1 to D7), the critical conditions (named fault states, CC1 to CC6, that cap the score while active) and the availability measure. See SPEC.md §3, and §4 below.
6. **Scoring scope.** Every vital, coverage figure (coverage is the share of declared capacity that telemetry, the fabric's exported measurements, reports on) and critical-condition threshold is computed within one declared scoring scope (S23), the unit of the fabric scored as one, never blended across scopes. See SPEC.md §2.6.
7. **Comparability.** Scores are comparable only between fabrics on the same class preset, or on identical spec sheets, under the same Rulebook version. See SPEC.md §12.

## 2. The template

Field IDs S1–S23 are used throughout the specification. "Register" names the Rulebook parameter (T-ID) or design predicate (P-…, a yes-or-no test of the build) that the field declares a value for. "Checked by" names what confirms the promise: a vital, a critical condition, a metric from [`METRICS.md`](METRICS.md) (M-ID) or the conformance check. Names such as `K_planes` are values not yet set.

| ID | Section | Field | What the owner declares | Register | Checked by |
|---|---|---|---|---|---|
| S1 | Identity | **Fabric scope and inventory** | The switches, links and NIC ports in scope, and which capacity is job-bearing, that is, carries accelerator jobs. v0.2 covers back-end scale-out fabrics. | — | Inventory for every vital and for coverage |
| S2 | Identity | **Purpose and workload profile** | Purpose: training, inference or mixed. Scoring profile: TRAINING, INFERENCE or GENERAL. A mixed-purpose fabric names the one profile it is scored under. See SPEC.md §10. | — | Selects the D4 tail statistic, the D6 headroom reading and the D7 test suite |
| S3 | Build | **Topology** | Tiers and shape: Clos, rail-optimized (each NIC position on every server connects to the same leaf, forming a rail), rail-only (no any-to-any paths) or multi-plane (several independent parallel fabrics); the designed endpoint-pair paths | P-PATH | Conformance check (static review); D1 |
| S4 | Build | **Host attachment** | Each accelerator NIC: single-homed (one leaf), dual-homed (two distinct leaves), or attached to `K_planes` independent planes | P-HOME | Conformance check; D1, D2; CC4 |
| S5 | Build | **Uplinks and subscription ratio** | Leaf uplink ÷ downlink capacity; disjoint equal-cost paths per tier | P-SUB, P-PATH | Conformance check; D2, D6 |
| S6 | Build | **Planes** | Number of independent planes, and which NIC ports attach to each | P-HOME | Conformance check; D2, D6 |
| S7 | Build | **Transport and load distribution** | Transport, for example RoCEv2 (RDMA over Converged Ethernet), UET (Ultra Ethernet Transport) or InfiniBand; congestion-control mode, for example DCQCN (Data Center Quantized Congestion Notification) on or off; load distribution: flow hashing, where each flow keeps to one path, or packet spraying, where a flow's packets are spread over many paths | P-TX | Conformance check; selects the D3 metrics (for example whether CNP, congestion notification packet, counts apply) and the D6 imbalance metric |
| S8 | Build | **Lossless-transport configuration** | For lossless classes: the priorities on which PFC (priority flow control, the per-priority pause of lossless Ethernet) is enabled; the ECN (explicit congestion notification, the congestion mark that slows senders before loss) marking configuration; the DSCP-to-traffic-class mapping; and the MTU. Declared once for switches and NICs. See §3. | P-CFG | Conformance check (static review); a live mismatch is D3 evidence, through metric M43 |
| S9 | Build | **Physical diversity** | Cabling availability class for inter-cabinet links | P-PHY | Conformance check (declaration and audit) |
| S10 | Resilience promise | **Failures ridden through without capacity loss** | Per tier, the number of concurrent link or switch failures `K_k(tier)` the fabric absorbs, the residual capacity kept after them, and the largest share of job-bearing capacity any single component may remove (`K_fd`) | P-K, P-FD; T12 | Computed check and outcome tests; D2; CC4, CC5 |
| S11 | Resilience promise | **Recovery objective** | Per failure class: recovery mechanism (routing convergence, NIC multipath or spraying, or job restart), time to restore designed capacity, routing convergence time where routing is the mechanism, and tolerated job impact (continue, degrade or restart) | P-REC; T33 | Outcome tests; D2, through metric M45 |
| S12 | Availability | **Availability target** | "Healthy X% of the time" over a stated period: the share of scoring windows in which the Vitals Score is in the healthy band (the top score band) and no critical condition is active; and whether windows inside declared maintenance windows count against the target. See SPEC.md §9.2 and §9.3. | — | Availability measure |
| S13 | Performance envelope | **Bandwidth per accelerator** | Designed scale-out bandwidth per accelerator | — | D6 (declared capacity) |
| S14 | Performance envelope | **Collective bandwidth reference** | The bus bandwidth the fabric promises for synthetic collectives (test traffic that imitates the group communication of AI jobs), per (collective, message size, rank count) cell, measured by method M-D7 | T26 | D7 |
| S15 | Performance envelope | **Tail-delay budget** | Per path class, the tail statistic of probe delay the fabric promises, loaded and unloaded, measured by method M-DLY | T10 | D4 |
| S16 | Performance envelope | **Loss budget** | Loss per cause and traffic class, and NIC retransmission, out-of-sequence and timeout rates, per GB and per QP-hour | T4 | D3 |
| S17 | Performance envelope | **Pause budget** | PFC pause-time fraction per priority and port | T3 | D3 |
| S18 | Performance envelope | **Physical-layer budgets** | Per PHY type: the IEEE 802.3 budget, a fixed floor no sheet may relax (T37), and any stricter early-warning margin (T5) | T37, T5 | D5; CC6 |
| S19 | Required tests | **Synthetic collectives and conformance tests** | Whether communication testing with synthetic collectives (D7) is required; its footprint within the Rulebook bounds (test duration `K_d7dur`, a small reserved node set `K_d7nodes` or scheduled gaps, and cadence `K_cad`); conformance outcome-test cadence `K_conf` | P-D7 | D7 rules; conformance check. See SPEC.md §4.3. |
| S20 | Required tests | **Telemetry profile** | The metrics exported per entity class, with model paths and sampling intervals. It must cover the Rulebook minimum for the class (T35) | P-TEL; T35 | Coverage. See SPEC.md §8. |
| S21 | Class | **Declared class** | A preset ID or CUSTOM. See §5. | T32 | Conformance check, which reports the verified class (the most redundant preset the fabric as built satisfies) beside it |
| S22 | Class | **Spec-sheet version** | Version, date, signer, and the Rulebook version the sheet is declared against | — | Score record identity. See SPEC.md §11. |
| S23 | Identity | **Scoring scope** | The unit within which jobs run and which is scored as one: a pod or scalable unit, listed by ID with its share of S1. A fabric larger than one scope is reported as a set of scope scores. See SPEC.md §2.6. | — | Denominator for every vital, for coverage and for blast-radius thresholds (how much capacity a problem must affect before it counts as critical) |

## 3. The lossless-transport configuration check (S8)

**Why it is named.** Configuration errors are a documented cause of failure in lossless RDMA fabrics. In Meta's RoCE fabrics, congestion drops were "uncommon and observed mostly due to misconfiguration" [1]. Microsoft reports a production incident "caused by the buffer misconfiguration of a newly introduced switch type", whose pause frames spread and affected thousands of servers, and runs "a configuration monitoring service to check if the running configurations of the switches and the servers are the same as their desired configurations" [2]. Lossless operation depends on switches and NICs agreeing: "DSCP-based PFC requires both NICs and switches to classify and queue packets based on the DSCP value" [2].

**What is checked.** For every declared lossless traffic class, on every job-bearing path (NIC → switches → NIC):
1. the same priorities are PFC-enabled on every hop and on both NICs;
2. ECN marking is enabled, with the declared configuration, on every queue that carries the class;
3. the DSCP-to-traffic-class mapping is identical on every switch and NIC;
4. the MTU is consistent along the path.

**How it enters the score.**
- **At declaration and conformance.** S8 is the predicate P-CFG. A path whose running configuration differs from S8 fails the predicate, and the conformance status lists it. See SPEC.md §3.
- **In operation.** Where running configuration can be read, a live mismatch is D3 evidence (metric M43). It lowers D3 for the affected capacity and produces a mandatory finding tagged OPERATIONAL. It is not a critical condition in v0.2: the consequences that matter (sustained loss, pause storms, black holes) are already capped by CC3, CC2 and CC1. A pause storm is a PFC pause spreading from hop to hop.
- **Vendor-neutral visibility is partial.** Switch-side MTU, DSCP classification and ECN enablement have OpenConfig models; PFC configuration does not, and NIC-side configuration is driver-specific. See METRICS.md M43.

## 4. Which vital checks which field

| Vital or measure | Spec-sheet fields it checks | How |
|---|---|---|
| **D1 Reachability** | S1, S3, S4 | Designed endpoint-pair paths up and forwarding (control plane and probes); routing stability on the designed sessions, judged by the Rulebook (M02, M44) |
| **D2 Resilience** | S4, S5, S6, S10, S11 | Remaining redundancy and residual capacity against the declared tolerance; measured recovery and convergence time against the recovery objective (M45) |
| **D3 Congestion and loss** | S7, S8, S16, S17 | Loss and retransmission against the loss budget; pause time against the pause budget; configuration consistency (M43) |
| **D4 Delay and tail** | S2, S15 | Probe tail delay per path class against the tail-delay budget, using the statistic the workload profile selects |
| **D5 Physical link integrity** | S18 | Distance to the physical-layer budgets per PHY type |
| **D6 Effective capacity** | S5, S7, S13 | Peak utilization against declared capacity; imbalance measured the way the declared load distribution requires (flow hashing or spraying) |
| **D7 AI communication** | S14, S19 | Synthetic collectives against the collective bandwidth reference, where the sheet requires them |
| **Critical conditions** | S4 and S10 for the single-point-of-failure and redundancy-exhausted conditions, CC4 and CC5; S7 for the pause-storm and sustained-loss conditions, CC2 and CC3, which apply to lossless classes; S18 for the uncorrectable-error condition, CC6 | Class and transport decide which conditions apply. See SPEC.md §7. |
| **Every vital and condition** | S23 | Computed within the declared scoring scope |
| **Availability measure** | S12 | Share of scoring windows healthy against the declared target. See SPEC.md §9.2. |
| **Conformance check** | S3–S9, S19, S20, S21 | Static and computed checks of the build; outcome tests of S10 and S11 |

## 5. Class presets

**Status: PROPOSED — open for critique.** R1/R2/R3 are proposed class presets and candidate reference profiles, not an established universal taxonomy. The scheme is the author's proposal, derived from public sources on facility tiers and availability classes [3, 4, 5, 6, 7, 8, 9] and from published AI-fabric designs [1, 10, 11]. It is not derived from the requirement tables of any paywalled standard, which were not consulted.

**What a preset is.** A class preset is a published, complete spec sheet: its **structural predicates** (the build a fabric must have) and its **promise fields** (what a fabric of that class promises).

**What a preset is not.** The three v0.2 presets are starting points for industry critique. They do not claim to enumerate every valid AI-fabric architecture, and their final taxonomy remains an open question.

**Classes are design patterns, not quality tiers.** The three presets are ordered by the amount of redundancy they build in, not by how good they are. A fabric that keeps the promises of its class is healthy, whichever class it is. Scores are never ranked across classes. See SPEC.md §12.

| Code | Name | Description | Evidence for the pattern |
|---|---|---|---|
| **R1** | Rail-optimized, single-homed | A documented training design pattern that appears in multiple current reference designs and operator reports. Each accelerator NIC attaches to one leaf of its rail, and recovery from a leaf failure is by checkpoint restart. | Juniper's validated design: "rail Nth connects all GPUs in position Nth on all the servers, to leaf node Nth" [12]; NVIDIA's reference compute fabric "is rail-optimized" [13]; Alibaba calls single-ToR attachment "widely used in the majority of current cloud providers" [10]. |
| **R2** | Dual-homed | Rides through a leaf failure, or a bounded number of uplink failures per rail, without losing capacity. | Alibaba's HPN network "connects two ports of each NIC to different ToRs in an active-active way. … If one ToR (or a port) is down, the other can still work", in production [10]. |
| **R3** | Multi-plane, sprayed, tested | Independent planes, spraying across them, and continuous synthetic collective tests (D7 required). | Multi-plane spraying rides out tier-to-tier link failures [11]; a vendor reference design prescribes dual planes [14]. |

The preset's name fixes its structural pattern (single-homed, dual-homed, multi-plane with spraying); the numeric predicate values and all promise values are open. See the table below.

**Why failure consequence, not path counts.** Facility standards count distribution paths [4, 6]. Several AI designs, however, attach each NIC to a single rail switch by design [12, 13], and one open design states that "no redundancy is assumed or required" [15]. AI resilience comes from planes and spraying [11], dual attachment [10] or designed spare capacity; Meta chose an under-subscription ratio "to allow for buffer for up to two link failures" [1]. Presets are therefore stated as failure consequence, what the fabric absorbs and how it recovers (S10, S11).

**Preset fields.** Every preset fills in the same fields. All values are PROPOSED and not set, except S18, where the IEEE budget applies.

| Part | Field | Preset content | Value status |
|---|---|---|---|
| Structural | P-HOME host attachment (S4, S6) | single-homed, dual-homed, or at least `K_planes` planes | PROPOSED, not set |
| Structural | P-PATH path diversity (S3, S5) | at least `K_paths(tier)` disjoint equal-cost paths between any two leaves | PROPOSED, not set |
| Structural | P-SUB subscription (S5) | minimum uplink ÷ downlink ratio | PROPOSED, not set |
| Structural | P-TX transport (S7) | permitted transports, congestion-control modes and load-distribution modes | PROPOSED, not set |
| Structural | P-CFG lossless configuration (S8) | consistency across switches and NICs, required for every lossless class | Rule defined; no value needed. See §3. |
| Structural | P-PHY physical diversity (S9) | cabling availability class | PROPOSED, not set |
| Structural | P-TEL telemetry (S20) | the class's minimum telemetry profile (T35) | PROPOSED, not set |
| Structural | P-D7 testing (S19) | synthetic collectives required or not; cadences `K_cad`, `K_conf` | PROPOSED, not set |
| Promise | P-K / P-FD failures ridden through (S10) | `K_k(tier)`, residual capacity (T12), `K_fd` | PROPOSED, not set |
| Promise | P-REC recovery objective (S11) | mechanism, time to restore, routing convergence time, tolerated job impact (T33) | PROPOSED, not set |
| Promise | Availability target (S12) | healthy share of windows over a period | PROPOSED, not set |
| Promise | Bandwidth per accelerator (S13) | minimum designed bandwidth | PROPOSED, not set |
| Promise | Collective bandwidth reference (S14) | acceptance criterion `K_acc_D7` for T26 | PROPOSED, not set |
| Promise | Tail-delay budget (S15) | per path class (T10) | PROPOSED, not set |
| Promise | Loss budget (S16) | per cause and traffic class (T4) | PROPOSED, not set |
| Promise | Pause budget (S17) | pause-time fraction (T3) | PROPOSED, not set |
| Promise | Physical-layer budgets (S18) | IEEE 802.3 budget per PHY type (T37); early-warning margin (T5) | T37 BUDGET CITED (a standard exists); T5 PROPOSED, not set |

**Where each structural predicate comes from.** Authority grades in brackets follow the Rulebook conventions. See RULEBOOK.md §1.

| Predicate family | Checkable form | Evidence for the check | Borrowed from (grade) |
|---|---|---|---|
| P-HOME: host attachment | each accelerator NIC is single-homed, dual-homed to distinct leaves, or attached to at least `K_planes` independent planes | Declared intent compared with LLDP and cabling records (M06) | Alibaba dual-ToR (single-operator) [10]; multi-plane (operator group) [11]; NVIDIA dual-plane reference design (single-vendor) [14] |
| P-PATH: path diversity per tier | at least `K_paths(tier)` disjoint equal-cost paths between any two leaves in scope | Topology model (M07) | Facility ladder concept (standard, cabling only) [4, 6] |
| P-SUB: subscription | leaf uplink ÷ downlink capacity is at least the declared ratio | Inventory | Vendor designs (single-vendor) [12] |
| P-TX: transport and load distribution | declared transport (RoCEv2, UET or InfiniBand), congestion-control mode (for example DCQCN on or off), and flow hashing or spraying | Configuration snapshot | — |
| P-CFG: lossless-transport configuration | PFC priorities, ECN configuration, DSCP-to-class mapping and MTU consistent across switches and NICs on every job-bearing path | Running configuration compared with S8 (M43). See §3. | Operator practice (single-operator) [1, 2] |
| P-PHY: physical diversity | inter-cabinet cabling meets the declared cabling availability class | Declaration and audit | EN 50600-2-4 / ISO/IEC TS 22237-5; TIA-942-C (standard) [4, 6] |
| P-K: tolerated concurrent failures | after any `K_k(tier)` link or switch failures per tier, residual capacity is at least `K_resid` (T12) | Computed check, step 2. See RULEBOOK.md §4.2. | Meta "up to two link failures" (single-operator) [1] |
| P-FD: failure domain | no single component whose failure removes more than `K_fd` of job-bearing capacity | Computed | Uptime "Fault Tolerant" concept (proprietary standard) [3] |
| P-REC: recovery mechanism and objectives | declared mechanism is one of routing convergence, NIC multipath or spraying, or job restart; objectives per T33, including routing convergence time | Outcome test, step 3. See RULEBOOK.md §4.2. | ISO 22301 / 27031 business-continuity process (standard) [8, 9] |
| P-TEL: minimum telemetry profile | exports every metric listed for its entity class at the required resolution (T35) | Capability query and coverage (M41, M42) | — |
| P-D7: communication testing | runs M-D7 at cadence `K_cad` | Registration records | — |

**Verified class.** A fabric's verified class is the most redundant preset whose structural predicates all hold on the fabric as built, following the facility rule that a site's rating "is the lowest of the individual subsystem ratings" [3]. No fractional classes. Promise fields are not checked at this point: they are what the vitals confirm in operation.

**Where the ideas come from.** Owner declaration before design, from business impact [5]; rating by the weakest subsystem, no fractional ratings, and outcome-based confirmation tests [3]; recovery objectives declared by the organization and verified by exercise [8, 9].

**How presets get values.** Preset promise values are set only by the validation programme, [`VALIDATION.md`](VALIDATION.md), through experiment E1 and expert critique, frozen before use, and published with a new Rulebook version under the change process in [`GOVERNANCE.md`](GOVERNANCE.md). Until then an owner who adopts a preset declares its structure and fills in its promise values; comparability between such fabrics holds for the structure only, and the score record says so.

## References

1. A. Gangidi, R. Miao, S. Zheng et al. (Meta). "RDMA over Ethernet for Distributed AI Training at Meta Scale". ACM SIGCOMM 2024, August 2024. Single operator. https://engineering.fb.com/wp-content/uploads/2024/08/sigcomm24-final246.pdf (accessed 2026-09-28).
2. C. Guo, H. Wu, Z. Deng, G. Soni, J. Ye, J. Padhye, M. Lipshteyn (Microsoft). "RDMA over Commodity Ethernet at Scale". ACM SIGCOMM 2016, August 2016. Single operator. https://www.microsoft.com/en-us/research/wp-content/uploads/2016/11/rdma_sigcomm2016.pdf (accessed 2026-09-23).
3. Uptime Institute. "Data Center Site Infrastructure Tier Standard: Topology". Uptime Institute, 2018 (effective October 2018). https://www.gpxglobal.net/wp-content/uploads/2018/11/Uptime-Tier-Standard-Topology.pdf (accessed 2026-09-23).
4. TIA. "ANSI/TIA-942: The Global Data Center Standard" (brochure describing TIA-942-C). Telecommunications Industry Association, April 2024. Brochure, not the standard text. https://tiaonline.org/wp-content/uploads/2024/05/Data-Centers-Brochure_040124.pdf (accessed 2026-09-23).
5. BICSI. "An Overview of the ANSI/BICSI 002-2019 Data Center Availability Class Methodology". BICSI, 2019. Public overview, not the standard text. https://www.bicsi.org/docs/default-source/publications/002-2019-methodology.pdf (accessed 2026-09-23).
6. ISO/IEC JTC 1. "ISO/IEC TS 22237-5:2018 Data centre facilities and infrastructures — Part 5: Telecommunications cabling infrastructure". ISO/IEC, May 2018. Public preview only. https://cdn.standards.iteh.ai/samples/73012/f90c18a9cfdf49e2aa38e45fec4e420d/ISO-IEC-TS-22237-5-2018.pdf (accessed 2026-09-23).
7. CommScope. "Data Center Cabling Design Fundamentals" (white paper WP-321067-EU). 2015. Vendor white paper. https://www.commscope.com/globalassets/digizuite/3511-wp-321067-eu-data-center-cabling-design-fundamentals.pdf (accessed 2026-09-23).
8. ISO/TC 292. "ISO 22301:2019 Security and resilience — Business continuity management systems — Requirements". ISO, October 2019. Public preview only. https://cdn.standards.iteh.ai/samples/75106/5e083fd428f54407a6aae14cb574019c/ISO-22301-2019.pdf (accessed 2026-09-23).
9. ISO/IEC JTC 1/SC 27. "ISO/IEC 27031:2025 Cybersecurity — ICT readiness for business continuity". ISO/IEC, 2025. Public preview only. https://cdn.standards.iteh.ai/samples/80975/8e844992be7e4ec88c4c364d22e73a4f/ISO-IEC-27031-2025.pdf (accessed 2026-09-23).
10. K. Qian et al. (Alibaba Cloud). "Alibaba HPN: A Data Center Network for Large Language Model Training". ACM SIGCOMM 2024, August 2024. Single operator. https://ennanzhai.github.io/pub/sigcomm24-hpn.pdf (accessed 2026-09-23).
11. J. Araujo, A. Chow, M. Handley, J. Padhye et al. (49 authors; OpenAI, Microsoft, AMD, Broadcom, NVIDIA). "Resilient AI Supercomputer Networking using MRC and SRv6". arXiv 2605.04333v1, May 2026. Preprint; results depend on its multipath transport. https://arxiv.org/abs/2605.04333 (accessed 2026-09-23).
12. Juniper Networks. "AI Data Center Network with Juniper Apstra, NVIDIA GPUs, ConnectX NIC, and WEKA Storage — Juniper Validated Design" (JVD-AICLUSTERDC-AIML-02-10). August 2026. Single-vendor validated design. https://www.juniper.net/documentation/us/en/software/jvd/jvd-ai-dc-apstra-nvidia-weka/jvd-ai-dc-apstra-nvidia-weka.pdf (accessed 2026-09-28).
13. NVIDIA. "NVIDIA DGX SuperPOD (B300/XDR): Key Components". NVIDIA reference architecture documentation, last updated September 2026. Single-vendor reference design. https://docs.nvidia.com/dgx-superpod/reference-architecture/scalable-infrastructure-b300-xdr/latest/dgx-superpod-components.html (accessed 2026-09-28).
14. NVIDIA. "NVIDIA HGX AI Factory Enterprise Reference Architecture: Networking Logical Architecture". NVIDIA documentation (latest edition, undated). Single-vendor reference design. https://docs.nvidia.com/enterprise-reference-architectures/hgx-ai-factory/latest/network-logical-architecture.html (accessed 2026-09-23).
15. L. D. Lamb, L. Staley, J. Mora, A. Raman. "Open Pod Group for M xPUs (OPG-M) System Architecture". Open Compute Project, January 2026. Contributor document. https://www.opencompute.org/documents/opg-m-system-architecture-final-14-january-2026-pdf (accessed 2026-09-23).
