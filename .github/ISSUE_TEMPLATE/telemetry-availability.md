---
name: Telemetry availability
about: Tell us which metrics your platform exports by default, and how
title: "[telemetry] "
labels: telemetry
---

**Platform**
<!-- The switch or NIC platform (a NIC is a network interface card, the adapter that connects a server to the network) and its software version. Vendor names are welcome as evidence; please do not promote products. -->

**Metrics exported by default**
<!-- For each metric in METRICS.md (M01–M45): is it exported by default, with no special setup? Through which data model: an OpenConfig path (OpenConfig is a vendor-neutral set of data models for network devices), IETF YANG (a model in the YANG modelling language, published by the Internet Engineering Task Force), IEEE (a counter defined by the Institute of Electrical and Electronics Engineers, publisher of the Ethernet standards), SAI (the Switch Abstraction Interface, a common programming interface to switch chips), or a driver counter name? -->

| Metric ID | Exported by default? | Model or counter name | Default interval |
|---|---|---|---|
|  |  |  |  |

**Needs special configuration?**
<!-- For example: allocating hardware counters in the switch chip, setting up streaming subscriptions (a standing request for the device to push data), or licences. -->

**Configuration visibility (for M43)**
<!-- Metric M43 is the lossless-transport configuration check. Can the PFC priorities (Priority Flow Control, which pauses a traffic class rather than dropping packets), the ECN configuration (Explicit Congestion Notification, a mark that tells senders to slow down), the DSCP-to-class mapping (DSCP is the Differentiated Services Code Point, the packet field that names a traffic class) and the MTU (maximum transmission unit, the largest packet a link carries) be read through a vendor-neutral model, on switches and on NICs? -->
