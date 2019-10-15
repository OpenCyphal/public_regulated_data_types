Regulated DSDL definitions
==========================

[![Build Status](https://travis-ci.org/UAVCAN/public_regulated_data_types.svg?branch=master)](https://travis-ci.org/UAVCAN/public_regulated_data_types)
[![Forum](https://img.shields.io/discourse/https/forum.uavcan.org/users.svg)](https://forum.uavcan.org)

This repository contains definitions of the regulated UAVCAN data types.
[UAVCAN](http://uavcan.org) is an open lightweight protocol designed for reliable communication
in aerospace and robotic applications via robust vehicle bus networks such as CAN, Ethernet, and similar.
The name stands for *Uncomplicated Application-level Vehicular Communication And Networking*.

Regulated data types include the standard data types and vendor-specific public definitions.

Per the specification, standard data types are contained in the root namespace `uavcan`,
whereas vendor-specific public definitions are contained in separate appropriately named root namespaces
(e.g., `sirius_cyber_corp` for the Sirius Cybernetics Corporation).

Vendors seeking to make their data types regulated (e.g., for easier integration of their COTS equipment,
or if fixed port ID are desired) are advised to send a pull request to this repository.
If a fixed regulated ID is needed, vendors are free to choose any unoccupied identifier from the ranges
defined by the specification before submitting the pull request.

Contributors must obey the guidelines defined in this document.

Feedback and proposals are welcome on the [UAVCAN forum](https://forum.uavcan.org).

## Identifier ranges

Refer to the specification for background information and motivation.

### Subjects

For message subjects, the following range mapping is adopted (limits inclusive).
Unused ranges are reserved for future expansion of adjacent ranges.

From    | To        | Capacity | Purpose
--------|-----------|----------|-------------------------------------
0       | 24575     | 24576    | Unregulated identifiers
28672   | 29695     | 1024     | Non-standard (vendor-specific) regulated identifiers
31744   | 32767     | 1024     | Standard regulated identifiers

### Services

For services, the following range mapping is adopted (limits inclusive).
Unused ranges are reserved for future expansion of adjacent ranges.

From    | To        | Purpose
--------|-----------|------------------------------------------------
0       | 127       | Unregulated identifiers
256     | 319       | Non-standard (vendor-specific) regulated identifiers
384     | 511       | Standard regulated identifiers

## Standard data types

### Standard fixed identifier allocation

#### Subjects

Ordered by priority from high to low.

Namespace                   | Lower bound (inclusive)
----------------------------|-------------------------
`uavcan.time`               | 31744
`uavcan.node`               | 32085
`uavcan.pnp`                | 32740
`uavcan.internet`           | 32750
`uavcan.diagnostic`         | 32760

The value 32085 contains the longest possible sequence of alternating bits,
which can be leveraged for automatic bit rate detection (depending on the physical layer).

#### Services

Ordered by priority from high to low.

Namespace                   | Lower bound (inclusive)
----------------------------|-------------------------
`uavcan.register`           | 384
`uavcan.pnp`                | 390
`uavcan.file`               | 400
`uavcan.node`               | 430
`uavcan.internet`           | 500
`uavcan.time`               | 510

### Generic data type definitions

#### SI

The namespace `uavcan.si` contains a collection of generic data types describing commonly used
physical quantities.

All units follow the [International System of Units](https://en.wikipedia.org/wiki/International_System_of_Units).
All units are unscaled basic units of measure (e.g., meters rather than kilometers, kilograms rather than milligrams),
unless a different multiplier is explicitly specified in the definition (e.g., nanosecond).

All coordinate systems are right-handed.
In relation to body, the preferred standard is as follows: **X** -- forward, **Y** -- right, **Z** -- down.
In case of cameras, the following convention should be preferred: **Z** -- forward, **X** -- right, **Y** -- down.
For world frames, the North-East-Down (NED) notation should be preferred.

#### Primitives

A collection of primitive data types is intended as a very generic solution for odd use cases
and prototyping. They permit the user to broadcast a completely arbitrary value via the bus
while not having to deal with custom data type design and distribution.

Since these types lack any semantic information, their usage in production environments is discouraged.

Another important application of these types is in the schemaless register protocol defined
in the namespace `uavcan.register`.

#### Registers

The register protocol provides a highly generic interface to vendor-specific functionality
and configuration parameters via named registers.

## Non-standard regulated data types

Every vendor must have a dedicated root namespace.
The root namespace should be named after the vendor's legal entity name.

All root namespaces are contained in the root folder of this repository.

## Guidelines for data type authors

In order to maximize compatibility with resource-constrained nodes,
standard data structures should not be larger than 313 bytes when serialized.
The number is dictated by the size of the largest data structures,
which in turn is limited to 5 CAN FD frames max
((64 bytes per frame - 1 tail byte) * 5 frames - 2 bytes for transfer CRC = 313 bytes)
(or 45 CAN 2.0 frames)
in order to simplify the worst case analysis.
Non-standard (vendor-specific) types are recommended to follow this advice as well to maximize compatibility.

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
    # Mind the blank comment lines before and after the header comment.
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
