#!/bin/bash
# v0.2.5 autodetect and launch terminal
#ps -o 'cmd=' -p $(ps -o 'ppid=' -p $$) && bash

x-terminal-emulator -e "python PyFFmpeg.py; bash"
