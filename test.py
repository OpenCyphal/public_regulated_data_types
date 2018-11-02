#!/usr/bin/env python3

import sys
import time
import pydsdl


MAX_SERIALIZED_BIT_LENGTH = 366 * 8     # Dictated by uavcan.node.GetInfo.Response


def on_print(definition, line, value):
    print('%s:%d: %s' % (definition.file_path, line, value),
          file=sys.stderr)


started_at = time.monotonic()
output = pydsdl.parse_namespace('uavcan', [], print_directive_output_handler=on_print)
elapsed_time = time.monotonic() - started_at

print('\n'.join(map(str, output)))
print('%d data types in %.1f seconds' % (len(output), elapsed_time),
      file=sys.stderr)

largest = None
for t in output:
    if isinstance(t, pydsdl.data_type.ServiceType):
        tt = t.request_type, t.response_type
    else:
        tt = t,

    for t in tt:
        largest = largest if largest and (largest.bit_length_range.max >= t.bit_length_range.max) else t

if largest.bit_length_range.max > MAX_SERIALIZED_BIT_LENGTH:
    print('The largest data type', largest, 'exceeds the bit length limit of', MAX_SERIALIZED_BIT_LENGTH,
          file=sys.stderr)
    sys.exit(1)
else:
    print('Largest data type is', largest, 'up to', (largest.bit_length_range.max + 7) // 8, 'bytes',
          file=sys.stderr)
