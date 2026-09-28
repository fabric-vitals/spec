# Fabric Vitals — Related work and positioning (v0.2)

**Status:** Fabric Vitals v0.2 (draft) — a technical proposal for discussion. Not a standard. Rulebook values not yet set.

This file is a fuller version of the paper's section on related work. It records where Fabric Vitals agrees with, borrows from, and differs from existing standards, drafts and practice. Facts about external documents are quoted from the primary texts wherever possible.

## 1. Summary of the landscape

The review behind this proposal covered standards bodies, consortia, vendor documentation, academic and hyperscaler publications, scoring methodology from other fields, and design-classification standards. By category:

| Category | Composite score? | Takeaway for Fabric Vitals | Key sources |
|---|---|---|---|
| Standards bodies (ITU-T, IETF, IEEE) | M.3042 (health index); E.840 (relative benchmark score); G.107 (0–100 R); QoO (0–100, min); SAIN (0–100 container) | Scoring containers and methods exist. **No standardized AI-fabric metric set with semantics.** IEEE supplies counters, and has deprecated PFC frame counters in its YANG. | [1, 2, 3, 4, 5, 6] |
| Consortia and telemetry models (UEC, OCP SAI, SONiC, OpenConfig, IBTA) | None. Only per-component states (SONiC OK / Not OK; OpenConfig HEALTHY/UNHEALTHY) | UEC §6.3 FEC → UCR → MTBPE is the most reusable standardized sub-indicator method (UEC 1.0.3 current). PFC, buffer and RoCE NIC counters lack a vendor-neutral export model. | [7, 8, 9, 10, 11, 12] |
| Vendor implementations | Cisco, NVIDIA NetQ, Nokia EDA, Dell, Juniper DCA | Four patterns: worst-of per device then % healthy; % time meeting threshold; averages and weighted roll-ups; anomalies without an index. None is vendor-neutral or AI-input-based. | [13, 14, 15, 16, 17] |
| Hyperscaler, academic, HPC | ANSC (categorical, simulated); Monet bands (called "qualitative") | "Health" means pass/fail gates, operator thresholds and localization. The network share of job disruption depends on the deployment. | [18, 19, 20, 21, 22, 23] |
| Scoring methodology outside networking | OECD/JRC, HDI, Apdex, NBI bridges, CIGRE, Opensignal, FICO | Linear and geometric aggregation are compensatory. Safety-oriented indexes use the minimum or permit worst-mode. Uncertainty is kept beside the score, or the score is withheld. | [24, 25, 26, 27, 28, 29] |
| IETF new work (2026) | **LQS**: per-link congestion composite, 0–255, vendor-agnostic, AI/ML CLOS; computation implementation-defined | Major prior art (see §4 below). A candidate D3/D6 input. Not a fabric health score. | [30, 31] |
| Design-classification standards | None (they are classes, not scores) | Ladder vocabulary; owner declaration before design; lowest-subsystem rule; outcome-based confirmation. **None classes AI fabrics.** | [32, 33, 34, 35] |

**Positioning.** Fabric Vitals is a **new combination of existing pieces**, not a new category:
- M.3042's health-index concept;
- the minimum aggregation used by QoO and M.3042's inner indexes;
- SAIN's −1 value and mandatory symptoms;
- withholding precedents from FICO and Apdex;
- facility-standard class declaration;
- UEC's link-reliability method.

What is new is the combination with AI-fabric inputs, a Rulebook shared by every fabric, a spec sheet declared per fabric (with class presets), reference-first normalization and bounded health. Section 6 explains why this differs from the common metric-checklist view.

## 2. Mapping Fabric Vitals onto ITU-T M.3042 (03/2025) [1]

M.3042 is the principal prior work. Fabric Vitals is a separately named method, not an M.3042 profile. The mapping below lets readers familiar with M.3042 see exactly where the two agree and differ. The M.3042 facts are taken from a reading of its full text, including the appendices.

