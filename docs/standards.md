# The house standard

The frameworks in `drills/frameworks/` are one standard of our own. Outside standards are how it is
kept honest. This page is the rulebook for both.

## What the house standard is

- **One path.** Every objective has a position from counting to 100 onward, and its prerequisites
  come before it. A framework `requires` other frameworks; an objective `needs` other objectives.
- **Stable codes.** `HT-2.2.A` is framework, unit, topic, objective. A code is never reused for a
  different objective, because drill cards, streaks and worksheets hang off it.
- **One shape.** Big ideas, units, topics, objectives (one testable action each, verb first), the
  knowledge each rests on, and the practices it exercises. Every subject uses the same shape, which
  is what lets a sport, a language skill and thermodynamics sit in one system.
- **Drills answer to objectives**, never to books or outside codes directly.

## What an outside standard is for

An outside standard does three jobs, in this order of strength.

1. **Structure**: the units and their order come from it (AP course descriptions, Common Core).
2. **Coverage check**: its outline is listed item by item in `drills/standards.yaml`, objectives cite
   the items, and the report shows which items nothing answers to (the FE Chemical specification).
3. **Reference**: it is named as a source but nothing cites it item by item.

Kinds are not equal. A curriculum standard or exam specification says what to learn. A rulebook says
what is legal, a rubric how performance is scored, a textbook how one author ordered the material.
A framework resting on the last three has its unit order chosen by us, and the report says so.

## Rules

1. Every framework declares `basis.primary`, and optionally `also` and `wanted`.
2. A standard is `read: full` only if its own text was read. Through someone else's table is
   `crosswalk`; named but unopened is `none`.
3. Cite at the highest level that is true: on the unit if the whole unit answers to the item, else
   the topic, else the objective.
4. Objectives nothing outside asks for are **house only**. That is allowed, and it is where the house
   standard goes beyond its sources (graduate material past an exam specification, for example). It
   should be a decision, not an accident, so the report counts them per framework.
5. When a standard is outlined, its uncovered items are the to-do list for new objectives.

## Moving a framework onto a standard

1. Read the standard's own text. Add it to `drills/standards.yaml` with its outline.
2. Add `std` citations. Do not renumber existing objectives.
3. Read the report. Uncovered items become new objectives at the end of the right topic (new letters,
   so old codes stand). House-only objectives stay, with the note explaining why.
4. Only then set it as `basis.primary`, and move the old basis to `also`.

## Where things stand

See `docs/coverage/standards.md`, rebuilt on every `npm run skills`.
