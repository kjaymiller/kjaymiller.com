<!-- v2.3.71 available, run SearchLink on the word 'update' to install. --><!-- v2.3.71 available, run SearchLink on the word 'update' to install. -->---

## title:

My Friend [Jeff Tripplet](https://@webology@mastodon.social) hosts these python calls on Fridays and he's been asking about how things are tested and if we were team [tox][4700-0001] or team [nox][4700-0002]. A lot of folks mentioned using nox, so I thought I would give it a try.

### Why nox

Nox (as the website says) "is a command-line tool that automates testing in multiple Python environments". This is great for making sure that your code works on several versions of Python.

Nox is special because you configure it with Python.

### Why wasn't I testing multiple versions before

That's the thing, I WAS. I was using a [GitHub Matrix][4700-0003] to test.

The problem with this is that I have to push my changes to GitHub to test all the versions.

With Nox, I can test this prior to pushing to GitHub.

### Nox does more than testing

The thing that caught my eye mostly in [the tutorial](https://nox.thea.codes/en/stable/tutorial.html)

[4700-0001]: https://tox.chat/
[4700-0002]: https://nox.thea.codes/en/stable/index.html
[4700-0003]: https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/running-variations-of-jobs-in-a-workflow


<!-- Report:
(14:39:26): [GitHub Matrix]() => https://docs.github.com/en/actions/writing-workflows/choosing-what-your-workflow-does/running-variations-of-jobs-in-a-workflow
(0:39:62): Processed: 3 links, 0 errors.
-->
