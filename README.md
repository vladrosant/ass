# autonomous spacecraft safety

**this is an ever work in progress**

## introduction
ass is a study created to develop autonomous, safe spacecraft control.
the project is a combination of image processing and ai.

## project status
**implemented:**
- edge detection benchmarking (canny, sobel, laplacian of gaussian) against sample debris images, with processing-time logging and comparison charts.
- a heuristic centroid-based maneuver suggestion (`src/run_avoidance_system.py`): detects the largest edge contour and suggests a move direction relative to image center.

**planned, not yet implemented:**
- cnn-based object classification (a model architecture exists in `src/obj_classification.py` but is untrained, with no dataset or training pipeline)
- rnn-based trajectory prediction
- reinforcement learning avoidance policy
- fault-tolerant / thruster-failure handling
- gazebo simulation integration (`src/avoidance_world.sdf` is a minimal stub world, not yet wired to the python code)

## development
```
pip install -r requirements.txt
pip install pytest
pytest
```

## key features
- **edge detection**: compares the utilization of canny, laplacian of gaussian and sobel algorithms to detect object boundaries, differentiating obstacles from the space background.
- **object detection and classification**: employs convolutional neural networks (cnns) to classify objects based on shape, size, and velocity.
- **optical flow**: analyzes pixel movement across sequential images to track debris motion, predicting future paths.

## artificial intelligence approaches
- **convolutional neural networks (cnns)**: high accuracy and speed in classifying space debris.
- **recurrent neural networks (rnns)**: predict future positions of debris based on current trajectories.
- **reinforcement learning (rl)**: optimal avoidance strategies through simulation of various scenarios, enhancing energy-efficient and safe maneuvers.

## redundancy and failure handling
to ensure robustness, the system incorporates a fault-tolerant control strategy that adjusts movements based on operational thrusters. ai models trained with simulated failures ensure that the spacecraft can safely maneuver even with partial system failures.

## planned simulation and testing
validation of the proposed system is conducted through simulations using opencv for real-time image processing and tensorflow for ai modeling. a test environment in gazebo simulates various debris fields, spacecraft trajectories, and failure modes.

### simulation details
- varying densities and velocities of debris.
- measurements of response time, energy efficiency, and collision avoidance accuracy.
- redundancy tests by disabling thrusters and sensors to observe ai adaptation.

## references
- [esa space debris office](https://www.esa.int/Enabling_Support/Operations/Ground_Systems_Engineering/ESA_Space_Debris_Office)
- [phys.org: algorithms for autonomous spacecraft safety](https://phys.org/news/2024-08-algorithms-autonomous-spacecraft-safety.html)
- [science.org: scirobotics](https://www.science.org/doi/10.1126/scirobotics.adn4722)
