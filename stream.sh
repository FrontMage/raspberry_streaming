#!/bin/bash
while true
do
  raspivid -vf -n -w 640 -h 480 -o - -t 0 -b 2000000 -fps 10 | nc -v 10.168.7.128 5777
done
