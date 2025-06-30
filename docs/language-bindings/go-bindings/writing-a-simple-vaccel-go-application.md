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
                fmt.Printf("Usage: %s <filename>\n", os.Args[0])
                return
        }

        /* Get the filename from command line argument */
        filePath := os.Args[1]

        var session vaccel.Session
        err := session.Init(0)
        if err != vaccel.OK {
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
        if err != vaccel.OK {
                fmt.Println("Image Classification failed")
                os.Exit(err)
        }

        fmt.Println("Output: ", outText)

        /* Free Session */
        if session.Release() != vaccel.OK {
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

## Resource Handling

Furthermore, you may also need a model to perform the classification operation.
A vAccel plugin will probably require the model in the form of a vAccel
resource. The following snippet demonstrates how to initialize, register and
correspondingly unregister and re- lease the resource:

```c
var resource vaccel.Resource
modelPath := "/path/to/model.pt"
err := resource.Init(modelPath, vaccel.ResourceModel)
if err != vaccel.OK {
    fmt.Printf("Could not initialize resource: %d\n", err)
    [...]
}

err = session.Register(&resource)
if err != vaccel.OK {
    fmt.Printf("Could not register resource: %d\n", err)
    [...]
}

err = session.Unregister(&resource)
if err != vaccel.OK {
    fmt.Printf("Could not unregister resource: %d\n", err)
    [...]
}

err = resource.Release()
if err != vaccel.OK {
    fmt.Printf("Could not release resource: %d\n", err)
    [...]
}
```
