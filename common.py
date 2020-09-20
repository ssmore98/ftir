import re

def CSVname(path):
    filename = re.sub(r'/', '_', path)
    return "{0}.csv".format(filename)
