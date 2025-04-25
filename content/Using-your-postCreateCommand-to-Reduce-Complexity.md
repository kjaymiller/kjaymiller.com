---
date: 2023-03-02 05:03:00
description: I recently discovered how my `postCreateCommand` can simplify GitHub
  Actions and reduce complexity in our development systems - read on to learn how.
tags:
- github
title: Using your `postCreateCommand`to Reduce Complexity
---

In prep for my talk at [SCALE](https://socallinuxexpo.org), I've been playing with making my development systems moare streamlined using [Dev Containers](https://containers.dev).

Something that I recently did was use the `PostStartCommand` for my GH Action.

My original thought was to just use the dev container as my environment. Currently that doesn't seem possible.

That said, I can use the same file that I have for my dev container to prep my GH Actions.

Here is a cleaner version of my [devcontainer.json](https://github.com/kjaymiller/render_engine/blob/main/.devcontainer/devcontainer.json)

```json
{
	"name": "Python",
	"build": {
		"dockerfile": "Dockerfile",
		"context": "..",
		"args": {"IMAGE": "python:3.11"}
	},
	"postCreateCommand": "bash .devcontainer/setup.sh",
	"customizations": {
		"vscode": {"extensions": ["microsoft.python"]}
	}
```

that `postCreateCommand` can be used in a GitHub Action. For my [PyTest Action](https://github.com/kjaymiller/render_engine/blob/main/.github/workflows/test.yml)

```yaml
name: PyTest
...
jobs:
  test-with-pytest:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - name: Install requirements
        run: |
          bash .devcontainer/setup.sh
      - name: Run tests
        run: python -m pytest
```

I could see a benefit of using everything in a container but at the moment it's easier to maintain each one separately.
