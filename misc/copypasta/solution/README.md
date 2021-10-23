# Copypasta

## Write-up

A rather stupid challenge just to annoy people.  
The flag shown in the challenge contains more than printable characters, it also contains
zero-width whitespaces, so copy/pasting the flag will not yield a correct flag, since those
invisible characters would also be copied.

```python
>>> s = "s​h​e​l​l​m​a​t​e​s​{​3​6​a​2​5​e​9​c​7​0​d​f​4​d​5​f​4​2​0​e​4​9​b​1​b​1​5​a​2​7​8​7​0​0​d​3​9​4​7​c​6​7​e​4​c​9​e​c​4​e​0​9​e​f​6​8​e​7​8​6​1​a​4​8​0​2​4​2​5​f​e​c​8​f​7​9​b​5​5​5​e​9​2​7​2​5​9​d​4​9​0​e​f​c​b​8​5​7​2​8​7​1​3​e​c​2​1​5​5​7​8​5​9​3​4​5​9​d​2​b​3​c​b​3​f​d​b​7​}​"
>>> s
's\u200bh\u200be\u200bl\u200bl\u200bm\u200ba\u200bt\u200be\u200bs\u200b{\u200b3\u200b6\u200ba\u200b2\u200b5\u200be\u200b9\u200bc\u200b7\u200b0\u200bd\u200bf\u200b4\u200bd\u200b5\u200bf\u200b4\u200b2\u200b0\u200be\u200b4\u200b9\u200bb\u200b1\u200bb\u200b1\u200b5\u200ba\u200b2\u200b7\u200b8\u200b7\u200b0\u200b0\u200bd\u200b3\u200b9\u200b4\u200b7\u200bc\u200b6\u200b7\u200be\u200b4\u200bc\u200b9\u200be\u200bc\u200b4\u200be\u200b0\u200b9\u200be\u200bf\u200b6\u200b8\u200be\u200b7\u200b8\u200b6\u200b1\u200ba\u200b4\u200b8\u200b0\u200b2\u200b4\u200b2\u200b5\u200bf\u200be\u200bc\u200b8\u200bf\u200b7\u200b9\u200bb\u200b5\u200b5\u200b5\u200be\u200b9\u200b2\u200b7\u200b2\u200b5\u200b9\u200bd\u200b4\u200b9\u200b0\u200be\u200bf\u200bc\u200bb\u200b8\u200b5\u200b7\u200b2\u200b8\u200b7\u200b1\u200b3\u200be\u200bc\u200b2\u200b1\u200b5\u200b5\u200b7\u200b8\u200b5\u200b9\u200b3\u200b4\u200b5\u200b9\u200bd\u200b2\u200bb\u200b3\u200bc\u200bb\u200b3\u200bf\u200bd\u200bb\u200b7\u200b}\u200b'
>>> s = s.replace("\u200b", "")
>>> s
'shellmates{36a25e9c70df4d5f420e49b1b15a278700d3947c67e4c9ec4e09ef68e7861a4802425fec8f79b555e927259d490efcb85728713ec215578593459d2b3cb3fdb7}'
>>> __import__("clipboard").copy(s)
>>> # Paste the flag in CTFd
```

## Flag

`shellmates{36a25e9c70df4d5f420e49b1b15a278700d3947c67e4c9ec4e09ef68e7861a4802425fec8f79b555e927259d490efcb85728713ec215578593459d2b3cb3fdb7}`
