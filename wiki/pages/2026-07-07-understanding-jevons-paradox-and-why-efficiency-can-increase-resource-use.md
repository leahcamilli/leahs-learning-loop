---
title: "Understanding Jevons Paradox and Why Efficiency Can Increase Resource Use"
source: "https://youtu.be/a6sYYrLTOjQ?is=G7luggJVB68BFE4m"
date: "2026-07-07"
tags: [economics, efficiency, energy, sustainability, systems-thinking]
source_type: "youtube"
channel: "Hank Green"
published: "2026-07-06"
duration_seconds: 2002
kind: "deep-dive"
depth: 2
actionability: 2
---

## TL;DR

> Efficiency lowers resource use per unit, but it can also lower costs enough to expand demand and increase total consumption. To achieve absolute reductions, measure system-wide use and pair efficiency gains with limits or incentives that manage demand.

## Key Takeaways

1. Track total resource use as resource per unit multiplied by total activity; improving only the first factor does not guarantee aggregate savings.
2. Expect stronger rebound effects when lower costs unlock many new users, applications, or operating hours.
3. Distinguish partial rebound, which erodes some expected savings, from a Jevons-style increase, where total resource use rises above its original level.
4. Evaluate unit economics, behavioral responses, and scale responses before concluding that an optimization will reduce costs, energy use, or emissions.
5. A drop from 10 to 4 energy units per API call still raises total energy from 10,000 to 12,000 if demand grows from 1,000 to 3,000 calls.
6. Pair efficiency improvements with workload budgets, capacity limits, pricing, quotas, or other constraints when absolute consumption must fall.

## Overview

Jevons Paradox describes a counterintuitive pattern: when a resource is used more efficiently, total consumption of that resource can rise rather than fall. The idea matters because engineers, product teams, and policy makers often assume that better efficiency automatically reduces costs, energy demand, or environmental impact, but real-world systems frequently respond through changes in behavior, demand, and market expansion.

This lesson explains the paradox in practical terms, shows the mechanism that causes it, and outlines how to reason about it when designing technology or evaluating policy. If you work on infrastructure, AI systems, energy-intensive software, hardware, or sustainability planning, understanding this concept helps you avoid simplistic conclusions about optimization.

## Key Concepts

- **Jevons Paradox**: Jevons Paradox is the claim that improvements in efficiency can increase the total use of a resource. The paradox arises because efficiency lowers the effective cost of using that resource, which can stimulate more demand. It is especially relevant in systems where demand is elastic or where cheaper usage enables entirely new applications.
- **Rebound effect**: The rebound effect is the mechanism behind the paradox. If a device, process, or service becomes more efficient, each unit of output costs less, so people may use more of it. A small rebound means some expected savings are lost; a large rebound can erase the savings entirely or even push total usage above the starting point.
- **Direct and indirect demand growth**: Direct demand growth happens when cheaper operation causes more of the same activity, such as driving more because fuel costs per mile fall. Indirect demand growth happens when saved money or capacity is spent elsewhere in the economy, potentially increasing total resource consumption in other forms. Both effects matter when evaluating whether efficiency actually reduces system-wide use.
- **Elasticity of demand**: Demand elasticity describes how strongly usage responds to changes in price or cost. Jevons-style outcomes are more likely when lower effective prices unlock many additional users, use cases, or operating hours. Engineers should treat elasticity as a system property, not just a business metric.
- **System-level optimization**: Local optimization improves one component, but system-level optimization asks what happens after users, markets, and adjacent systems respond. An efficient model, server, or process may reduce per-unit cost while increasing total workload. The relevant question is not only whether the unit is cheaper, but whether the system expands because it is cheaper.
- **Policy and constraint design**: Efficiency alone often does not guarantee lower absolute consumption. To ensure reductions, organizations or governments may need caps, budgets, pricing, quotas, or operational limits alongside efficiency gains. This distinction is important in energy planning, cloud cost control, and environmental policy.

## How It Works

At the core of Jevons Paradox is a simple sequence:

1. A technology becomes more efficient.
2. The cost per unit of useful output falls.
3. Lower cost makes the activity more attractive.
4. Usage expands through existing demand, new users, or new applications.
5. Total resource consumption may fall less than expected, stay flat, or even increase.

A classic historical example is coal and steam power. If steam engines use coal more efficiently, it seems intuitive that coal consumption should drop. But the improved efficiency also makes steam-powered work cheaper, which encourages broader industrial adoption. More factories, machines, and use cases can lead to higher total coal demand even though each engine is individually better.

This logic shows up repeatedly in modern engineering:

- **Compute efficiency**: If inference becomes 10x cheaper, teams may run far more experiments, serve more requests, or embed models into many more products.
- **Network efficiency**: Better compression can reduce bandwidth per video stream, but lower delivery cost can increase streaming volume and video quality.
- **Vehicle efficiency**: More efficient cars reduce fuel per mile, but people may drive more, buy larger vehicles, or shift farther from work.
- **Data storage efficiency**: Cheaper storage encourages retention of more logs, media, and backups.

