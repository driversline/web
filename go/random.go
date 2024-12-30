package main

import (
    "fmt"
    "math/rand"
    "time"
)

func main() {
    max := 999999

    rand.Seed(time.Now().UnixNano())

    for {
        randomNum := rand.Intn(max + 1)
        fmt.Println(":", randomNum)
        fmt.Print("Press Enter to generate...")
        fmt.Scanln()
    }
}
