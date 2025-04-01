---
title: "vAccel-Go: Go bindings for vAccel"
date: 2024-01-02T14:28:46Z
tags: [vAccel, go]
---

[Go](https://go.dev/) bindings for vAccel are implemented in the `vaccel` Go
package. The `vaccel` package leverages the vAccel C API to provide native Go
support for vAccel operations.

## Installation Guide

### vAccel Installation

First of all, a vAccel installation is required before proceeding to the next
sections. Instructions on how to install vAccel can be found
[here](https://docs.vaccel.org/quickstart/).

### vAccel-Go Bindings Installation

Prior to installing the bindings, we have to make sure that Go 1.20 or newer is
installed on our system. We can check this using the following command:

```sh
go version
```

Otherwise, Go 1.20 needs to be installed. You can find instructions on how to
install Go [here](https://go.dev/doc/install).

Afterwards:

```sh
git clone https://github.com/nubificus/go-vaccel.git
cd go-vaccel
make all
```

Now you have successfully built some vAccel programs using Go. The executables
are located in go-vaccel/bin. You can run the `noop` example:

```sh
export VACCEL_LOG_LEVEL=4
export VACCEL_PLUGINS=/usr/lib/x84_64-linux-gnu/libvaccel-noop.so
./bin/noop
```

Or the `exec` example, providing a path for the shared object and an integer:

```sh
export VACCEL_PLUGINS=/usr/lib/x86_64-linux-gnu/libvaccel-exec.so
./bin/exec /usr/local/lib/libmytestlib.so 100
```

## Tutorial

The following example demonstrates the usage of the `vaccel` package to build
vAccel-enabled Go programs. The tutorial will perform an image classification
operation, using the no-op plugin.

### Example

**Create the project directory**

```sh
cd ~
mkdir go-vaccel-test
cd go-vaccel-test
```

**Initialize the Module**

```sh
go mod init go-vaccel-test
```

**Download the bindings**

```sh
go get github.com/nubificus/go-vaccel
```

**Add a Go file**

```sh
touch main.go
```

**Add the following lines to perform Image Classification**

```go
package main

import (
        "fmt"
        "os"

        "github.com/nubificus/go-vaccel/vaccel"
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

**Build the source file:**

```sh
go build main.go
```

**Define the location of the plugin:**

```sh
export VACCEL_PLUGINS=/usr/lib/x84_64-linux-gnu/libvaccel-noop.so
```

**And run:**

```sh
./main </path/to/image>
```

**You must see the following message:**

```console
[noop] Calling Image classification for session 1
[noop] Dumping arguments for Image classification:
[noop] len_img: <numBytes>
[noop] will return a dummy result
Output:  This is a dummy classification tag!
```

### Conclusion

The above example shows how to use the `vaccel` package in Go to use various
vAccel features. As you can see, the example doesn't run an actual image
classification operation, since we use the no-op plugin for testing purposes.
However, we could use a vAccel backend that performs the operation.
[Here](https://github.com/nubificus/go-vaccel/), you can find more vAccel tools
and operations that you could possibly use in your Go programs. For example,
except image classification, you can write
[programs that use the exec plugin](https://github.com/nubificus/go-vaccel/blob/main/exec/main.go),
which gives you the opportunity to use functions contained in a shared object.
Or, finally, you could also use the
[`noop` example](https://github.com/nubificus/go-vaccel/blob/main/noop/main.go)
if you just want to test the installation of the package.
