# rl avoidance policy

## status: blocked
don't start this one yet. it needs both:
- `sim-loop.md` closed (an actual environment to train against)
- `autonomy-health.md` phase 2 (defined fault modes) far enough along to give the policy something harder than "move toward the target"

training RL against a plain "center the box" environment is a toy — the interesting, portfolio-worthy version of this problem is a policy that stays robust when actuators are degraded, which is exactly what the fault modes from `autonomy-health.md` provide. this doc exists now so the dependency and the eventual shape of the problem are written down, not because there's anything to implement yet.

## goal, once unblocked
learn a maneuver policy that performs well under uncertainty and degraded actuators — not just avoidance in the nominal case, which the existing heuristic (`compute_move_direction`) already handles reasonably.

## planned approach
- [ ] wrap the closed ros2/gazebo loop as a `gymnasium` environment (the standard RL environment interface — worth doing even though it's some boilerplate, since it makes the environment reusable with any standard RL library)
- [ ] start with a simple reward: some combination of minimizing collision risk / maintaining safe separation / minimizing fuel (thruster command magnitude)
- [ ] **establish a classical baseline before training anything** — run the existing heuristic avoidance logic through the same environment/reward and record its performance. without this, "the RL policy works" has nothing to be compared against
- [ ] train with a modern default algorithm — PPO or SAC via `stable-baselines3` is a reasonable starting point, not because it's the only option but because it's well-documented and hard to misuse
- [ ] evaluate specifically on the fault-mode scenarios from `autonomy-health.md`, not just the nominal case — that comparison (baseline vs. RL, nominal vs. degraded) is the actual result worth writing up

## an open decision, not urgent yet
`stable-baselines3` is pytorch-based. the existing (untrained, unused) CNN in `src/obj_classification.py` is tensorflow/keras. that's fine to leave unresolved for now — nothing forces a single deep learning framework across independent components — but worth a deliberate call when this phase actually starts, rather than accumulating a second framework by accident.

## resources
`gymnasium` docs, `stable-baselines3` docs, OpenAI's *Spinning Up in Deep RL* if you want the theory tightened up beyond what the Cloudwalk/Unitree work already covered.

## progress log
- 2026-07-21: doc written to record the dependency and shape of the problem. not started, not startable yet.
