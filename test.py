#!/usr/bin/env python3

import sys
import time
import string
import pydsdl
from functools import partial


MAX_SERIALIZED_BIT_LENGTH = 313 * 8     # See README
MAX_LINE_LENGTH = 120
NAMESPACES_EXEMPTED_FROM_HEADER_COMMENT_REQUIREMENT = 'uavcan.primitive', 'uavcan.si'
ALLOWED_CHARACTERS = set(string.digits + string.ascii_letters + string.punctuation + ' ')


def die_at(ty, line_index, *text):
    prefix = '%s:%d:' % (ty.source_file_path, line_index + 1)
    print(prefix, *text, file=sys.stderr)
    sys.exit(1)


def on_print(file_path, line, value):
    print('%s:%d: %s' % (file_path, line, value), file=sys.stderr)


def compute_max_num_frames_canfd(bit_length):
    b = (bit_length + 7) // 8
    if b <= 63:
        return 1
    else:
        return (b + 2 + 62) // 63


started_at = time.monotonic()
ns_list = [
    'uavcan',
    'regulated',
]
output = []
for ns in ns_list:
    output += pydsdl.read_namespace(ns, ns_list, print_output_handler=on_print)
elapsed_time = time.monotonic() - started_at

print('Full data type name'.center(58),
      'FSID'.center(5),
      'CAN FD fr'.center(9))

for t in output:
    num_frames_to_str = lambda x: str(x) if x > 1 else ' '      # Return empty for single-frame transfers
    if isinstance(t, pydsdl.ServiceType):
        max_canfd_frames = '  '.join([
            num_frames_to_str(compute_max_num_frames_canfd(max(x.bit_length_set)))
            for x in (t.request_type, t.response_type)
        ])
    else:
        max_canfd_frames = num_frames_to_str(compute_max_num_frames_canfd(max(t.bit_length_set)))

    print(str(t).ljust(58),
          str(t.fixed_port_id if t.has_fixed_port_id else '').rjust(5),
          max_canfd_frames.rjust(7) + ' ')

print('%d data types in %.1f seconds' % (len(output), elapsed_time),
      file=sys.stderr)

for t in output:
    text = open(t.source_file_path).read()
    for index, line in enumerate(text.split('\n')):
        line = line.strip('\r\n')
        abort = partial(die_at, t, index)

        # Check header comment.
        if index == 0 and not line.startswith('# '):
            if not any(map(lambda e: t.full_namespace.startswith(e),
                           NAMESPACES_EXEMPTED_FROM_HEADER_COMMENT_REQUIREMENT)):
                abort('Every data type definition shall have a header comment unless it is a member of:',
                      NAMESPACES_EXEMPTED_FROM_HEADER_COMMENT_REQUIREMENT)

        # Check trailing comment placement.
        # TODO: this test breaks on string literals containing "#".
        if not line.startswith('#') and '#' in line and '  #' not in line:
            abort('Trailing line comments shall be separated from the preceding text with at least two spaces')

        if line != '#' and '#' in line and '# ' not in line:
            abort('The text of a comment shall be separated from the comment character with a single space')

        if line.endswith(' '):
            abort('Trailing spaces are not permitted')

        # Check line length limit
        if len(line) > MAX_LINE_LENGTH:
            abort('Line is too long:', len(line), '>', MAX_LINE_LENGTH, 'chars')

        # Make sure we're not using any weird characters such as tabs or non-ASCII-printable
        for char_index, char in enumerate(line):
            if char not in ALLOWED_CHARACTERS:
                abort('Disallowed character', repr(char), 'code', ord(char), 'at column', char_index + 1)

    if not text.endswith('\n') or text.endswith('\n' * 2):
        abort('A file shall contain exactly one blank line at the end')


def get_max_bit_length(ty) -> int:
    if isinstance(ty, pydsdl.DelimitedType):
        ty = ty.inner_type
    if isinstance(ty, pydsdl.ServiceType):
        return max(map(get_max_bit_length, [ty.request_type, ty.response_type]))
    else:
        return max(ty.bit_length_set)


for t in output:
    max_bit_length = get_max_bit_length(t)
    if max_bit_length > MAX_SERIALIZED_BIT_LENGTH:
        text = open(t.source_file_path).read()
        if '#pragma:no-bit-length-limit' not in text.replace(' ', ''):
            print('The data type', t, 'exceeds the bit length limit of', MAX_SERIALIZED_BIT_LENGTH, file=sys.stderr)
            sys.exit(1)
