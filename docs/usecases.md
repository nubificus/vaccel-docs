# Use Cases

## HW Acceleration on Serverless deployments

Serverless Computing has gained significant ground over the past couple of
years, especially due to its unprecedented "on-demand" computing offering at a
fraction of the price of having a dedicated VM or bare-metal machine.

However, apart from the limitation that one has to re-write its application to
match the Serverless computing paradigm (micro-service, event triggered),
access to "specialized" equipment is not something common / supported now.
Major serverless offerings such as AWS Lambda, Azure functions, or Google
Functions do not offer access to hardware acceleration for even the most common
tasks (ML inference).

To work around this issue, and study the implications of hardware acceleration
in serverless computing we started experimenting on
[OpenFaaS](https://openfaas.com) and its integration with
[vAccel](https://vAccel.org)

Given OpenFaaS huge community support, installing it on a working k8s cluster is 
a piece of cake. You can find more information in the following document:

- [Deployment guide for Kubernetes](https://docs.openfaas.com/deployment/kubernetes/)


Assuming you have a working OpenFaaS installation, leveraging the hardware
acceleration capabilities of your cluster with vAccel should be really
straightforward.

### Create a new OpenFaaS Profile

To take advantage of vAccel on Firecracker via OpenFaaS, all you have to do, is
tell OpenFaaS to spawn the relevant functions using a different profile. 

To allow maximum flexibility without overloading the OpenFaaS function
configuration, the OpenFaaS developers have introduced the concept of Profiles.
This is simply a reserved function annotation that the `faas-provider` can
detect and use to apply the advanced configuration.

Profiles must be pre-created, similar to Secrets, by the cluster admin. When
installing OpenFaaS on Kubernetes, Profiles use a CRD. This must be installed
during or prior to start the OpenFaaS controller. When using the official Helm
chart this will happen automatically. Alternatively, you can apply [this
YAML](https://github.com/openfaas/faas-netes/blob/master/yaml/crd.yml) to
install the CRD.

So, let's create a hardware acceleration profile on our OpenFaaS installation!

As mentioned earlier in the docs, to deploy vAccel-able workloads on a k8s
cluster we have to follow the [relevant instructions](/k8s/kata.md).
Essentially, we leverage the awesome work done by the `kata-containers` team
and provide an alternative to the generic Firecracker `RuntimeClass`, kata-fc.

So, assuming you have a working cluster with [vAccel installed on
k8s](/k8s/kata.md), all you need to do to run an OpenFaaS function there is to
create a Profile:

```
kubectl apply -f- << EOF
kind: Profile
apiVersion: openfaas.com/v1
metadata:
    name: gvisor
    namespace: openfaas
spec:
    runtimeClassName: kata-fc
EOF
```

### Build an image classification function example

Then, we need to build a function that consumes the vAccel API, as exposed to
the available functions. Check out
[this](https://github.com/nubificus/stdinout/tree/vaccel) repo to get an idea
of how easy it is to create a function that classifies images ;-)

```
git clone https://github.com/nubificus/stdinout -b vaccel
cd stdinout
```

Examine `test.c`: it is a simple file that gets its input from stdin, stores it
into a memory buffer and pushes it to be classified, using the vAccel API. The
output is a string of the classification label, along with the accuracy given
by the specific model used. Lets build this simple function:

```
make
```

The output of this command is an executable that given an image from `STDIN`
will output the classification text, consuming the vAccel API. More or less,
something like the following:

```
# Set the library path to ./ for libfileread.so and 
# /usr/local/lib for libvaccel.so
export LD_LIBRARY_PATH=./:/usr/local/lib

# set the vAccel Backend (running on an RTX 2060 Super
export VACCEL_BACKENDS=/usr/local/lib/libvaccel-jetson.so

cat dog_0.jpg | ./test
```
Given the input is the file below:


<p align="center">
  <img src="/img/dog_0.jpg">
</p>


the output should be something like the following:

```
Initialized session with id: 1
imagenet: 60.54688% class #249 (malamute, malemute, Alaskan malamute)
classification tags: 60.547% malamute, malemute, Alaskan malamute
```

### Integrate this operation into a function for OpenFaaS

To integrate this into a function, we first need to build a container image,
with the libvaccel library along with the vAccel-virtio backend (Since this
workload is going to be running on a Firecracker VM ;-).

```
docker build -t nubificus/fclassify -f Dockerfile.virtio .
```

Then, a simple YAML like the following (`fclassify.yaml`) will instantiate a
function that will execute the `fprocess:` directive, in our case, `test`:

```
provider:
  name: openfaas
  gateway: http://myclusternode:31112

functions:
  fclassify:
    skip_build: false
    image: nubificus/fclassify
    fprocess: "/test"
    annotations:
      com.openfaas.profile: kata
    labels:
      com.openfaas.scale.min: 12
      com.openfaas.scale.max: 100
      com.openfaas.scale.factor: 40
    limits:
      cpu: 10m
    requests:
      cpu: 10m
```

The important parts to note at this YAML file are:

```
      com.openfaas.profile: kata
```

which makes sure that the function will be invoked on the kata profile, using
the kata-fc RuntimeClass (which supports vAccel).

and

```
    image: nubificus/fclassify
    fprocess: "/test"
```

which denotes that the image to be used is nubificus/fclassify, built earlier
using `Dockerfile.virtio`, with /test being the entrypoint.

### Deploy the function

Finally, using the command below:

```
faas-cli deploy -f fclassify.yaml
```

will instantiate the number of replicas chosen for fclassify as well as listen
to requests for image classification, ready to forward them to the actual
hardware securely and efficiently!


### Consume the function

Given an ingress rule that will route traffic to the fclassify function, we can
invoke this operation externally. For instance, given the following three
images:

<p align="center">
  <img src="/img/object_0.jpg" width=200px>
  <img src="/img/object_2.jpg" width=200px>
  <img src="/img/object_3.jpg" width=200px>
</p>

we can invoke the OpenFaaS function on our local K8s OpenFaaS cluster:

```
for x in object_0.jpg object_2.jpg object_3.jpg
do 
  cat $x | curl -L -X POST https://openfaas.nbfc.io/function/fclassify \
	--data-binary "@$x" & 
done 
```

and the output should be:
```
[1] 3129602
[2] 3129604
[3] 3129606

Initialized session with id: 1
classification tags: 23.145% mountain bike, all-terrain bike, off-roader
Initialized session with id: 1
classification tags: 45.776% freight car
Initialized session with id: 1
classification tags: 90.771% canoe
```
