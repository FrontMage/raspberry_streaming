#!/bin/bash
raspivid -vf -n -w 640 -h 480 -o - -t 0 -b 2000000 -fps 20 -ss 7000 | nc -v 10.168.7.128 5777
