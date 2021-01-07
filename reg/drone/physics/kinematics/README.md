# Kinematic states

This namespace contains data types that model basic [kinematic](https://en.wikipedia.org/wiki/Kinematics) states.

A full kinematic state of a rigid body or fluid includes its position, velocity, acceleration, and orientation.
The data types contained here model either full or partial kinematic states (e.g., there are types for velocity only).

Forces acting on the body or fluid are part of its *dynamic* state, so they are excluded from the model.

See UAVCAN Specification chapter "Application layer" for the applicable conventions.
Key excerpts:

- For world fixed frames, the North-East-Down(NED) right-handed notation is preferred:
  X – northward, Y – eastward, Z – downward.

- In relation to a body, the convention is as follows, right-handed: X – forward, Y – rightward, Z – downward.

- Angular velocities should be represented using the right-handed, fixed-axis (extrinsic) convention:
  X (roll), Y (pitch), Z (yaw).

- Matrices are represented in the row-major order.

- For NED frames, the initial (zero) rotation of a body is the state where the axes of the body frame are
  aligned with the axes of the local NED frame: X points north, Y points east, Z points down.
