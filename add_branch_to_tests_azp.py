#!/usr/bin/python3

import os
import sys

from copy import copy
from shutil import copyfile

try:
    f = open(sys.argv[1], 'r')
except Exception:
    print('No such file')
    sys.exit(1)

HEADERS_TO_HANDLE = ('Ansible_devel', 'Docker_devel', 'Remote_devel')
ignore_txt_to_copy = None

if len(sys.argv) == 3:
    ignore_txt_to_copy = sys.argv[2]

for header in HEADERS_TO_HANDLE:
    f = open(sys.argv[1], 'r')
    file_content = f.readlines()
    f.close()

    start_block_pos = None
    end_block_pos = None
    for i, line in enumerate(file_content):
        if header in line:
            start_block_pos = i
            continue

        if start_block_pos is not None and '- stage:' in line:
            end_block_pos = i
            break

    # Debug
    if start_block_pos is None:
        print('start of %s not found' % header)
        sys.exit(1)
    if end_block_pos is None:
        print('end of %s not found' % header)
        sys.exit(1)

    new_block = copy(file_content[start_block_pos:end_block_pos])

    for i, line in enumerate(new_block):
        if 'devel' in line:
            line = line.replace(' # Only on devel', '')
            line = line.replace('_devel', '_2_11')
            line = line.replace('devel', '2.11')
            new_block[i] = line

    insert_pos = end_block_pos
    for line in new_block:
        #print(insert_pos)
        #print(line)
        file_content.insert(insert_pos, line)
        insert_pos += 1

    f = open(sys.argv[1], 'w')
    f.writelines(file_content)
    f.truncate()
    f.close()

    start_block_pos = None
    end_block_pos = None
    insert_pos = None
    file_content = []
    new_block = []

# Handle ignore.txt if needed
if ignore_txt_to_copy is not None:
    if not os.path.exists(ignore_txt_to_copy):
        print('%s does not exist' % ignore_txt_to_copy)
        sys.exit(1)
else:
    sys.exit(0)

ignore_txt_dst = ignore_txt_to_copy.replace('2.11', '2.12')
copyfile(ignore_txt_to_copy, ignore_txt_dst)

sys.exit(0)
