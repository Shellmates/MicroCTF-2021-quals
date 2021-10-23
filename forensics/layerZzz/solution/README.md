# layerZzz

## Write-up

1. Extract the archive :  

```bash
tar xvzf layerZzz.tar.gz
```

2. Read `message.txt` :  

```txt
Hello there challenger !
We're looking for a file which has a name that starts with "secret" and ends with b64 extension.
Can you **find** it ??
Flag format : shellmates{}
```

3. Find the file described :  

```bash
find find_me/ -name "secret*.b64"
# We find a base64 encoded file named "secret-dumpfile.b64"
```

4. Base64 decode `secret-dumpfile.b64` and redirect output to `secret-dumpfile` :

```bash
base64 -d secret-dumpfile.b64 > secret-dumpfile
```

5. `secret-dumpfile` contains what looks like a hex dump, so let's revert it while redirecting output to `secret` :  

```bash
xxd -r secret-dumpfile > secret
```

6. Check file type of `secret` :  

```bash
file secret
# secret: Zip archive data, at least v2.0 to extract
# => zip file
```

7. Unzip `secret` :  

```bash
unzip secret
# Archive:  secret
#   inflating: nothing_to_see_here
```

8. Check file type of `nothing_to_see_here` :  

```bash
file nothing_to_see_here
# nothing_to_see_here: ELF 64-bit LSB executable, x86-64, version 1 (GNU/Linux), statically linked, for GNU/Linux 3.2.0, BuildID[sha1]=d3bff38b01c1cd033ea3081df665cb6187d0301e, not stripped
# => Linux executable file
```

9. Execute `nothing_to_see_here` :  

```bash
./nothing_to_see_here
# Output: Nothing to see here 👀
```

10. Stringrep :  

```bash
strings nothing_to_see_here | grep shellmates
# Output: shellmates{CONGrATzZzz_U_d3FEa73d_a1l_Layer$!!!}
```

## Flag

`shellmates{CONGrATzZzz_U_d3FEa73d_a1l_Layer$!!!}`
