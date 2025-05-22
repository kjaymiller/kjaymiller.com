---
title: Fixing the double logging issue with a logging.filter
date: 2025-05-22T10:22:46
tags:
  - frontmatter-check
---

I finally fixed a very annoying issue with [frontmatter-check](https://github.com/kjaymiller/frontmatter-check).

## The problem

frontmatter-check currently has two levels:

- `WARN` - generates a warning if a frontmatter key is missing
- `ERROR` - generates an error instead

To break in this we actually have a few logging handlers:

- stdout - Pass Warnings to stdout
- stderr - Pass Errors to stderr
- MemoryHandler - pass Errors to MemoryHandler so that those errors can be used in frontmatter-check itself.

The problem here lived in `stdout`. Logging operates on levels:

- 10 DEBUG
- 20 INFO
- 30 WARNING
- 40 ERROR

Any level higher than the level set will also show. This meant that `ERROR` messages were appearing in both stdout and stderr which is why Errors would show twice.

```sh
❯ pre-commit try-repo ../frontmatter-check
[INFO] Initializing environment for ../frontmatter-check.
===============================================================================
Using config:
===============================================================================
repos:
-   repo: ../frontmatter-check
    rev: 258bcb39385a76ac54610121bf89abb04c9b904e
    hooks:
    -   id: frontmatter-check
===============================================================================
[INFO] Installing environment for ../frontmatter-check.
[INFO] Once installed this environment will be reused.
[INFO] This may take a few minutes...
frontmatter check........................................................Failed
- hook id: frontmatter-check
- exit code: 1

Checking File: content/test-content-fm-check.md
ERROR - Missing field: 'description'
ERROR - Missing field: 'description'
ERROR - Missing field: 'date'
ERROR - Missing field: 'date'
```

## The solution

I added a filter to the `stdout_handler`.

```python
class WarningOnlyFilter(logging.Filter):
    def filter(self, record):
        return record.levelno == logging.WARNING

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.WARNING)
stdout_handler.setFormatter(formatter)
stdout_handler.addFilter(WarningOnlyFilter())
```

This means that ONLY `WARNING` messages will pass through `stdout`.

## Considerations

The only concern I have here is that if you are trying to specifically capture message you have to capture **BOTH** `stdout` and `stderr`.

You can see this change and more in [PR #42](https://github.com/kjaymiller/frontmatter-check/pull/42).
