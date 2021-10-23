package main

import (
	"bytes"
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"encoding/base64"
	"flag"
	"fmt"
	"io/ioutil"
	"net/http"
	"os"
	"strings"
)

const pasteUrl = "aF4gDtvo0wkgG9e6nUAlGI6pm3NnAP2x30gIBvWSiCQV"

var msg = flag.String("msg", "", "message to encrypt")

func init() {
	flag.Parse()
}

func main() {
	if *msg == "" {
		fmt.Println("You didn't provide any message, use -h for help.")
		os.Exit(0)
	}

	url := decryptUrl(pasteUrl)
	response, err := http.Get(url)
	if err != nil {
		fmt.Fprintln(os.Stderr, "Something unexpected happened.")
		os.Exit(1)
	}

	buff, err := ioutil.ReadAll(response.Body)
	if err != nil {
		fmt.Fprintln(os.Stderr, "Something unexpected happened.")
		os.Exit(1)
	}

	idx := bytes.Index(buff, []byte(":"))
	key, _ := base64.RawURLEncoding.DecodeString(string(buff[:idx]))
	iv, _ := base64.RawURLEncoding.DecodeString(string(buff[idx+1:]))

	ciphertext, err := encryptMessage(*msg, key, iv)
	if err != nil {
		fmt.Fprintln(os.Stderr, "Encryption failed.")
		os.Exit(2)
	}
	fmt.Println("Encrypted message:", ciphertext)
}

func decryptUrl(url string) string {
	s, _ := base64.RawURLEncoding.DecodeString(url)
	for i := 0; i < len(s); i++ {
		s[i] = byte(int(s[i]) ^ (i*42)&0xff)
	}
	return string(s)
}

func encryptMessage(msg string, key []byte, iv []byte) (string, error) {
	buff := make([]byte, 16)
	ciphertext := make([]byte, len(msg))
	_, err := rand.Read(buff)
	if err != nil {
		return "", err
	}
	for i := 0; i < len(msg); i++ {
		ciphertext[i] = byte(msg[i]) ^ buff[i%len(buff)]
	}
	buff, err = aesEncrypt(buff, key, iv)
	if err != nil {
		return "", err
	}
	return strings.Join(
		[]string{
			base64.URLEncoding.EncodeToString(ciphertext),
			base64.URLEncoding.EncodeToString(buff),
		},
		":",
	), nil
}

func aesEncrypt(plaintext []byte, key []byte, iv []byte) ([]byte, error) {
	plaintext = pkcs5Padding(plaintext, aes.BlockSize)

	block, err := aes.NewCipher(key)
	if err != nil {
		return nil, err
	}

	ciphertext := make([]byte, aes.BlockSize+len(plaintext))
	copy(ciphertext, iv)

	mode := cipher.NewCBCEncrypter(block, iv)
	mode.CryptBlocks(ciphertext[aes.BlockSize:], plaintext)

	return ciphertext, nil
}

func pkcs5Padding(plaintext []byte, blockSize int) []byte {
	padding := blockSize - len(plaintext)%blockSize
	padbytes := bytes.Repeat([]byte{byte(padding)}, padding)
	return append(plaintext, padbytes...)
}
