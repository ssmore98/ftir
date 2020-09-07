#!/bin/python3
import sys
import os

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

print(','.join(["\"{0}\"".format(fields[field]) for field in fields.keys()]))
for arg in sys.argv[1:]:
    cmd = "find '{0}' -printf '{1}\\n'".format(arg, ','.join([field for field in fields.keys()]))
    os.system(cmd)
