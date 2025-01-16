---
date: 2023-09-13 01:29:26+00:00
description: 'Here''s a subtle description to encourage the reader to read the blog
  post:


  "Want to know how I used GitHub Actions to create an accessible website testing
  workflow? From running tests on a local server to generating summary reports and
  comparing accessibility audits, discover my step-by-step approach.'
image: https://jmblogstorrage.blob.core.windows.net/media/gh-action-a11y-build-and-deploy-job.png
title: Website Accessibility Audit Reports via GH Actions
---

I promise this isn't a stalling tactic. I will be working on the accessibility violations. I wanted to create a way to easily see the report.

This is where GH Actions comes in. Currently I have a few issues that GH Actions can temporarily solve.

- Tests have to be on a live server and not the HTML
- Test Results need to be veiwable and optionally downloadable

## Testing the new site <strike>after</strike> BEFORE publishing

One of the original issues I ran into was how to actually load the site to test it. My early tests for this were just testing against my live-url. That said it's kinda sucky to test something after you've deployed it.

Luckily I had recent solved this issue at work while writing tests for a flask application. In the [cookiecutter-relecloud](https://github.com/kjaymiller/cookiecutter-relecloud) project. We used the [multiprocess'](https://docs.python.org/3/library/multiprocessing.html) `Process` method to create a background process that loads the serve. Then we run our tests and then kill the background daemon.

```python
def run_server():
    class server(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory="output", **kwargs)

    httpd = http.server.HTTPServer(('localhost', 8000), server)
    httpd.serve_forever()


def main(url: str = "http://localhost", output: str = "test-results.md") -> None:
    """Run Axe on a URL and save the results to a file."""
    render_engine.build(site_module="routes:app")
    proc = Process(target=run_server, daemon=True)
    proc.start()
    ... # code for running tests
    proc.kill()
```

For those familiar with render-engine that runserver process is very similar to the `render_engine.cli.serve` module. In fact it's practically identical but I couldn't get it to work as I think you have to supply the function and not call it. I believe this is possible but it would require a change to the render-engine codebase.

## The GitHub action to test

The GitHub action is relatively simple as we're doing the same process that we normally do with many Python-based workflows
1. Install the dependencies
2. Run the workflow
3. _Generate a Summary and Artifact the File??_

Okay the last thing is pretty new but it's a cool feature that I would like to use more often.

You can [output results](https://github.blog/2022-05-09-supercharging-github-actions-with-job-summaries/) to your GH Action using the `GITHUB_STEP_SUMMARY` value.

I `cat` the output of our accessibilty report to the value.

```yaml
    run: |
          python a11y.py --output "accessibility-report-${{steps.date.outputs.DATE}}-${{github.run_id}}.txt"
          cat "accessibility-report-${{steps.date.outputs.DATE}}-${{github.run_id}}.txt" >> $GITHUB_STEP_SUMMARY
```

![snippet of action step summary](https://jmblogstorrage.blob.core.windows.net/media/action-step-summary.png)

But what if I want to compare two reports? This is where using the [upload-artifact action](https://github.com/actions/upload-artifact) comes into play.  Upload Artifact allows us to take the report file and make it available as a download.

![Accessibility Artifact in GitHub actions](https://jmblogstorrage.blob.core.windows.net/media/accessibility-audit-gh-actions.png)

## Deploy after testing

I did all that work to make it so that I can test the site prior to loading the website; how do we make it a pre-requisite.

We can use Github Actions `needs` parameter and we call the action as a job in our deploys action.

```yml
jobs:
  runs_a11y:
    uses: ./.github/workflows/a11y-test.yml
  build_and_deploy_job:
    needs: runs_a11y
...
```

![deploy post relying on a11y.yml](https://jmblogstorrage.blob.core.windows.net/media/gh-action-a11y-build-and-deploy-job.png)

## What's left

Now the goal is improvement. That being said it's very unlikely that a site that is built by a theme will add lots of breaking accessibility changes.

But that is what testing is for (catching the unexpected). My hope is I can set a value based on the `violations_count` parameter.  That said a I do have an issue with how violations are counted.

Even though in [the last post on this](https://kjaymiller.com/blog/using-python-to-fix-my-accessibility-nightmare-of-a-website.html#how-bad-is-it) the report claims 3 violations, there were several errors for each violation. This means that while I can catch errors, I can't check against a total count of issues.

I'd like to figure out the best way to do this. I have some ideas with the generated report, which is in JSON.

But I'm excited to learn more about how how to ensure that my site is as accessible as possible.
