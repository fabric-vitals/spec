# Governance

**Status:** Fabric Vitals v0.2 (draft) — a technical proposal for discussion. Not a standard. Rulebook values not yet set.

## Steward

**datacenternetwork.ai** is the initial author of Fabric Vitals, and the publisher and steward of its specification, Rulebook and class presets. The method's name is deliberately independent of the steward.

**Commitment to a neutral body.** It is the steward's intent that stewardship move to an open, multi-party body (for example a standards organization, consortium or foundation) if the community prefers. If stewardship moves, datacenternetwork.ai commits to **transfer the marks "Fabric Vitals" and "Vitals Score"** ([`TRADEMARK.md`](TRADEMARK.md)) together with stewardship of the specification, the Rulebook and the class presets to that body. Any such move will be announced in [`CHANGELOG.md`](CHANGELOG.md).

## What is versioned

| Artifact | Version form | Meaning |
|---|---|---|
| Specification ([`SPEC.md`](SPEC.md), [`SPEC_SHEET.md`](SPEC_SHEET.md) template) | `v<major>.<minor>` | A major version changes normative requirements. A minor version clarifies without changing results. |
| Rulebook ([`RULEBOOK.md`](RULEBOOK.md)) and class presets ([`SPEC_SHEET.md`](SPEC_SHEET.md) §5) | `RB-<major>.<minor>` | A major version changes structure, categories or methods. A minor version sets or revises values, including preset values. During the 0.x series any version may change structure. |
| A fabric's spec sheet (held by its owner) | owner's version (S22) | Any change to a field creates a new version and a new score series. |

Every score records the specification version, the Rulebook version and the spec-sheet version it was computed under. Scores under different versions are never compared without recomputation ([`SPEC.md`](SPEC.md) §12).

## The pre-registration rule

Principle 1 of Fabric Vitals is that a score is measured against a declared reference, fixed before measurement. Therefore:
1. **Frozen values.** Every Rulebook value or method, every preset value, and every value on a fabric's spec sheet is frozen at its **freeze point** ([`RULEBOOK.md`](RULEBOOK.md) §1):
   - at publication of the Rulebook version (Rulebook and preset values);
   - at declaration of the fabric's spec sheet (declared values);
   - at commissioning registration (per-fabric measured references).
2. **No retroactive change.** A value is never changed to alter the score of a measurement window that has already begun. Values are **never tuned after the fact**.
3. **Visible re-registration.** A re-registration or a new spec-sheet version applies only to windows after its effective time, and it is visible in every subsequent score record.
4. **Evidence required.** A Rulebook or preset value in category (c) can be set only with the evidence named in the Rulebook, usually a validation experiment ([`VALIDATION.md`](VALIDATION.md)). A value in category (a) or (b) cites its source and authority grade.
5. **Experiments are registered before they run.** A validation experiment that will set a value is described in an issue (setup, metric, analysis and the decision rule for the value) before its data is collected.

## Change process

The process is open: anyone can propose a change, and every decision is public.
1. **Open an issue.** Anyone can open one ([`CONTRIBUTING.md`](CONTRIBUTING.md)). A change proposal states the rationale and the evidence: a source with its authority grade, or an experiment result with data.
2. **Public discussion.** The issue stays open for comment for a stated period before a decision.
3. **Pull request.** Accepted changes are made by pull request. They reference the issue and update [`CHANGELOG.md`](CHANGELOG.md).
4. **Decision record.** The steward records each decision and its reason in the issue, including rejections.
5. **Release.** Changes are released as a new specification or Rulebook version.

## Conflict of interest

The steward's own products receive no special treatment in the method, the Rulebook or the presets. Proposals from any party follow the same process.
