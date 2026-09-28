# Fabric Vitals — Specification v0.2

**Status:** Fabric Vitals v0.2 (draft) — a technical proposal for discussion. Not a standard. Rulebook values not yet set.

This document specifies the Fabric Vitals method for AI data-center fabrics precisely enough for independent implementations to produce identical results, once a Rulebook with values exists. The method has two inputs:
- the **Rulebook** ([`RULEBOOK.md`](RULEBOOK.md)): how every fabric is measured and judged, identical for all fabrics (parameters T1–T40);
- the **Fabric Spec Sheet** ([`SPEC_SHEET.md`](SPEC_SHEET.md)): what this fabric promises, declared by its owner before measurement (fields S1–S23), either as a published **class preset** or as a custom sheet.

Metric IDs (M01–M45) refer to [`METRICS.md`](METRICS.md). Rationale and evidence are summarized here, and positioning is in [`RELATED_WORK.md`](RELATED_WORK.md).

## 0. Conventions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "NOT RECOMMENDED", "MAY" and "OPTIONAL" in this document are to be interpreted as described in BCP 14 (RFC 2119, RFC 8174) when, and only when, they appear in all capitals, as shown here.

Terms used throughout:
- **Numbers.** Numbers marked ILLUSTRATIVE are invented to show a mechanism and are not proposed values. "VALUE NOT SET" marks a Rulebook parameter whose value has not been defined. "VALUE DECLARED BY OWNER" marks a spec-sheet parameter.
- **Implementation.** Software that computes Vitals Scores.
- **Operator.** The party that runs the fabric.
- **Owner.** The party that declares the fabric's spec sheet. It may be the same as the operator.

## 1. Terminology

| Term | Definition |
|---|---|
| **Fabric Vitals (FV)** | The method specified here. |
| **Vitals Score** | The headline number: an integer 0–100, or UNSCORABLE. "FV score" is an acceptable short form. |
| **Vital** | One of the seven dimensions D1–D7 (§4). Each vital has a value from 0 to 100: the fraction of the declared promise being delivered (§4.1). |
| **Rulebook** | The versioned, pre-registered register of how every fabric is measured and judged (e.g. RB-0.2). |
| **Fabric Spec Sheet** | The versioned declaration of what one fabric promises: purpose, build, resilience promise, availability target, performance envelope, required tests and class (§2). |
| **Class preset** | A published spec sheet (R1, R2, R3) with structural predicates and promise fields (§2.2). Classes are design patterns ordered by redundancy, not quality tiers. |
| **Custom spec sheet** | A spec sheet that is not an unchanged preset. |
| **Fabric scope** | The set of switches, links and NIC ports covered by a spec sheet, declared with its inventory (S1). v0.2 covers back-end scale-out fabrics (§2.5). |
| **Scoring scope** | The unit within which jobs run (a pod or scalable unit), declared on the spec sheet (S23). Each scoring scope receives its own Vitals Score (§2.6). |
| **Verified class** | The most redundant class preset whose structural predicates all hold on the fabric as built (§3). |
| **Conformance status** | CONFORMANT, NON-CONFORMANT (with the failed predicates listed), or NOT ASSESSED (§3). |
| **Confirmed score** | The Vitals Score computed with unmeasured capacity treated as worst: the lower bound. |
| **Upper bound** | The same computation with unmeasured capacity treated as best. The confirmed score and upper bound form the score's **range**. |
| **Coverage** | For a vital or a critical condition's evidence set, the share of *declared* capacity for which the required telemetry is observed within the grace period. |
| **Critical condition** | A named state (CC1–CC6) that caps the Vitals Score (§7). |
| **Binding reason** | The vital or critical condition that sets the Vitals Score, tagged DESIGN SHORTFALL, OPERATIONAL or PLANNED (§7). |
| **Declared maintenance window** | A maintenance period declared in advance as a versioned event (§9.3). |
| **Day-One Set** | The smallest set of vitals, counters and probes that yields a valid Vitals Score (§13). |
| **UNSCORABLE** | The result when coverage is below the coverage floor. It means "conformance not confirmed" (§8.4). |
| **Score band** | The display colour of a result: green, amber, red or grey, set by the band edges T40 (§11.2). |
| **Availability** | The share of scoring windows in which the fabric was healthy (§9.2). |

## 2. The Fabric Spec Sheet

### 2.1 Fields

