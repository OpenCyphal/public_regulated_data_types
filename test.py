#!/usr/bin/env python3

import sys
import time
import pydsdl


MAX_SERIALIZED_BIT_LENGTH = 313 * 8     # See README


def on_print(definition, line, value):
    print('%s:%d: %s' % (definition.file_path, line, value),
          file=sys.stderr)


def compute_max_num_frames_canfd(bit_length):
    b = (bit_length + 7) // 8
    if b <= 63:
        return 1
    else:
        return (b + 2 + 62) // 63


started_at = time.monotonic()
output = pydsdl.parse_namespace('uavcan', [], print_directive_output_handler=on_print)
elapsed_time = time.monotonic() - started_at

print('Full data type name'.center(58),
      'FSID'.center(5),
      'CAN FD fr'.center(9))

for t in output:
    num_frames_to_str = lambda x: str(x) if x > 1 else ' '      # Return empty for single-frame transfers
    if isinstance(t, pydsdl.data_type.ServiceType):
        max_canfd_frames = '  '.join([
            num_frames_to_str(compute_max_num_frames_canfd(x.bit_length_range.max))
            for x in (t.request_type, t.response_type)
        ])
    else:
        max_canfd_frames = num_frames_to_str(compute_max_num_frames_canfd(t.bit_length_range.max))

    print(str(t).ljust(58),
          str(t.fixed_port_id if t.has_fixed_port_id else '').rjust(5),
          max_canfd_frames.rjust(7) + ' ')

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
