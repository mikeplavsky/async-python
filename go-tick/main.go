package main

import (
	"fmt"
	"os"
	"strconv"
	"time"
)

func tick(i int, done chan<- bool) {

	time.Sleep(5000 * time.Millisecond)
	fmt.Println(i)

	done <- true

}

func main() {

	times, _ := strconv.Atoi(os.Args[1])

	done := make(chan bool)

	for i := 0; i < times; i++ {

		go func(i int) {
			tick(i, done)
		}(i)

	}

	for i := 0; i < times; i++ {
		<-done
	}

}
