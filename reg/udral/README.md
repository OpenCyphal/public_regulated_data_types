# UDRAL

This namespace contains data type definitions, network service specifications, usage guidelines and best practices,
and other documentation relating to the UAVCAN DRone Application Layer Specification (UDRAL).
The specification defines the application layer for applying UAVCAN v1 to (un)manned aerial vehicles,
including multirotors and fixed wing aircraft.

The definitions are contained in two namespaces:

- `physics` -- abstract data types to encapsulate many standard physical quantities, in scalar and vector,
  timestamped and non-timestamped combinations.
- `service` -- narrowly specialized types for common applications.

## Design philosophy and goals

UDRAL is designed per the following goals:

- Modern, highly orthogonal, consumer-focused service-oriented architecture optimized for composability and reuse.
- Robust interoperability between hardware supplied by different vendors.
- Reasonable bandwidth efficiency that allows satisfactory operation on a Classic CAN bus at 1 Mbps in simple vehicles.
  Sophisticated deployments are expected to require a more capable transport, such as Ethernet or CAN FD.
- Plug-and-play (PnP) operation for simple use cases out of the box.

### Service-oriented architecture

The user of this standard is advised to get familiar with the basic principles of service-oriented design.
As a quick primer, [read Wikipedia](https://en.wikipedia.org/wiki/Service-oriented_architecture).
For a more in-depth review, please read the [UAVCAN Guide](https://uavcan.org/guide).

The value of this or any other interoperability standard is in enabling compatible, composable,
and extensible complex systems.
A design that does not put these principles above the resource utilization concerns risks defeating the purpose
of the standard.
Hence, when designing a new network service, put the clarity of your models first,
then think about their performance implications.

In service-oriented architectures, deciding what capabilities *not* to provide is just as important as
deciding what to include.
Imagine that in an aircraft you have an air data computer (not to be confused with a mere differential pressure sensor)
publishing the current airspeed estimate.
The air data computer is aware of the placement of the pitot probe and the local effects that may
influence its readings, so correcting for these effects is the task of the air data computer itself.
Therefore, the published airspeed should be the calibrated airspeed (CAS) rather than the raw
indicated airspeed (IAS).
The air data computer may require the ground speed estimate for calibration purposes,
in which case it is to subscribe to a ground speed topic published by another service (e.g., a GNSS receiver).
One might be tempted to enrich the service by providing the IAS alongside with CAS for the benefit of
the service consumer and for enhanced flexibility.
While easy to accomplish, it would be a design mistake because it might incentivize service consumers to
depend on the irrelevant implementation details of the service,
resulting in fragile architectures that are also hard to understand, maintain, and verify.
Encapsulation and interface segregation are just as important here as in software design.

Composability is desirable for high-integrity systems also because it facilitates subsystem isolation for
testing and confines changes to a smaller number of subsystems,
thus reducing the costs of validation and verification.

These design principles may constitute a departure from the practices commonly accepted in legacy systems,
which is necessitated by the increasing complexity of modern intravehicular software.

However, the above is not to say that this design has no place for simpler network services that merely produce data
without much processing (e.g., basic sensor nodes), as long as the core values of UDRAL are respected.

### Transports and bandwidth utilization

Being forward-looking, this design is optimized for transports that offer
the data rates of at least ~4 Mbps and the MTU of at least ~64 bytes.
It is expected that in the foreseeable future all new applications will be leveraging transports whose
data transfer capability is at this level or higher
(this includes, for example, UAVCAN/UDP over Ethernet, UAVCAN/CAN over CAN FD, UAVCAN/serial over RS-422 or USB, etc).

Note that UAVCAN v1 allows integrators to selectively disable irrelevant publications by reconfiguring the
appropriate port-ID registers (`uavcan.pub.*.id`), which is a powerful bandwidth management tool.

Applications relying on Classic CAN (maximum data rate 1 Mbps, MTU 8 bytes) can still deploy these network services,
but the designer needs to be aware that most transfers will be multi-frame transfers and the resulting bus utilization
may be comparatively high.
Multi-frame transfers are not expected to cause performance issues because the official
UAVCAN implementation libraries are optimized for handling multi-frame transfers efficiently.

The following resources are provided to help the integrator analyze bandwidth usage:

- [UAVCAN/CAN bandwidth validation: Classic CAN](https://docs.google.com/spreadsheets/d/1zjpdPfmBf9oje2qjLYddlhFfkaQuTJ-VvQjHxzITils/edit)
- [UAVCAN/CAN bandwidth validation: CAN FD](https://docs.google.com/spreadsheets/d/1iK0MegMuEC55c-zTW6ssWhrA_sGUuSlT0S26xv5gytE/edit)

## Typical applications

The definitions in the `service` namespace contain descriptions of some common use cases
that can be addressed with this standard.
Adopters are expected to mix and match various components to create new network services that were not originally
envisioned by the authors of this standard.
This is possible while retaining full vendor-agnostic compatibility thanks to the service composability capabilities
described earlier.

A practical hardware node would typically implement multiple services concurrently.
For example, a COTS (commercial off-the-shelf) electric drive may realistically implement the following:

- Naturally, the ESC service.
- The servo service for generality.
- Acoustic feedback by subscribing to `reg.udral.physics.acoustics.Note`.
- Visual feedback via the LED by subscribing to `reg.udral.physics.optics.HighColor`.

Another service that is interested in tracking the state of, say, a propeller drive
(say, for thrust estimation) would not need to concern itself with the ESC service at all.
Instead, it would simply subscribe to the generalized subject of type
`reg.udral.physics.dynamics.rotation.PlanarTs` published by the unit that drives the propeller
and extract its business-level information from that while being unaware of the specifics of the drive
(the propeller drive may be changed from an electric motor to a turboprop engine without affecting the
thrust estimation service).

As another example, a flight control unit would not need to depend on the specifics of a GNSS positioning
service to obtain the location of the vehicle.
Instead, it would subscribe to a generic subject of a highly abstract type that models the location of
the vehicle in space (along with other related information such as time and pose),
which may as well be published by a mocap rig.

## Port naming and auto-configuration

### Port name prefixes

In UAVCAN, the name of a port (i.e., subject or RPC-service) defines the names of related registers
as described in the documentation for the standard RPC-service `uavcan.register.Access`.
For instance, a node that publishes to the subject named `measurement` would have registers named
`uavcan.pub.measurement.id` and `uavcan.pub.measurement.type` (among others).

> N.B.: Contrary to other protocols, in UAVCAN, the name of a port is a node-local property that does not affect
  network exchanges over that port.
  This means that nodes can publish/subscribe to a port even if they name it differently
  as long as they are configured to use the same numerical port-ID.
  The details are given in the UAVCAN Specification.

Network service specifications given here under the `service` namespace provide the recommended names for
every defined port.
For example, the smart battery network service specification defines subjects named `status` and `parameters`.

Using the suggested names in practical implementations directly is not always possible because nodes that
implement different network services or multiple instances of the same service would see naming conflicts
(e.g., many services define a subject named `status`).
Hence, implementations are advised to use the recommended port names with an application-defined prefix
such that ports that relate to the same instance of a network service share the same prefix.

Imagine a node that implements two smart battery services (primary and secondary)
and a servo service (suppose we call it the main drive);
then it might have the following registers (among others):

    uavcan.pub.battery.primary.energy_source.id
    uavcan.pub.battery.primary.status.id
    uavcan.pub.battery.primary.parameters.id
    uavcan.pub.battery.secondary.energy_source.id
    uavcan.pub.battery.secondary.status.id
    uavcan.pub.battery.secondary.parameters.id
    uavcan.sub.main_drive.setpoint.id
    uavcan.sub.main_drive.readiness.id
    uavcan.pub.main_drive.feedback.id
    uavcan.pub.main_drive.status.id
    uavcan.pub.main_drive.power.id
    uavcan.pub.main_drive.dynamics.id

By virtue of such *semantic grouping* with shared prefixes, the registers clearly define three network services:

- `battery.primary`
- `battery.secondary`
- `main_drive`

The convention can be described in UML notation as follows:

    +-----------------------------------+
    |   Network service specification   |   E.g., the smart battery network service
    +-----------------------------------+   defined under reg.udral.service.battery
                    △ 0..*
                    ┆
                    ┆ implements
                    ┆
    +-----------------------------------+   Example group "battery.primary":
    |        Prefixed port group        |   - battery.primary.energy_source
    +-----------------------------------+   - battery.primary.status
                    │                       - battery.primary.parameters
                    │ has
                    │
                    ♢ 1..*
    +-----------------------------------+
    |             Port                  |
    |     (subject or RPC-service)      |
    +-----------------------------------+

Following this convention is highly recommended as it aids one's understanding of the node's functional capabilities
and may enable some systems to implement automatic assignment of port identifiers, as described next.

### Special registers for auto-configuration

A node can optionally permit automatic configuration of its port-ID registers (such as `uavcan.pub...`, etc.)
by providing special registers intended for this purpose.

#### UDRAL cookie register

The *cookie register* is a persistent mutable register named `udral.pnp.cookie` of type `string`.
Its default value is an empty string.

This register should not be modified by the node locally;
instead, it is intended for remote modification over the register access service during the automatic port-ID
assignment process.

The purpose of this register is to keep arbitrary state saved by an external node that is responsible for
automatic configuration of network participants.
For instance, on an UAV, the automatic configuration process may be carried out by the flight controller
or a mission computer.
The format and meaning of the stored string is entirely implementation-defined.

#### Network service discovery registers

In the example given earlier, we have a group of registers that define ports pertaining to two instances
of the standard UDRAL smart battery service and one instance of the standard UDRAL servo instance.
In order to enable automatic configuration of these services,
the node should announce the fact that they follow the UDRAL specification.
This is done with the help of the network service discovery registers.

A network service discovery register is an immutable persistent (i.e., constant) register of type `string`
that contains space-separated port name prefixes such as `battery.primary`, `main_drive`, etc.
The name of a service discovery register is the name of the DSDL namespace that contains the service definition.
For example:

- Register named `reg.udral.service.battery` is used to announce conformance to the UDRAL smart battery service.
- Register named `reg.udral.service.actuator.servo` --- UDRAL servo service.
- Register named `reg.udral.service.actuator.esc` --- UDRAL ESC service.

The following table shows the registers and their values that announce conformance with the relevant services.
Observe how the main drive group implements two distinct (but similar) services simultaneously.

Register name                    | Register type   | Value
---------------------------------|-----------------|-------------------------------------------
`reg.udral.srv.battery`          | `string`        | `battery.primary battery.secondary`
`reg.udral.srv.actuator.servo`   | `string`        | `main_drive`
`reg.udral.srv.actuator.esc`     | `string`        | `main_drive`

It is not necessary to include the leading and trailing name component separators `.` in the prefix names.
Registers that are not known to the auto-configuration authority are to be silently ignored,
which permits addition of implementation-defined ports without breaking compatibility with standard services.


#### Type signature register

In many use cases it is desirable to have the ability to statically check the compatibility between sender and
receiver of a message. This capability could be used both during automatic configuration and by manual configurator tools.
The design allows this by adding an optional register per port that contains a string _data type signature_.

    uavcan.pub.PORT_NAME.type_sig
    uavcan.sub.PORT_NAME.type_sig
    uavcan.cln.PORT_NAME.type_sig
    uavcan.srv.PORT_NAME.type_sig

Where `PORT_NAME` is a placeholder defined in the
[documentation for `uavcan.register.Access`](https://github.com/UAVCAN/public_regulated_data_types/blob/b02e6899a319ddefbab41b820d167c95dd00174d/uavcan/register/384.Access.1.0.uavcan#L136-L139).
For example: `uavcan.sub.main_drive.setpoint.type_sig`

Example signature would look like `(u12{u8}a5[f16]=i8)`, and be interpreted as

 - `()` delimit sealed type
 - `{}` delimit extensible type
 - `b`, `u`, `i`, `f`, `v` followed by size in bits encode primitive types
 - `a` and `A` followed by length in items and brackets encode variable and fixed size arrays
 - `=` marks byte alignment point

This is a draft and informal description which would likely change.
Sample proof-of-concept code that generates type string from DSDL and compares two strings for compatibility can be seen at this
(temporary) location: <https://gitlab.com/vadimz1/dsdl-sig-gen/-/tree/main>.


## Conventions

- Conventions defined in the UAVCAN Specification shall be followed.

- All physical quantities except error variance should be represented as `float32` by default.
  Error variance and covariance matrices should use `float16` by default.

- Covariance matrices should be represented as their upper-right triangles using the matrix packing rules
  defined in the Specification.

- Types with (co)variance should be suffixed `Var`; types with timestamp should be suffixed `Ts`;
  types with both should be suffixed `VarTs`.
  The timestamp field, if present, should be the first one;
  error (co)variance information should follow the data field(s) it relates to.

- Publishers of measurements or estimates should apply low-pass filtering to avoid frequency aliasing.
