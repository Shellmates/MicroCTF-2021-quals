# untar me 100

## Write-up

```bash
#!/bin/bash

TAR_FILE="archive.tar.gz"
NUM=100

# extract from archive NUM times
for ((i=0; i < $NUM; i++)); do
  tar xzf $TAR_FILE
done

cat flag.txt
```

### Flag

`shellmates{woW_u_Re_N0T_4_SCr1pT_K1Dd13}`
