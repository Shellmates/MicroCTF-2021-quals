# Vault

## Write-up

After decompiling the jar file, use this simple python script:

print(bytes([52037 - 0xCafe ,
     52077 - 0xCafe ,
     52077 - 0xCafe ,
     52066 - 0xCafe ,
     52046 - 0xCafe ,
     52063 - 0xCafe ,
     52081 - 0xCafe ,
     52081 - 0xCafe ,
     52085 - 0xCafe ,
     52077 - 0xCafe ,
     52080 - 0xCafe ,
     52066 - 0xCafe]).decode("utf8"))

## Flag

shellmates{g00D_j0B_rIo_wE_h4Ve_Th3_m0N3Y}
