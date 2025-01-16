---
date: 2023-04-04 21:03:00-07:00
description: 'Here''s a subtle description to encourage the reader to read the blog
  post:


  "I recently discovered a game-changing way to chain GitHub Actions - and it''s simplifying
  my deployment process in the best way possible.'
tags:
- gh
- render-engine devlog
title: chaining gh actions
---

You can see an example of this in [render-engine-rss](https://github.com/kjaymiller/render-engine-rss/)


## Quick Steps

### Create your first workflow

For my workflow I'm running PyTest.

Ensure that the first workflow has `workflow_call` as a possible trigger.

```yaml
	name: PyTest
	on:
		... # other triggers
		workflow_call:
```

### Create your second workflow and call the first in jobs

My second action is publishing based on Github Tagging (using `setuptools_scm`).

To reference the first action add it as a job and provide the path to the file in the `uses` path.

```yaml
jobs:
	test:
    uses: ./.github/workflows/test.yml
	publish:
		... # rest of workflow
```

### Why I do this

I want to make sure that I don't have to do too much to deploy updates but I don't want to publish if I have failing tests.
