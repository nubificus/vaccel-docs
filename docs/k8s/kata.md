# vAccel on k8s using Kata-containers & Firecracker

## Prerequisites

In order to run vAccel on Kata containers with Firecracker you need to meet the following prerequisites on each k8s node that will be used for acceleration:

- containerd as container manager
- devicemapper as CRI plugin default snapshotter ([info](../devmapper.md))
- nvidia GPU which supports CUDA (*for now*) ([info](../useful-docs/jetson.md))
- [jetson-inference](https://github.com/dusty-nv/jetson-inference) libraries (libjetson-inference.so must be installed and properly linked with CUDA libraries) ([info](../useful-docs/jetson.md))


## Quick start

### Deploy vAccel with Kata
<sup>*We rely on* [kata-containers/kata-deploy](https://github.com/kata-containers/packaging/tree/master/kata-deploy) *to create the vaccel-kata-deploy daemon. Our fork repo can be found on* [cloudkernels/packaging](https://github.com/cloudkernels/packaging/tree/vaccel-dev).*We are working on building a Kata Containers release with vAccel support.*</sup>

Label each node where vAccel-kata should be deployed:

```
$ kubectl label nodes <your-node-name> vaccel=true
```

Create service account and cluster role for the kata-deploy daemon
```
$ kubectl apply -f https://raw.githubusercontent.com/cloudkernels/packaging/vaccel-dev/kata-deploy/kata-rbac/base/kata-rbac.yaml
```

Install vAccel-kata on each "vaccel=true" node:
```
$ kubectl apply -f https://raw.githubusercontent.com/cloudkernels/packaging/vaccel-dev/kata-deploy/kata-deploy/base/kata-deploy.yaml

# or for k3s

$ k3s kubectl apply -k github.com/cloudkernels/packaging/kata-deploy/kata-deploy/overlays/k3s?ref=vaccel-dev
```

The kata-deploy daemon calls the vAccel download script. It may take a few minutes to download the ML Inference models.

```
$ kubectl get pods --all-namespaces
NAMESPACE     NAME                                     READY   STATUS      RESTARTS   AGE
kube-system   kata-deploy-575tm                        1/1     Running     0          101m
...
...
```
Check the pod logs to be sure that the installation is complete. You should see something like the following:
```
$ kubectl -n kube-system logs kata-deploy-575tm
...
...
Done! containerd-shim-kata-v2 is now configured to run Firecracker with vAccel
node/node3.nubificus.com labeled
```
**That's it! You are now ready to accelerate your functions on Kubernetes with vAccel.**

*Alternatively* use the following daemon which already contains all the vAccel artifacts and required components in the container image. The image is slightly bigger than before as it already contains jetson inference models.

```
$ kubectl apply -k github.com/cloudkernels/packaging/kata-deploy/kata-deploy/overlays/full?ref=vaccel-dev

# or for k3s

$ k3s kubectl apply -k github.com/cloudkernels/packaging/kata-deploy/kata-deploy/overlays/full-k3s?ref=vaccel-dev
```

Don't forget to create a RuntimeClass in order to run your workloads with vAccel enabled kata runtime

```
$ kubectl apply -f https://raw.githubusercontent.com/cloudkernels/packaging/vaccel-dev/kata-deploy/k8s-1.14/kata-fc-runtimeClass.yaml
```

### Deploy an image classification function as a Service

The following will deploy a custom HTTP server that routes POST requests to a handler. The handler gets an image from the POST body and calls vAccel to perform image-classification operation using the GPU.

```
$ kubectl create -f https://raw.githubusercontent.com/cloudkernels/packaging/vaccel-dev/kata-deploy/examples/web-classify.yaml
```
```
$ kubectl get pods
NAME                                    READY   STATUS    RESTARTS   AGE
web-classify-kata-fc-5f44fd448f-mtvlv   1/1     Running   0          92m
web-classify-kata-fc-5f44fd448f-h7j84   1/1     Running   0          92m

$ kubectl get svc                  
NAME                   TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)   AGE
web-classify-kata-fc   ClusterIP   10.43.214.52   <none>        80/TCP    91m
```

Run a `curl` command (from a cluster node) like the following to send your POST request to the Service web-classify-kata-fc (to access the Service from outside the cluster use nodePort or deploy an ingress route)

```
$ wget https://pbs.twimg.com/profile_images/1186928115571941378/1B6zKjc3_400x400.jpg -O - | curl -L -X POST 10.43.214.52:80/classify --data-binary @-
```

And see the result of the image classification!
```
--2021-02-05 20:17:15--  https://pbs.twimg.com/profile_images/1186928115571941378/1B6zKjc3_400x400.jpg
Resolving pbs.twimg.com (pbs.twimg.com)... 2606:2800:134:fa2:1627:1fe:edb:1665, 192.229.233.50
Connecting to pbs.twimg.com (pbs.twimg.com)|2606:2800:134:fa2:1627:1fe:edb:1665|:443... connected.
HTTP request sent, awaiting response... 200 OK
Length: 12605 (12K) [image/jpeg]
Saving to: 'STDOUT'

-                             100%[================================================>]  12.31K  --.-KB/s    in 0.04s   

2021-02-05 20:17:15 (296 KB/s) - written to stdout [12605/12605]

["web-classify-kata-fc-567bddccc4-s79b5"]: "29.761% wall clock"
```

<p align="center">
  <img width="300" height="300" src="https://pbs.twimg.com/profile_images/1186928115571941378/1B6zKjc3_400x400.jpg">
</p>

### Cleanup everything

Delete the web-classify-fc deployment and service:

```
$ kubectl delete -f https://raw.githubusercontent.com/cloudkernels/packaging/vaccel-dev/kata-deploy/examples/web-classify.yaml
```

Delete the daemon:
(removes artifacts from host paths /opt/vaccel & /opt/kata and restores containerd configuration)

```
$ kubectl delete -f https://raw.githubusercontent.com/cloudkernels/packaging/vaccel-dev/kata-deploy/kata-deploy/base/kata-deploy.yaml

# or for k3s

$ k3s kubectl delete -k github.com/cloudkernels/packaging/kata-deploy/kata-deploy/overlays/k3s?ref=vaccel-dev
```

or in case you deployed the full vAccel overlay:

```
$ kubectl delete -k github.com/cloudkernels/packaging/kata-deploy/kata-deploy/overlays/full?ref=vaccel-dev

# or for k3s

$ k3s kubectl delete -k github.com/cloudkernels/packaging/kata-deploy/kata-deploy/overlays/full-k3s?ref=vaccel-dev
``` 

Reset the runtime and remove kata related labels from nodes:
```
$ kubectl apply -f https://raw.githubusercontent.com/cloudkernels/packaging/vaccel-dev/kata-deploy/kata-cleanup/base/kata-cleanup.yaml

# or for k3s

$ k3s kubectl apply -k github.com/cloudkernels/packaging/kata-deploy/kata-cleanup/overlays/k3s?ref=vaccel-dev
``` 


Delete the kata-fc RuntimeClass and the rbac

```
$ kubectl delete -f https://raw.githubusercontent.com/cloudkernels/packaging/vaccel-dev/kata-deploy/k8s-1.14/kata-fc-runtimeClass.yaml
```

```
$ kubectl delete -f https://raw.githubusercontent.com/cloudkernels/packaging/vaccel-dev/kata-deploy/kata-rbac/base/kata-rbac.yaml
```

Delete the cleanup daemon

```
$ kubectl delete -f https://raw.githubusercontent.com/cloudkernels/packaging/vaccel-dev/kata-deploy/kata-cleanup/base/kata-cleanup.yaml

# or for k3s

$ k3s kubectl delete -k github.com/cloudkernels/packaging/kata-deploy/kata-cleanup/overlays/k3s?ref=vaccel-dev
``` 

Remove `vaccel=true` from each node

```
$ kubectl label nodes <your-node-name> vaccel=true-
```

