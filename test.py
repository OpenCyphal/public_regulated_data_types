#!/usr/bin/env python3

import sys
import time
import string
import pydsdl


MAX_SERIALIZED_BIT_LENGTH = 313 * 8     # See README
MAX_LINE_LENGTH = 120
ALLOWED_CHARACTERS = set(string.digits + string.ascii_letters + string.punctuation + ' ')


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
output = pydsdl.read_namespace('uavcan', [], print_output_handler=on_print)
elapsed_time = time.monotonic() - started_at

print('Full data type name'.center(58),
      'FSID'.center(5),
      'CAN FD fr'.center(9))

for t in output:
    num_frames_to_str = lambda x: str(x) if x > 1 else ' '      # Return empty for single-frame transfers
    if isinstance(t, pydsdl.ServiceType):
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
    for index, line in enumerate(open(t.source_file_path).readlines()):
        line = line.strip('\r\n')

        # Check line length limit
        if len(line) > MAX_LINE_LENGTH:
            print('%s:%d: Line is too long:' % (t.source_file_path, index + 1),
                  len(line), '>', MAX_LINE_LENGTH, 'chars',
                  file=sys.stderr)
            sys.exit(1)

        # Make sure we're not using any weird characters such as tabs or non-ASCII-printable
        for char_index, char in enumerate(line):
            if char not in ALLOWED_CHARACTERS:
                print('%s:%d: Disallowed character' % (t.source_file_path, index + 1),
                      repr(char), 'code', ord(char), 'at column', char_index + 1,
                      file=sys.stderr)
                sys.exit(1)

    if isinstance(t, pydsdl.ServiceType):
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
