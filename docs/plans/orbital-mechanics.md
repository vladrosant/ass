# orbital mechanics (strategic layer)

## goal
answer one question with real physics instead of hand-waving: **given the propagated orbits of the spacecraft and a debris object, is a conjunction (close approach) coming, and does it warrant a maneuver?**

this is deliberately separate from the existing vision pipeline. the camera/edge-detection code answers "which way do i dodge *right now*, given what's in front of the camera" — a close-range, reactive problem in pixel/relative space. orbital mechanics answers a longer-horizon, strategic question in absolute orbital-element space: two different problems, two different math toolkits, and they don't need to know about each other until phase 5.

## why this track, and why now
this is the piece that's actually "astrodynamics," not computer vision wearing a space costume. it has zero dependency on gazebo/ros2 being installed, so it can be worked in parallel with `sim-loop.md` whenever the vm/ros2 side stalls on setup friction. it's also the most direct application of the fundamentals (kepler, two-body problem, orbital elements) worth studying independent of this repo.

## how we're working this one
same pattern as `sim-loop.md`: this doc is plan + progress log, i act as reviewer/mentor (explain concepts, sanity-check the math, review code you paste in), you write the propagator and tests. check off boxes and add dated log entries as you go.

## a library note before you start
**poliastro is archived** (unmaintained since october 2023) — don't build on it. the maintained fork is [**hapsira**](https://github.com/pleiszenburg/hapsira) (same api lineage, active releases). `astropy` (time systems, reference frames, units) is still the right dependency for the parts hapsira builds on.

that said — **write the two-body propagator by hand first**, in plain numpy, before reaching for hapsira. the two-body problem is one ODE and maybe 30 lines of integration code; hand-writing it and checking it against analytic invariants (energy, angular momentum conservation) builds the intuition that using a library from day one skips entirely. bring hapsira in once you want perturbations, orbital-element conversions, or want a second implementation to cross-check yours against — not as the first thing you type.

## phase 0 — concepts
- [ ] kepler's three laws, the two-body problem, the vis-viva equation
- [ ] classical orbital elements (a, e, i, Ω, ω, ν) and what each one physically means
- [ ] frames: what "inertial" vs "relative/rotating" frame means here, and why conjunction assessment needs a consistent one

**resources:** Curtis, *Orbital Mechanics for Engineering Students* (best entry point, does the derivations without assuming you already know them). Bate/Mueller/White, *Fundamentals of Astrodynamics* (denser, the classic reference once Curtis feels too slow).

## phase 1 — hand-rolled two-body propagator
- [ ] state vector representation: position `r` and velocity `v` (3-vectors)
- [ ] the two-body equation of motion (`r'' = -mu * r / |r|^3`) integrated numerically — `scipy.integrate.solve_ivp` is fine, or hand-rolled RK4 if you want the extra rep
- [ ] verification, not just "it runs": propagate a known circular/elliptical orbit and confirm specific energy and angular momentum stay constant over the integration window, and that the period matches the analytic Kepler-orbit formula
- [ ] pytest coverage in the same style as the existing tests (`tests/test_navigation.py`) — pure functions in, numeric assertions with a tolerance out

**why the verification step matters:** a propagator that "looks plausible" but silently violates conservation laws is worse than no propagator — it'll produce confident-looking wrong answers three phases from now. catch it here while it's cheap to catch.

## phase 2 — orbital elements ↔ state vector
- [ ] conversion functions both directions: classical elements → (r, v) and back
- [ ] cross-check against hapsira for the same inputs — this is the first point where the library earns its place, as a second opinion on your own math, not a replacement for it

## phase 3 — perturbations
space debris is overwhelmingly a LEO problem, so this isn't optional polish — J2 dominates over pure two-body in LEO on timescales of hours to days.
- [ ] J2 zonal harmonic perturbation added to the propagator
- [ ] (optional, only if you want to push realism further) simple atmospheric drag model

## phase 4 — conjunction assessment
- [ ] given two independently propagated trajectories (spacecraft + debris object) over a shared time window, compute time of closest approach and minimum separation distance — `scipy.optimize.minimize_scalar` over a relative-range function is a reasonable starting approach
- [ ] a simple distance-threshold flag ("conjunction warning if minimum separation < X km") before anything fancier
- [ ] optional stretch, not required for this phase to be "done": a real collision-probability estimate (e.g. Foster/Alfano-style Pc) — this requires covariance propagation and is a legitimate rabbit hole; don't let it block the rest of the plan

## phase 5 — bridge to the tactical layer
- [ ] once both this and `sim-loop.md` are far enough along: take a conjunction event's relative position/velocity at a chosen point in the encounter and use it to generate spawn parameters for `avoidance_world.sdf` (or a generated variant of it) — this is the actual integration point between the two layers, and it's what turns "two unrelated toy simulations in one repo" into "a strategic layer handing a realistic scenario to the tactical layer"

## progress log
- 2026-07-21: doc written, no implementation started yet.
