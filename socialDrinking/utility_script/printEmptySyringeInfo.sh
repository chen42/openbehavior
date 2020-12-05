#!/bin/bash


read -p "Enter the summary file name: " fname


# filter and print which box contains the information of empty syringe
cat $fname | awk '{ if($1 != "ratUnknown" && $11 > 0 ) { print $1 , $4 } }'



