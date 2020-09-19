#!/bin/python3
import sys
import os
import io
import subprocess
import shlex
import re
import csv
import argparse

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

parser = argparse.ArgumentParser(description=""""This script scan the entire
filesystem and creates the dataset containing information about
accessible files and directories. The name of the file is root.csv.""",
formatter_class=argparse.RawDescriptionHelpFormatter, epilog="")
parser.add_argument('-P', action='store_true', required=False,
help="""Never follow symbolic
links. This is the default behaviour.  When find examines or prints 
information a file,  and  the file is a symbolic link, the information used
shall be taken from the properties of the symbolic link itself.""")
parser.add_argument('-L', action='store_true', help="""Follow symbolic links.
When find examines or prints information about files, the information used
shall be taken from the properties of the file to which the link points, not
from the link itself (unless it is a broken  symbolic  link  or find is unable
to examine the file to which the link points). Use of this option implies
-noleaf. If you later use the -P option, -noleaf will still be in effect.  If
-L is in effect and find discovers a symbolic link to a subdirectory during its
search, the subdirectory pointed to by the symbolic link will be searched.

When the -L option is in effect, the -type predicate will always match against
the type of the file that a symbolic link points to rather than the link itself
(unless the symbolic link is broken). Using -L causes the -lname  and -ilname
predicates always to return false.""")
parser.add_argument('-H', action='store_true', required=False,
help="""Do not follow symbolic
links, except while processing the command line arguments. When find examines
or prints information about files, the information used shall be taken from the
properties of the symbolic link itself. The only exception to this behaviour
is when a file specified on the command line is a symbolic link, and the link
can be resolved. For that situation, the information used is taken from
whatever the link points to (that is, the link is followed). The information
about the link itself is used as a fallback if the file pointed to by the
symbolic link cannot be examined. If -H is in effect and one of the paths
specified on the command line is a symbolic link to a directory, the contents
of that directory will be examined (though of course -maxdepth 0 would prevent
this).""")
parser.add_argument('-O', type=int, choices=[0, 1, 2, 3], action='store',
required=False,
help="""Enables query
optimisation. The find program reorders tests to speed up execution while
preserving the overall effect; that  is,  predicates  with  side effects are
not reordered relative to each other.  The optimisations performed at each
optimisation level are as follows.
       0      Equivalent to optimisation level 1.
       1      This is the default optimisation level and corresponds to the
              traditional behaviour. Expressions  are  reordered so that tests
              based only on the names of files (for example -name and -regex)
              are performed first.
       2      Any  -type  or  -xtype tests are performed after any tests based
              only on the names of files, but before any tests that require
              information from the inode.  On many modern versions of Unix,
              file types are returned  by  readdir() and so these predicates
              are faster to evaluate than predicates which need to stat the
              file first.  If you use the -fstype FOO predicate and specify a
              filsystem type FOO which is not known (that is, present  in
              `/etc/mtab')  at the time find starts, that predicate is
              equivalent to -false.
       3      At  this  optimisation  level, the full cost-based query
              optimiser is enabled.  The order of tests is modified so that
              cheap (i.e. fast) tests are performed first and more expensive
              ones  are  performed  later,  if  necessary. Within  each cost
              band, predicates are evaluated earlier or later according to
              whether they are likely to succeed or not.  For -o, predicates
              which are likely to succeed are evaluated earlier, and for -a,
              predicates  which  are likely to fail are evaluated earlier.

The  cost-based  optimiser  has  a fixed idea of how likely any given test is
to succeed.  In some cases the probability takes account of the specific nature
of the test (for example, -type f is assumed to be  more  likely  to  succeed
than -type  c).   The cost-based optimiser is currently being evaluated.
If it does not actually improve the performance of find, it will be removed
again.  Conversely, optimisations that prove to  be  reliable,  robust  and
effective  may  be enabled  at lower optimisation levels over time.  However,
the default behaviour (i.e. optimisation level 1) will not be changed in the
4.3.x release series.  The findutils test suite runs all the tests on find at
each optimisation level and ensures that the result is the same.""")
parser.add_argument('-d', '--depth', action='store_true',
required=False,
help="""Process each directory's contents before the directory itself.""")
parser.add_argument('--daystart', action='store_true',
required=False,
help="""Measure  times  (for  -amin,  -atime,  -cmin, -ctime, -mmin, and
-mtime) from the beginning of today rather than from 24 hours ago.  This option
only affects tests which appear later on the command line.""")
parser.add_argument('--ignore_readdir_race', action='store_true',
required=False,
help="""Normally,  find  will emit an error message when it fails to stat a
file.  If you give this option and a file is deleted between the time find
reads the name of the file from the directory and the time it tries to stat
the  file,  no  error message  will  be  issued.    This also applies to files
or directories whose names are given on the command line.  This option takes
effect at the time the command line is read, which means that you cannot search
one part of the  filesystem with  this  option  on and part of it with this
option off (if you need to do that, you will need to issue two find commands
instead, one with the option and one without it).""")
parser.add_argument('--maxdepth', action='store', type=int,
required=False,
help="""Descend at most MAXDEPTH levels (a non-negative integer) levels of
directories below the command line arguments. --maxdepth 0 means only apply the
tests and actions to the command line arguments.""")
parser.add_argument('--mindepth', action='store', type=int,
required=False,
help="""Do not apply any tests or actions at levels less than MINDEPTH (a
non-negative integer). --mindepth 1  means  process  all files except the
command line arguments.""")
parser.add_argument('--mount', action='store_true',
required=False,
help="""Don't descend directories on other filesystems.  An alternate
name for --xdev""")
parser.add_argument('--noignore_readdir_race', action='store_true',
required=False,
help="""Turns off the effect of --ignore_readdir_race.""")
parser.add_argument('--noleaf', action='store_true',
required=False,
help="""Do not optimize by assuming that directories contain 2 fewer
subdirectories than their hard link count.  This option  is needed  when
searching  filesystems  that  do  not  follow the Unix directory-link
convention, such as CD-ROM or MS-DOS filesystems or AFS volume mount points.
Each directory on a normal Unix filesystem has at least 2 hard links: its  name
and  its  `.'  entry.  Additionally, its subdirectories (if any) each have a
`..'  entry linked to that directory.  When find is examining a directory,
after it has statted 2 fewer subdirectories than the directory's  link  count,
it  knows that  the  rest  of  the entries in the directory are non-directories
(`leaf' files in the directory tree).  If only the files' names need to be
examined, there is no need to stat them; this gives a significant increase in
search speed.""")
parser.add_argument('--regextype', choices=['emacs', 'posix-awk', 'posix-basic',
    'posix-egrep', 'posix-extended'], action='store',
required=False,
help="""Changes the regular expression syntax understood by -regex and -iregex
tests which occur  later  on  the  command  line.  Currently-implemented types
are emacs (this is the default), posix-awk, posix-basic, posix-egrep and
posix-extended.""")
parser.add_argument('--xautofs', action='store_true',
required=False,
help="""Don't descend directories on autofs filesystems.""")
parser.add_argument('--xdev', action='store_true',
required=False,
help="""Don't descend directories on other filesystems.""")
parser.add_argument('PATH', nargs='+', action="store",
help="""Path in the file system""")