The spec sheet has the fields S1–S23 listed in [`SPEC_SHEET.md`](SPEC_SHEET.md) §2, in seven parts:
- **identity:** fabric scope and inventory (S1); purpose and workload profile (S2); scoring scope (S23);
- **build:** topology (S3), host attachment (S4), uplinks and subscription ratio (S5), planes (S6), transport and load distribution (S7), lossless-transport configuration (S8), physical diversity (S9);
- **resilience promise:** failures ridden through without capacity loss (S10); recovery objective, including routing convergence time (S11);
- **availability target** (S12);
- **performance envelope:** bandwidth per accelerator (S13), collective bandwidth reference (S14), tail-delay budget (S15), loss budget (S16), pause budget (S17), physical-layer budgets (S18);
- **required tests and telemetry:** synthetic collectives and conformance tests (S19), telemetry profile (S20);
- **class and version:** declared class (S21), spec-sheet version (S22).

Every vital checks one or more fields. The mapping is normative and is given in [`SPEC_SHEET.md`](SPEC_SHEET.md) §4.

### 2.2 Class presets

1. **Status.** The class scheme is **proposed and open for critique**. It is derived from public sources on facility tiers and availability classes [1, 2, 3, 4, 5, 6] and from published AI-fabric designs [7, 8, 9]. It is not derived from the requirement tables of any paywalled standard.
2. **Shape.** There are three presets, each a complete spec sheet with structural predicates (S3–S9, S19, S20) and promise fields (S10–S18). They are **design patterns ordered by redundancy, not quality tiers**; a fabric that keeps the promises of its class is healthy whichever class it is:
   - **R1 Rail-optimized, single-homed:** the most common training design in published reference designs today; recovery by checkpoint restart [8, 10, 11];
   - **R2 Dual-homed:** rides through a leaf failure, or a bounded number of uplink failures per rail, without losing capacity [8];
   - **R3 Multi-plane, sprayed, tested:** independent planes, packet spraying, continuous synthetic collective tests [9].

   The evidence for each pattern is given in [`SPEC_SHEET.md`](SPEC_SHEET.md) §5.
3. **Values.** A preset's name fixes its structural pattern (single-homed, dual-homed, multi-plane with spraying and required D7). Its numeric values are parameter T32 and the preset columns of T3, T4, T5, T10, T12, T26 and T33. They are PROPOSED and not set, except the physical-layer budgets (S18), where the IEEE budget applies (T37).
4. **Why failure consequence rather than path counts.** Presets are expressed as failure consequence. Some AI designs attach each NIC to a single rail leaf by design [10, 11]. One open design states that "no redundancy is assumed or required" [12]. AI resilience comes instead from planes, dual attachment and designed spare capacity [7, 8, 9].
5. **Custom sheets.** An owner **MAY** declare a custom spec sheet. A custom sheet **MUST NOT** carry a preset's name (§12).
6. **Standards floors.** Where a field has a standard behind it (today S18), a declared value **MAY** be stricter than the standard and **MUST NOT** be laxer.

### 2.3 Lossless-transport configuration consistency

1. For every lossless traffic class, the spec sheet **MUST** declare (S8) the PFC-enabled priorities, the ECN marking configuration, the DSCP-to-traffic-class mapping and the MTU, for switches and NICs.
2. The conformance check **MUST** evaluate predicate P-CFG: on every job-bearing path, the running configuration of every switch hop and both NICs matches S8 (§3).
3. Where running configuration is observable during operation, a mismatch **MUST** be reported as D3 evidence (M43) and as a mandatory finding tagged OPERATIONAL. It lowers D3 for the affected capacity through the value function (T25).
4. **Rationale.** Configuration errors are a documented cause of failure in lossless RDMA fabrics: Meta reports congestion drops "observed mostly due to misconfiguration" [7], and Microsoft checks "if the running configurations of the switches and the servers are the same as their desired configurations" after an incident caused by a buffer misconfiguration [13]. Lossless operation needs NICs and switches to agree on classification [13]. A mismatch is not a critical condition in v0.2, because its harmful consequences are already capped by CC1–CC3 (§7).

### 2.4 Declaration

1. The owner **MUST** declare a spec sheet before any measurement window counts toward a score.
2. The choice of class **SHOULD** be derived from an assessment of the impact of downtime and of the allowable disruption per failure class, following the public BICSI and ISO 22301 practice [4, 5].
3. The spec sheet **MUST** be signed, dated and versioned (S22), and **MUST** name the Rulebook version it is declared against.
4. Any change to a field **MUST** create a new spec-sheet version. Scores under different spec-sheet versions form separate series (§12).

