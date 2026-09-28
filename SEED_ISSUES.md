# Seed issues: the open questions

**Status:** Fabric Vitals v0.2 (draft) — a technical proposal for discussion. Not a standard. Rulebook values not yet set.

These are the questions we most want the community to answer. Each will be opened as an issue on the first day, using the issue templates (pre-filled forms) in [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE/). Evidence is more useful than opinion: please cite a standard, a paper or operational data, and say where it comes from (a lab or production) and at what scale. Each question ends with the template to use and the label to give the issue.

## 1. Lossless-transport configuration consistency

**Summary.** Configuration errors are a documented cause of failure in lossless RDMA fabrics. RDMA is remote direct memory access, which lets one server read and write another server's memory directly across the network, and a lossless fabric is one configured to pause traffic rather than drop packets. So v0.2 names a consistency check as spec-sheet field S8 and metric M43. The check covers the PFC priorities (Priority Flow Control, the mechanism that pauses a traffic class on a link when its queue fills), ECN (Explicit Congestion Notification, a mark set on packets to tell senders to slow down before queues overflow), the DSCP-to-class mapping (DSCP is the Differentiated Services Code Point, the header field that says which traffic class a packet belongs to) and the MTU (maximum transmission unit, the largest packet a link will carry), across all switches and NICs (network interface cards, the adapters that connect servers to the network). PFC configuration has no OpenConfig model (OpenConfig is a vendor-neutral set of data models for network devices), and the configuration on the NIC side is specific to each driver. See [`SPEC_SHEET.md`](SPEC_SHEET.md) §3.

**Question.** Which of these configuration items does your platform expose through a vendor-neutral model? And should a live mismatch between devices be treated as a critical condition, a fault that caps the score on its own, rather than as evidence feeding vital D3? *Template: telemetry availability or method critique. Label: `method`, `telemetry`.*

## 2. Routing stability and convergence time

**Summary.** v0.2 treats routing stability as control-plane evidence for vital D1 (metric M44); the control plane is the part of the network that works out the routes, as opposed to the part that forwards packets. It treats routing convergence time, the time the network takes to settle on new routes after a change or failure, as part of the recovery objective that vital D2 checks (metric M45 and spec-sheet field S11). Convergence time has no standard counter, so it is measured in outcome tests and, where probes allow, on real events.

**Question.** How do you measure convergence time in production AI (artificial intelligence) fabrics today, and at what resolution, that is, how finely in time you can see it? *Template: telemetry availability. Label: `telemetry`.*

## 3. The commensurability assumption

**Summary.** The Vitals Score is the minimum across the vitals: the lowest vital sets the score. That assumes the vitals are commensurable, meaning measured on a comparable scale, so that a value of 60 in one vital means a state as bad as 60 in another. The Rulebook makes this true by definition, relative to each vital's declared reference. Whether it also holds for real operational impact, the effect on the jobs the fabric carries, is untested; experiment E4 in [`VALIDATION.md`](VALIDATION.md) is meant to test it.

**Question.** Do you have evidence, from incidents or experiments, that equal distances from the reference in different vitals have similar impact on AI jobs, or very different impact? *Template: method critique. Label: `method`.*

## 4. The role of D7 (AI communication)

**Summary.** Vital D7 measures AI communication by running synthetic collectives: test runs of the group communication patterns that AI training uses, sent between hosts known to be healthy. D7 enters the minimum (counts towards the score) only where the spec sheet requires it; otherwise it corroborates the other vitals, confirming what they show without setting the score. This avoids penalizing fabrics that test themselves. See [`SPEC.md`](SPEC.md) §4.3.

**Question.** Should synthetic collectives be required for some class presets, and how often can operators run them without disturbing tenants, the jobs and users sharing the fabric? *Template: method critique. Label: `method`.*

## 5. The class-preset proposal

**Summary.** A class preset is a published, ready-made spec sheet that a fabric can adopt. There are three: R1 (rail-optimized, a common wiring layout for AI fabrics, and single-homed, meaning one connection into the fabric for each endpoint), R2 (dual-homed, meaning two connections) and R3 (multi-plane, sprayed, tested, meaning several parallel network planes with traffic spread across them and the design proven by tests). Each preset has structural predicates (yes-or-no tests of how the fabric is built) and promise fields (what the fabric commits to). They are design patterns ordered by how much redundancy they carry, not quality tiers, and the redundancy is stated as what happens when something fails rather than as a count of paths. The scheme is the author's proposal, and all preset values are unset. See SPEC_SHEET.md §5.

**Question.** Are these three patterns the right ones for real AI fabrics, and are the families of predicates and the promise fields right for each? *Template: method critique. Label: `method`, `presets`.*

## 6. Evidence from mid-sized clusters

**Summary.** Most public evidence on normal ranges and failure rates comes from a few hyperscale operators, the handful of companies that run the very largest fabrics. For clusters of about 32 to 2,000 GPUs (graphics processing units, the accelerator chips that AI runs on), public operational evidence is thin, and every value carried over from hyperscale is marked "not validated at this scale".

**Question.** Can you share per-link rates of flaps (a link going down and coming back up), bit errors and pauses, or tell us which telemetry your equipment makes available, from a mid-sized cluster? Or can you run the shadow-mode experiment V-S2, in which a fabric is scored in the background while it runs its normal work? *Template: validation offer. Label: `validation`.*

## 7. Band calibration

**Summary.** Score bands are the colour groups a score is displayed in: green, amber and red, with grey for UNSCORABLE (the result given when a fabric cannot be measured well enough to score). The bands are a display rule only. Their edges are Rulebook parameter T40, and they will be published only once they have been calibrated, that is, set from measured evidence of the communication impact attributed to the fabric (experiment E6). Until then, any bands that are displayed are illustrative and are labelled so.

**Question.** What outcome data would convince you that a band edge is in the right place, and can you help collect it? *Template: validation offer or method critique. Label: `validation`, `method`.*
