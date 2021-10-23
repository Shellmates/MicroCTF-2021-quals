# dicteval

## Write-up

* Challenge source :  

```python
#!/usr/bin/env python3

with open("./flag.txt") as f:
    FLAG = f.read().strip()

BLACKLIST = '"%&\',-/:;@\\_`{|}~ \t\n\r\x0b\x0c'
OPEN_LIST = '(['
CLOSE_LIST = ')]'

class BadInput(Exception):
    pass

def check_balanced(s):
    stack = []
    for i in s:
        if i in OPEN_LIST:
            stack.append(i)
        elif i in CLOSE_LIST:
            pos = CLOSE_LIST.index(i)
            if ((len(stack) > 0) and
                (OPEN_LIST[pos] == stack[len(stack)-1])):

                stack.pop()
            else:
                return False
    return len(stack) == 0

def check(s):
    return all(ord(x) < 0x7f for x in s) and all(x not in s for x in BLACKLIST) and check_balanced(s)

def safe_eval(s, func):
    if not check(s):
        print("Input is bad")
    else:
        try:
            print(eval(f"{func.__name__}({s})", {"__builtins__": {func.__name__: func}, "flag": FLAG}))
        except:
            print("Error")

if __name__ == "__main__":
    safe_eval(input("Input : "), dict)
```

* After carefully reading the source code, it is clear that the goal is to make `dict(OUR_INPUT)` return the flag

* In python, you can create dictionaries out of keyword arguments like so :  

```python
>>> dict(key1=5, key2=10)
{'key1': 5, 'key2': 10}
```

* To get the flag, we can just pass `flag=flag` as our input :  

```txt
Input : flag=flag
{'flag': 'shellmates{9286a596f6a2b68bfd4eae4e4d0d6f10}'}
```

* You can find an automated solve script [here](./solve.py)

## Flag

`shellmates{9286a596f6a2b68bfd4eae4e4d0d6f10}`
