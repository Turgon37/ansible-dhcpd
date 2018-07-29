#!/usr/bin/env python

import json
import re
import subprocess
import sys

content = dict()

version_re = re.compile('^isc-dhcpd-(?P<version>(?P<major>[0-9]+)[^ ]+)$')
try:
    result = subprocess.Popen(['/usr/bin/env', 'dhcpd', '--version'],
                              stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE,
                              universal_newlines=True)
    (stdout, stderr) = result.communicate()
    output = stdout + stderr
    for line in output.split():
        match = version_re.search(line)
        if match:
            content['version_full'] = match.group('version')
            content['version_major'] = match.group('major')
            break
except subprocess.CalledProcessError as e:
    content['error'] = str(e)

if not content:
    content = None

print(json.dumps(content))
sys.exit(0)
