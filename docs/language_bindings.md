# Frameworks and Language bindings

To facilitate the use of vAccel, we provide bindings for popular languages,
apart from `C`. Essentially, the vAccel `C` API can be called from any language
that interacts with `C` libraries. Building on this, we provide support for
[Python](python_bindings.md) and Rust, while we are working on extending
support for various other high- or low-level languages.

Additionally, we have implemented a subset of
[Tensorflow](tensorflow_bindings.md) and PyTorch APIs in a way that the user
can execute an application written for those frameworks over vAccel with
minimal and/or no changes.