The important analytical distinction is between **per-unit efficiency** and **absolute consumption**. Engineers often measure the first very well: milliseconds per request, joules per inference, cost per transaction, grams of CO2 per mile. But decision makers often care about the second: total cloud spend, total electricity consumed, total emissions, or total hardware deployed.

To reason about the paradox in practice, break the system into three layers:

- **Unit economics**: What got cheaper or more efficient?
- **Behavior response**: How will users, product teams, or customers react?
- **Scale response**: Does lower cost enable more traffic, larger models, more automation, or new markets?

A practical mental model is:

```text
Total resource use = resource per unit of activity × total activity
```

Efficiency improves the first term. Jevons Paradox asks whether the second term grows enough to offset the improvement.

For example, suppose an API call used to cost 10 units of energy and now costs 4. If usage stays fixed at 1,000 calls, total energy drops from 10,000 to 4,000. But if the lower cost causes usage to rise to 3,000 calls, total energy becomes 12,000. The system is more efficient per call and yet uses more energy overall.

This does not mean efficiency is bad. In many cases efficiency is necessary and beneficial. The lesson is that efficiency by itself is not a guarantee of lower aggregate usage. If your goal is absolute reduction, you must pair efficiency with some mechanism that limits or guides total demand.

In engineering organizations, that can mean:

- setting workload budgets,
- defining hard capacity limits,
- pricing internal resource use,
- measuring total demand after optimization,
- forecasting induced demand before rollout,
- and evaluating whether new efficiency enables product expansion.

So the practical takeaway is not "don't optimize." It is "optimize with a system model." If you only track the efficiency gain and ignore induced demand, you can misread the business, infrastructure, or environmental outcome.

## Training Exercise

Build a simple rebound model in a spreadsheet or a short script to see when efficiency decreases total usage and when it increases it.

### Goal
Model how a drop in per-unit resource cost changes total consumption when demand grows.

### Steps
1. Pick a resource-driven activity, such as API inference calls, vehicle miles, or video streaming hours.
2. Define a baseline:
   - resource per unit: `R0`
   - number of units consumed: `U0`
   - total resource use: `T0 = R0 * U0`
3. Define an efficiency improvement:
   - new resource per unit: `R1 = R0 * efficiency_factor`
   - Example: a 40% improvement means `efficiency_factor = 0.6`
4. Define a demand response multiplier:
   - new usage: `U1 = U0 * demand_multiplier`
5. Compute new total usage:
   - `T1 = R1 * U1`
6. Vary `demand_multiplier` to find the break-even point where `T1 = T0`.
7. Write 3-5 sentences explaining whether your example shows no rebound, partial rebound, or a Jevons-style increase.

### Example Python snippet
```python
R0 = 10      # resource units per task
U0 = 1000    # tasks
T0 = R0 * U0

for demand_multiplier in [1.0, 1.2, 1.5, 2.0, 3.0]:
    R1 = R0 * 0.4   # 60% more efficient
    U1 = U0 * demand_multiplier
    T1 = R1 * U1
    print({
        "demand_multiplier": demand_multiplier,
        "baseline_total": T0,
        "new_total": T1,
        "change_pct": round((T1 - T0) / T0 * 100, 1)
    })
```

### Stretch task
Apply the same model to an engineering scenario you know well, such as LLM inference, CI builds, GPU training jobs, or mobile data usage. Then propose one policy or product constraint that would ensure total consumption actually falls even after efficiency improves.

## Test Yourself

<details><summary>How can an activity become more efficient while consuming more resources overall?</summary>

Efficiency reduces the resource required per unit, but the resulting lower cost can stimulate enough additional activity to offset that reduction. Total consumption rises when activity grows faster than resource use per unit falls.

</details>

<details><summary>What three layers should engineers examine when assessing a possible rebound effect?</summary>

They should examine unit economics, behavioral responses, and scale responses. Together, these reveal what became cheaper, how users may react, and whether the system may expand into more traffic, applications, or markets.

</details>

<details><summary>In the lesson&#x27;s model, what demand multiplier is the break-even point when the efficiency factor is 0.4?</summary>

The break-even demand multiplier is 2.5 because 0.4 × 2.5 = 1. Demand growth above 2.5 produces a Jevons-style increase in total resource use.

</details>

## Further Reading

- [Jevons paradox - Wikipedia](https://en.wikipedia.org/wiki/Jevons_paradox)
- [The Coal Question by William Stanley Jevons](https://archive.org/details/coalquestionanin00jevouoft)
- [Rebound Effect - The Economist](https://www.economist.com/the-economist-explains/2018/03/07/what-is-the-rebound-effect)
- [Energy Efficiency and the Rebound Effect - International Energy Agency](https://www.iea.org/topics/energy-efficiency)