### 2.5 Scope and deliberate exclusions

1. v0.2 covers **back-end scale-out fabrics** carrying accelerator traffic.
2. **Security** is deliberately excluded (ITU-T M.3042 includes it; Fabric Vitals keeps to fabric health).
3. **Roadmap of excluded areas.** The following are out of scope in v0.x and are candidate future profiles, in order of likely demand:
   1. front-end and inference-serving networks;
   2. storage and checkpoint traffic;
   3. scale-up interconnects (NVLink-class, including Ethernet-based scale-up);
   4. multi-tenant isolation.

### 2.6 Scoring scope

1. The spec sheet **MUST** declare one or more **scoring scopes** (S23): the unit within which jobs run, such as a pod or scalable unit.
2. Every vital, every coverage figure and every critical-condition threshold, including the blast-radius threshold T16 and the coverage floor T29, **MUST** be computed within one scoring scope.
3. A fabric with more than one scoring scope **MUST** be reported as the set of scope scores, with their distribution and the **lowest scope** named. An implementation **MUST NOT** publish a single capacity-blended Vitals Score for several scopes.
4. **Rationale.** A job is gated by the slowest transfer inside the unit it runs in [8, 9]; blending a failed pod into a large healthy fabric would reintroduce the averaging the method rejects (§6).

## 3. Conformance check

1. An implementation **MUST** compute the verified class as the most redundant preset whose structural predicates all hold (the lowest-predicate rule, after facility tier practice [2]). Fractional classes **MUST NOT** be reported.
2. The check **MUST** include:
   - (a) **static** evaluation of the declared build (S3–S9) against the discovered topology (e.g. LLDP), the inventory and the running configuration, including P-CFG (§2.3);
   - (b) **computed** residual capacity under the declared tolerated failures (S10).
3. The check **SHOULD** include (c) **outcome-based** controlled-failure or drain tests, measured with the D7 method (T26), with the measured recovery and routing convergence times compared with the recovery objective (S11). These tests **SHOULD** run at commissioning and at the declared cadence `K_conf` (S19). They follow outcome-based confirmation practice [2, 6].
4. The conformance status **MUST** be CONFORMANT, NON-CONFORMANT (with every failed predicate listed), or NOT ASSESSED.
5. **Scoring uses the declared spec sheet.** Vitals and critical conditions **MUST** be evaluated against the **declared** spec sheet, not the verified class. The verified class and the conformance status **MUST** be reported beside the score (§11).
6. **Over-claim rule.** Redundancy that was declared but never built **MUST** count as absent. By the common-currency definition (§4.1), a complete over-claim scores 0 on D2; a partial shortfall scores the delivered fraction. The binding reason is tagged DESIGN SHORTFALL.
7. **Counterfactual.** Whenever the declared class differs from the verified class, the record and any display **MUST** show: "declared Rx, built as Ry; as Ry it would score N", where N is the score recomputed with the verified class's preset promises, and **MUST** name re-declaration as the remedy. The counterfactual is informative; the Vitals Score remains the score against the declared spec sheet.

## 4. Vitals

### 4.1 Common currency and definitions

1. **Every vital is on one scale: the fraction of the declared promise being delivered,** from 0 (none of it) to 100 (all of it), measured against the spec sheet and, where the Rulebook sets the reference, against the Rulebook reference for the declared class.
2. This common currency is what makes the weakest-vital rule (§6) meaningful: equal values in two vitals mean the same share of each promise delivered.
3. It is the design intent behind the value functions (T25) and their anchors (T31) (§5.5). Their shapes remain to be calibrated (E4).

