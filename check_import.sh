#!/bin/bash
# This script check the use of modules, and reports when a module is imported withoug being used
# They may be false positive since it only checks for ' modulenale_' presence in files,
# so most global variables won't be properly detected

SOURCE=$REFRESCO_CODE_DIR/src

fileList=$(find $SOURCE -name "*.F90" | sort)

while read file
do
    echo "--------------------------------"
    echo $file
    echo "--------------------------------"

    USEModule=$(grep "^USE " $file | awk '{print $2}')

    while read module
    do
        [[ ! $(grep -i -m 1 "^[^'\!']* ${module}_" $file) ]] && echo '  -- ' $module

    done <<<"$USEModule"

    echo

done <<<"$fileList"


#moduleList=$(grep -m 1 '^MODULE ' $SOURCE/*F90 | awk '{print $NF}' | sort) # | head -n 3)

#cd $SOURCE

#while read module
#do
#    echo "--------------------------------"
#    echo $module
#    echo "--------------------------------"
#    echo
#    USEModule=$(grep -B 5000 -m 1 -i "^USE $module" *F90 | grep '\-MODULE ' | awk '{print $NF}' | sort)
#    CALLModule=$(grep -B 50000 -i -m 1 "^[^'\!']* ${module}_" *F90 | grep '\-MODULE ' | awk '{print $NF}' | sort)

#    diff  <(echo "$USEModule") <(echo "$CALLModule") | grep '^<'
#    echo

#done <<<"$moduleList"


