# UDRAL
This namespace contains message definitions, usage guidelines and best practices,
and other documentation relating to the UAVCAN DRone Application Layer Specification (UDRAL). The specification defines the application layer for applying UAVCANv1 to unmanned (and potentially manned) aerial vehicles, including multirotors and fixed wing aircraft.

## Design philosophy and goals
UDRAL is designed per the following goals:
* Robust interoperability between hardware supplied by different vendors
* A bandwidth-efficient message set that allows satisfactory operation on a Classic CAN bus (1mbit/s) for simple/standard use cases. Note that more demanding network setups may require the use of CAN-FD if bandwidth becomes a problem. See the `Transports & bandwidth utilization` section for more details.
* Plug-and-Play operation for standard use cases out of the box.
* A simple to understand, semantic yet flexible message set.

## Transports and bandwidth utilization
UDRAL is primarily designed to be used over a Controller Area Network (CAN) bus as this is the most common transport found on unmanned aerial vehicles. However, it should work on other transports as well, including Ethernet-based networks.

UDRAL is designed to be able to accomodate standard (simple) network designs on a Classic CAN bus. However, in certain cases, it chooses to optimize for composability and reusability rather than network efficiency. As such, more complex network designs may require the use of CAN FD (4mbps+, MTU ~64 bytes) if increased bandwidth is required. This is not considered to be a problem since it is expected that in the foreseeable future, vehicles will start leveraging more capable transports (including UAVCAN/CAN FD, UAVCAN/UDP over Ethernet, UAVCAN/Serial over RS-422 or USB, etc).

The following documents are provided to help the integrator analyze bandwidth usage:
[UDRAL bandwidth validation: Classic CAN](https://docs.google.com/spreadsheets/d/1kFx1hupmQrzEaEnaTDngViIM4W9Xd9Oq2I_2sb6320Q/edit#gid=787650889)
[UDRAL bandwidth validation: CAN FD](https://docs.google.com/spreadsheets/d/1GqZe3HzGumPf0zEKZv5BEdcqg2CAh-YjcYwV6i5bNX8/edit#gid=0)

## Service classes
UDRAL defines a set of service classes. Each service class provides a set of standard (required and optional) APIs, messages, and registers implemented by devices on a UDRAL network. All fields should be in SI units unless otherwise specified or not applicable.

Service classes are segregated by semantic function, not physical device. A physical electronic device implementing UDRAL may choose to implement one or more service classes. For example, a standard "GNSS Puck" designed for use on UAVs may implement the GNSS class (`sensor.gnss`) and the Arming Mechanism class (`control.arm_authorization`).

Each service class is referred to with a two part name: a "class group" and "class function".
Class groups are chosen from the following:
* `network`: the network class includes services meant to keep the UDRAL network operational. These classes are often implemented on network nodes that implement other services as well.
* `control`: the control class includes services that carry out logical reasoning, navigation, planning, fault handling, control, etc.
* `sensor`: the sensor class includes services that provide data to the network, including position, attitude and heading references, air data, or system power information.
* `actuator`: the actuator class include sservices that control physical actions on a UDRAL power vehicle, including servo motors and electronic speed controllers (ESCs).
* `power`: the power class includes devices that provide power to the network, including batteries and fuel tanks.

## Namespace layout
### Physics namespace
The `physics` namespace contains messages to encapsulate many standard physical quantities, in scalar and vector, timestamped and non-timestamped combinations. These messages serve two main purposes:
1. Physics messages may be (and are often) embedded into service messages, to maximize composability/interoperability and enhance the semantic meaning of service messages.
2. Physics messages may be directly published on a port as directed by the service message. Examples of this include publishing telemetry and sensor data (`sensor` service class) if encapsulation of the message in a parent type is not necessary.
3. Physics message may be directly published by a vendor extension. While this is encouraged (over using custom vendor-specific data types), publications that are not governed by UDRAL service classes are not regulated and therefore not guaranteed to conform to the UDRAL specification.

### Services namespaces
The `services` namespace contains messages and documentation related to the various UDRAL service classes.
