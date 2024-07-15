---
title: "vAccel-go: Golang bindings for vAccel"
date: 2024-01-02T14:28:46Z
tags: [vAccel, go] 
---

To facilitate the use of vAccel, we provide bindings for popular languages,
apart from `C`. Essentially, the vAccel `C` API can be called from any language
that interacts with `C` libraries. Building on this, we are thrilled to present
support for [Go](https://golang.dev).

Essentially, the `C`/`Go` interaction is already pretty smooth, given the
native `CGO` support available. We introduce v0.1 of the vAccel-go bindings,
pending a feature-full update in the coming months. In this post, we go
through the initial implementation details, as well as a hands-on tutorial on
how to write your first vAccel program in `Go`!

### Golang overview
The `Go` Programming Language is designed for scalability, 
making it suitable for cloud computing and large-scale servers.
Go enhances development speed and efficiency, since it compiles
quickly (compared to other languages), and provides a great
Standard Library, along with built-in concurrency tools. Golang 
is also a cloud-native Programming Language. Information
about Go installation can be found [here](https://go.dev/doc/install), 
but there are also instructions on how to install `Go` in the
[vAccel-go bindings installation guide](https://github.com/nubificus/go-vaccel).

### vAccel Go package
The vaccel package in Golang provides access to vAccel operations, which
can be used by the developers on their own `Go` programs. The vaccel package uses 
the native `C` bindings in order to use the vAccel `C` API. The following diagram 
demonstrates the functionality of the vaccel package:

<figure>
  <img src="img/vaccel_go.png" align=center />
  <figcaption>Figure 1: High-level overview of the vAccel Go package</figcaption>
</figure>

### Installation Guide
#### vAccel Installation
First of all, a vAccelRT installation is required before proceeding to the next sections. 

#### Build from source
In Ubuntu-based systems, you need to have the following packages to build vaccelrt:
1. `cmake`
2. build-essential

You can install them using the following command:
```
sudo apt-get install -y cmake build-essential
```
Get the source code for **vaccelrt**:
```
git clone https://github.com/cloudkernels/vaccel --recursive
```
Prepare the build directory:
```
cd vaccelrt
mkdir build
cd build
```
#### Building the core runtime library
```
# This sets the installation path to /usr/local, and the current build
# type to 'Release'. The other option is the 'Debug' build
cmake ../ -DCMAKE_INSTALL_PREFIX=/usr/local -DCMAKE_BUILD_TYPE=Release -DBUILD_EXAMPLES=ON -DBUILD_PLUGIN_EXEC=ON -DBUILD_PLUGIN_NOOP=ON
```
```
make
sudo make install
```
#### vAccel-Go Bindings Installation

##### Go Installation
Of course, prior to installing the bindings, we have to make sure that Golang 1.20 or newer is installed in our system. We can check this using the following command:
```
go version
```
Otherwise, `go 1.20` needs to be installed. You can find instructions on how to install Go [here.](https://go.dev/doc/install) 

##### Build the Bindings from source
Download the source code:
```
git clone https://github.com/nubificus/go-vaccel.git
```
First, you can build the examples:
```
# Set vaccel location
export PKG_CONFIG_PATH=/usr/local/share/
cd go-vaccel
make all
```
Now you have successfully built some vaccel programs using Go. The executables are located in go-vaccel/bin. You can run the `noop` example:
```
export VACCEL_BACKENDS=/usr/local/lib/libvaccel-noop.so
./bin/noop
```
Or the `exec` example, providing a path for the shared object and an integer:
```
export VACCEL_BACKENDS=/usr/local/lib/libvaccel-exec.so
./bin/exec /usr/local/lib/libmytestlib.so 100
# if everything go as expected, the
# plugin will probably double the integer 
```

### Tutorial
The following example demonstrates the usage of the `vaccel` package to build vaccel-enabled `Go` programs. The tutorial will perform an image classification operation, using the no-op plugin.
Keep in mind the following three conditions before building:

**1. Make sure to import the package in your programs:**
```go
import "github.com/nubificus/go-vaccel/vaccel"
```
**2. Define `vaccel` location:**
```
export PKG_CONFIG_PATH=/usr/local/share
```
**3. And finally, always define the location of the `vaccel-plugin` you are willing to use:**
```
# In case of No-Op for testing:
export VACCEL_BACKENDS=/usr/local/lib/libvaccel-noop.so
```

### Example
**Create the project directory**
```
cd ~
mkdir go-vaccel-test
cd go-vaccel-test
```
**Initialize the Module**
```
go mod init go-vaccel-test
```

**Download the bindings**
```
go get github.com/nubificus/go-vaccel
```

**And create a `Go` file**
```
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
	if vaccel.SessionFree(&session) != 0 {
		fmt.Println("An error occurred while freeing the session")
	}
}
```
**Then, specify vaccel location:**
```
export PKG_CONFIG_PATH=/usr/local/share
```
**Define the location of the plugin:**
```
export VACCEL_BACKENDS=/usr/local/lib/libvaccel-noop.so
```
**Build the source file:**
```
go build main.go
```
**And run:**
```
./main </path/to/image>
```
**You must see the following message:**
```
[noop] Calling Image classification for session 1
[noop] Dumping arguments for Image classification:
[noop] len_img: <numBytes>
[noop] will return a dummy result
Output:  This is a dummy classification tag!
```
### Conclusion
The above example shows how to use the `vaccel` package in `Go` to use various vaccel features. As you can see, the example doesn't run an actual image classification operation, since we use the no-op plugin for testing purposes. However, we could use a vaccel backend that performs the operation. [Here](https://github.com/nubificus/go-vaccel/), you can find more vaccel tools and operations that you could possibly use in your `Go` programs. For example, except image classification, you can write [programs that use the exec plugin](https://github.com/nubificus/go-vaccel/blob/main/exec/main.go), which gives you the opportunity to use functions contained in a shared object. Or, finally, you could also use the [`noop` example](https://github.com/nubificus/go-vaccel/blob/main/noop/main.go) if you just want to test the installation of the package.