| ID | Vital | Question | Definition | Metrics | Spec-sheet fields checked |
|---|---|---|---|---|---|
| D1 | **Reachability** | Can every endpoint that should reach every other get packets through? | Capacity-weighted share of declared endpoint-pair paths that are control-plane correct (links and sessions up and stable; FIB and cabling match intent) **and** verified in the data plane by active probes. Control-plane evidence includes **routing stability** (session flaps and route churn, M44). | M01–M06, M44 | S1, S3, S4 |
| D2 | **Resilience** | If the next tolerated failure happens, will the fabric still do its job? | The fraction of the **declared resilience promise** available now: remaining redundancy and residual capacity, with declared-but-unbuilt redundancy counted as absent (§3), and measured recovery against the **recovery objective**, including **routing convergence time** (M45) | M07–M09, M45 | S4, S5, S6, S10, S11 |
| D3 | **Congestion and loss** | Is traffic getting through without harmful loss, pausing or congestion spread? | Loss by cause and class against the loss budget; PFC pause-time fraction against the pause budget; storms and deadlock; buffer stress; ECN and CNP against registered commissioning references; NIC transport anomalies; lossless-transport configuration consistency | M10–M22, M43 | S7, S8, S16, S17 |
| D4 | **Delay and tail** | Is the network adding more delay than it should, at the tail? | The profile's tail statistic of probe delay per path class, loaded and unloaded, against the declared tail-delay budget; queue-delay watermarks | M23–M26 | S2, S15 |
| D5 | **Physical link integrity** | Are the links, optics and PHYs healthy? | Distance to the physical-layer budgets (T37 and any declared margin T5); link reliability from FEC statistics (T38); FEC histogram tail; CRC and symbol errors; flaps; optics against module thresholds | M27–M34 | S18 |
| D6 | **Effective capacity** | Is there enough usable bandwidth where traffic goes, spread well? | Peak or percentile utilization within communication phases against declared capacity (S13); imbalance on flow-hash fabrics; plane imbalance on spraying fabrics | M35–M37 | S5, S7, S13 |
| D7 | **AI communication** | Tested the way AI jobs use it, does the fabric perform as promised? | Synthetic-collective bus bandwidth and all-pair RDMA scans on known-good hosts, against the declared collective bandwidth reference | M38, M39 | S14, S19 |

### 4.2 Evidence scope

1. Only network-attributable evidence is in scope:
   - (a) signals originating in switches, NIC ports, NIC transport counters or optics;
   - (b) active measurements that exercise the network independently of tenant compute;
   - (c) the running configuration of switches and NICs, for the consistency check (§2.3).
2. Job-derived signals (step time, job completion, collective-library errors inside tenant jobs) **MUST NOT** enter a vital unless attributed to a network element by a declared attribution method [14, 15]. Raw job signals mix in non-network causes [15, 16].
3. A NIC-local symptom **MUST NOT** lower a fabric-wide vital without cross-host correlation or attribution. Host and NIC-internal causes appear as PFC and ECN symptoms [13, 16].

### 4.3 D7 rules

D7 corroborates the other vitals unless the class requires it. Of the presets, only R3 requires it; a custom spec sheet may require it (S19).

1. Where the spec sheet requires communication testing (S19, predicate P-D7), D7 **MUST** be included in the minimum (§6) and **MUST** follow the method T26. If D7 is not run, it counts as unobserved (§8).
2. Where the spec sheet does not require it, D7 **MUST NOT** enter the minimum. In that case:
   - a D7 result consistent with D1–D6 **SHOULD** raise evidence-quality confidence;
   - a D7 result below its reference while D1–D6 meet theirs **MUST** produce the finding "unexplained communication regression" and **SHOULD** start attribution;
   - attributed evidence lowers the vital of the attributed element.
3. **Footprint.** Synthetic collective tests **MUST** stay within the footprint the Rulebook fixes as part of method M-D7 (T26), values not set:
   - short duration per run (`K_d7dur`);
   - a small reserved set of nodes (`K_d7nodes`), or scheduled gaps between tenant jobs;
   - a frequency bound on `K_cad`.

   The spec sheet declares the footprint used, within those bounds (S19).

## 5. Normalization

1. Every metric **MUST** be judged against a reference that is either registered in the Rulebook or declared on the spec sheet, as the register column "Rulebook / Spec sheet" states ([`RULEBOOK.md`](RULEBOOK.md) §2). Rulebook references fall in one of four categories:
   - **(a) standard exists;**
   - **(b) best practice exists**, graded by authority: consortium specification > multi-vendor community practice > single-operator practice > single-vendor reference design > marketing;
   - **(c) must be defined by Fabric Vitals;**
   - **(d) method only.**
2. A category (b) value from a single vendor or single operator **MAY** be used only as a declared reference for its own technology.
3. For category (d), the reference is produced per fabric by the registered method:
   - (i) declared configuration;
   - (ii) a measurement definition;
   - (iii) a commissioning measurement under the standard test suite (T34) after burn-in (T36);
   - (iv) the value declared on the spec sheet, and the preset acceptance criterion where one exists;
   - (v) re-registration as a versioned event on any configuration or design change.
