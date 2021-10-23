# agent47

## Write-up

We can see that no keys are provided, we can deduce that it was encrypted using a shift cipher.
We notice that the message contains non alphanumeric values and the challenge's named agent-47- we deduce that it's ROT47.
We can use [CyberChef](https://gchq.github.io/CyberChef/#recipe=ROT47(47)From_Base64('A-Za-z0-9%2B/%3D',true)&input=J3Y5PTYkcWIyKElEeHZkPTU%2BJ0p4dnk9eHZ1OjN2Jjg1dmc4ND4nOStycV8ydj1LeHZgPTRifTkrYSY4fjhBSzJ2J0QzdmA5NXYnSzZieEg1cyJiKUt0YClfQWB9JyM3JXN1Q3xgaEp8dyJJfGJfbA) to decrypt it from ROT47 then we get the flag in base64.

## Flag
`shellmates{r0t47_15_Ju5T_L1k3_r0t13}`
