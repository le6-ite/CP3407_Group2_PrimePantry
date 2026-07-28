# User story 04: Weekly order window & cutoff (USP)

*As a customer, I want to see when this week's ordering window closes so that I order in time to
be included in the group buy.*

## Priority: P1 (highest) — Iteration 1 · **Unique selling point**
This is the group-buying mechanic that defines the product (orders are pooled per window and
sourced against demand, not stock).

## Estimation: 1.0 day
Planning poker:
* Eti: 1 day
* Kei: 1 day
* **Agreed: 1.0 day**

## Assumptions
* The window closes every **Wednesday at 18:00, Australia/Brisbane**.
* The countdown is computed server-side and ticks client-side.

## Description
A banner on every inner page (and the home hero) shows *"Window closes Wed 6:00 PM · Xd Yh Zm
left"* with a live countdown. Each order records the cutoff it belongs to (`Order.round_cutoff`),
which later drives the admin quantity aggregate (story 07).

## Tasks
1. `next_cutoff()` / `cutoff_label()` / `countdown_text()` helpers (utils), 0.4 d
2. Order-window banner partial + context processor, 0.3 d
3. Live countdown JavaScript, 0.3 d

## UI design
INO mock-up. Live on every page, e.g. the banner at `http://147.93.56.126:8080/catalog/`.

## Completed
✅ Iteration 1. Timezone set to Australia/Brisbane; `round_cutoff` stamped on every order in
Iteration 2.
