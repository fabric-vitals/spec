# Fabric Vitals: a health score for AI data-center fabrics — two-page summary

**Shankar Gopidas, Founder & CEO, datacenternetwork.ai**

*Fabric Vitals v0.2 (draft) — a technical proposal for discussion. Not a standard. Rulebook values not yet set.*

## The problem

AI data centers connect thousands of GPUs through a dedicated network, the "fabric". The people who run these fabrics watch dozens of separate signals: links up or down, dropped packets, congestion signals, delays, error rates on cables and optics, and results from test traffic. Each is useful, but none answers the question everyone asks: *is this AI network healthy?* Today the answer depends on who you ask. Each operator uses its own thresholds, and vendor dashboards score only their own equipment. Worse, many summary scores are averages, and an average lets one badly broken area hide behind several good ones.

## The idea

Fabric Vitals proposes a single number, the **Vitals Score**, for the fabric that connects the GPUs in an AI data center. It is meant to be read the way a credit score is read: at a glance. It does not express an opinion about the network. It confirms whether the network keeps the promises its owner declared. If a fabric is built to survive two link failures without disrupting training, the score checks that it still can. It does not ask whether the fabric looks "normal" compared with last week.

Think of how a car's range is rated. Every car is measured by the same official test procedure, but each car has its own rated range on its spec sheet. Fabric Vitals works the same way: one **Rulebook** says how every fabric is measured and judged, and each fabric has its own **Fabric Spec Sheet** saying what it promises.

## How it works

**1. The owner fills in a spec sheet.** Before anything is measured, the owner declares what the fabric is for (training, inference or both), how it is built, which failures it rides through, how quickly it recovers, how much of the time it should be healthy, and the performance it promises. Owners can adopt one of three published **class presets**, ready-made spec sheets like the standard models in a car maker's range: R1 rail-optimized (a wiring layout in which the GPUs in the same position in each server share a switch) and single-homed (one connection into the fabric per GPU), the most common training design in published reference designs today; R2 dual-homed (two connections, so one can fail); and R3 multi-plane (several separate, parallel networks), with traffic sprayed across planes (each flow spread over all of them) and continuous tests (test traffic running all the time). They are design patterns ordered by redundancy, not quality tiers, and fabrics of the same class can be compared. Large fabrics are scored pod by pod, with the weakest pod named, rather than blended into one number. The build the owner declared is checked against the fabric as actually built. If the owner promises more than was built, the missing redundancy counts as absent, and the score says what it would be under the class actually built. The honest fix is a new, versioned spec sheet.

**2. The Rulebook is fixed before measurement.** Every measurement is judged by a published Rulebook, set in advance and versioned, and identical for every fabric. Where an industry standard exists, it is used. Where none exists, the rule is either defined with documented reasoning or set by a standard test procedure. The rules are never tuned after the fact to make a result look better.

**3. The headline is the weakest area, and severe problems cap it.** The fabric is scored in seven areas, called **vitals**: reachability, resilience, congestion and loss, delay, physical link quality, usable capacity and, where the spec sheet requires it, performance under AI-style test traffic. Each area is scored on the same scale, the share of its promise actually being delivered, and the headline equals the worst of these, not their average. Named critical conditions, such as a traffic "black hole" (traffic enters a part of the network and silently disappears) or a congestion storm (an overload that spreads from path to path), cap the score whatever the other areas show. The difference is easy to see: if four areas are perfect (100) and one has collapsed (10), an average gives 82, which looks healthy. Fabric Vitals gives 10.

**4. Missing data never makes the score look better.** Parts of the fabric that are not being measured count as unknown, not as healthy. The headline is the health the evidence actually confirms, and it is shown beside the best case if the unmeasured parts turned out to be fine. If too much is unmeasured, the result is "unscorable", together with a list of exactly which measurements are missing and where. Hiding telemetry, the readings the equipment reports about itself, therefore cannot raise the score. The only exception is a short, bounded allowance for momentary gaps in data collection, so that a restarting collector (the software that gathers those readings) does not look like a failing network.

**5. Every score explains itself.** Each score names the area or condition that set it. It lists the main contributors in order, and links every number back to the raw measurements, the rule that was applied and the promise it was judged against. It also shows how many areas fall short, so that broad deterioration is visible even when the headline has not moved. The score can be shown in green, amber or red, with any critical condition shown red; those colour bands will be published only once they are calibrated, and until then any colours shown are illustrative. "Healthy 99% of the time" gets a precise meaning: the share of time the score was green with no critical condition active. A score is always shown with its class, in the form "Vitals Score N, class R2 (spec sheet version)". Scores are always computed by a fixed, repeatable method. AI language models may help explain a result, but they never calculate it.

## What makes it different

Fabric Vitals is vendor-neutral and open. Anyone can implement it, and it is not tied to any product. It builds on existing work rather than competing with it:
- **ITU-T M.3042** already defines a health index for telecom networks. It averages at its top levels, where Fabric Vitals uses the weakest-area rule instead. M.3042 already applies the weakest-area rule inside some of its lower-level indexes.
- **IETF drafts on benchmarking AI fabrics** define health indicators that can feed Fabric Vitals.
- **A recent IETF draft** scores individual links for congestion. Fabric Vitals treats it as related work and a possible input.

The class idea borrows from how data-center facilities are rated. There, a site is rated by its weakest subsystem, and resilience levels are declared before design. The class presets themselves are the author's proposal, drawn from public sources and open for critique.

## What is not done yet

The method is defined, but the Rulebook's values are not, and the class presets carry no promise values yet. Most thresholds have no industry standard behind them, so they will be set through open validation experiments. The first round needs no GPUs: it runs on an emulated network with replayed data and tests the scoring machinery itself. Its results produce the first Rulebook with values, which will be published openly. Tests that need real hardware and GPUs come later. Until then, scores are for discussion and experimentation, not for acceptance decisions.

The available evidence is strongest for the very largest AI clusters and thinnest for mid-sized ones, roughly 32 to 2,000 GPUs, which is where many readers operate. Some requirement texts of paid industry standards were not consulted. Fabrics with limited monitoring will often be "unscorable" at first, and they will be told what to add; a published minimum set of standard counters and probes lets any operator start on day one. Front-end and inference-serving networks, storage and checkpoint traffic, scale-up interconnects and multi-tenant isolation are out of scope for now and are on the roadmap, in that order.

## How to get involved

We are asking for three things:
- **Expert review:** critique of the method, the Rulebook and spec-sheet split, and the class presets, through the specification repository's issue tracker.
- **Validation partners:** access to lab or production fabrics, including mid-sized clusters, to help set the Rulebook's values.
- **Standards and community input:** in particular on vendor-neutral definitions of network-card and congestion counters, and of lossless-network configuration.

Specification and issues: https://github.com/fabric-vitals/spec · Contact: hello@datacenternetwork.ai

## Disclosure

The author organization develops network software. The proposal is written to be implementable by any vendor or operator. The method, its Rulebook and its class presets are vendor-neutral and are offered for open discussion.

---

Full paper: *Fabric Vitals: a vendor-neutral health score for AI data-center fabrics, measured against a declared design* (v0.2) · Specification: https://github.com/fabric-vitals/spec
