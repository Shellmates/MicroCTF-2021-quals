#!/bin/sh

while ! (echo "$output" | grep "shellmates"); do
  ./trigger.py &
  output="$(./xpl.py)"
done

echo "$output"
