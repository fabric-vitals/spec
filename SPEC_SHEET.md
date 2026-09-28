# Fabric Vitals — Fabric Spec Sheet and class presets (v0.2)

**Status:** Fabric Vitals v0.2 (draft) — a technical proposal for discussion. Not a standard. Rulebook values not yet set.

Fabric Vitals separates two things that v0.1 kept in one register:
- **The Rulebook** ([`RULEBOOK.md`](RULEBOOK.md)) says *how* every fabric is measured and judged. It is identical for every fabric.
- **The Fabric Spec Sheet** (this file) says *what this fabric promises*. The owner fills it in before measurement, and the Vitals Score confirms whether the fabric keeps those promises.

The model is the car. Every car's range is measured by the same official test procedure, but each car has its own rated range. The test procedure is the Rulebook; the rated range is on the car's spec sheet; and the standard models in a maker's range are the **class presets** in §5: different designs for different jobs, not better and worse versions of one design.

Normative requirements for declaring and checking a spec sheet are in [`SPEC.md`](SPEC.md) §2 and §3. This file holds the template, the field-to-vital mapping and the presets. A fillable copy of the template is [`templates/fabric-spec-sheet.yaml`](templates/fabric-spec-sheet.yaml).

## 1. Rules for a spec sheet

1. **Declared before measurement.** No measurement window counts toward a Vitals Score until a spec sheet is in force ([`SPEC.md`](SPEC.md) §2).
2. **Signed, dated and versioned.** A change to any field creates a new spec-sheet version, and scores under different versions form separate series ([`SPEC.md`](SPEC.md) §12).
3. **Preset or custom.** The owner either adopts a class preset (§5) unchanged, or declares a custom spec sheet. A custom sheet **must not** carry a preset's class name.
4. **No laxer than a standard.** Where a field has a standard behind it (today only the physical-layer budgets, S18), the owner may declare a stricter value but never a laxer one.
5. **Checked two ways.** The *build* fields are checked by the conformance check ([`SPEC.md`](SPEC.md) §3). The *promise* fields are checked continuously by the vitals, the critical conditions and the availability measure (§4).
6. **Scoring scope.** Every vital, coverage figure and critical-condition threshold is computed within one declared scoring scope (S23), never blended across scopes ([`SPEC.md`](SPEC.md) §2.6).
7. **Comparability.** Scores are comparable only between fabrics on the same class preset, or on identical spec sheets, under the same Rulebook version ([`SPEC.md`](SPEC.md) §12).

## 2. The template

Field IDs S1–S23 are used throughout the specification. "Register" names the Rulebook parameter (T-ID) or design predicate (P-…) that the field declares a value for. "Checked by" names what confirms the promise.

