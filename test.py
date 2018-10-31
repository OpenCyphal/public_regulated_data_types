#!/usr/bin/env python3

import sys
import time
import pydsdl

def on_print(definition, line, value):
    print('%s:%d: %s' % (definition.file_path, line, value), file=sys.stderr)

started_at = time.monotonic()

output = pydsdl.parse_namespace('uavcan', [], print_directive_output_handler=on_print)

elapsed_time = time.monotonic() - started_at

print('\n'.join(map(str, output)))

print('%d data types in %.1f seconds' % (len(output), elapsed_time), file=sys.stderr)
