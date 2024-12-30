package main

import (
    "fmt"
    "net"
)

func main() {
    var serverAddress string
    var port string

    fmt.Print("Enter the Minecraft server address: ")
    fmt.Scanln(&serverAddress)

    fmt.Print("Enter the port (default 25565): ")
    fmt.Scanln(&port)

    if port == "" {
        port = "25565"
    }

    fullAddress := fmt.Sprintf("%s:%s", serverAddress, port)

    conn, err := net.Dial("tcp", fullAddress)
    if err != nil {
        fmt.Println("Server is unavailable:", err)
        return
    }
    defer conn.Close()

    fmt.Println("Server is running!")
}
