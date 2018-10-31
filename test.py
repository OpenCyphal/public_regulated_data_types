#!/usr/bin/env python3

import sys
import pydsdl

output = pydsdl.parse_namespace('uavcan', [])

print('\n'.join(map(str, output)))