4. Rolling baselines and peer comparisons (T27) **MAY** be computed. They **MUST NOT** change a vital's value. Their outputs are anomaly findings, triggers for attribution, and flags on evidence-quality confidence. The reason: a learned baseline turns a fabric's current state into its reference [17]. Peer symmetry across planes is valid only where the transport enforces equal per-plane load [9].
5. **Value functions.** Each metric **MUST** pass through a value function mapping to the common currency of §4.1, anchored so that the same states map to the same values in every vital (T31):
   - 100 = the declared promise (or the Rulebook reference for the class) is fully delivered;
   - intermediate values = the fraction of the promise delivered, for example the capacity share that meets it;
   - 0 = none of the promise is delivered; a critical condition on the capacity concerned is at 0.

   Shapes between anchors are T25 (VALUE NOT SET). Value functions **MUST** be monotone: a worse input never yields a higher value.
6. **Utilization** **MUST NOT** be scored as a mean. It is scored as a peak or percentile within communication phases, against declared capacity and failure state [18].
7. **Physical-layer budgets.** These are category (a) (T37) and are used as distance to budget, not as alarm levels:
   - the complete-PHY post-FEC frame loss ratio: 6.2×10⁻¹¹ for 64-octet frames at 200 Gb/s and above, and 6.2×10⁻¹⁰ at 100 Gb/s [19, 20, 21, 22, 23, 24, 25, 26];
   - the PMD pre-FEC BER allocation of 2.4×10⁻⁴ for RS(544,514) PHYs at 50/100G per lane [27, 28].

## 6. Aggregation

1. **Within a vital:**
   - quantities **MUST** be intensive (per link-hour, per GB, fraction of time);
   - entities **MUST** be weighted by capacity share over the **declared** inventory;
   - the worst entity **MUST** be reported alongside the vital value;
   - the specific within-vital rule is part of the value-function definition (T25).
2. **Across vitals:** the Vitals Score **MUST** be the minimum over the confirmed (lower-bound) values of the vitals the spec sheet requires, capped by any active critical condition (§7). No weights are used.
3. **Companions.** With every Vitals Score an implementation **MUST** report:
   - the **breadth indicator**: the number of vitals not delivering their full promise (below 100), out of the number required;
   - the **next-binding vital** and its value;
   - the full vector of vital values.
4. **Why the minimum.** The comparison of aggregation formulas on the masking example (four vitals at 100, one at 10) is in [`SCENARIOS.md`](SCENARIOS.md) §1. Only rules that let the collapsed vital decide the score pass it, and the minimum is the only one of them that needs no weights and no cap constants.
5. **Commensurability.** The minimum assumes commensurability across vitals. Implementations and Rulebooks **SHOULD** treat this assumption as unvalidated until experiment E4 ([`VALIDATION.md`](VALIDATION.md)) reports.

## 7. Critical conditions

| ID | Condition | Evidence | Applies where |
|---|---|---|---|
| CC1 | Partition or black hole | Probe-verified: M04; M01–M03 | Always |
| CC2 | PFC storm or deadlock | M14, M13 | Lossless transport declared (S7) |
| CC3 | Sustained loss on a lossless class | M10, M17; "sustained" is T14 | Lossless transport declared (S7); keyed by transport mode |
| CC4 | Single point of failure on job-bearing capacity | M01 and the declared build | **Only where the spec sheet promises no single point of failure** (S4, S10) |
| CC5 | Redundancy exhausted | For a job-bearing path class: M07–M09 | Relative to the declared tolerance (S10) |
| CC6 | Uncorrectable errors beyond the IEEE budget | On job-bearing links: M28, M30; T37, T38 | Keyed by PHY type (S18) |

1. A condition **MUST** cap the Vitals Score at the cap value (T15) only when the affected share of job-bearing capacity is at least the blast-radius threshold T16. Persistence and hold times are T17.
2. The affected share **MUST** be computed as the observed share in the condition **plus** the unobserved share of that condition's evidence set.
3. A raised condition **MUST** remain raised until the cleared state is positively observed. Loss of telemetry **MUST NOT** clear it.
4. A capping condition **MUST** be reported as the binding reason, tagged DESIGN SHORTFALL (a failed predicate against the declared spec sheet), PLANNED (inside a declared maintenance window, §9.3) or OPERATIONAL (otherwise).
5. Expected behaviour for nineteen representative failures and events (which vitals move, when a condition caps the score, and recovery time scales) is tabulated in [`SCENARIOS.md`](SCENARIOS.md) §2. The table is informative, not normative.