| ID | Section | Field | What the owner declares | Register | Checked by |
|---|---|---|---|---|---|
| S1 | Identity | **Fabric scope and inventory** | The switches, links and NIC ports in scope, and which capacity is job-bearing. v0.2 covers back-end scale-out fabrics. | — | Inventory for every vital and for coverage |
| S2 | Identity | **Purpose and workload profile** | Purpose: training, inference or mixed. Scoring profile: TRAINING, INFERENCE or GENERAL ([`SPEC.md`](SPEC.md) §10). A mixed-purpose fabric names the one profile it is scored under. | — | Selects the D4 statistic, D6 headroom semantics and D7 suite |
| S3 | Build | **Topology** | Tiers and shape: Clos, rail-optimized, rail-only or multi-plane; the designed endpoint-pair paths | P-PATH | Conformance check (static); D1 |
| S4 | Build | **Host attachment** | Each accelerator NIC: single-homed, dual-homed to distinct leaves, or attached to `K_planes` independent planes | P-HOME | Conformance check; D1, D2; CC4 |
| S5 | Build | **Uplinks and subscription ratio** | Leaf uplink ÷ downlink capacity; disjoint equal-cost paths per tier | P-SUB, P-PATH | Conformance check; D2, D6 |
| S6 | Build | **Planes** | Number of independent planes, and which NIC ports attach to each | P-HOME | Conformance check; D2, D6 |
| S7 | Build | **Transport and load distribution** | Transport (e.g. RoCEv2, UET, InfiniBand); congestion-control mode (e.g. DCQCN on or off); load distribution: flow hashing or packet spraying | P-TX | Conformance check; selects D3 metrics (e.g. CNP applicability) and the D6 imbalance metric |
| S8 | Build | **Lossless-transport configuration** | For lossless classes: the PFC-enabled priorities, ECN marking configuration, DSCP-to-traffic-class mapping and MTU, declared once for switches and NICs (§3) | P-CFG | Conformance check (static); live mismatches are D3 evidence (M43) |
| S9 | Build | **Physical diversity** | Cabling availability class for inter-cabinet links | P-PHY | Conformance check (declaration and audit) |
| S10 | Resilience promise | **Failures ridden through without capacity loss** | Per tier, the number of concurrent link or switch failures `K_k(tier)` the fabric absorbs, the residual capacity kept after them, and the largest share of job-bearing capacity any single component may remove (`K_fd`) | P-K, P-FD; T12 | Computed check and outcome tests; D2; CC4, CC5 |
| S11 | Resilience promise | **Recovery objective** | Per failure class: recovery mechanism (routing convergence, NIC multipath or spraying, job restart), time to restore designed capacity, **routing convergence time** where routing is the mechanism, and tolerated job impact (continue, degrade or restart) | P-REC; T33 | Outcome tests; D2 (M45) |
| S12 | Availability | **Availability target** | "Healthy X% of the time" over a stated period: the share of scoring windows in which the Vitals Score is in the healthy band and no critical condition is active ([`SPEC.md`](SPEC.md) §9.2); and whether windows inside declared maintenance windows count against the target ([`SPEC.md`](SPEC.md) §9.3) | — | Availability measure |
| S13 | Performance envelope | **Bandwidth per accelerator** | Designed scale-out bandwidth per accelerator | — | D6 (declared capacity) |
| S14 | Performance envelope | **Collective bandwidth reference** | The synthetic-collective bus bandwidth the fabric promises per (collective, message size, rank count) cell, measured by method M-D7 | T26 | D7 |
| S15 | Performance envelope | **Tail-delay budget** | Per path class, the tail statistic of probe delay the fabric promises, loaded and unloaded, measured by method M-DLY | T10 | D4 |
| S16 | Performance envelope | **Loss budget** | Loss per cause and traffic class, and NIC retransmission, out-of-sequence and timeout rates, per GB and per QP-hour | T4 | D3 |
| S17 | Performance envelope | **Pause budget** | PFC pause-time fraction per priority and port | T3 | D3 |
| S18 | Performance envelope | **Physical-layer budgets** | Per PHY type: the IEEE 802.3 budget (fixed floor, T37) and any stricter early-warning margin (T5) | T37, T5 | D5; CC6 |
| S19 | Required tests | **Synthetic collectives and conformance tests** | Whether communication testing (D7) is required; its footprint within the Rulebook bounds (test duration `K_d7dur`, a small reserved node set `K_d7nodes` or scheduled gaps, and cadence `K_cad`); conformance outcome-test cadence `K_conf` | P-D7 | D7 rules ([`SPEC.md`](SPEC.md) §4.3); conformance check |
| S20 | Required tests | **Telemetry profile** | The metrics exported per entity class, with model paths and sampling intervals. It must cover the Rulebook minimum for the class (T35) | P-TEL; T35 | Coverage ([`SPEC.md`](SPEC.md) §8) |
| S21 | Class | **Declared class** | A preset ID (§5) or CUSTOM | T32 | Conformance check (verified class) |
| S22 | Class | **Spec-sheet version** | Version, date, signer, and the Rulebook version the sheet is declared against | — | Score record identity ([`SPEC.md`](SPEC.md) §11) |
| S23 | Identity | **Scoring scope** | The unit within which jobs run and which is scored as one: a pod or scalable unit, listed by ID with its share of S1. A fabric larger than one scope is reported as a set of scope scores ([`SPEC.md`](SPEC.md) §2.6) | — | Denominator for every vital, for coverage and for blast-radius thresholds |

## 3. The lossless-transport configuration check (S8)

**Why it is named.** Configuration errors are a documented cause of failure in lossless RDMA fabrics. In Meta's RoCE fabrics, congestion drops were "uncommon and observed mostly due to misconfiguration" [1]. Microsoft reports a production incident "caused by the buffer misconfiguration of a newly introduced switch type", whose pause frames spread and affected thousands of servers, and runs "a configuration monitoring service to check if the running configurations of the switches and the servers are the same as their desired configurations" [2]. Lossless operation depends on switches *and* NICs agreeing: "DSCP-based PFC requires both NICs and switches to classify and queue packets based on the DSCP value" [2].

**What is checked.** For every declared lossless traffic class, on every job-bearing path (NIC → switches → NIC):
1. the same priorities are PFC-enabled on every hop and on both NICs;
2. ECN marking is enabled, with the declared configuration, on every queue that carries the class;
3. the DSCP-to-traffic-class mapping is identical on every switch and NIC;
4. the MTU is consistent along the path.