| Element | M.3042 | Fabric Vitals | Agreement / difference |
|---|---|---|---|
| Object | "A single summary indicator expressed in quantitative terms indicating the degree of communication network health" (§3.2.2) | A single headline confirming conformance of an AI fabric to its declared class | Same concept; different domain and definition of health |
| Scope | Operator public networks and industry private networks; worked examples are 5G core and NFV | AI back-end scale-out fabrics (v0.2) | Different domain |
| Level 1 | T = w1K1 + w2K2 + w3K3 + w4K4; "the definition of the weights for T is outside the scope of this Recommendation" (§7.1) | Headline = min over vital lower bounds, capped by critical conditions | **Differs.** Fabric Vitals is non-compensatory across vitals and needs no weights. |
| Level 2 | Four indexes: "availability, reliability, security and maintainability" (§6.2); weighted sums of level 3 (§7.2) | D1–D7 | D1 ≈ availability. D2 and D5 ≈ reliability. Maintainability → spec sheet (resilience promise and recovery objective), conformance tests. **Security excluded** (excluded to keep the method focused on fabric health). |
| Level 3 | 21 indexes. **8 take the minimum across NE types**: RUQR, NAR, NPQR, NEFRR, network toughness, NRPR, CERRDRPR, RRCMCR (§9.2–9.3), e.g. "RUQR score = min RUQRi" (§9.2.1). The other 13 are weighted sums. | Within-vital aggregation: capacity-weighted share over the designed denominator, worst entity reported | **Same spirit** as M.3042's inner minimum (non-compensatory across element types). Fabric Vitals weights by capacity share, not type. |
| Level 4 | Scenario-specific indexes | Metrics M01–M42 ([`METRICS.md`](METRICS.md)) | Analogous |
| Normalization | Min-max scaling clamped to [qmin, qmax] (§7.3) | Reference-anchored value functions (SPEC §5) | **Differs.** Fabric Vitals anchors to pre-registered references, not operator-chosen limits. |
| Non-compensatory devices | Only the level-3 minimum. No veto, cap, override or forced level anywhere. | Minimum across vitals **plus** critical conditions (caps) | Fabric Vitals adds cross-vital non-compensation |
| Health levels | Non-integral App. III: Healthy / Subhealthy / Unhealthy assigned from T, thresholds "determined by operators" | Bands are a display rule with edges T40, published only once calibrated; any earlier bands are labelled ILLUSTRATIVE | Both leave the edges open; Fabric Vitals states how they will be calibrated |
| Weights | Out of scope. Methods listed: Delphi, AHP (App. IV "The results should pass the AHP consistency test"), CV, PCA, entropy (§8.3) | None used (minimum). If a compensatory element is ever adopted, M.3042's elicitation methods apply (T24). | Compatible |
| Evaluation period | "The period can be week, month, quarter and year." (§9.1) | Minutes to daily views (T19) | **Differs**: operational vs periodic assessment |
| Testing | Network toughness measured with chaos engineering (§9.3.2, App. V) | Outcome-based conformance tests; validation programme | Compatible; Fabric Vitals cites M.3042 App. V as precedent |
| Status | ITU-T Recommendation, in force, approved 2025-03-29; no amendment or revision item as of 2026-09-23 [36] | Technical proposal for discussion (v0.2) | — |

## 3. IETF AI-fabric benchmarking drafts: Fabric Health Indicators as Fabric Vitals inputs

**Status.** The drafts are draft-calabria-bmwg-ai-fabric-{terminology, training-bench, inference-bench}, individual Internet-Drafts, not adopted by BMWG [37, 38, 39]. Status on 2026-09-23: all three are -04 individual drafts, which BMWG lists as related drafts [37, 38, 39].

**Scope.** They define Fabric Health Indicators (FHIs) for lab benchmarking and state that "the definition of acceptance criteria or performance requirements is explicitly outside the scope of this Working Group" [37]. The FHI lists differ between the terminology draft and the two methodology drafts.

**Relationship.** Fabric Vitals is **complementary**, and FHIs map to Fabric Vitals inputs as follows:

| FHI (draft) | Fabric Vitals input | Note |
|---|---|---|
| PFC event rate (terminology) | D3, M12/M13 (pause *duration* preferred) | T3 |
| PFC storm occurrence (terminology) | CC2, M14 | |
| ECN marking ratio (terminology) | D3, M15 | Method-only reference T1 |
| Packet loss rate (terminology) | D3, M10/M11; CC3 | T14 |
| Buffer occupancy P99 (terminology) | D3, M19/M20 | T9 |
| Retransmission rate (terminology) | D3, M18 | T4 |
| Link flap count (training-bench) | D5, M32 | T8, T21 |
| CRC/FCS errors (both methodology drafts) | D5, M31 | |
| FEC error rate / post-FEC BER (inference-bench) | D5, M28/M30 | T37 budget. The draft's "< 1e-12 post-FEC BER" is an indicative range, "not pass/fail criteria" (§4.4), so it is **not** used as a reference. |
| FIB / route convergence time (training-bench) | D2, M45; recovery objective S11 (T33) | Named explicitly in v0.2 |
| BGP/OSPF stability (inference-bench) | D1, M02, M44 | Routing stability named explicitly in v0.2 |
| NIC QP state (inference-bench) | D3 / D1, NIC boundary rule (SPEC §4.2) | Needs cross-host correlation |
| Switch CPU / memory utilization (methodology drafts) | Not a vital. At most D1 via component health (M05) where it affects forwarding. | Device health ≠ fabric health |
| Power consumption (training-bench) | Out of scope | |
| GPU–NIC PCIe bandwidth (inference-bench, "contextual") | Out of the scored path; attribution input (SPEC §4.2) | Host-side |
| JCT Ratio, BusBW (training-bench App. B) | Validation (M40); D7 (M38) | Non-normative values are not used as references |

**Proposed collaboration**:
- FHIs as named inputs to Fabric Vitals;
- the drafts' benchmarking methodology as a basis for the commissioning test suite (T34);
- a shared vocabulary.

Fabric Vitals uses "Score" to avoid overloading "Indicator".

## 4. The Link Quality Score draft as a Fabric Vitals input [30]

| LQS element | Fabric Vitals use | Condition |
|---|---|---|
| Per-link LQS (0–255) | Derived metric feeding D3 (congestion) and D6 (effective capacity) as a per-link value, capacity-weighted | Only where the implementation follows the draft's RECOMMENDED Appendix A pipeline. Otherwise semantic trust is lowered, per the draft's own comparability caveat (§5.2). |
| Congestion Level (CL, 0–7) | Anomaly evidence (SPEC §5) | — |
| "Healthy" range 192–254 | **Not adopted as a reference.** It is defined for load balancing, is unvalidated as a health reference, and comes from a single-vendor proposal (single-vendor values are usable only as declared references for their own technology). | — |
| Monotonicity requirement (§5.2) | Same property as Fabric Vitals test E9 | — |
| Hysteresis states (HEALTHY / DEGRADED / CONGESTED / CRITICAL; App. A.6) | Informs T17/T18 design for congestion conditions | Not adopted as values |

## 5. Other precedents

- **SAIN (RFC 9417, Informational; RFC 9418, Standards Track)** [5, 40]:
  - health score range −1..100, where −1 is "no value could be computed";
  - "a non-maximal score must always be explained by one or more symptoms" (RFC 9417 §2);
  - the calculation is left to implementers, and RFC 9418's worked example is additive.

  Fabric Vitals's UNSCORABLE and binding-reason rules conform, and its vitals can be expressed as SAIN subservices.
- **QoO (draft-ietf-ippm-qoo, WG draft in the RFC Editor queue, not an RFC)** [4]. A 0–100 score as the minimum over sub-scores with application-profile thresholds. Fabric Vitals follows the minimum and profiles.
- **Uptime Tier Standard: Topology (2018)** [33]:
  - network excluded ("independent of the IT systems operating within the site");
  - "The site's Tier rating is not the average of the ratings … The site's Tier rating is the lowest of the individual subsystem ratings";
  - "there are no partial or fractional Tier ratings";
  - "Compliance … is measured by outcome-based confirmation tests".

  Fabric Vitals borrows the lowest-subsystem rule for the verified class and the confirmation-test model.
