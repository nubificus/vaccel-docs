# Configuration

vAccel can be configured at runtime using environment variables.

## Overview

<!-- markdownlint-disable line-length -->

| Variable Name              | Description                                   | Expected Values                                | Default |
| -------------------------- | --------------------------------------------- | ---------------------------------------------- | ------- |
| `VACCEL_PLUGINS`           | Path(s) or filename(s) of backend plugin(s)   | Absolute path, filename, or `:`-separated list |         |
| `VACCEL_LOG_LEVEL`         | Controls log verbosity                        | `1`, `2`, `3`, `4`                             | `1`     |
| `VACCEL_LOG_FILE`          | Filename of a log file                        | Filename (without extension)                   |         |
| `VACCEL_PROFILING_ENABLED` | Enables or disables profiling                 | `1`, `0`                                       | `0`     |
| `VACCEL_VERSION_IGNORE`    | If set, ignores plugin/lib version mismatches | `1`, `0`                                       | `0`     |
| `VACCEL_BOOTSTRAP_ENABLED` | Enables or disables lib auto-bootstrap        | `1`, `0`                                       | `1`     |
| `VACCEL_CLEANUP_ENABLED`   | Enables or disables lib auto-cleanup          | `1`, `0`                                       | `1`     |

<!-- markdownlint-restore -->

## Description

### `VACCEL_PLUGINS`

Specifies one or more plugins to be used as backends.

**Expected values:**

- An _absolute path_ (e.g., `/usr/local/lib/libvaccel-noop.so`)
- A _filename_ that can be found in standard library locations (e.g.,
  `libvaccel-noop.so`)
- A _colon-separated (`:`) list_ of absolute paths or filenames

### `VACCEL_LOG_LEVEL`

Sets the verbosity of logging output.

**Expected values:**

- `1` – Critical errors or errors that require attention
- `2` – Warnings that indicate potential issues
- `3` – General application events
- `4` – Detailed debug logs for development and troubleshooting

**Default:** `1`

### `VACCEL_LOG_FILE`

Specifies the filename (without the extension) of the log file where application
logs will be written.

The file is created in the current directory and the date and extension are
automatically appended to the filename with the format `-<YYYY>-<MM>-<DD>.log`.
If no path is provided, logs are written to _standard output_ (`stdout`)

**Expected values:**

- A _filename_ for the log file (e.g., `mylog`)

### `VACCEL_PROFILING_ENABLED`

Controls whether profiling is enabled or disabled.

**Expected values:**

- `1` – Enables profiling
- `0` – Disables profiling

**Default:** `0`

### `VACCEL_VERSION_IGNORE`

Controls whether to ignore a mismatch between the plugin vAccel version and the
core vAccel library version.

**Expected values:**

- `1` – Ignore version mismatch
- `0` – Do not ignore version mismatch

**Default:** `0`

### `VACCEL_BOOTSTRAP_ENABLED`

Controls whether to bootstrap the vAccel components upon loading the library.
Useful when setting `vaccel_config` programmatically, so the library can be
configured before bootstrapping the components.

**Expected values:**

- `1` – Bootstrap components on library load
- `0` – Do not bootstrap components on library load

**Default:** `1`

### `VACCEL_CLEANUP_ENABLED`

Controls whether to automatically cleanup the allocated objects upon unloading
the vAccel library.

**Expected values:**

- `1` – Cleanup components on library unload
- `0` – Do not cleanup components on library unload

**Default:** `1`
