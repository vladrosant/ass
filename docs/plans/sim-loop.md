# close the sim loop

## goal
right now `src/run_avoidance_system.py` is a one-shot script: it loads a static jpg, runs sobel edge detection once, prints a suggested direction, and exits. `src/avoidance_world.sdf` is a gazebo world with a ground plane, a sun, and one box — not connected to any of the python code.

"closing the loop" means: gazebo renders a camera view of a debris object, that frame streams out continuously, the existing avoidance logic decides a direction on each frame, and a velocity command streams back in and actually moves something in the sim. that's the difference between a demo script and a control loop.

## how we're working this one
this doc is the plan and the progress log. i (claude) keep it updated and act as reviewer/guide — explaining concepts, sanity-checking design choices, reviewing code you paste in — but you write the ros 2 nodes, sdf changes, and launch files yourself. check off boxes and add dated log entries as you go; that's the record of what actually happened, not just what was planned.

## environment
- gazebo runs on your existing debian vm, not wsl2/docker/windows.
- ros 2 bridges gazebo and python (over talking to gazebo transport directly) — it's the standard robotics middleware and the more transferable skill.
- **heads up before you install anything:** open robotics only publishes official ros 2 apt binaries for specific ubuntu releases, not debian. don't assume `apt install ros-*` works on a stock debian VM. the two reliable paths are:
  - **robostack** (conda/mamba-based ros 2 + gazebo, actively maintained, works well cross-distro including debian) — probably the least friction.
  - **docker** inside the vm (official ros/gazebo images) — more isolation, more reproducible, slightly more moving parts for gui forwarding.
  - building from source is the fallback if both of those hit a wall, but it's a much bigger time sink.
- check the current ros 2 <-> gazebo recommended pairing before picking versions (search "rep 2000 ros 2 distributions" for the current table) — both projects move fast enough that hardcoding a version here would go stale.

## phase 0 — environment stands up
- [ ] ros 2 installed on the debian vm (robostack or docker, your call)
- [ ] gazebo installed, `gz sim` (or `gazebo`, depending which major version you land on) launches an empty world with a gui you can see
- [ ] ros 2 demo works: `ros2 run demo_nodes_cpp talker` / `listener` (or the python equivalents) talk to each other
- [ ] `ros_gz` (or `ros_ign`, depending on version) bridge package installed

**why this phase matters:** everything downstream depends on this working. don't skip straight to writing nodes against a shaky install — confirm each piece independently first.

## phase 1 — a camera and a movable body in the world
- [ ] add a camera sensor to `src/avoidance_world.sdf` (or a new model referenced from it) — sdf `<sensor type="camera">`, with a sane resolution/fov for a debris-spotting camera
- [ ] add a simple movable body to represent the spacecraft (a velocity-controlled box/sphere is fine to start — this is about proving the loop closes, not modeling real spacecraft dynamics yet)
- [ ] bridge the camera topic and a velocity command topic through `ros_gz_bridge` so they show up as ros 2 topics
- [ ] verify: `ros2 topic echo` on the camera topic shows image messages; manually publishing a twist/velocity message on the command topic visibly moves the body in the gazebo gui

**concepts worth reading up on before writing sdf:** gazebo sensor plugins, the `ros_gz_bridge` topic mapping config format, `sensor_msgs/Image` vs gazebo's native image message type.

## phase 2 — the avoidance logic becomes a node
- [ ] write a ros 2 node that subscribes to the camera topic, converts each frame to a numpy array (`cv_bridge` handles the `sensor_msgs/Image` -> cv2 conversion), and reuses the existing pure functions as-is: `sobel_edge_detection.detect_edges`, `run_avoidance_system.calculate_object_center`, `run_avoidance_system.compute_move_direction`
- [ ] publish a velocity/twist command from `compute_move_direction`'s output on the bridged command topic
- [ ] verify end to end: put a debris-like object in view of the camera, launch world + bridge + node together, watch the body react

this is the payoff from the earlier refactor — those functions were extracted specifically so they could be called from something other than a `__main__` block reading a jpg off disk. if you find yourself wanting to copy-paste their logic instead of importing them, that's a sign the node is fighting the existing code shape rather than reusing it.

## phase 3 — polish
- [ ] one `ros2 launch` file that brings up world + bridge + avoidance node together
- [ ] clamp/rate-limit velocity commands so a bad frame can't send a huge command
- [ ] update the main readme's "project status" section once this phase is real
- [ ] optional stretch: log each maneuver decision somewhere (same spirit as `docs/performance_log.json`) so there's data to look at later, or visualize the detected centroid in rviz

## progress log
- 2026-07-16: plan written, environment decisions made (debian vm, ros 2). no implementation started yet.
