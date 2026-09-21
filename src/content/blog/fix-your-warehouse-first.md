---
title: "Before you buy AI, fix your warehouse"
description: "A demo warehouse with one missing filter reports 2023 revenue 20.76% too high, and the assistant reading it is not at fault. What a year of pipeline work taught me about what AI-readiness actually means."
pubDate: 2026-09-21
tags: [data, engineering, ai, build-years]
demo: https://github.com/tdesmedt-tdsgn/labs/tree/main/fix-your-warehouse-first
businessNote: "Most of what gets sold as AI-readiness is ordinary data discipline, and you can check whether you have it without a budget line. Ask your data lead three questions: what is the grain of our core tables, which tests would fail if that grain broke, and what happens to a dashboard when they do fail. If the third answer is that the dashboard keeps serving numbers, then your reporting and any assistant you put on top of it share the same failure mode, which is confident wrongness with no error message. Fixing that is weeks of unglamorous work by people you already employ, and it is the cheapest risk reduction available before an AI project starts. Buying a chat interface first does not skip the step, it just moves the discovery of the problem to a more embarrassing moment."
---

*Part of The Build Years series, about work from 2023.*

An assistant I built reports 2023 revenue as EUR 276,072.90. The real figure
is EUR 228,611.75. It is overstated by 20.76%, and nothing anywhere in the
system says so. No error, no warning, no null. The number arrives with two
decimal places and a clean regional breakdown, which is exactly what makes it
dangerous.

The assistant is not the problem. Its SQL is correct. I checked it by writing
the query generator to be deterministic, so the only variable left is the
warehouse underneath. The entire defect is one missing line in one model.

## The year I stopped believing in the AI part

2023 was a data platform year for me. Warehouses, orchestration, a lot of
pipelines, and a recurring conversation that went roughly: we would like to do
something with AI on this data. The honest answer was usually that the data
was not ready, which sounds like a stalling tactic, so I got better at
demonstrating it instead of asserting it.

The demonstration is always the same shape. Put a natural language interface
over a warehouse nobody has tested, ask it a question that a human already
knows the answer to, and watch it confidently disagree with the finance team.
The disagreement is never resolved in the AI layer, because the AI layer is
working correctly.

This costs money in a specific way. Bad data does not stop the meeting. It
produces a number that someone puts in a slide, and the cost lands weeks later
when a decision gets revisited and nobody can reconstruct which version of the
truth it was based on. An outage is cheap by comparison, because an outage is
visible.

## The bug is always the grain

The demo repo builds a small dbt project on DuckDB, with synthetic data, in
about a minute. The bug I planted is the most common one I have met in real
warehouses, and it is not exotic.

A CRM exports one row per customer *version*. When a customer changes region,
the old row stays and a new one is written with `is_current` set. The customer
dimension is supposed to reduce that to one row per customer. Here is the
entire fault, the `where` clause that is present in one build and absent in
the other:

```sql
select
    customer_id,
    region,
    valid_from
from {{ ref('stg_customers') }}
{% if var('scenario') == 'fixed' %}
where is_current
{% endif %}
```

Nine of sixty customers have moved at some point, so the dimension holds 70
rows for 60 customers. The revenue fact table then joins to it on
`customer_id`. That join is written correctly. It is correct code against an
incorrect table, and a join to a non-unique key fans out: 83 orders get
counted twice.

"Grain" is the jargon worth knowing here. It is the answer to "what does one
row of this table represent". Almost every silent warehouse error I have
chased was a table whose grain quietly stopped being what its name implied,
and every downstream join inherited the damage without complaint.

## Two kinds of test, and the one people skip

The dbt tests in the demo are ordinary: `unique` and `not_null` on the keys,
a relationship test, an accepted values test. Nine tests in total. They are
cheap, they are declarative, and three of them fail on the broken build.

The one that earns its place is different. It is a reconciliation test, and it
checks the thing a finance director would check by hand, which is that the
total coming out of the pipeline is still the total that went in:

```sql
with source_total as (
    select round(sum(amount_eur), 2) as total
    from {{ ref('stg_orders') }} where status = 'completed'
),
mart_total as (
    select round(sum(revenue_eur), 2) as total from {{ ref('fct_revenue') }}
)
select s.total, m.total, round(m.total - s.total, 2) as difference
from source_total s cross join mart_total m
where abs(s.total - m.total) > 0.01
```

Column tests check shapes. This one checks money. When it fails it does not
say "duplicate key", it says the mart is EUR 47,461.15 heavier than the source
it came from, and that is a sentence a non-technical stakeholder can act on.

The last piece is four lines, and it is the part most teams have not built. If
the warehouse tests failed, the assistant does not answer. It does not run the
query at all and then discard the result, because a partially rendered wrong
number still ends up in someone's screenshot. It refuses, and it names the
tests that failed.

## What I measured

Both builds, same question, same assistant. The full run is in the demo's
[RESULTS.md](https://github.com/tdesmedt-tdsgn/labs/blob/main/fix-your-warehouse-first/RESULTS.md).

| | broken | fixed |
|---|---|---|
| dbt data tests | 3 of 9 failed | 9 of 9 passed |
| answer | EUR 276,072.90 | EUR 228,611.75 |
| error against ground truth | +20.76% | exact |

The detail I did not expect is that the error is not a constant. Broken down
by region it ranges from +11.98% to +32.34% against that +20.76% total,
because a customer who moved has their revenue counted in both their old
region and their new one. There is no correction factor to apply afterwards.
You cannot discount the number by a fifth and move on.

I should be honest about the limits. This is one bug of one shape, on
synthetic data, with a seed file I wrote. The 20.76% is a property of that
file, not an industry statistic, and nine customers with history out of sixty
is a mild case rather than a worst one. Late-arriving data, timezone drift and
a source system quietly changing its semantics all produce wrong numbers that
sail through all nine of these tests. In this dataset the regional ranking
also happens to survive the corruption, which it would not always.

None of that weakens the point, because the point is not the magnitude. It is
that the magnitude was unknowable from the inside. Every component was
behaving exactly as written.

## What this means for an AI budget

The useful reframing is that an AI assistant is not a new risk. It is a much
faster way to distribute a risk you already have. Your existing dashboards
have been reading the same tables, just more slowly and in front of fewer
people.

So the readiness question is not whether your data is clean. It is whether you
would find out if it were not. Nine declarative tests and one reconciliation
check took an afternoon here, and they are the difference between a wrong
number and a failed build.

If you are scoping an AI project on top of a warehouse nobody tests, the
warehouse is the project. Working on something similar, or disagreeing with
me? tom@tdsgn.be.
