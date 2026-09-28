# Governance

**Status:** Fabric Vitals v0.2 (draft) — a technical proposal for discussion. Not a standard. Rulebook values not yet set.

## Steward

**datacenternetwork.ai** is the initial author of Fabric Vitals, and the publisher and steward of its specification, its Rulebook and its class presets. The steward is the organization that maintains the method and decides on changes to it. The Rulebook is the single set of measuring and judging rules that applies to every fabric. A class preset is a published, ready-made spec sheet (the declaration of what a fabric promises) that fabric owners can adopt. The method's name is deliberately independent of the steward.

**Commitment to a neutral body.** It is the steward's intent that stewardship move to an open, multi-party body (for example a standards organization, an industry consortium or a foundation) if the community prefers that. If stewardship moves, datacenternetwork.ai commits to transfer the marks "Fabric Vitals" and "Vitals Score" (the names, which are claimed as trademarks; the policy is in [`TRADEMARK.md`](TRADEMARK.md)) together with stewardship of the specification, the Rulebook and the class presets to that body. Any such move will be announced in [`CHANGELOG.md`](CHANGELOG.md).

## What is versioned

| Artifact | Version form | Meaning |
|---|---|---|
| The specification: [`SPEC.md`](SPEC.md) and the template in [`SPEC_SHEET.md`](SPEC_SHEET.md) | `v<major>.<minor>` | A major version changes normative requirements, the rules an implementation has to follow. A minor version clarifies the text without changing any result. |
| The Rulebook ([`RULEBOOK.md`](RULEBOOK.md)) and the class presets in SPEC_SHEET.md §5 | `RB-<major>.<minor>` | A major version changes the structure, the categories or the methods. A minor version sets or revises values, including preset values. During the 0.x series any version may change the structure. |
| A fabric's own spec sheet, held by its owner | the owner's version number (field S22) | Any change to any field creates a new version of the sheet and starts a new series of scores. |

Every score records the specification version, the Rulebook version and the spec-sheet version it was computed under. Scores computed under different versions are never compared without being recomputed. See SPEC.md §12.

## The pre-registration rule

Principle 1 of Fabric Vitals is that a score is measured against a declared reference that was fixed before measurement began. Pre-registration means writing down the reference and the rules before the data is collected. Therefore:
1. **Frozen values.** Every Rulebook value or method, every preset value, and every value on a fabric's spec sheet is frozen (fixed, and no longer changeable) at its **freeze point**. The freeze point is defined in RULEBOOK.md §1, and it is:
   - at publication of the Rulebook version, for Rulebook and preset values;
   - at declaration of the fabric's spec sheet, for the values the owner declares;
   - at commissioning registration, for the references measured on the fabric itself when it is brought into service.
2. **No retroactive change.** A value is never changed in order to alter the score of a measurement window (the period of time one score covers) that has already begun. Values are never tuned after the fact.
3. **Visible re-registration.** A re-registration, or a new version of the spec sheet, applies only to windows after its effective time, and it is visible in every score record from then on.
4. **Evidence required.** The Rulebook gives each of its values a category letter that says what kind of evidence can set it. A Rulebook or preset value in category (c) can be set only with the evidence the Rulebook names for it, usually a validation experiment; the experiments are in [`VALIDATION.md`](VALIDATION.md). A value in category (a) or (b) cites its source and the source's authority grade, a label for how strong the source is.
5. **Experiments are registered before they run.** A validation experiment that will set a value is described in an issue before any of its data is collected. The description states the setup, the metric, the analysis and the decision rule that will turn the result into the value.

## Change process

The process is open: anyone can propose a change, and every decision is public.
1. **Open an issue.** Anyone can open one; [`CONTRIBUTING.md`](CONTRIBUTING.md) explains how. A change proposal states the reasoning and the evidence: either a source, with its authority grade, or an experiment result with its data.
2. **Public discussion.** The issue stays open for comment for a stated period before any decision is taken.
3. **Pull request.** Accepted changes are made by pull request, a proposed edit to the files submitted for review. Each pull request references the issue and updates CHANGELOG.md.
4. **Decision record.** The steward records each decision and its reason in the issue, including rejections.
5. **Release.** Changes are released as a new specification version or a new Rulebook version.

## Conflict of interest

The steward's own products receive no special treatment in the method, the Rulebook or the presets. Proposals from any party follow the same process.
