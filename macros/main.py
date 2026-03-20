# SPDX-License-Identifier: Apache-2.0

def define_env(env):
    # Returns base version, stripping semver metadata
    env.filters["base_version"] = lambda v: v.split("+")[0]
    # Replaces '+' with '-' so semver build metadata is valid in Docker tags
    env.filters["docker_tag"] = lambda v: v.replace("+", "-")
