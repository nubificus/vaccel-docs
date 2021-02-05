# vAccel on k8s using Kata & Firecracker

TODO
- add proper links to yaml files
- add correct outputs
- add components build documentation

## Prerequisites

In order to run vAccel on Kata containers with Firecracker you need to meet the following prerequisites on each k8s node that will be used for acceleration:

- containerd as container manager
- devicemapper as CRI plugin default snapshotter
- NVIDIA GPU which supports CUDA (*for now*)
- [jetson-inference](https://github.com/dusty-nv/jetson-inference) libraries (libjetson-inference.so must be installed and properly linked with CUDA libraries)


## Quick start
<sup>*We built on* [kata-containers/kata-deploy](https://github.com/kata-containers/packaging/tree/master/kata-deploy) *to deploy vAccel on Kata Containers. Our fork repo can be found on* [cloudkernels/packaging](https://github.com/cloudkernels/packaging/tree/vaccel-dev)</sub>

### Deploy vAccel with Kata

First label each node where vAccel-kata should be deployed:

```
$ kubectl label nodes <your-node-name> vaccel=true
```

Install vAccel-kata on each "vaccel=true" node:

```
$ kubectl kata-deploy.yaml 
```

The kata-deploy daemon calls the vAccel download script. It may take a few minutes to download the ML Inference models.
Check the pod logs to be sure that the installation is complete. You should see something like the following:

```
$ kubectl get pods --all-namespaces
NAMESPACE     NAME                                     READY   STATUS      RESTARTS   AGE
kube-system   kata-deploy-575tm                        1/1     Running     0          101m
default       web-classify-kata-fc-5f44fd448f-mtvlv    1/1     Running     0          76m
default       web-classify-kata-fc-5f44fd448f-h7j84    1/1     Running     0          76m
...
...
$ k3s kubectl -n kube-system logs kata-deploy-575tm
...
...
...
Done! containerd-shim-kata-v2 is now configured to run Firecracker with vAccel
warning: containerd-shim-kata-fc-v2 already exists
node/node3.nubificus.com labeled
```
That's it! You are now ready to accelerate your functions on Kubernetes with vAccel.

**Alternatively** use the following daemon which already contains all the vAccel artifacts and required components in the container image. The image is slightly bigger than before (~2GB).

```
$ kubectl kata-deploy-full.yaml
```


Don't forget to create a RuntimeClass in order to run your workloads with vAccel enabled kata runtime

```
$ kubectl apply https://raw.githubusercontent.com/cloudkernels/packaging/vaccel-dev/kata-deploy/k8s-1.14/kata-fc-runtimeClass.yaml
```

### Deploy an image classification function as a Service

The following will deploy a custom HTTP server that routes POST requests to a handler. The handler gets an image from the POST body and calls vAccel to perform image-classification operation using the GPU.

```
$ kubectl web-classify.yaml
NAME                                    READY   STATUS    RESTARTS   AGE
web-classify-kata-fc-5f44fd448f-mtvlv   1/1     Running   0          92m
web-classify-kata-fc-5f44fd448f-h7j84   1/1     Running   0          92m
$ k3s kubectl get svc                  
NAME                   TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
web-classify-kata-fc   ClusterIP   10.43.214.52   <none>        80/TCP    91m

$ wget https://pbs.twimg.com/profile_images/1186928115571941378/1B6zKjc3_400x400.jpg -O - | curl -L -X POST classify.nbfc.io/classify --data-binary @-
```
