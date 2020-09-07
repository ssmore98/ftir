#!/bin/python3
import sys
import os
import io
import subprocess
import shlex
import re
import csv
import hashlib
import json
from pprint import pprint

fields = {"%b":"blocks",
        "\"%c\"":"update",
        "%d":"depth",
        "%D":"device",
        "\"%f\"":"basename",
        "\"%F\"":"fstype",
        "\"%g\"":"group",
        "%G":"GID",
        "\"%h\"":"path",
        "%i":"inode",
        "%k":"Kbytes",
        "\"%l\"":"softlink",
        "%m":"permissions",
        "\"%M\"":"permissions",
        "%n":"hardlinks",
        "%s":"bytes",
        "%S":"sparseness",
        "\"%t\"":"modification",
        "\"%u\"":"user",
        "%U":"UID",
        "\"%y\"":"type",
        "\"%p\"":"name"}

output = [','.join(["\"{0}\"".format(fields[field]) for field in fields.keys()])]
for arg in sys.argv[1:]:
    cmd = "find '{0}' -name \"[^\.]*\" -printf '{1}\\n'".format(arg, ','.join([field for field in fields.keys()]))
    cmd = shlex.split(cmd)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output.extend([line.strip() for line in proc.communicate()[0].decode("utf-8", "ignore").splitlines()])
    reader = csv.DictReader(output)
    data = list(reader)
    for row in data:
        if row['type'] in ['f'] and os.path.exists(row['name']):
            with open(row['name'], 'rb') as fp:
                row['sha512'] = hashlib.sha512(fp.read()).hexdigest()
        else:
            row['sha512'] = None
    with open("{0}.json".format(os.path.basename(arg)), 'w') as fp:
        json.dump(data, fp, indent=4)
