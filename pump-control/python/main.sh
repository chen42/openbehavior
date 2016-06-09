#!/bin/bash
python /home/pi/openbehavior/pump-control/python/main.py 2>&1 | logger -t pump-control
