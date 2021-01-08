# Kinematic states

This namespace contains data types that model basic [kinematic](https://en.wikipedia.org/wiki/Kinematics) states.

A full kinematic state of a rigid body or fluid includes its position, velocity, acceleration, and orientation.
The data types contained here model either full or partial kinematic states (e.g., there are types for velocity only).

Forces acting on the body or fluid are part of its *dynamic* state, so they are excluded from the model.