**How it enters the score.**
- **At declaration and conformance.** S8 is the predicate P-CFG. A path whose running configuration differs from S8 fails the predicate, and the conformance status lists it ([`SPEC.md`](SPEC.md) §3).
- **In operation.** Where running configuration can be read, a live mismatch is D3 evidence (metric M43, [`METRICS.md`](METRICS.md)). It lowers D3 for the affected capacity and produces a mandatory finding tagged OPERATIONAL. It is not a critical condition in v0.2: the consequences that matter (sustained loss, pause storms, black holes) are already capped by CC3, CC2 and CC1.
- **Vendor-neutral visibility is partial.** Switch-side MTU, DSCP classification and ECN enablement have OpenConfig models; PFC configuration does not, and NIC-side configuration is driver-specific ([`METRICS.md`](METRICS.md) M43).

## 4. Which vital checks which field

| Vital or measure | Spec-sheet fields it checks | How |
|---|---|---|
| **D1 Reachability** | S1, S3, S4 | Designed endpoint-pair paths up and forwarding (control plane and probes); routing stability on the designed sessions, judged by the Rulebook (M02, M44) |
| **D2 Resilience** | S4, S5, S6, S10, S11 | Remaining redundancy and residual capacity against the declared tolerance; measured recovery and convergence time against the recovery objective (M45) |
| **D3 Congestion and loss** | S7, S8, S16, S17 | Loss and retransmission against the loss budget; pause time against the pause budget; configuration consistency (M43) |
| **D4 Delay and tail** | S2, S15 | Probe tail delay per path class against the tail-delay budget, using the statistic the workload profile selects |
| **D5 Physical link integrity** | S18 | Distance to the physical-layer budgets per PHY type |
| **D6 Effective capacity** | S5, S7, S13 | Peak utilization against declared capacity; imbalance measured the way the declared load distribution requires (flow-hash or spraying) |
| **D7 AI communication** | S14, S19 | Synthetic collectives against the collective bandwidth reference, where the sheet requires them |
| **Critical conditions** | S4, S10 (CC4, CC5); S7 (CC2, CC3 apply to lossless classes); S18 (CC6) | Class and transport decide which conditions apply ([`SPEC.md`](SPEC.md) §7) |
| **Every vital and condition** | S23 | Computed within the declared scoring scope |
| **Availability measure** | S12 | Share of windows healthy against the declared target ([`SPEC.md`](SPEC.md) §9.2) |
| **Conformance check** | S3–S9, S19, S20, S21 | Static and computed checks of the build; outcome tests of S10 and S11 |

## 5. Class presets

**Status: PROPOSED — open for critique.** The class scheme is the author's proposal, derived from public sources on facility tiers and availability classes [3, 4, 5, 6, 7, 8, 9] and from published AI-fabric designs [1, 10, 11]. It is not derived from the requirement tables of any paywalled standard, which were not consulted.

**What a preset is.** A class preset is a published, complete spec sheet: its **structural predicates** (the build a fabric must have) *and* its **promise fields** (what a fabric of that class promises).

**Classes are design patterns, not quality tiers.** The three presets are ordered by the amount of redundancy they build in, not by how good they are. A fabric that keeps the promises of its class is healthy, whichever class it is. Scores are never ranked across classes ([`SPEC.md`](SPEC.md) §12).

| Code | Name | Description | Evidence for the pattern |
|---|---|---|---|
| **R1** | Rail-optimized, single-homed | The most common training design in published reference designs today; each accelerator NIC attaches to one leaf of its rail, and recovery from a leaf failure is by checkpoint restart. | Juniper's validated design: "rail Nth connects all GPUs in position Nth on all the servers, to leaf node Nth" [12]; NVIDIA's reference compute fabric "is rail-optimized" [13]; Alibaba calls single-ToR attachment "widely used in the majority of current cloud providers" [10]. |
| **R2** | Dual-homed | Rides through a leaf failure, or a bounded number of uplink failures per rail, without losing capacity. | Alibaba HPN "connects two ports of each NIC to different ToRs in an active-active way. … If one ToR (or a port) is down, the other can still work", in production [10]. |
| **R3** | Multi-plane, sprayed, tested | Independent planes, packet spraying across them, and continuous synthetic collective tests (D7 required). | Multi-plane spraying rides out tier-to-tier link failures [11]; a vendor reference design prescribes dual planes [14]. |

The preset's name fixes its structural *pattern* (single-homed, dual-homed, multi-plane with spraying); the numeric predicate values and all promise values are open (below).

**Why failure consequence, not path counts.** Facility standards count distribution paths [4, 6]. Several AI designs, however, attach each NIC to a single rail switch by design [12, 13], and one open design states that "no redundancy is assumed or required" [15]. AI resilience comes from planes and spraying [11], dual attachment [10] or designed spare capacity; Meta chose an under-subscription ratio "to allow for buffer for up to two link failures" [1]. Presets are therefore stated as failure consequence (S10, S11).

