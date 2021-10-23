# EncryptedKey

## Write-up

- Source code :  

```c
#include  <string.h>
#include  <stdio.h>
#include  <stdlib.h>
#include  <unistd.h>

#define  KEY_LENGTH  34
#define  CIPHER_LENGTH  33

int  main(){
//Result after xoring the flag
char  cipher[CIPHER_LENGTH] = "\x1b\xd\x9\x0\x1\xc\x15\x11\x16\x8\x11\x1f\x40\x41\x2b\x27\x17\x1d\x2d\x2b\x1c\x5b\x6c\x3e\x5\xe\x5e\x57\x50\x5d\x1a\x7\xe";

//Turn OFF Buffering
setbuf(stdin, NULL);
setbuf(stdout, NULL);

printf("Enter the secret key : ");
//The input buffer
char  input[KEY_LENGTH];
memset(&input, '\0', KEY_LENGTH);
read(STDIN_FILENO, input, KEY_LENGTH);

//The xored input
char  xoredInput[CIPHER_LENGTH];
memset(&xoredInput, '\0', CIPHER_LENGTH);
for (size_t  i = 0; i < CIPHER_LENGTH ; i++){
xoredInput[i] = input[i] ^ input[i + 1];
}

//Compare the xored input with the key
if (!memcmp(xoredInput, cipher, 33))
printf("Go submit it !\n%s", input);
else
printf("Wrong key! Try again!");
return  0;
}
```


- solution :
	- Using any c decompiler (ghidra, cutter) you can notice that we're xoring adjacent characters and then compare the result with a sequence of bytes.
	- Knowing that the flag format is shellmates{}, and using xor properties, we xor the first byte with 's' to get the second character .We xor the result with the next byte to get the next character and so on .
 
## Flag

`shellmates{ju5t_xor_th3_adj4c3nts}`
