# Contributing

**Status:** Fabric Vitals v0.2 (draft) — a technical proposal for discussion. Not a standard. Rulebook values not yet set.

Thank you for helping make Fabric Vitals credible. Three kinds of contribution are especially useful now: a critique of the method, a report of which telemetry (measurement data) your equipment exports, and an offer of data or fabrics for validation. Each kind has its own issue template, a pre-filled form that opens when you create an issue, in the folder [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE/). The questions we most want answered are listed in [`SEED_ISSUES.md`](SEED_ISSUES.md).

## 1. Method critique

Open an issue with the Method critique template ([`method-critique.md`](.github/ISSUE_TEMPLATE/method-critique.md)) and give it the label `method`. Useful topics:
- **the Rulebook / spec-sheet split:** the Rulebook is the set of rules that is the same for every fabric, and the spec sheet is the set of promises each owner declares for their own fabric. Every parameter of the method sits on one side or the other. Is each one on the right side? See [`RULEBOOK.md`](RULEBOOK.md) §2.
- **the class presets:** the three published, ready-made spec sheets that fabrics can adopt. Each has structural predicates (yes-or-no tests of how the fabric is built) and promise fields (what the fabric commits to). Are they right, and are the presets meaningful for real AI (artificial intelligence) fabrics? See [`SPEC_SHEET.md`](SPEC_SHEET.md) §5.
- **the weakest-vital aggregation:** the score is the lowest of the seven vitals rather than an average. This rests on the commensurability assumption: that the same number means an equally bad state in every vital. See [`SPEC.md`](SPEC.md) §6.
- **the coverage rules:** the confirmed score (only what has been measured counts, and unmeasured capacity counts as worst), the grace period (how long a lapse in telemetry is tolerated), the coverage floor (the least telemetry that still allows a score at all) and the blast-radius coupling (the floor is tied to how much of the fabric a single failure can take out). See SPEC.md §8.
- **the critical conditions:** the short list of faults that cap the score on their own, and when each of them applies. See SPEC.md §7.
- **availability and score bands:** how the share of time a fabric counts as healthy is defined, and how scores are grouped into bands such as green, amber and red. See SPEC.md §9.2 and §11.2.

Please cite evidence: a standard, a paper or operational data. State its scope: whether it comes from a lab or from production, and at what scale.

## 2. Telemetry availability

Telemetry is the measurement data that switches and network adapters export. Open an issue with the Telemetry availability template ([`telemetry-availability.md`](.github/ISSUE_TEMPLATE/telemetry-availability.md)) and give it the label `telemetry`. Tell us, for your platform:
- which of the metrics in [`METRICS.md`](METRICS.md) are exported by default, with no special setup, and through which data model. The choices are an OpenConfig path (OpenConfig is a vendor-neutral set of data models for network devices), IETF YANG (a model written in the YANG modelling language and published by the Internet Engineering Task Force, the body that publishes internet standards), IEEE (a counter defined by the Institute of Electrical and Electronics Engineers, publisher of the Ethernet standards), SAI (the Switch Abstraction Interface, a common programming interface to switch chips), or a driver counter name (the name a NIC driver gives the counter; a NIC is a network interface card, the adapter that connects a server to the network);
- the default sampling or streaming interval, that is, how often the platform reports each value;
- anything that needs special configuration before the metric appears, for example allocating hardware counters in the switch chip;
- whether the lossless-transport configuration can be read on switches and NICs. This is metric M43. A lossless fabric is one set up to pause traffic rather than drop packets, and the configuration in question is: the PFC priorities (Priority Flow Control, the mechanism that pauses one traffic class on a link when its queue fills), ECN (Explicit Congestion Notification, a mark set on packets to tell senders to slow down before queues overflow), the DSCP-to-class mapping (DSCP is the Differentiated Services Code Point, the field in a packet header that says which traffic class the packet belongs to) and the MTU (maximum transmission unit, the largest packet a link will carry).

Your answers set two Rulebook parameters: the minimum telemetry profile, the smallest set of telemetry the method needs (T35), and the coverage floor (T29). Vendor-specific counter names are welcome. How to map them onto one vendor-neutral meaning is still an open question.

## 3. Validation data and partnership

Open an issue with the Validation offer template ([`validation-offer.md`](.github/ISSUE_TEMPLATE/validation-offer.md)) and give it the label `validation`. We are looking for:
- emulated or replayed telemetry, meaning telemetry from a fabric simulated in software, or real telemetry recorded earlier and played back, for the stage of the programme that needs no GPUs (experiments E2, E3, E8, E9 and E12; a GPU is a graphics processing unit, the accelerator chip that AI computation runs on);
- lab fabrics of 32–256 GPUs for fault-injection experiments, in which failures are caused on purpose to see how the score responds;
- mid-sized production fabrics (about 32–2,000 GPUs) for shadow scoring, in which a fabric is scored in the background while it runs its normal work;
- outcome data for band calibration (experiment E6), that is, records of the real impact on jobs, used to decide where the edges between score bands belong.

[`VALIDATION.md`](VALIDATION.md) says what each experiment needs. Do not post confidential data in public issues. Describe what you can offer, and we will arrange a suitable channel.

## How changes are reviewed

1. **Proposal.** Every proposed change starts as an issue that states the reasoning behind it and the evidence for it. The rules are in [`GOVERNANCE.md`](GOVERNANCE.md).
2. **Discussion.** The issue stays open for comment for a stated period.
3. **Pull request.** Accepted changes arrive as pull requests (proposed edits to the files, submitted for review) that reference the issue.
4. **Review.** Pull requests are checked for:
   - consistent terms and IDs (the labels, such as T-, S-, M- and D- numbers, that name parameters, fields, metrics and vitals) across `SPEC.md`, `RULEBOOK.md`, `SPEC_SHEET.md` and `METRICS.md`;
   - a citation for every factual claim;
   - no invented numbers (any example value is labelled ILLUSTRATIVE);
   - no change to a frozen value (a value fixed at publication) outside the versioning rules.
5. **Decision.** The steward, the organization that maintains the method, records the decision and its reason in the issue.

## Ground rules

- Be respectful. Critique ideas, not people.
- **No product promotion.** Vendor-specific information is welcome as evidence, as long as you state its scope.
- Use of the names "Fabric Vitals" and "Vitals Score" follows the policy in [`TRADEMARK.md`](TRADEMARK.md).
- By contributing, you agree that your contribution is licensed under the repository's license, CC BY 4.0 ([`LICENSE`](LICENSE)). That is the Creative Commons Attribution licence: anyone may copy, share and adapt the text as long as they credit the source.

Contact: hello@datacenternetwork.ai
