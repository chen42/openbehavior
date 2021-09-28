#!/bin/bash


branch=$1

git checkout $branch && git pull

sudo reboot