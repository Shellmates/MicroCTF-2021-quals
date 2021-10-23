#!/bin/sh

MAXLEN=256

exec 2>/dev/null

while echo -n "What's your name? " && read name; do
  name="$(echo -n "${name}" | tr -d '\n\r' | awk '/^[0-9A-z]+$/ { print $0 }')"
  if [ -z "${name}" ]; then
    echo "I don't like your name."
  elif [ "$(echo -n "${name}" | wc -c)" -gt "$MAXLEN" ]; then
    echo "Name too long."
  else
    /bin/sh -c "echo \"Hello, ${name}!\""
  fi
done