args = parser.parse_args()

find_options = []
if args.P:
    find_options.append("-P")
if args.L:
    find_options.append("-L")
if args.H:
    find_options.append("-H")
if args.O:
    find_options.append("-O{0}".format(args.O))
if args.depth:
    find_options.append("-d")
if args.daystart:
    find_options.append("-daystart")
if args.ignore_readdir_race:
    find_options.append("-ignore_readdir_race")
if args.noignore_readdir_race:
    find_options.append("-noignore_readdir_race")
if args.maxdepth:
    find_options.append("-maxdepth {0}".format(args.maxdepth))
if args.mindepth:
    find_options.append("-mindepth {0}".format(args.mindepth))
if args.mount:
    find_options.append("-mount")
if args.noleaf:
    find_options.append("-noleaf")
if args.regextype:
    find_options.append("-regextype {0}".format(args.regextype))
if args.xautofs:
    find_options.append("-xautofs")
if args.xdev:
    find_options.append("-xdev")

output = [','.join(["\"{0}\"".format(fields[field]) for field in fields.keys()])]
for path in [os.path.abspath(i) for i in args.PATH]:
    cmd = "find '{0}' {2} -name \"[^\.]*\" -printf '{1}\\n'".format(path,
            ','.join([field for field in fields.keys()]),
            ' '.join(find_options))
    cmd = shlex.split(cmd)
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    output.extend([line.strip() for line in proc.communicate()[0].decode("utf-8", "ignore").splitlines()])
    reader = csv.DictReader(output)
    with open("{0}.csv".format(os.path.basename(path)), 'w') as fp:
        writer = csv.DictWriter(fp, fieldnames=fields.values(), quoting=csv.QUOTE_NONNUMERIC)
        writer.writeheader()
        for row in reader:
            writer.writerow(row)
