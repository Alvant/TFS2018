#!/bin/bash

ProgramName="httpd"
ProgramFolder="/root/homework/materials/class03/src/tinyhttpd/tinyhttpd"
ProgramPath="$ProgramFolder/$ProgramName"
LogFile="/root/${ProgramName}_start.log"

if [ `pidof $ProgramName` ]
then
  echo $ProgramName running
else
  "$ProgramPath"&
  echo "$(date '+%Y %b %d, %H:%M') $ProgramName was not running, starting..." >> "$LogFile"
fi
