This software is used to analyze a file system to determine the factors that affect the file size.

The software consists of two python scripts:

1. **find.py** This script scan the entire filesystem and creates the dataset containing information about accessible files and directories. The name of the file is *root.csv*. This scripts accepts *most* of the command line options accepted by the *find* command.
1. **process.py** This script,
    - Imports the dataset in the file *root.csv*.
    - Performs data wrangling.

**find.py**

    usage: find.py [-h] [-P] [-L] [-H] [-O {0,1,2,3}] [-d] [--daystart]
               [--ignore_readdir_race] [--maxdepth MAXDEPTH]
               [--mindepth MINDEPTH] [--mount] [--noignore_readdir_race]
               [--noleaf]
               [--regextype {emacs,posix-awk,posix-basic,posix-egrep,posix-extended}]
               [--xautofs] [--xdev] [--amin n] [--anewer FILE] [--atime n]
               [--cmin n] [--cnewer FILE] [--ctime n] [--empty] [--executable]
               [--false] [--fstype type] [--gid n] [--group gname]
               [--ilname PATTERN] [--iname PATTERN] [--inum n]
               [--ipath PATTERN] [--iregex PATTERN] [--iwholename PATTERN]
               [--links n] [--lname PATTERN] [--mmin n] [--mtime n]
               [--name PATTERN] [--newer FILE]
               PATH [PATH ...]

This script scan the entire filesystem and creates the dataset containing information about accessible files and directories. The name of the file is root.csv.

positional arguments:

    PATH                  Path in the file system


