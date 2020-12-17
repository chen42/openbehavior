#!/bin/bash

program_file_dir="/home/pi/openbehavior/socialDrinking/python"

num_empty_files=`ls -l $program_file_dir/*.py | awk '{if($7==0) print($9)}' | wc -l`

if [ $num_empty_files -gt 0 ]
then
  echo "There are $num_empty_files program files. Please check"
  exit 1
fi


exit 0