**Preset fields.** Every preset fills in the same fields. **All values are PROPOSED and not set**, except S18, where the IEEE budget applies.

| Part | Field | Preset content | Value status |
|---|---|---|---|
| Structural | P-HOME host attachment (S4, S6) | single-homed / dual-homed / ≥ `K_planes` planes | PROPOSED, not set |
| Structural | P-PATH path diversity (S3, S5) | ≥ `K_paths(tier)` disjoint equal-cost paths between any two leaves | PROPOSED, not set |
| Structural | P-SUB subscription (S5) | minimum uplink ÷ downlink ratio | PROPOSED, not set |
| Structural | P-TX transport (S7) | permitted transports, congestion-control modes and load-distribution modes | PROPOSED, not set |
| Structural | P-CFG lossless configuration (S8) | consistency across switches and NICs required for every lossless class | Rule defined (§3); no value needed |
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
| Promise | Physical-layer budgets (S18) | IEEE 802.3 budget per PHY type (T37); early-warning margin (T5) | **T37 BUDGET CITED** (standard); T5 PROPOSED, not set |

**Where each structural predicate comes from.** Authority grades follow the Rulebook conventions ([`RULEBOOK.md`](RULEBOOK.md) §1).

| Predicate family | Checkable form | Evidence for the check | Borrowed from (grade) |
|---|---|---|---|
| P-HOME: host attachment | each accelerator NIC is {single-homed / dual-homed to distinct leaves / attached to ≥ `K_planes` independent planes} | Intent vs LLDP and cabling (M06) | Alibaba dual-ToR (single-operator) [10]; multi-plane (operator group) [11]; NVIDIA dual-plane reference design (single-vendor) [14] |
| P-PATH: path diversity per tier | ≥ `K_paths(tier)` disjoint equal-cost paths between any two leaves in scope | Topology model (M07) | Facility ladder concept (standard, cabling only) [4, 6] |
| P-SUB: subscription | leaf uplink ÷ downlink capacity ≥ declared ratio | Inventory | Vendor designs (single-vendor) [12] |
| P-TX: transport and load distribution | declared transport (RoCEv2 / UET / InfiniBand), congestion-control mode (e.g. DCQCN on or off), flow hashing or packet spraying | Configuration snapshot | — |
| P-CFG: lossless-transport configuration | PFC priorities, ECN configuration, DSCP-to-class mapping and MTU consistent across switches and NICs on every job-bearing path (§3) | Running configuration vs S8 (M43) | Operator practice (single-operator) [1, 2] |
| P-PHY: physical diversity | inter-cabinet cabling per the declared cabling availability class | Declaration and audit | EN 50600-2-4 / ISO/IEC TS 22237-5; TIA-942-C (standard) [4, 6] |
| P-K: tolerated concurrent failures | after any `K_k(tier)` link or switch failures per tier, residual capacity ≥ `K_resid` (T12) | Computed check ([`RULEBOOK.md`](RULEBOOK.md) §4.2 step 2) | Meta "up to two link failures" (single-operator) [1] |
| P-FD: failure domain | no single component whose failure removes more than `K_fd` of job-bearing capacity | Computed | Uptime "Fault Tolerant" concept (proprietary standard) [3] |
| P-REC: recovery mechanism and objectives | declared mechanism ∈ {routing convergence, NIC multipath or spraying, job restart}; objectives per T33, including routing convergence time | Outcome test ([`RULEBOOK.md`](RULEBOOK.md) §4.2 step 3) | ISO 22301 / 27031 process (standard) [8, 9] |
| P-TEL: minimum telemetry profile | exports every metric listed for its entity class at the required resolution (T35) | Capability query and coverage (M41, M42) | — |
| P-D7: communication testing | runs M-D7 at cadence `K_cad` | Registration records | — |

**Verified class.** A fabric's verified class is the most redundant preset whose **structural** predicates all hold on the fabric as built, following the facility rule that a site's rating "is the lowest of the individual subsystem ratings" [3]. No fractional classes. Promise fields are not checked at this point: they are what the vitals confirm in operation.

**Where the ideas come from.** Owner declaration before design, from business impact [5]; rating by the weakest subsystem, no fractional ratings, and outcome-based confirmation tests [3]; recovery objectives declared by the organization and verified by exercise [8, 9].

**How presets get values.** Preset promise values are set only by the validation programme ([`VALIDATION.md`](VALIDATION.md), E1 and expert critique), frozen before use, and published with a new Rulebook version ([`GOVERNANCE.md`](GOVERNANCE.md)). Until then an owner who adopts a preset declares its structure and fills in its promise values; comparability between such fabrics holds for the structure only, and is stated so in the score record.

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
