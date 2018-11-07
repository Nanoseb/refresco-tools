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