- **ANSI/BICSI 002** [35, 41]. Network Infrastructure classes N0–N4 and Cable Plant classes C0–C4. The owner declares the class before design: "required performance levels of availability and reliability should be defined, prior to the start or formalization of the design". The N-class tactics are paywalled and were not consulted. The Fabric Vitals class scheme is a proposal derived from the public overview, not from those tables.
- **ANSI/TIA-942-C (2024)** [32]. Rated-1..4. Rated-4 "has redundant capacity components, active redundant distribution paths to serve the equipment, and protection against single failure scenarios". Covers telecommunications cabling and spaces only.
- **EN 50600-2-4 / ISO/IEC TS 22237-5** [34, 42]. Availability Class 1–4 for telecommunications cabling. The requirement text is paywalled; per-class wording comes from secondary sources.
- **OCP MRC 1.0 specification** (Rev 1.0, 2026-03-21; joint contribution from AMD, Broadcom, Intel, Microsoft, NVIDIA and OpenAI) [43]. It defines a per-path health state machine: GOOD / DENIED / SKIP / ASSUMED_BAD, with "Recovery is implementation-defined" (§9.3.1). It also defines a controller API that "exposes telemetry and controls for integration with monitoring and orchestration agents" (§3.4). It defines no score and no numeric thresholds. Relevance: MRC path states are candidate D1/D2 evidence on MRC fabrics.
- **OCP ESUN Network Operator Requirements, Base Rev 1.0** (2026-02-09; Meta, Microsoft authors) [44]. It treats resilience as a capability: "Resilience is required in these networks to deal with link level and path level failures." (§5.3). The capability is link-level retry, yes or no. It defines no health criteria. Relevance: scale-up fabrics, which v0.2 deliberately excludes (its scope is back-end scale-out).
- **ISO 22301 / ISO/IEC 27031:2025** [45, 46]. Recovery objectives are declared by the organization and verified by exercise. This is the model for T33.

## 6. Why not a metric checklist?

A common way to describe AI-fabric health is a checklist of metrics: NIC speed, bisection bandwidth, oversubscription, tail latency, loss, ECN and PFC activity, link utilization, job completion time (JCT) and, for inference, tokens per second. The IETF benchmarking drafts state this view for the lab. For training, "the backend network fabric determines Job Completion Time (JCT), training throughput, and accelerator utilization" [37]; for inference, the fabric determines time to first token, inter-token latency "and aggregate throughput in tokens per second (TPS)" [38]. These metrics are useful, and Fabric Vitals uses many of them as inputs (§3). A checklist on its own, however, has five gaps.

| Gap in the checklist view | What Fabric Vitals does instead |
|---|---|
| **It gives no verdict.** A list of numbers does not say whether the fabric is healthy. The benchmarking drafts themselves leave "acceptance criteria or performance requirements" out of scope [37]. | One verdict, the Vitals Score with its band, explained by its binding reason and contributors ([`SPEC.md`](SPEC.md) §6, §11). |
| **It mixes build with operation.** NIC speed, bisection bandwidth and oversubscription describe how the fabric was built; loss, pauses and delay describe how it is running. | The build is declared on the spec sheet and checked by the conformance check; operation is scored by the vitals against the spec sheet ([`SPEC_SHEET.md`](SPEC_SHEET.md) §4). |
| **It judges design choices universally.** A checklist implies that more bisection or less oversubscription is always healthier. But rail-only fabrics are meant to lack any-to-any paths [47], and one open design states that "no redundancy is assumed or required" [48]. | Each fabric is judged against its own declared promises; comparisons hold only within a class preset or between identical spec sheets ([`SPEC.md`](SPEC.md) §12). |
| **It counts workload performance.** JCT and tokens per second depend on accelerators, software, models and scheduling as well as the network. One collective-library error code covers GPU crashes, network disconnection, out-of-memory and user code [49]. | Only network-attributable evidence is scored. Job signals enter only after attribution to a network element; JCT ratio is used for validation only (M40) ([`SPEC.md`](SPEC.md) §4.2). |
| **It has no rule for missing data.** Unmonitored links simply drop out of the list. | Unmeasured capacity counts as unknown, never healthy; below the coverage floor the result is UNSCORABLE with a list of the missing telemetry ([`SPEC.md`](SPEC.md) §8). |