## 8. Coverage, confirmed score and range

### 8.1 Telemetry profile

The declared telemetry profile (S20) lists one row per (entity class, vital, metric). It **MUST** cover the Rulebook minimum for the declared class (T35). Each row gives:
- the metric ID;
- the model path or per-driver mapping;
- the metric type (counter, gauge, watermark, event or histogram);
- the declared sampling interval Δ and resolution requirement (T20);
- the grace period G (T30);
- whether the metric is required for coverage;
- which critical conditions' evidence sets it belongs to.

A metric declared NOT APPLICABLE by a predicate (e.g. CNP without DCQCN) is removed from the coverage denominator. A missing export **MUST NOT** remove a metric from the denominator.

### 8.2 Grace period

For each (entity, metric), let *a* be the age of the latest valid sample at computation time.
1. If a ≤ Δ + G, the slice is **observed**:
   - cumulative counters use the rate over the last completed interval;
   - gauges and watermarks carry the last value forward;
   - event and state streams use the last state, provided a heartbeat or sync arrived within Δ + G.
2. If a > Δ + G, the slice is **unobserved** from t_last + Δ + G onward.
3. Carry-forward **MUST NOT** clear a raised critical condition.
4. A published score **MUST NOT** be revised when late data arrives. A recomputation with a later data cut-off produces a new score record. Counter discontinuities follow RFC 8343 `discontinuity-time` [29].
5. **Property.** Removing telemetry never raises the confirmed score above the value full telemetry would have produced at some time within the preceding G. G = 0 gives the strict property.

### 8.3 Bounded values and the confirmed score

1. For each vital, the implementation **MUST** compute:
   - a **lower bound**, with every unobserved entity or time slice set to 0;
   - an **upper bound**, with every unobserved entity or time slice set to 100.
2. The **Vitals Score is the confirmed score**: the minimum of the lower bounds, capped by critical conditions. It **MUST** be displayed with the upper bound (computed with upper bounds) and the coverage per vital.

### 8.4 Coverage floor and UNSCORABLE

1. If any required vital, or any critical condition's evidence set, has coverage below the coverage floor F (T29), the result **MUST** be UNSCORABLE (−1).
2. UNSCORABLE **MUST** rank below every numeric score in any conformance use and **MUST NOT** be displayed as a pass. The −1 value follows IETF service-assurance practice [30].
3. **Missing-telemetry list.** An UNSCORABLE result **MUST** list exactly which required telemetry is missing, and where: per vital or condition, the entity IDs, the metric IDs, the capacity share below the floor, and for each item whether it is *missing*, *stale beyond grace* or *unsupported by the platform*.

### 8.5 Coupling constraint (T39)

