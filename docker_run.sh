#!/bin/bash
nvidia-docker run -p 8888:8888 \
            -it \
            --rm \
            --hostname face_recognition --name face_recognition \
            -v /tmp/.X11-unix:/tmp/.X11-unix \
            -v /home/xinbg/Documents/named_pipe:/face_recognition \
            -e DISPLAY=$DISPLAY \
            -e AUDIO_GID=`getent group audio | cut -d: -f3` \
            -e VIDEO_GID=`getent group video | cut -d: -f3` \
            -e GID=`id -g` \
            -e UID=`id -u` \
            face_recognition /bin/bash

