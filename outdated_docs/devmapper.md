## Configure contained CRI plugin with devicemapper

Follow the [documentation](https://pkg.go.dev/github.com/containerd/containerd/snapshots/devmapper) to configure containerd with devicemapper.

Don't forget to configure devicemapper as the default CRI snapshotter; make sure that the following lines exist in your containerd config.toml:

```
[plugins.cri.containerd]
  snapshotter = "devmapper"
```

### k3s

k3s ships with a minimal version of containerd where the devicemapper plugin is not included. Additionally to the above, you also need to either configure k3s to use a different containerd binary or built k3s-containerd from [source](https://github.com/k3s-io/k3s), patch it and eject it to `/var/lib/rancher/k3s/data/current/bin`.

```diff
diff --git a/pkg/containerd/builtins_linux.go b/pkg/containerd/builtins_linux.go
index 2b28979b15..7b9afcd2a8 100644
--- a/pkg/containerd/builtins_linux.go
+++ b/pkg/containerd/builtins_linux.go
@@ -25,4 +25,5 @@ import (
        _ "github.com/containerd/containerd/runtime/v2/runc/options"
        _ "github.com/containerd/containerd/snapshots/native"
        _ "github.com/containerd/containerd/snapshots/overlay"
+       _ "github.com/containerd/containerd/snapshots/devmapper"
 )
diff --git a/vendor/modules.txt b/vendor/modules.txt
index 3ac906547a..84b4691e12 100644
--- a/vendor/modules.txt
+++ b/vendor/modules.txt
@@ -301,6 +301,8 @@ github.com/containerd/containerd/services/snapshots
 github.com/containerd/containerd/services/tasks
 github.com/containerd/containerd/services/version
 github.com/containerd/containerd/snapshots
+github.com/containerd/containerd/snapshots/devmapper
+github.com/containerd/containerd/snapshots/devmapper/dmsetup
 github.com/containerd/containerd/snapshots/native
 github.com/containerd/containerd/snapshots/overlay
 github.com/containerd/containerd/snapshots/proxy
```

*The devicemapper pool should be placed to k3s path* (e.g `DATA_DIR=/var/lib/rancher/k3s/agent/containerd/io.containerd.snapshotter.v1.devmapper`)

#### Restart k8s/k3s services on each node affected

If you are already running k8s/k3s with a different containerd snapshotter, after configuring devmapper and restarting containerd, you probably need to restart kubelet/k3s services and make sure that all the containers running in `k8s.io` containerd namespace are now running using devicemapper.
