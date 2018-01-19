#!/bin/sh
# Outputs time, hostname and task name on start and finish. The output of this
# program will appear in the web page without changes.

worker_info="Worker $(hostname)"
task_info="Task $@"

echo "$(date +%T) $worker_info started  $task_info"
sleep 4  # Simulate CPU work
echo "$(date +%T) $worker_info finished $task_info"
