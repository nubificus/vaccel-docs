# Deploying vAccel applications using Kubernetes

This guide describes how to deploy a **vAccel**-enabled application, alongside
the **vAccel Agent** with the Torch plugin using Kubernetes. It includes:

- Full explanation of the deployment architecture
- Sidecar-based co-location of client and agent
- Split deployment with remote agent access
- Dockerfiles for both client and agent
- Simple block diagram for visual reference

## Architecture Overview

The deployment includes:

- The **vAccel Agent** (running `vaccel-rpc-agent`) exposing a Unix socket or
  TCP endpoint.
- The **vAccel**-enabled Application, packaged with the RPC plugin, which
  connects to the agent.
- A sidecar option to colocate both agent and client in one pod for
  latency-sensitive workloads.
- A split deployment option where the agent runs as a standalone DaemonSet.

## Deployment Graph

```mermaid
flowchart TD
  subgraph Node1["K8s Node"]
    subgraph PodA["Sidecar Pod"]
      A1[vAccel Client]
      A2[vAccel RPC Agent]
    end
  end

  subgraph Node2["K8s Node"]
    subgraph PodB["Client Only Pod"]
      B1[vAccel Client]
    end
    subgraph PodC["Agent Pod"]
      C1[vAccel RPC Agent]
    end
  end

  B1 -->|RPC over vsock/tcp| C1
  A1 -->|Unix socket| A2
```