1. For every critical condition *k*, with the coverage floor F_k and the blast-radius threshold T16_k defined over the **same** denominator (the job-bearing capacity of k's evidence set), the Rulebook **MUST** satisfy **F_k + T16_k > 1**.
2. A Rulebook **MAY** relax the constraint for a specific condition only by setting `unobserved_capacity_can_be_critical = true` for that condition, with a written rationale recorded in the Rulebook.
3. **Why.** A fabric is scorable only if its unobserved share u ≤ 1 − F_k. Unobserved capacity alone reaches the threshold only if u ≥ T16_k. Both hold together exactly when F_k + T16_k ≤ 1.
4. **Consequences:**
   - Under the constraint, hiding a region large enough to trigger condition *k* forces coverage below F_k, so the result is UNSCORABLE rather than escaping the cap.
   - If the floor is measured over a denominator D larger than the gate's J, the constraint becomes T16_k > (1 − F_k)·|D|/|J|.
   - Fabrics with thin telemetry will be UNSCORABLE for affected conditions. The missing-telemetry list tells the operator what to add.

### 8.6 Evidence-quality confidence

Implementations **MUST** report evidence-quality confidence per vital and overall. It covers:
- freshness within grace;
- resolution;
- capability (unsupported required metrics also count as unobserved);
- counter integrity;
- semantic trust (driver-specific or device-specific semantics [31, 32]);
- D7 corroboration.

Confidence **MUST NOT** change the Vitals Score. The flag level and the combination rule are T23.

## 9. Temporal behaviour

### 9.1 Windows and trends

1. Within a window, vitals **SHOULD** score the share of time or samples in a good state.
2. Implementations **SHOULD** publish three labelled views: current, rolling and daily. Window lengths are T19.
3. Short catastrophes **MUST** register through critical conditions and paired short and long windows.
4. Decay and hysteresis are per condition class (T18).
5. Trends **MUST** be reported on the full vital vector and the breadth indicator, not on the headline alone.
6. Trends against the fabric's own history are descriptive and **MUST NOT** re-base any reference.

### 9.2 Availability

1. **Definition.** Over a period P, divided into scoring windows of the current-view length (T19), the fabric's **availability** is the share of windows in which:
   - the result is numeric (not UNSCORABLE);
   - the Vitals Score is at or above the upper band edge (T40), i.e. in the healthy band; and
   - no critical condition is active.

   "Healthy X% of the time" means availability = X% over P.
2. UNSCORABLE windows **MUST** count as not healthy, following the rule that unknown is not healthy. Implementations **MUST** report the share of UNSCORABLE windows beside the availability figure.
3. Availability **MUST** be reported against the target declared on the spec sheet (S12), as MET or NOT MET for the period, with the period stated.
4. Availability is a companion to the Vitals Score, not an input to it. It **MUST NOT** change any vital or the headline.
5. The Rulebook sets no availability targets. Until the band edges (T40) are set, availability can be computed only with illustrative edges, and **MUST** then be labelled ILLUSTRATIVE.

### 9.3 Planned maintenance

1. Maintenance reduces the resilience actually available, and the score **MUST** reflect it: vitals and critical conditions are computed as for any other window.
2. A maintenance window **MAY** be declared in advance, with its scope, affected entities, start and end. Declarations are versioned events, like the spec sheet, and **MUST** precede the window.
3. Contributors and binding reasons inside a declared window, on the declared entities, **MUST** be tagged **PLANNED**.
4. The spec sheet (S12) states whether windows inside declared maintenance count against the availability target. The availability report **MUST** state which rule applied.
5. There is **no undeclared maintenance mode**. Nothing suspends scoring; an undeclared intervention is OPERATIONAL.

## 10. Workload profiles

The workload profiles are TRAINING, INFERENCE and GENERAL.
- **What a profile selects:** the D4 tail statistic, the D6 headroom semantics, the D3 value functions and the D7 and commissioning test suites.
- **What it does not change:** the vitals, the aggregation, the critical-condition set or the coverage rules.
- **Mixed fabrics:** a fabric whose declared purpose is mixed (S2) **MUST** declare the one profile it is scored under.
- **Candidate profiles:** the excluded areas of §2.5 item 3 (front-end and inference-serving networks, storage and checkpoint traffic, scale-up, multi-tenant isolation) are candidates for later profiles, in that order.

Evidence for the profile split: [8, 33, 34, 35].

## 11. Explanation record and presentation

### 11.1 The record

Every score record **MUST** contain the following.

**Identity:**
- Rulebook ID and version;
- spec-sheet version, and the class preset it adopts or CUSTOM;
- scoring scope ID (and, for a multi-scope fabric, the full set of scope scores with their distribution and the lowest scope);
- declared maintenance windows in force;
- declared class, verified class, conformance status and the date of the last conformance check;
- registered commissioning references in force;
- metric-definition and aggregation versions.

**Context:**
- workload profile;
- fabric scope ID;
- window;
- data cut-off and computation timestamp.

**Result:**
- the Vitals Score (confirmed) and upper bound, with coverage per vital; or UNSCORABLE with the missing-telemetry list;
- the score band (§11.2), marked ILLUSTRATIVE where the edges are not calibrated;
- the breadth indicator, the next-binding vital and the vital vector;
- evidence-quality confidence;
- the binding reason with its origin tag (DESIGN SHORTFALL, OPERATIONAL or PLANNED);
- where the declared class differs from the verified class, the counterfactual "declared Rx, built as Ry; as Ry it would score N" and the remedy (§3);
- ordered contributors [36] and mandatory findings;
- availability over the reporting period against the declared target (§9.2), where reported.

The record **MUST** satisfy "a non-maximal score must always be explained by one or more symptoms" [30].

### 11.2 Score bands

1. Bands are a **display rule**. They never change the Vitals Score.
2. The band edges are Rulebook parameter T40 (an upper and a lower edge; VALUE NOT SET). The display is:
   - **green** at or above the upper edge;
   - **amber** at or above the lower edge and below the upper edge;
   - **red** below the lower edge;
   - **red, whatever the number,** while any critical condition is active;
   - **grey** for UNSCORABLE.
3. Bands are part of the Rulebook and are published only once calibrated (E6, method T22). Until then, any displayed bands are illustrative and **MUST** be labelled ILLUSTRATIVE wherever they appear. Demonstrations of the method published before calibration use illustrative edges.
4. The cap value T15 **MUST** lie below the lower edge, so that a capped score is red by number as well as by rule.

### 11.3 Presentation rules

- **A score is never shown without its class.** The unit of presentation is **"Vitals Score N, class Rx (spec sheet version)"**, with CUSTOM in place of Rx for a custom sheet. A bare number is non-conformant presentation.
- Scores **MUST** be displayed as integers.
- Language models **MAY** render explanations from the record. They **MUST NOT** compute or change any value in it.

## 12. Comparability and versioning

1. Scores are comparable only when all of the following are the same:
   - the fabric over time; or fabrics on the **same class preset**, or on **identical spec sheets**;
   - the Rulebook version;
   - the workload profile;
   - the kind of scoring scope (a scope score is compared with scope scores, never with a blended fabric figure).
2. While preset promise values are not set, fabrics that adopt the same preset structure but declare their own promise values are comparable on structure only, and the record **MUST** say so.
3. Scores of different classes, or of different custom spec sheets, **MUST NOT** be ranked against each other. A score confirms conformance to its own spec sheet.
4. A score **MUST NOT** be compared across Rulebook versions, spec-sheet versions or re-registrations without recomputation.
5. **Rulebook versions:** RB-<major>.<minor>. A major version changes structure or methods; a minor version sets or revises values, including preset values. Values are frozen at their freeze point (see [`GOVERNANCE.md`](GOVERNANCE.md)).
6. The **determinism** requirement: identical telemetry, spec sheet and Rulebook version **MUST** produce a bit-identical score record.

## 13. Minimum implementation: the Day-One Set

1. **Purpose.** An operator should be able to compute a valid Vitals Score on the first day, from telemetry most platforms already export. The **Day-One Set** is the smallest set of vitals, counters and probes for which that is possible. A score computed from it is a Vitals Score like any other: the same Rulebook, the same rules and the same meaning.
2. **Contents** (PROPOSED; it becomes the common core of the minimum telemetry profile T35 for every class):

| Vital or condition | Counters and probes | Vendor-neutral model ([`METRICS.md`](METRICS.md)) |
|---|---|---|
| D1 Reachability | Interface oper-status (M01), BGP session state (M02), LLDP against intended cabling (M06), active probe mesh (M04, method M-PRB) | OpenConfig; RFC 7679/7680 metric definitions |
| D2 Resilience | Remaining path diversity and residual capacity (M07–M09), derived from M01, M06 and the declared inventory | Derived |
| D3 Congestion and loss | Queue and interface drops (M10, M11); switch-side ECN marks (M15); on lossless classes, PFC pause duration and storm events (M13, M14) | OpenConfig; SAI for M13, M14 |
| D4 Delay and tail | Probe delay from the same mesh (M23) | RFC 7679 |
| D5 Physical link integrity | FEC corrected and uncorrectable codewords (M27, M28), FCS errors (M31), link flaps (M32) | OpenConfig; IEEE |
| D6 Effective capacity | Interface octets, peak per sampling interval (M35) | OpenConfig |
| D7 AI communication | Only where the class requires it (R3): synthetic collectives (M38) | — |
| Critical conditions | The evidence sets of §7, drawn from the rows above | — |

3. **Everything else is optional in the Day-One Set:** NIC transport counters (M16–M18), buffer and queue watermarks (M19, M20, M24), in-band telemetry (M25, M26), FEC histograms (M29), optics (M33), link-level retry (M34), configuration reads beyond the switch side (M43), routing churn and convergence measurements (M44, M45). An optional metric that is not observed is listed in the record as **UNSCORABLE** at the metric level, with its reason (missing, stale or unsupported). It does not enter the coverage denominator, and it is reflected in evidence-quality confidence (§8.6), never in the score.
4. A class's minimum telemetry profile (T35) **MUST** include the Day-One Set and **MAY** require more.

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
