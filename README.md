# refresco-tools
Collection of scripts I use when working with ReFRESCO


## residisp
Python script to display ReFRESCO residuals (steady or not). A help page is available via `residisp -h`.

Example usage:
```
residisp 3729365          # slurm job ID
residisp ~/path/to/computation/folder
residisp --very-end -l2
residisp --max-it 20000   # to reduce the memory consumption: limit the number of iteration loaded
residisp --follow         # to automatically refresh the output
```

## rdiff
Very small script to run `vimdiff` between a branch and the trunk of an svn repository (hence not limited to refresco)

Usage:
```
# use full path
rdiff ~/ReFRESCO/Dev/branches/overset/Code/src/refresco.F90

# or any relative path works too
rdiff src/refresco.F90
```

Small `vimdiff` cheat sheet:
```
]c                    go to the next difference
[c                    go to the previous difference
do                    get the diff from the other file (diff obtain)
dp                    send the diff to the other file  (diff put)
zr                    unfold the entire file
:diffupdate           re-scan the files for differences
:set diffopt+=iwhite  ignore white space comparison (can be added in .vimrc)
ctrl-w w              switch between windows
```
 
## check\_import
Check if a module that has been imported is actually used.
This also generates a script called `check_impot_cleanup.sh` that will comment out all the useless `USE ` statements.

Dependencies: ctags

## module-graph
This script generates a graph made of ReFRESCO's module, module are linked based on they `USE` statements.

Dependencies: pyvis

## latex-trim
This script returns trim parameters for the image given in argument using mouse selection.

```
$ latex-trim graph.png
trim={0.00cm 1.80cm 8.37cm 0.00cm}, clip
```

Dependencies: imagemagick (for pdf images only)

## refresco-cmake
Helper script to compile ReFRESCO using cmake

## check\_declar
Script to detect non declared variables of a fortran subroutine

```
$ check_declar file.F90 subroutineName
```

## report2metadata
Script that extracts metadata from marin reports
```
$ report2metadata report.pdf
```

## BCstatus
Script to get the method used by ReFRESCO to handle each boundary condition, needs `$REFRESCO_CODE_DIR` to be defined correctly. The output is an html table that can be put directly on mods.


```
$ BCstatus
```
