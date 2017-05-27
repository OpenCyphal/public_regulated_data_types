Internet/LAN forwarding protocol
================================

Data types defined in this namespace can be used to establish direct connectivity between arbitrary
local UAVCAN nodes and hosts on the Internet or a local area network (LAN) by means of so called
*modem nodes*.
Normally, a modem node would be implemented on an on-board cellular, RF, or satellite communication
hardware, such as an on-board telemetry modem.

## Application examples

* Direct telemetry transmission from UAVCAN nodes with no dependency on external means of broadcasting.
* Creation of web API for on board equipment. For example, a camera vendor can provide a web API
for their products that directly interacts with the cameras on board, bypassing all third party logic.
* Automatic firmware upgrades directly from vendor's website.
