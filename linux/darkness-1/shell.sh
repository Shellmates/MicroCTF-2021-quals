#!/bin/sh

MAXLEN=256

echo -n '$ '

while read cmd; do
  if [ "$(echo -n "$cmd" | wc -c)" -gt "$MAXLEN" ]; then
    echo "Command too long."
  else
    /bin/sh -c "$cmd" >/dev/null 2>&1
    echo "Return code: $?"
  fi
  echo -n '$ '
done
