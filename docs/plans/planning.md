# plans

one file per initiative. each file holds the plan (phases, concepts, resources) and a running progress log (dated entries, checkboxes). update the checkboxes and log as work actually happens, don't rewrite history.

## architecture: three layers

as of 2026-07-21, `ass` is organized as a small onboard autonomy stack — loosely mirroring how a real spacecraft splits guidance, perception, and fault management into semi-independent subsystems:

| layer | question it answers | doc | depends on |
|---|---|---|---|
| strategic (orbital) | given two propagated orbits, is a conjunction coming, and does it warrant a maneuver? | [orbital-mechanics.md](orbital-mechanics.md) | nothing — pure math, no sim required |
| tactical (perception) | given a close-range camera frame, which way do i dodge right now? | [sim-loop.md](sim-loop.md) | nothing — already in progress |
| autonomy / health | do i trust my own sensors and actuators, and what mode should i be in? | [autonomy-health.md](autonomy-health.md) | state estimation half: nothing. fault/mode-switching half: sim-loop closed |
| decision optimization | what's the best maneuver policy when actuators are degraded and the future is uncertain? | [rl-avoidance-policy.md](rl-avoidance-policy.md) | sim-loop closed **and** autonomy-health's fault modes defined |

these are intentionally loosely coupled — orbital mechanics doesn't need gazebo, state estimation doesn't need orbital mechanics. work them in whatever order interest/time allows, respecting the dependency column. the one real coupling point is documented as phase 5 of `orbital-mechanics.md`: a conjunction event from the strategic layer eventually seeds the scenario the tactical layer reacts to.

"vehicle management" (command sequencing, safe-mode transitions) — one of the NASA software categories flagged as interesting — isn't a separate doc. it's the mode-management phase of `autonomy-health.md`. no need for a fifth doc to cover it.

## suggested working order

not a hard sequence — the dependency column above is the only real constraint. but given one person working roughly one thing at a time, this is the order that manages risk best:

1. **start `sim-loop` phase 0 (environment) first**, even if you don't finish it in one sitting. it's the slowest thing to de-risk (unknown ros2-on-debian friction) and it blocks the most downstream work (`autonomy-health` phase 2+, all of `rl-avoidance-policy`). better to hit that friction early than discover it months from now when everything else is finally ready and stuck behind an unresolved vm issue.
2. **use `orbital-mechanics` and `autonomy-health` phase 1 as fallback tracks** whenever phase 0 stalls or you want a change of pace — both are pure math, zero environment dependency, and can be picked up in either order or interleaved freely.
3. once the environment is confirmed working, push `sim-loop` through phases 1-2 (camera + node) — this is the one that, once closed, unlocks everything else.
4. with the loop closed, `autonomy-health` phases 2-3 (fault injection, mode state machine) become available.
5. `rl-avoidance-policy` last, once fault modes exist to train a policy against.

the rule of thumb: the sim-loop environment work should never be the *only* thing in flight, because it's the one track whose timeline is genuinely unpredictable.

## initiatives

| initiative | status | doc |
|---|---|---|
| close the sim loop | in progress (phase 0 not yet started) | [sim-loop.md](sim-loop.md) |
| orbital mechanics (propagation + conjunction assessment) | not started, unblocked | [orbital-mechanics.md](orbital-mechanics.md) |
| autonomy & health monitoring (state estimation + fault management) | not started, phase 1 unblocked | [autonomy-health.md](autonomy-health.md) |
| rl avoidance policy | blocked on sim-loop + autonomy-health | [rl-avoidance-policy.md](rl-avoidance-policy.md) |

## parked

- **cnn debris classification** (`src/obj_classification.py`): a model architecture exists but has never been trained — no dataset, no training loop. classification doesn't unlock anything the other initiatives need (reactive avoidance only needs "where's the edge," not "what is it"), and a debris-image dataset good enough to train on doesn't obviously exist. leaving the file as-is rather than carrying it forward as a false "planned" item. revisit if a real or synthetic dataset shows up, or a concrete use for the classification output appears (e.g. distinguishing debris from a cooperative object, once proximity operations become a topic).
- **rnn trajectory prediction**: superseded by the orbital-mechanics propagator for anything beyond the very short camera-relative horizon — a physics-based propagator will outperform a learned model at this scale of data, and it removes a training-data dependency the rnn approach never had a real answer for.