## References

1. ITU-T Study Group 2. "Recommendation ITU-T M.3042: Framework of communication network health evaluation". ITU-T, March 2025. https://www.itu.int/rec/T-REC-M.3042 (accessed 2026-09-23).
2. ITU-T Study Group 12. "Recommendation ITU-T E.840: Statistical framework for end-to-end network-performance benchmark scoring and ranking". ITU-T, June 2018. https://www.itu.int/rec/T-REC-E.840 (accessed 2026-09-23).
3. ITU-T Study Group 12. "Recommendation ITU-T G.107: The E-model: a computational model for use in transmission planning". ITU-T, June 2015. https://www.itu.int/rec/T-REC-G.107 (accessed 2026-09-23).
4. B. I. T. Monclair, M. Olden, I. Kunze (Ed.). "Quality of Outcome (QoO)" (draft-ietf-ippm-qoo-11). IETF IPPM Working Group, May 2026. Working-group Internet-Draft in the RFC Editor queue; not yet an RFC. https://datatracker.ietf.org/doc/draft-ietf-ippm-qoo/ (accessed 2026-09-23).
5. B. Claise, J. Quilbeuf, D. Lopez, D. Voyer, T. Arumugam. "Service Assurance for Intent-Based Networking Architecture" (RFC 9417). IETF, July 2023. Informational. https://www.rfc-editor.org/rfc/rfc9417 (accessed 2026-09-23).
6. IEEE 802.3 Working Group. "IEEE Std 802.3.2-2025, Ethernet YANG Data Model Definitions". IEEE, approved September 2025. https://standards.ieee.org/ieee/802.3.2/11245/ (accessed 2026-09-23).
7. Ultra Ethernet Consortium. "Ultra Ethernet Specification", version 1.0.2. UEC, January 2026. https://ultraethernet.org/wp-content/uploads/sites/20/2026/01/UE-Specification-1.0.2-1.pdf (accessed 2026-09-23).
8. Ultra Ethernet Consortium. "Ultra Ethernet Specification", version 1.0.3. UEC, July 2026. https://ultraethernet.org/wp-content/uploads/sites/20/2026/08/UE-Specification-1.0.3.pdf (accessed 2026-09-23).
9. Open Compute Project SAI project. "Switch Abstraction Interface headers" (saiport.h, saiqueue.h, saibuffer.h), API version 1.19.0. GitHub, September 2026. https://github.com/opencomputeproject/SAI/tree/master/inc (accessed 2026-09-23).
10. K. Liu, J. Chen. "SONiC System Health Monitor high-level design", rev. 0.2. SONiC project, GitHub, undated. https://github.com/sonic-net/SONiC/blob/master/doc/system_health_monitoring/system-health-HLD.md (accessed 2026-09-23).
11. OpenConfig. "openconfig/public: YANG models" (release/models; openconfig-qos revision 2026-04-30). GitHub, September 2026. https://github.com/openconfig/public (accessed 2026-09-28).
12. Linux kernel. RDMA driver sources (mlx5 counters.c, bnxt_re hw_counters.c, irdma verbs.c, ionic ionic_hw_stats.c). Linux source tree, master branch (July 2026). https://github.com/torvalds/linux/tree/master/drivers/infiniband/hw (accessed 2026-09-23).
13. Cisco. "Monitor and Troubleshoot Network Health". Cisco Catalyst Assurance User Guide 3.1.x, December 2025. Vendor documentation. https://www.cisco.com/c/en/us/td/docs/cloud-systems-management/network-automation-and-management/catalyst-center-assurance/3-1-x/b_cisco_catalyst_assurance_3_1_x_ug/b_cisco_catalyst_assurance_3_1_x_ug_chapter_0110.html (accessed 2026-09-23).
14. Juniper Networks. "Service Level Expectations Overview". Juniper Data Center Assurance user guide. Vendor documentation. https://www.juniper.net/documentation/us/en/software/juniper-data-center-assurance/user-guide/topics/concept/juniper-data-center-assurance-sle-overview.html (accessed 2026-09-23).
15. NVIDIA. "Validate Overall Network Health". Cumulus NetQ 4.11 documentation, 2026. Vendor documentation. https://docs.nvidia.com/networking-ethernet-software/cumulus-netq-411/Validate-Operations/Validate-Overall-Network-Health (accessed 2026-09-23).
16. Nokia. "Units of automation". Nokia EDA documentation, release 25.8. Vendor documentation. https://docs.eda.dev/25.8/getting-started/units-of-automation/ (accessed 2026-09-23).
17. Dell Technologies. "Monitoring SFM and the SONiC switches". SmartFabric Manager for SONiC User Guide, release 1.0.0. Vendor documentation. https://www.dell.com/support/manuals/en-us/smartfabric-manager-for-sonic/sfm-100-user-guide-pub/monitoring-sfm-and-the-sonic-switches?guid=guid-2f01bcd7-0e79-49c3-ac38-d4da8018bd13&lang=en-us (accessed 2026-09-23).
18. Y. Xiong, Y. Jiang, Z. Yang, L. Qu et al. (Microsoft). "SuperBench: Improving Cloud AI Infrastructure Reliability with Proactive Validation". USENIX ATC 2024, July 2024. https://www.usenix.org/system/files/atc24-xiong.pdf (accessed 2026-09-23).
19. A. Kokolis, M. Kuchnik, J. Hoffman et al. (FAIR at Meta). "Revisiting Reliability in Large-Scale Machine Learning Research Clusters". IEEE HPCA 2025, February 2025. https://arxiv.org/pdf/2410.21680 (accessed 2026-09-23).
20. M. Gaikwad, A. Gandhi (Microsoft). "ANSC: Probabilistic Capacity Health Scoring for Datacenter-Scale Reliability". arXiv 2508.16119v1, August 2025. Preprint; simulation only. https://arxiv.org/pdf/2508.16119 (accessed 2026-09-23).
21. S. Jha, A. Patke, J. Brandt, A. Gentile et al. "Measuring Congestion in High-Performance Datacenter Interconnects". USENIX NSDI 2020, February 2020. https://www.usenix.org/system/files/nsdi20-paper-jha.pdf (accessed 2026-09-23).
22. J. Araujo, A. Chow, M. Handley, J. Padhye et al. (49 authors; OpenAI, Microsoft, AMD, Broadcom, NVIDIA). "Resilient AI Supercomputer Networking using MRC and SRv6". arXiv 2605.04333v1, May 2026. Preprint; results depend on its multipath transport. https://arxiv.org/abs/2605.04333 (accessed 2026-09-23).
23. C. Guo, L. Yuan, D. Xiang et al. (Microsoft). "Pingmesh: A Large-Scale System for Data Center Network Latency Measurement and Analysis". ACM SIGCOMM 2015, August 2015. https://conferences.sigcomm.org/sigcomm/2015/pdf/papers/p139.pdf (accessed 2026-09-23).
24. OECD and European Commission Joint Research Centre (M. Nardo, M. Saisana, A. Saltelli, S. Tarantola, A. Hoffmann, E. Giovannini). "Handbook on Constructing Composite Indicators: Methodology and User Guide". OECD Publishing, 2008. https://www.oecd.org/content/dam/oecd/en/publications/reports/2008/08/handbook-on-constructing-composite-indicators-methodology-and-user-guide_g1gh9301/9789264043466-en.pdf (accessed 2026-09-23).
25. J. Klugman, F. Rodríguez, H.-J. Choi. "The HDI 2010: New Controversies, Old Critiques". UNDP Human Development Research Paper 2011/01, April 2011. https://hdr.undp.org/system/files/documents/hdrp201101.pdf (accessed 2026-09-23).
26. Apdex Alliance. "Application Performance Index — Apdex Technical Specification", version 1.1. January 2007. https://www.apdex.org/wp-content/uploads/2020/09/ApdexTechnicalSpecificationV11_000.pdf (accessed 2026-09-23).
27. US Federal Highway Administration. "23 CFR 490.409: Calculation of National performance management measures for assessing bridge condition". US Code of Federal Regulations (current text via the Legal Information Institute). https://www.law.cornell.edu/cfr/text/23/490.409 (accessed 2026-09-23).
28. CIGRE Working Group B3.48. "Asset health indices for equipment in existing substations" (Technical Brochure 858, summary). ELECTRA No. 320, February 2022. Summary page only. https://electra.cigre.org/320-february-2022/technical-brochures/asset-health-indices-for-equipment-in-existing-substations.html (accessed 2026-09-23).
29. J. Gaskin. "FICO Fact: Does FICO's Minimum Scoring Criteria Limit Consumers' Access to Credit?". FICO, October 2021. Score owner's own publication. https://www.fico.com/blogs/fico-fact-does-ficos-minimum-scoring-criteria-limit-consumers-access-credit (accessed 2026-09-23).
30. S. P. K. Pasalapudi, V. P. Beeram. "A YANG Data Model for Link Quality Telemetry in CLOS Data Center Fabrics" (draft-praveen-fann-lq-telemetry-info-00). IETF, July 2026. Individual Internet-Draft; work in progress. https://datatracker.ietf.org/doc/draft-praveen-fann-lq-telemetry-info/ (accessed 2026-09-23).
31. S. P. K. Pasalapudi, V. P. Beeram. "A UDP Transport Binding for Link Quality Telemetry in CLOS Data Center Fabrics" (draft-praveen-fann-lq-telemetry-udp-00). IETF, July 2026. Individual Internet-Draft; work in progress. https://datatracker.ietf.org/doc/draft-praveen-fann-lq-telemetry-udp/ (accessed 2026-09-23).
32. TIA. "ANSI/TIA-942: The Global Data Center Standard" (brochure describing TIA-942-C). Telecommunications Industry Association, April 2024. Brochure, not the standard text. https://tiaonline.org/wp-content/uploads/2024/05/Data-Centers-Brochure_040124.pdf (accessed 2026-09-23).
33. Uptime Institute. "Data Center Site Infrastructure Tier Standard: Topology". Uptime Institute, 2018 (effective October 2018). https://www.gpxglobal.net/wp-content/uploads/2018/11/Uptime-Tier-Standard-Topology.pdf (accessed 2026-09-23).
34. ISO/IEC JTC 1. "ISO/IEC TS 22237-5:2018 Data centre facilities and infrastructures — Part 5: Telecommunications cabling infrastructure". ISO/IEC, May 2018. Public preview only. https://cdn.standards.iteh.ai/samples/73012/f90c18a9cfdf49e2aa38e45fec4e420d/ISO-IEC-TS-22237-5-2018.pdf (accessed 2026-09-23).
35. BICSI. "An Overview of the ANSI/BICSI 002-2019 Data Center Availability Class Methodology". BICSI, 2019. Public overview, not the standard text. https://www.bicsi.org/docs/default-source/publications/002-2019-methodology.pdf (accessed 2026-09-23).
36. ITU-T Study Group 2. Work programme for Question 6/2 (2025–2028). ITU-T, retrieved September 2026. No amendment or revision of M.3042 listed. https://www.itu.int/ITU-T/workprog/wp_search.aspx?isn_sp=9677&isn_sg=9678&isn_wp=11193&isn_qu=10749 (accessed 2026-09-23).
37. F. Calabria, C. Pignataro, Q. Wu, G. Fioccola, S. Reddy. "Benchmarking Methodology for AI Training Network Fabrics" (draft-calabria-bmwg-ai-fabric-training-bench-04). IETF, August 2026. Individual Internet-Draft, not adopted by a working group; work in progress. https://datatracker.ietf.org/doc/draft-calabria-bmwg-ai-fabric-training-bench/ (accessed 2026-09-28).
38. F. Calabria, C. Pignataro, Q. Wu, G. Fioccola, S. Reddy. "Benchmarking Methodology for AI Inference Serving Network Fabrics" (draft-calabria-bmwg-ai-fabric-inference-bench-04). IETF, August 2026. Individual Internet-Draft, not adopted by a working group; work in progress. https://datatracker.ietf.org/doc/draft-calabria-bmwg-ai-fabric-inference-bench/ (accessed 2026-09-28).
39. F. Calabria, C. Pignataro, Q. Wu, G. Fioccola, S. Reddy. "Benchmarking Terminology for AI Network Fabrics" (draft-calabria-bmwg-ai-fabric-terminology-04). IETF, August 2026. Individual Internet-Draft, not adopted by a working group; work in progress. https://datatracker.ietf.org/doc/draft-calabria-bmwg-ai-fabric-terminology/ (accessed 2026-09-28).
40. B. Claise, J. Quilbeuf, P. Lucente, P. Fasano, T. Arumugam. "A YANG Data Model for Service Assurance" (RFC 9418). IETF, July 2023. Proposed Standard. https://www.rfc-editor.org/rfc/rfc9418 (accessed 2026-09-23).
41. BICSI. "ANSI/BICSI 002-2014, Data Center Design and Implementation Best Practices" (demonstration version). BICSI, 2014. Superseded edition; sample pages only. https://www.bicsi.org/docs/default-source/publications/bicsi_002_14_sample.pdf (accessed 2026-09-23).
42. CommScope. "Data Center Cabling Design Fundamentals" (white paper WP-321067-EU). 2015. Vendor white paper. https://www.commscope.com/globalassets/digizuite/3511-wp-321067-eu-data-center-cabling-design-fundamentals.pdf (accessed 2026-09-23).
43. R. Sohan, E. Spada, E. Davis, M. Handley et al. (joint contribution of AMD, Broadcom, Intel, Microsoft, NVIDIA and OpenAI). "Multipath Reliable Connection (MRC) Specification", revision 1.0. Open Compute Project, March 2026. https://www.opencompute.org/documents/ocp-mrc-1-0-pdf (accessed 2026-09-23).
44. M. Wadekar, R. Sankaran (OCP Networking Project, ESUN workstream). "OCP ESUN Network Operator Requirements — Base Specification", revision 1.0. Open Compute Project, February 2026. https://www.opencompute.org/documents/ocp-esun-network-operator-requirements-base-specification-rev-1-0-final-pdf (accessed 2026-09-23).
45. ISO/TC 292. "ISO 22301:2019 Security and resilience — Business continuity management systems — Requirements". ISO, October 2019. Public preview only. https://cdn.standards.iteh.ai/samples/75106/5e083fd428f54407a6aae14cb574019c/ISO-22301-2019.pdf (accessed 2026-09-23).
46. ISO/IEC JTC 1/SC 27. "ISO/IEC 27031:2025 Cybersecurity — ICT readiness for business continuity". ISO/IEC, 2025. Public preview only. https://cdn.standards.iteh.ai/samples/80975/8e844992be7e4ec88c4c364d22e73a4f/ISO-IEC-27031-2025.pdf (accessed 2026-09-23).
47. W. Wang, M. Ghobadi, K. Shakeri, Y. Zhang, N. Hasani. "Rail-only: A Low-Cost High-Performance Network for Training LLMs with Trillion Parameters". arXiv 2307.12169v5, July 2023 (v5 September 2024). Preprint. https://arxiv.org/abs/2307.12169 (accessed 2026-09-23).
48. L. D. Lamb, L. Staley, J. Mora, A. Raman. "Open Pod Group for M xPUs (OPG-M) System Architecture". Open Compute Project, January 2026. Contributor document. https://www.opencompute.org/documents/opg-m-system-architecture-final-14-january-2026-pdf (accessed 2026-09-23).
49. J. Dong, B. Luo, J. Zhang et al. (Alibaba, HKUST). "Enhancing Large-Scale AI Training Efficiency: The C4 Solution for Real-Time Anomaly Detection and Communication Optimization". IEEE HPCA 2025, March 2025. https://arxiv.org/abs/2406.04594 (accessed 2026-09-23).