optional arguments:

    -h, --help            show this help message and exit
    -P                    Never follow symbolic links. This is the default behaviour. When find examines or prints information a file, and the file is a symbolic link, the information used shall be taken from the properties of the symbolic link itself.
    -L                  Follow symbolic links. When find examines or prints information about files, the information used shall be taken from the properties of the file to which the link points, not from the link itself (unless it is a broken symbolic link or find is unable to examine the file to which the link points). Use of this option implies -noleaf. If you later use the -P option, -noleaf will still be in effect. If -L is in effect and find discovers a symbolic link to a subdirectory during its search, the subdirectory pointed to by the symbolic link will be searched. When the -L option is in effect, the -type predicate will always match against the type of the file that a symbolic link points to rather than the link itself (unless the symbolic link is broken). Using -L causes the -lname and -ilname predicates always to return false.   
    -H                  Do not follow symbolic links, except while processing
                        the command line arguments. When find examines or
                        prints information about files, the information used
                        shall be taken from the properties of the symbolic
                        link itself. The only exception to this behaviour is
                        when a file specified on the command line is a
                        symbolic link, and the link can be resolved. For that
                        situation, the information used is taken from whatever
                        the link points to (that is, the link is followed).
                        The information about the link itself is used as a
                        fallback if the file pointed to by the symbolic link
                        cannot be examined. If -H is in effect and one of the
                        paths specified on the command line is a symbolic link
                        to a directory, the contents of that directory will be
                        examined (though of course -maxdepth 0 would prevent
                        this).
    -O {0,1,2,3}          Enables query optimisation. The find program reorders
                        tests to speed up execution while preserving the
                        overall effect; that is, predicates with side effects
                        are not reordered relative to each other. The
                        optimisations performed at each optimisation level are
                        as follows. 0 Equivalent to optimisation level 1. 1
                        This is the default optimisation level and corresponds
                        to the traditional behaviour. Expressions are
                        reordered so that tests based only on the names of
                        files (for example -name and -regex) are performed
                        first. 2 Any -type or -xtype tests are performed after
                        any tests based only on the names of files, but before
                        any tests that require information from the inode. On
                        many modern versions of Unix, file types are returned
                        by readdir() and so these predicates are faster to
                        evaluate than predicates which need to stat the file
                        first. If you use the -fstype FOO predicate and
                        specify a filsystem type FOO which is not known (that
                        is, present in `/etc/mtab') at the time find starts,
                        that predicate is equivalent to -false. 3 At this
                        optimisation level, the full cost-based query
                        optimiser is enabled. The order of tests is modified
                        so that cheap (i.e. fast) tests are performed first
                        and more expensive ones are performed later, if
                        necessary. Within each cost band, predicates are
                        evaluated earlier or later according to whether they
                        are likely to succeed or not. For -o, predicates which
                        are likely to succeed are evaluated earlier, and for
                        -a, predicates which are likely to fail are evaluated
                        earlier. The cost-based optimiser has a fixed idea of
                        how likely any given test is to succeed. In some cases
                        the probability takes account of the specific nature
                        of the test (for example, -type f is assumed to be
                        more likely to succeed than -type c). The cost-based
                        optimiser is currently being evaluated. If it does not
                        actually improve the performance of find, it will be
                        removed again. Conversely, optimisations that prove to
                        be reliable, robust and effective may be enabled at
                        lower optimisation levels over time. However, the
                        default behaviour (i.e. optimisation level 1) will not
                        be changed in the 4.3.x release series. The findutils
                        test suite runs all the tests on find at each
                        optimisation level and ensures that the result is the
                        same.
  -d, --depth           Process each directory's contents before the directory
                        itself.
  --daystart            Measure times (for -amin, -atime, -cmin, -ctime,
                        -mmin, and -mtime) from the beginning of today rather
                        than from 24 hours ago. This option only affects tests
                        which appear later on the command line.
  --ignore_readdir_race
                        Normally, find will emit an error message when it
                        fails to stat a file. If you give this option and a
                        file is deleted between the time find reads the name
                        of the file from the directory and the time it tries
                        to stat the file, no error message will be issued.
                        This also applies to files or directories whose names
                        are given on the command line. This option takes
                        effect at the time the command line is read, which
                        means that you cannot search one part of the
                        filesystem with this option on and part of it with
                        this option off (if you need to do that, you will need
                        to issue two find commands instead, one with the
                        option and one without it).
  --maxdepth MAXDEPTH   Descend at most MAXDEPTH levels (a non-negative
                        integer) levels of directories below the command line
                        arguments. --maxdepth 0 means only apply the tests and
                        actions to the command line arguments.
  --mindepth MINDEPTH   Do not apply any tests or actions at levels less than
                        MINDEPTH (a non-negative integer). --mindepth 1 means
                        process all files except the command line arguments.
  --mount               Don't descend directories on other filesystems. An
                        alternate name for --xdev
  --noignore_readdir_race
                        Turns off the effect of --ignore_readdir_race.
  --noleaf              Do not optimize by assuming that directories contain 2
                        fewer subdirectories than their hard link count. This
                        option is needed when searching filesystems that do
                        not follow the Unix directory-link convention, such as
                        CD-ROM or MS-DOS filesystems or AFS volume mount
                        points. Each directory on a normal Unix filesystem has
                        at least 2 hard links: its name and its `.' entry.
                        Additionally, its subdirectories (if any) each have a
                        `..' entry linked to that directory. When find is
                        examining a directory, after it has statted 2 fewer
                        subdirectories than the directory's link count, it
                        knows that the rest of the entries in the directory
                        are non-directories (`leaf' files in the directory
                        tree). If only the files' names need to be examined,
                        there is no need to stat them; this gives a
                        significant increase in search speed.
  --regextype {emacs,posix-awk,posix-basic,posix-egrep,posix-extended}
                        Changes the regular expression syntax understood by
                        -regex and -iregex tests which occur later on the
                        command line. Currently-implemented types are emacs
                        (this is the default), posix-awk, posix-basic, posix-
                        egrep and posix-extended.
  --xautofs             Don't descend directories on autofs filesystems.
  --xdev                Don't descend directories on other filesystems.
  --amin n              File was last accessed n minutes ago.
  --anewer FILE         File was last accessed more recently than FILE was
                        modified. If FILE is a symbolic link and the -H option
                        or the -L option is in effect, the access time of the
                        file it points to is always used.
  --atime n             File was last accessed n*24 hours ago. When find
                        figures out how many 24-hour periods ago the file was
                        last accessed, any fractional part is ignored, so to
                        match -atime +1, a file has to have been accessed at
                        least two days ago.
  --cmin n              File's status was last changed n minutes ago.
  --cnewer FILE         File's status was last changed more recently than FILE
                        was modified. If FILE is a symbolic link and the -H
                        option or the -L option is in effect, the status-
                        change time of the file it points to is always used.
  --ctime n             File's status was last changed n*24 hours ago. See the
                        comments for -atime to understand how rounding affects
                        the interpretation of file status change times.
  --empty               File is empty and is either a regular file or a
                        directory.
  --executable          Matches files which are executable and directories
                        which are searchable (in a file name resolution
                        sense). This takes into account access control lists
                        and other permissions artefacts which the -perm test
                        ignores. This test makes use of the access(2) system
                        call, and so can be fooled by NFS servers which do UID
                        mapping (or root-squashing), since many systems
                        implement access(2) in the client's kernel and so
                        cannot make use of the UID mapping information held on
                        the server. Because this test is based only on the
                        result of the access(2) system call, there is no
                        guarantee that a file for which this test succeeds can
                        actually be executed.
  --false               Always false.
  --fstype type         File is on a filesystem of type type. The valid
                        filesystem types vary among different versions of
                        Unix; an incomplete list of filesystem types that are
                        accepted on some version of Unix or another is: ufs,
                        4.2, 4.3, nfs, tmp, mfs, S51K, S52K. You can use
                        -printf with the %F directive to see the types of your
                        filesystems.
  --gid n               File's numeric group ID is n.
  --group gname         File belongs to group gname (numeric group ID
                        allowed).
  --ilname PATTERN      Like -lname, but the match is case insensitive. If the
                        -L option or the -follow option is in effect, this
                        test returns false unless the symbolic link is broken.
  --iname PATTERN       Like -name, but the match is case insensitive. For
                        example, the patterns `fo*' and `F??' match the file
                        names `Foo', `FOO', `foo', `fOo', etc. The pattern
                        `*foo*` will also match a file called '.foobar'.
  --inum n              File has inode number n. It is normally easier to use
                        the -samefile test instead.
  --ipath PATTERN       Like -path. but the match is case insensitive.
  --iregex PATTERN      Like -regex, but the match is case insensitive.
  --iwholename PATTERN  See -ipath. This alternative is less portable than
                        -ipath.
  --links n             File has n links.
  --lname PATTERN       File is a symbolic link whose contents match shell
                        pattern PATTERN. The metacharacters do not treat `/'
                        or `.' specially. If the -L option or the -follow
                        option is in effect, this test returns false unless
                        the symbolic link is broken.
  --mmin n              File's data was last modified n minutes ago.
  --mtime n             File's data was last modified n*24 hours ago. See the
                        comments for -atime to understand how rounding affects
                        the interpretation of file modification times.
  --name PATTERN        Base of file name (the path with the leading
                        directories removed) matches shell pattern PATTERN.
                        Because the leading directories are removed, the file
                        names considered for a match with -name will never
                        include a slash, so `-name a/b' will never match
                        anything (you probably need to use -path instead). The
                        metacharacters (`*', `?', and `[]') match a `.' at the
                        start of the base name (this is a change in
                        findutils-4.2.2; see section STANDARDS CONFORMANCE
                        below). To ignore a directory and the files under it,
                        use -prune; see an example in the description of
                        -path. Braces are not recognised as being special,
                        despite the fact that some shells including Bash imbue
                        braces with a special meaning in shell patterns. The
                        filename matching is performed with the use of the
                        fnmatch(3) library function. Don't forget to enclose
                        the pattern in quotes in order to protect it from
                        expansion by the shell.
  --newer FILE          File was modified more recently than FILE. If FILE is
                        a symbolic link and the -H option or the -L option is
                        in effect, the modification time of the file it points
                        to is always used.
