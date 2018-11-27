Standard DSDL definitions
=========================

[![Build Status](https://travis-ci.org/UAVCAN/dsdl.svg?branch=master)](https://travis-ci.org/UAVCAN/dsdl)

This repository contains the DSDL definitions of the standard UAVCAN messages and services.
It is intended for inclusion as a submodule into implementations of the UAVCAN protocol stack.

UAVCAN is an open lightweight protocol designed for reliable communication in aerospace and robotic applications via
robust vehicle bus networks.

* [**UAVCAN website**](http://uavcan.org)
* [**UAVCAN forum**](https://forum.uavcan.org)

## Identifier ranges

### Subjects

For message subjects, the following range mapping is adopted (limits inclusive).
Unused ranges are reserved for future expansion of adjacent ranges.

From    | To        | Purpose
--------|-----------|------------------------------------------------
0       | 32767     | Application-specific unregulated identifiers (freely chosen by the integrator)
57344   | 59391     | Vendor-specific regulated identifiers (the definitions are stored in a public repository)
62804   | 65535     | Standard regulated identifiers

### Services

For services, the following range mapping is adopted (limits inclusive).
Unused ranges are reserved for future expansion of adjacent ranges.

From    | To        | Purpose
--------|-----------|------------------------------------------------
0       | 127       | Application-specific unregulated identifiers (freely chosen by the integrator)
256     | 319       | Vendor-specific regulated identifiers (the definitions are stored in a public repository)
384     | 511       | Standard regulated identifiers

## Standard static identifier allocation

### Subjects

Ordered by priority from high to low.

Namespace                   | Lower bound (inclusive)
----------------------------|-------------------------
`uavcan.time`               | 62804
`uavcan.node`               | 62805
`uavcan.pnp`                | 62810/65533
`uavcan.internet`           | 65510
`uavcan.diagnostic`         | 65520

### Services

Ordered by priority from high to low.

Namespace                   | Lower bound (inclusive)
----------------------------|-------------------------
`uavcan.register`           | 384
`uavcan.pnp`                | 390
`uavcan.file`               | 400
`uavcan.node`               | 430
`uavcan.internet`           | 500
`uavcan.time`               | 510

## Generic data type definitions

### SI

The namespace `uavcan.si` contains a collection of generic data types describing commonly used
physical quantities.

Some of the messages are time stamped, in which case the time stamp is always situated at the end in order
to facilitate binary compatibility with non-timestamped messages (both time-stamped and non-time-stamped
messages have identical headers, so if the time stamp is not required they can be used interchangeably).
Names of the time stamped messages have the suffux `TS`.

All units follow the [International System of Units](https://en.wikipedia.org/wiki/International_System_of_Units).
All units are unscaled basic units of measure (e.g., meters rather than kilometers, kilograms rather than milligrams),
unless a different multiplier is explicitly specified in the definition (e.g., nanosecond).

All coordinate systems are right-handed.
In relation to body, the preferred standard is as follows: **X** -- forward, **Y** -- right, **Z** -- down.
In case of cameras, the following convention should be preferred: **Z** -- forward, **X** -- right, **Y** -- down.
For world frames, the North-East-Down (NED) notation should be preferred.

Rotation and angular velocities are represented in fixed-axis roll (about X), pitch (about Y), and yaw (about Z).
Quaternions and other redundant representations are intentionally avoided due to bandwidth and latency concerns;
should they ever be used, the following element ordering should be adopted: W, X, Y, Z.

### Primitives

A collection of primitive data types is intended as a very generic solution for odd use cases
and prototyping. They permit the user to broadcast a completely arbitrary value via the bus
while not having to deal with custom data type design and distribution.

Since these types lack any semantic information, their usage in production environments is discouraged.

Another important application of these types is in the schemaless register protocol defined
in the namespace `uavcan.register`.

### Registers

The register protocol provides a highly generic interface to vendor-specific functionality
and configuration parameters via named registers.

## Guidelines for data type authors

In order to maximize compatibility with resource-constrained nodes,
standard messages should not be larger than 366 bytes when serialized.
The number is dictated by the size of the largest data structure, which is the response part of the service
`uavcan.node.GetInfo`.

Follow the naming conventions defined in the specification.

Every data type definition must have a header comment, where the first and the last lines are empty;
every field must be preceded by a comment, unless it is absolutely certain that it is completely
self-explanatory.
An exception is made for highly generic definitions which often do not require any additional comments.

Attributes must be separated by exactly one blank line, excepting tightly related attributes and
void fields used for pre-alignment (e.g., before dynamic arrays), in which case blank lines are not necessary.
More than one blank line is never allowed.
There must be exactly one blank line at the end of the file.

The lines of text must not be longer than 120 characters.

Here is an example:

    #
    # This is a header comment.
    # It explains what this data type definition is for and why do we need it.
    # Mind the empty lines before and after the header comment.
    #

    # This space is reserved for future use.
    void42

    # This is an enumeration.
    # We don't need blank lines because the items are tightly related.
    uint8 VALUE_A = 1       # A comment describing the constant.
    uint8 VALUE_B = 2       # Another one.
    uint8 value

    # This is a new field, mind the blank line above.
    void1
    float32[<100] aligned_array

Remember, the set of standard data types is an important part of the protocol specification,
so the quality of the documentation is very important.
