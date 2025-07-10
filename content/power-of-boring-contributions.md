---
date: 2024-09-30 00:49:40.145844
description: Discover how writing tests in your open-source project can lead to new
  skills and exciting career opportunities - even when it feels like 'boring' work.
tags:
- development
title: What I learned from a "Boring" Contribution
---

Someone in the [_BPD Open Source Program_](https://blackpythondevs.com/open-source-program) mentioned that they were "tired" of doing things like documentation and test updates.

I'm petty and still kinda upset with this mentality but my adventures the last few days really helped me rationalize my frustration and bring out some really important learnings.

## Boring is good

**Your project should be boring** most of the time. Professional code is often boring code. I've also learned that code tends to get more _boring_ the more stable if gets. In fact, the most exciting bit of open-source is often discovered when doing the _boring bits_.

### Finding excitement in boring work

Those bits are the things that no one wants to do.

- documentation
- automation
- triage
- testing
- logging

The excitement doesn't really come with _just_ doing the thing (unless you enjoy doing these things and some folks do!). You benefit from gaining familiarity with the project and learning patterns you can use in other projects.

## An example of discovery from boring

Here are is an example I've stumbled into.

I recieved a [PR that thins out the CSS](https://github.com/blackpythondevs/blackpythondevs.github.io/pull/473) of our deployment of [picocss](picocss). I mentioned to the author of the PR that I wanted to generate screenshots of the site so I could verify that the change would not have any visual issues.

![screenshot of comments from PR](https://jmblogstorrage.blob.core.windows.net/media/media/css-pr-review-comments.webp)

This was something that I had been playing with on my personal website since I had learned about using device emulation with Playwright for [my talk at RenderATL](https://www.youtube.com/watch?v=dBJowtn1lQE).

Before I could add this feature, I needed to fix my local environment. I setup [rbenv](rbenv) and finally **got jekyll running on my local machine**. This let me start development on the feature.

This is where I ran into friction. In order to run the playwright tests, I needed to run jekyll and then run the tests.

I remembered I could use `multiprocessor` to spawn a daemon process and then run the tests and shut down the process. I [recently updated Render Engine to test using `ephemeral_port_reserve`](https://github.com/render-engine/render-engine/pull/808/files). This grabs a free port and use so if your webserver is already running you don't get `port already in use` errors.

I learned how to do this when I was at Microsoft when Pamela and I were building cookiecutter templates that generate other cookiecutter templates and working to get near 100% test-coverage (not important but highlighting it was more _boring_ work).

Sadly, back on the website repo, things weren't working. While troubleshooting, I learned about the module [pytest-xprocess](pytest-xprocess) which, after reading the docs, I learned how `xprocess` doesn't use the same source as the project and instead uses a cache directory where the logs and other information are stored.

Then while getting things to work I noticed that there was a lot of duplicate code happening. That's when I decided to quickly refactor things to look similar to what I was doing with my new tests.

Then came the time to submit this PR. That's when I realized a big mistake I had made.

#### Mo' Code, Mo' Problems

My PR did the following things.

- Introduced a new module to run jekyll inside of tests
- Refactored Routes to parametrize tests
- Introduced the `design` marker and a playwright test that generates images and uses gh-actions `actions/upload-artifact` to make them available.

This was a problem because, ideally, [PRs should be small](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/getting-started/best-practices-for-pull-requests#write-small-prs) and solve documented problems. My code was massive and solved issues that were not highlighted before.

To fix this, I needed to split my changes into multiple PRs. Sadly I already had commits and no easy way to split them.

Here is how I solved this problem:

1. create issues for the other things that need to be accomplished
2. create a new branch
3. reset the branch to the commit before making the code that was changed staged
4. refactor the code AGAIN by adding a conftest and splitting the tests into separate files
5. use `git add -p` to add the changes for the first PR.
6. commit the added code and submit the initial pr

Doing this came with learning a lot of commands. Here are a few.

- `git reset <commit hash>`
- `git add -p`
- `git restore --staged <files>`
- `git add -p <files>`
- `git restore --staged <files> -p`
- `git diff --cached`

This wasn't easy and I've definitely asked others to do this thing, not realizing what went into doing it. Now I have hte ability to send this to folks to help them with this process.

## There's so much to learn with boring PRs

Yes this is a _mindset_ post. But I seriously mean it when I say doing boring things the boring way is boring. But when you are eager to learn implement things that you can take with you on your professional career, then you will have an exciting time contributing to open-source.

Writing tests resulted in learning:

- how to setup rbenv and fix my local environment
- parametrizing device profiles
- about the xprocess module and how I can use it to run processes in the background
- how to split a PR into multiple PRs using commands in git that I've never used before

It also resulted in creating a conference talk **IN WHICH I WAS PAID TO GIVE** as well as this post. More importantly, I was able to learn things that I can take to other projects.

There is this cycle that comes from doing things a lot and there are a lot of _boring_ things.

![image of a loop between boring tasks and exciting tasks](https://jmblogstorrage.blob.core.windows.net/media/media/boring-and-exciting-cycle.webp)

I'm not saying every open-source contribution needs to be a learning opportunity but let's not assume that the smallest of PRs don't have HUGE opportunities to learn.
