# vAccel documentation

This repository contains the assets required to build the
[vAccel documentation website](https://docs.vaccel.org).

The site is built with [MkDocs](https://www.mkdocs.org/) using the
[Material](https://squidfunk.github.io/mkdocs-material/) theme and versioned
with [mike](https://github.com/jimporter/mike). API reference pages for the
Python bindings are generated from the [`vaccel-python`][vaccel-python]
submodule via [mkdocstrings](https://mkdocstrings.github.io/).

[vaccel-python]: https://github.com/nubificus/vaccel-python

## Repository layout

- `docs/`: Markdown sources for the documentation site.
- `overrides/`: Theme overrides and template partials.
- `hooks/`: MkDocs hooks (custom copyright, Python reference generation).
- `macros/`: Jinja macros exposed to Markdown via `mkdocs-macros-plugin`.
- `variables/`: YAML data consumed by the macros (e.g. pinned versions).
- `external_repos/`: Git submodules for sources pulled into the build.
- `mkdocs.yml`: Site configuration.
- `requirements.txt`: Python build dependencies.
- `package.json`: Node dependencies for Markdown linting and formatting.

## Prerequisites

- Python 3.10+
- Node.js 18+ (only required for linting and formatting)

## Setup

Clone the repository and initialize the submodules:

```shell
git clone https://github.com/nubificus/vaccel-docs.git
cd vaccel-docs
git submodule update --init --recursive
```

Create a virtual environment and install the Python dependencies:

```shell
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Optionally install the Node dependencies for Markdown linting and formatting:

```shell
npm install --save-dev -g markdownlint-cli prettier
```

## Build and serve locally

To serve the site with live reload at `http://127.0.0.1:8000`:

```shell
mkdocs serve
```

To build the static site into `site/`:

```shell
mkdocs build
```

## Linting and formatting

Markdown files are linted with
[`markdownlint-cli`](https://github.com/igorshubovych/markdownlint-cli) and
formatted with [`prettier`](https://prettier.io/):

```shell
npx markdownlint '**/*.md'
npx prettier --check '**/*.md'
```

Run `npx prettier --write '**/*.md'` to apply formatting in place. Prettier
options are configured in `.prettierrc.yml` and exclusions in `.prettierignore`.

Python code is linted with [`ruff`](https://github.com/astral-sh/ruff):

```shell
ruff check .
```

## Deployment

The site is deployed automatically via GitHub Actions on pushes to `main` and on
release tags. Versioned deployments are managed with `mike`, and the live site
is hosted at <https://docs.vaccel.org>.

## License

This work is licensed under
[CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). See
[`LICENSE`](LICENSE) for the full text.
