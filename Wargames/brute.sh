#!/bin/bash

coproc nc localhost 30002

start=""
wrong=""
key=""

while read -r ans; do
  if [[ "$ans" == "$start" ]] || [[ "$ans" == "$wrong" ]]; then
        echo "$key `tail -n 1 ./dict`" && sed -i '$d' ./dict
        echo "$ans" >> ./log
  else
        break
  fi
done <&"${COPROC[0]}" >&"${COPROC[1]}"

kill "$COPROC_PID"
echo "$ans"
