# autonomy & health monitoring

## goal
two related sub-problems under one umbrella, both mapping directly to NASA's "Autonomous Systems" category (robotics, automated systems, **systems health monitoring**):

1. **state estimation** — how confidently does the spacecraft know its own position/velocity, given noisy sensors?
2. **fault detection & mode management** — when a sensor or actuator degrades, detect it and switch behavior (a lightweight FDIR: Fault Detection, Isolation, and Recovery), instead of the control loop confidently acting on bad data or a dead thruster forever.

this is also where the "vehicle management" category you flagged actually lives in this project — mode transitions (nominal → safe mode → recovering) are a small-scale version of the command-sequencing/mode-management work real C&DH software does. it doesn't need its own doc; it's phase 3 here.

## real-world reference points
worth reading the code of, not just the docs of, once you're past phase 1: [ProgPy](https://github.com/nasa/progpy) (NASA's prognostics/health-management python library, 2024 NASA software of the year — directly this problem, in python), and the JPL-MLIA repos for how a real lab structures fault-related ML tooling.

## how we're working this one
same pattern as the other docs: plan + progress log here, i review and explain, you implement.

## phase 1 — state estimation (no sim dependency, can start immediately)
- [ ] hand-write the linear Kalman filter equations yourself first (predict + update, maybe 20 lines of matrix algebra) against **synthetic** data: a known trajectory plus injected Gaussian measurement noise
- [ ] verify the filter's estimate tracks closer to ground truth than the raw noisy measurement does, and that its uncertainty (covariance) shrinks as expected
- [ ] once the linear KF is solid and understood, decide whether an Extended or Unscented KF is warranted (needed if the measurement or motion model you end up using is nonlinear — likely once this connects to the camera-relative frame from `sim-loop.md`) — `filterpy` is a reasonable library once you're past hand-rolling

**why hand-roll first:** same reasoning as the orbital propagator — a KF from a library that "just works" teaches you nothing about why it diverges when you feed it bad data later. write it once yourself.

**resources:** Dan Simon, *Optimal State Estimation* (rigorous, standard reference). filterpy's own docs/examples are a fine practical companion once the theory is in place.

## phase 2 — fault injection + detection (needs `sim-loop.md` closed)
this phase needs an actual running loop to inject a failure into — there's nothing real to detect a fault *in* until then.
- [ ] define a small, explicit set of fault modes to start: a thruster stuck/off, a camera dropout or noise spike
- [ ] detection via residuals, not ML, to start: commanded vs. actual velocity mismatch beyond a threshold flags a thruster fault; the Kalman filter's innovation (measurement vs. prediction residual) blowing up flags a sensor fault
- [ ] this threshold/residual-based approach isn't a simplification you'll throw away later — it's genuinely how a lot of real FDIR starts, before anything model-based

## phase 3 — mode management
- [ ] a small explicit state machine: `NOMINAL → SAFE → RECOVERING → NOMINAL`
- [ ] define what each mode actually changes (e.g. SAFE = hold last known-good state, only accept minimal commands, ignore the degraded sensor/actuator)
- [ ] log every mode transition — extend the existing `docs/performance_log.json` pattern rather than inventing a new logging mechanism

## phase 4 — prognostics (stretch, do not start before 1–3 are solid)
- [ ] predict degradation *before* failure (e.g. a thruster trending toward reduced efficiency) rather than only reacting after a fault crosses a threshold — this is what ProgPy actually targets, and is a meaningfully harder problem than phases 1–3

## progress log
- 2026-07-21: doc written, no implementation started yet. phase 1 is unblocked and can start any time; phase 2 is blocked on `sim-loop.md` phase 2/3.
