# Contributing

**Status:** Fabric Vitals v0.2 (draft) — a technical proposal for discussion. Not a standard. Rulebook values not yet set.

Thank you for helping make Fabric Vitals credible. Three kinds of contribution are especially useful now. Each has an issue template in [`.github/ISSUE_TEMPLATE/`](.github/ISSUE_TEMPLATE/), and the questions we most want answered are listed in [`SEED_ISSUES.md`](SEED_ISSUES.md).

## 1. Method critique

Open an issue with the **Method critique** template ([`method-critique.md`](.github/ISSUE_TEMPLATE/method-critique.md); label **`method`**). Useful topics:
- **the Rulebook / spec-sheet split:** is each parameter on the right side? ([`RULEBOOK.md`](RULEBOOK.md) §2);
- **the class presets:** are the structural predicates and promise fields right, and are the presets meaningful for real AI fabrics? ([`SPEC_SHEET.md`](SPEC_SHEET.md) §5);
- **the weakest-vital aggregation** and its commensurability assumption ([`SPEC.md`](SPEC.md) §6);
- **the coverage rules:** confirmed score, grace period, coverage floor and blast-radius coupling ([`SPEC.md`](SPEC.md) §8);
- **the critical conditions** and when they apply ([`SPEC.md`](SPEC.md) §7);
- **availability and score bands** ([`SPEC.md`](SPEC.md) §9.2, §11.2).

Please cite evidence: a standard, a paper or operational data. State its scope (lab or production; scale).

## 2. Telemetry availability

Open an issue with the **Telemetry availability** template ([`telemetry-availability.md`](.github/ISSUE_TEMPLATE/telemetry-availability.md); label **`telemetry`**). Tell us, for your platform:
- which metrics in [`METRICS.md`](METRICS.md) are exported **by default**, and through which model (OpenConfig path, IETF YANG, IEEE, SAI, or a driver counter name);
- the default sampling or streaming interval;
- anything that needs special configuration, for example hardware counter allocation;
- whether the lossless-transport configuration (PFC priorities, ECN, DSCP-to-class mapping, MTU) can be read on switches and NICs (M43).

This sets the minimum telemetry profile (T35) and the coverage floor (T29). Vendor-specific counter names are welcome. The mapping to a vendor-neutral meaning is an open question.

## 3. Validation data and partnership

Open an issue with the **Validation offer** template ([`validation-offer.md`](.github/ISSUE_TEMPLATE/validation-offer.md); label **`validation`**). We are looking for:
- emulated or replayed telemetry for the no-GPU stage (E2, E3, E8, E9, E12);
- lab fabrics of 32–256 GPUs for fault-injection experiments;
- mid-sized production fabrics (about 32–2,000 GPUs) for shadow scoring;
- outcome data for band calibration (E6).

See [`VALIDATION.md`](VALIDATION.md) for what each experiment needs. Do not post confidential data in public issues. Describe what you can offer, and we will arrange a suitable channel.

## How changes are reviewed

1. **Proposal.** Every proposed change starts as an issue with rationale and evidence ([`GOVERNANCE.md`](GOVERNANCE.md)).
2. **Discussion.** Discussion stays open for a stated period.
3. **Pull request.** Accepted changes arrive as pull requests that reference the issue.
4. **Review.** Pull requests are reviewed for:
   - consistency of terms and IDs across `SPEC.md`, `RULEBOOK.md`, `SPEC_SHEET.md` and `METRICS.md`;
   - a citation for every factual claim;
   - no invented numbers (examples labelled ILLUSTRATIVE);
   - no change to a frozen value outside the versioning rules.
5. **Decision.** The steward records the decision and its reason in the issue.

## Ground rules

- Be respectful. Critique ideas, not people.
- **No product promotion.** Vendor-specific information is welcome as evidence, with its scope stated.
- Use of the names "Fabric Vitals" and "Vitals Score" follows [`TRADEMARK.md`](TRADEMARK.md).
- By contributing, you agree that your contribution is licensed under the repository's license ([`LICENSE`](LICENSE), CC BY 4.0).

Contact: hello@datacenternetwork.ai
