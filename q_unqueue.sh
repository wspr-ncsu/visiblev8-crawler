#!/bin/bash

for i in {0..11}
do
    session_name="queue-$i"
    tmux kill-session -t $session_name
done