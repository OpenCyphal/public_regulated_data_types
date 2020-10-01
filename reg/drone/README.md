# Drone

This namespace contains the application-specific regulated DSDL namespace for aerial vehicles.
If you have any questions, feel free to bring them to the [UAVCAN Forum](https://forum.uavcan.org/c/sig/drone-sig/17).

This namespace contains two nested namespaces:

- `physics` -- abstract physical processes and states in the system.
- `service` -- narrowly specialized types for common device classes.

The motivation for such design is provided in [The UAVCAN Guide](https://uavcan.org/guide),
chapter "Interface Design Guidelines".

The value of this or any other interoperability standard is in enabling compatible, composable, and extensible
complex systems.
A design that does not put these capabilities above the resource utilization concerns would defeat the purpose
of the standard.
Hence, when designing a new network service, put the clarity of your models first, then think about their performance
implications.
