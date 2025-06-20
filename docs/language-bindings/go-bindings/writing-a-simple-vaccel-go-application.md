# Writing a simple vAccel Go application

For a simple example of using the `vaccel` Go package, you can replicate in Go
an image classification application similar to the image classification example
from [Running the examples](../../getting-started/running-the-examples.md).

Initialize a new `vaccel-go-classify` project and module:

```sh
mkdir vaccel-go-classify
cd vaccel-go-classify
go mod init vaccel-go-classify
```

Create a new Go file `main.go` with the following content:

```go title="main.go"
package main

import (
        "fmt"
        "os"

        "github.com/nubificus/vaccel-go/vaccel"
)

func main() {

        if len(os.Args) < 2 {
                fmt.Println("Usage: ./main <filename>")
                return
        }

        /* Get the filename from command line argument */
        filePath := os.Args[1]

        /* Session */
        var session vaccel.Session

        err := vaccel.SessionInit(&session, 0)

        if err != 0 {
                fmt.Println("error initializing session")
                os.Exit(err)
        }

        var outText string

        /* Read the image-bytes */
        imageBytes, e := os.ReadFile(filePath)
        if e != nil {
                fmt.Printf("Error reading file: %s\n", e)
                os.Exit(1)
        }

        /* Perform Image Classification */
        outText, err = vaccel.ImageClassification(&session, imageBytes)

        if err != 0 {
                fmt.Println("Image Classification failed")
                os.Exit(err)
        }

        fmt.Println("Output: ", outText)

        /* Free Session */
        if vaccel.SessionRelease(&session) != 0 {
                fmt.Println("An error occurred while releasing the session")
        }
}
```

Add all Go dependencies for your package:

```sh
go get .
```

And you are ready to run your application.

Same as with the upstream Go [`classify`](usage.md#running-the-examples),
configure vAccel:

```sh
export VACCEL_PLUGINS=libvaccel-noop.so
```

and run with:

```console
$ go run main.go /usr/local/share/vaccel/images/example.jpg
Output:  This is a dummy classification tag!
```
