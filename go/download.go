package main

import (
    "fmt"
    "io"
    "io/ioutil"
    "net/http"
    "net/url"
    "os"
    "path/filepath"
    "strings"
    "golang.org/x/net/html"
)

func downloadFile(fileUrl string, folder string) {
    response, err := http.Get(fileUrl)
    if err != nil {
        fmt.Printf("Error downloading %s: %v\n", fileUrl, err)
        return
    }
    defer response.Body.Close()

    if response.StatusCode != http.StatusOK {
        fmt.Printf("Error: %s\n", response.Status)
        return
    }

    _, fileName := filepath.Split(fileUrl)
    filePath := filepath.Join(folder, fileName)

    out, err := os.Create(filePath)
    if err != nil {
        fmt.Printf("Error creating file %s: %v\n", filePath, err)
        return
    }
    defer out.Close()

    _, err = io.Copy(out, response.Body)
    if err != nil {
        fmt.Printf("Error writing file %s: %v\n", filePath, err)
    } else {
        fmt.Printf("Downloaded: %s\n", filePath)
    }
}

func downloadWebsite(baseUrl string, folder string) {
    response, err := http.Get(baseUrl)
    if err != nil {
        fmt.Printf("Error downloading %s: %v\n", baseUrl, err)
        return
    }
    defer response.Body.Close()

    if response.StatusCode != http.StatusOK {
        fmt.Printf("Error: %s\n", response.Status)
        return
    }

    htmlContent, err := ioutil.ReadAll(response.Body)
    if err != nil {
        fmt.Printf("Error reading HTML: %v\n", err)
        return
    }

    htmlFilePath := filepath.Join(folder, "index.html")
    err = ioutil.WriteFile(htmlFilePath, htmlContent, 0644)
    if err != nil {
        fmt.Printf("Error saving HTML: %v\n", err)
        return
    }
    fmt.Printf("Downloaded HTML: %s\n", htmlFilePath)

    doc, err := html.Parse(strings.NewReader(string(htmlContent)))
    if err != nil {
        fmt.Printf("Error parsing HTML: %v\n", err)
        return
    }

    var f func(*html.Node)
    f = func(n *html.Node) {
        if n.Type == html.ElementNode {
            if n.Data == "link" {
                for _, a := range n.Attr {
                    if a.Key == "href" {
                        cssUrl := resolveURL(baseUrl, a.Val)
                        downloadFile(cssUrl, folder)
                    }
                }
            } else if n.Data == "script" {
                for _, a := range n.Attr {
                    if a.Key == "src" {
                        jsUrl := resolveURL(baseUrl, a.Val)
                        downloadFile(jsUrl, folder)
                    }
                }
            } else if n.Data == "img" {
                for _, a := range n.Attr {
                    if a.Key == "src" {
                        imgUrl := resolveURL(baseUrl, a.Val)
                        downloadFile(imgUrl, folder)
                    }
                }
            }
        }
        for c := n.FirstChild; c != nil; c = c.NextSibling {
            f(c)
        }
    }
    f(doc)
}

func resolveURL(base string, ref string) string {
    u, err := url.Parse(ref)
    if err != nil {
        return ref
    }
    if u.Scheme == "" {
        baseUrl, _ := url.Parse(base)
        u = baseUrl.ResolveReference(u)
    }
    return u.String()
}

func main() {
    var baseUrl string
    var folder string

    fmt.Print("Enter the website URL: ")
    fmt.Scanln(&baseUrl)

    fmt.Print("Enter the path to the folder for saving (or leave empty for the current folder): ")
    fmt.Scanln(&folder)

    if folder == "" {
        folder = "."
    }

    os.MkdirAll(folder, os.ModePerm)
    downloadWebsite(baseUrl, folder)
}
