#!/bin/bash

links=( $(find . -type l -not -xtype l)) # get all non-broken links
targets=()
num_rows=( ${#links[@]} )
for i in ${links[@]}
do
    a=( $(readlink $i))
    targets+=($a)
done

i=0
while [ "$i" -lt "$num_rows" ]
do
    echo "${links[$i]},${targets[$i]}" >> map.txt
    let "i++"
done