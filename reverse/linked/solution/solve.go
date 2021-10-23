package main

import (
	"encoding/binary"
	"fmt"
	"io"
	"os"
)

type Node struct {
	char byte
	next uint64
}

const (
	heapDump    = "23797_mem_55e44a780000-55e44a7813b0.bin"
	startAddr   = 0x55E44A780000
	startOffset = 0x4E0
	endOffset   = 0xB80
)

func main() {
	nodes := make(map[uint64]Node)

	f, err := os.Open(heapDump)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Couldn't read file: %s.\n", heapDump)
		os.Exit(1)
	}
	defer f.Close()

	_, err = f.Seek(startOffset, 0)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Couldn't seek to position: %#x.\n", startOffset)
		os.Exit(1)
	}

	size := endOffset - startOffset
	buff := make([]byte, size)
	_, err = io.ReadFull(f, buff)
	if err != nil {
		fmt.Fprintf(os.Stderr, "Couldn't read %d bytes from file.\n", size)
		os.Exit(1)
	}

	addresses := []uint64{}
	for i := 0; i < size; i += 0x20 {
		// discard heap metadata
		chunk := buff[i+0x10 : i+0x20]

		node_addr := uint64(startAddr + startOffset + i + 0x10)
		next_addr := binary.LittleEndian.Uint64(chunk[8:])
		nodes[node_addr] = Node{
			char: chunk[0],
			next: next_addr,
		}
		addresses = append(addresses, next_addr)
	}

	// inefficient
	var node_addr uint64
	for addr, _ := range nodes {
		if !contains(addresses, addr) {
			node_addr = addr
			break
		}
	}

	for node_addr != 0 {
		fmt.Printf("%c", nodes[node_addr].char)
		node_addr = nodes[node_addr].next
	}
	fmt.Println()
}

func contains(s []uint64, target uint64) bool {
	for _, v := range s {
		if v == target {
			return true
		}
	}
	return false
}
