package main

import (
	"fmt"
	"time"
)

func tick(i int, done chan<- bool) {

	time.Sleep(1000 * time.Millisecond)
	fmt.Println(i)

}

func main() {

	done := make(chan bool)
	go tick(1, done)

	<-done

}