We have gathered all necessary files in a
[Github repository](https://github.com/nubificus/vaccel-torch-bert-k8s-example).
Its file structure is as follows:

```console
├── docker
│   ├── Dockerfile
│   └── Dockerfile.agent
├── manifests
│   ├── client.yaml
│   ├── daemonset-agent.yaml
│   └── sidecar.yaml
└── README.md
```

In the `docker` folder we include two `Dockerfiles`, one for the client
application and one for the vaccel agent. Feel free to build on the client
`Dockerfile` to create your own. To showcase our example we have already
included our application binary in an example container image:
`harbor.nbfc.io/nubificus/vaccel-torch-bert-example:x86_64`.

The `manifests` folder contains YAML files to deploy this example in both modes
of operation.

### vAccel Agent as a **sidecar** container

The agent runs alongside the client application, in a single pod
(`sidecar.yaml`). Since this mode implicitly assumes that both containers share
the same mount namespaces, we can use the `UNIX` socket RPC transport. See the
following snippet from the YAML file:

```YAML
    containers:
        - name: vaccel-agent
          volumeMounts:
              - name: vaccel-sock
                mountPath: /var/run/vaccel
...
        - name: vaccel-client
...
          volumeMounts:
              - name: vaccel-sock
                mountPath: /var/run/vaccel
...
    volumes:
        - name: vaccel-sock
          emptyDir: {}
```

> Note: The `ENTRYPOINT` of the Agent's Dockerfile is the following:

```Dockerfile
ENTRYPOINT ["vaccel-rpc-agent", "-a", "unix:///var/run/vaccel/vaccel.sock"]
```

> and the env var that points to the vAccel endpoint in the Client's Dockerfile
> is:

```Dockerfile
ENV VACCEL_RPC_ADDRESS="unix:///var/run/vaccel/vaccel.sock"
```

Logs from an example deployment are shown below.

Agent logs, before the client start:

```console
$ kubectl logs vaccel-sidecar-pod -c vaccel-agent
[2026-04-30T14:52:39Z INFO  ttrpc::sync::server] server listen started
[2026-04-30T14:52:39Z INFO  ttrpc::sync::server] server started
[2026-04-30T14:52:39Z INFO  vaccel_rpc_agent] vAccel RPC agent started
[2026-04-30T14:52:39Z INFO  vaccel_rpc_agent] Listening on 'unix:///var/run/vaccel/vaccel.sock', press Ctrl+C to exit
```

Client logs:

```console
$ kubectl logs vaccel-sidecar-pod -c vaccel-client
2026.04.30-14:57:33.00 - <info> vAccel 0.7.1-25-8aea5ec0
2026.04.30-14:57:33.00 - <info> Registered plugin rpc 0.2.1-7-925667dc
Processing 26954 lines from: /data/tweets.txt
== [Vocab Loaded] ==
2026.04.30-14:57:33.03 - <warn> Path does not seem to have a `<prefix>://`
2026.04.30-14:57:33.03 - <warn> Assuming cnn_trace.pt is a local path
vaccel_resource_new(): Time Taken: 49075 nanoseconds
Created new model resource 1
Initialized vAccel session 1
Line 1: Duration: 101.775 ms Prediction: neither
Line 2: Duration: 126.993 ms Prediction: offensive-language
Line 3: Duration: 204.097 ms Prediction: offensive-language
Line 4: Duration: 63.1958 ms Prediction: offensive-language
...
```

Agent logs, after client initial connection:

```console
$ kubectl logs vaccel-sidecar-pod -c vaccel-agent
[2026-04-30T14:52:39Z INFO  ttrpc::sync::server] server listen started
[2026-04-30T14:52:39Z INFO  ttrpc::sync::server] server started
[2026-04-30T14:52:39Z INFO  vaccel_rpc_agent] vAccel RPC agent started
[2026-04-30T14:52:39Z INFO  vaccel_rpc_agent] Listening on 'unix:///var/run/vaccel/vaccel.sock', press Ctrl+C to exit
[2026-04-30T14:57:33Z INFO  vaccel_rpc_agent::session] Created session 1
[2026-04-30T14:57:34Z INFO  vaccel_rpc_agent::resource] Creating new resource
[2026-04-30T14:57:34Z INFO  vaccel_rpc_agent::resource] Registering resource 1 with session 1
[2026-04-30T14:57:34Z INFO  vaccel_rpc_agent::ops::torch] session:1 PyTorch load model
[2026-04-30T14:57:36Z INFO  vaccel_rpc_agent::ops::torch] session:1 PyTorch model run
[2026-04-30T14:57:36Z INFO  vaccel_rpc_agent::ops::torch] session:1 PyTorch model run
...
```

### vAccel Agent as a **daemonset**

The Agent runs as a daemonset providing a service to the k8s cluster, available
via a hostname and port. This mode offers a lot more flexibility, as it allows
multiple agent deployments, on heterogeneous nodes, with diverse hardware
characteristics. In our example we use a single `x86_64` node, but more complex
scenarios can be supported, with multiple GPUs/FPGAs or custom acceleration
nodes. In this mode of operation we have two YAML files:

(a) one for the agent daemonset (`daemoneset-agent.yaml`) that includes the
service:

```YAML
apiVersion: apps/v1
kind: DaemonSet
metadata:
    name: vaccel-agent
spec:
    selector:
        matchLabels:
            app: vaccel-agent
    template:
        metadata:
            labels:
                app: vaccel-agent
        spec:
            containers:
                - name: vaccel-agent
                  image: harbor.nbfc.io/nubificus/vaccel-torch-bert-example-agent:x86_64
                  command: ["vaccel-rpc-agent"]
                  args: ["-a", "tcp://0.0.0.0:8888"]
                  ports:
                      - containerPort: 8888
                        name: rpc
```

and the service:

```YAML
apiVersion: v1
kind: Service
metadata:
  name: vaccel-agent
  labels:
    app: vaccel-agent
spec:
  ports:
  - name: vaccel-agent
    port: 8888
    protocol: TCP
    targetPort: 8888
  selector:
    app: vaccel-agent
  sessionAffinity: None
```

(b) one for the client application (`client.yaml`) that points to the respective
vAccel agent service:

```YAML
apiVersion: v1
kind: Pod
metadata:
    name: vaccel-client
spec:
    containers:
        - name: vaccel-client
          image: harbor.nbfc.io/nubificus/vaccel-torch-bert-example:x86_64
          command: ["./build/classifier"]
          args: ["-m", "cnn_trace.pt", "-v", "bert_cased_vocab.txt", "-f", "/data/tweets.txt"]
          env:
              - name: VACCEL_RPC_ADDRESS
                value: "tcp://vaccel-agent:8888"
          volumeMounts:
              - name: tweets
                mountPath: /data
    volumes:
        - name: tweets
          hostPath:
            path: /tmp/data
```

Deployment logs are shown below.

Agent & service instantiation:

```console
$ kubectl apply -f daemonset-agent.yaml
daemonset.apps/vaccel-agent created
service/vaccel-agent created
$ kubectl get pods -o wide
NAME                             READY   STATUS         RESTARTS       AGE    IP              NODE         NOMINATED NODE   READINESS GATES
vaccel-agent-cgjmr               1/1     Running        0              15s    10.42.0.10      vaccel-k8s   <none>           <none>
$ kubectl logs vaccel-agent-cgjmr
[2026-04-30T15:01:10Z INFO  ttrpc::sync::server] server listen started
[2026-04-30T15:01:10Z INFO  ttrpc::sync::server] server started
[2026-04-30T15:01:10Z INFO  vaccel_rpc_agent] vAccel RPC agent started
[2026-04-30T15:01:10Z INFO  vaccel_rpc_agent] Listening on 'tcp://0.0.0.0:8888', press Ctrl+C to exit
```

```console
$ kubectl get svc -o wide
NAME               TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE     SELECTOR
vaccel-agent       ClusterIP   10.43.148.202   <none>        8888/TCP   2m13s   app=vaccel-agent
```

Client spawn:

```console
$ kubectl apply -f client.yaml
pod/vaccel-client created
$ kubectl get pods -o wide
NAME                             READY   STATUS             RESTARTS       AGE     IP              NODE         NOMINATED NODE   READINESS GATES
vaccel-agent-cgjmr               1/1     Running            0              3m35s   10.42.0.10      vaccel-k8s   <none>           <none>
vaccel-client                    1/1     Running            0              82s     10.42.0.11      vaccel-k8s   <none>           <none>
$ kubectl logs vaccel-client
2026.04.30-15:01:43.45 - <info> vAccel 0.7.1-25-8aea5ec0
2026.04.30-15:01:43.45 - <info> Registered plugin rpc 0.2.1-7-925667dc
Processing 26954 lines from: /data/tweets.txt
== [Vocab Loaded] ==
2026.04.30-15:01:43.48 - <warn> Path does not seem to have a `<prefix>://`
2026.04.30-15:01:43.48 - <warn> Assuming cnn_trace.pt is a local path
vaccel_resource_new(): Time Taken: 46303 nanoseconds
Created new model resource 1
Initialized vAccel session 1
Line 1: Duration: 98.7296 ms Prediction: neither
Line 2: Duration: 186.415 ms Prediction: offensive-language
Line 3: Duration: 236.044 ms Prediction: offensive-language
Line 4: Duration: 87.602 ms Prediction: offensive-language
Line 5: Duration: 111.111 ms Prediction: neither
...
```

## Next Steps

- Customize your Torch model or plugin inside the client image
- Test workloads in the sidecar first for simplified debugging
- Scale via Deployment/Job or integrate with KNative
