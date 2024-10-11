---
date: 2024-08-26 14:43:00-04:00
description: Discover why I rejected a 'good first issue' despite having created it
  - and what I learned from the experience.
slug: good-first-issues-are-hard
title: Good First Issues Aren't Always Good (But can be issues)
---

I'm a big fan of giving people easy tasks to entice them into contributing. In fact, many of my most regular contributors to projects that I work on have been from issues labeled `good first issue`.

Most of these issues are ones that I bump into while working on another issue and thing "I could fix this really quick...". That said, sometimes I think the problem is quick but turns out it's more complicated than it seems.

Take, for instance [issue 391 on the Black Python Devs Website][gh issue]. This issue was to mark our Open Source Program as closed. Simple task right. Currently says open, should say closed. Why then did I reject the issue that did exactly that.

> NOTE:
> I was the one that created this issue so in many ways I have only myself to blame.

## Bad title and body will lead to bad PRs

My first problem was that my title and description was incredibly weak.

> **Title**: Mark the open-source-program-page as closed
> **Body**: Currently the open source page says that applications are still open. This was closed.

![gif of Khaby Lame annoyed](https://media1.tenor.com/m/FRU2yGmIf1YAAAAd/seriously.gif)

If I'm being honest this was a description for me.

After rejecting a pr changed the word `open` to `closed` in the header I decided if someone else was going to work on it, then I should give them more guidance.

[Here is what I suggested][gh issue], after thinking about it for more that 5 seconds suggested.

> Just changing the header will not suffice on this.
> The program will open and close throughout the year. I would definitely consider making things a little more dynamic.
>
> Example:
> We can set projects in `_data/data.yml` that can be updated.
>
> Some values can be:
>
> - list of projects being worked on
> - status if program is open or closed
>   I would then create three templates.
>   A base template that will check it the program in `site.data.open_source_program.open == true/false
>
> if true (open):
> include open_source_program_open.html
> else:
> include open_source_program_closed.html

## That doesn't look like a good first issue

I mean if you're familiar with [Jekyll][3391-0001] or [Jinja2][Jinja2]. You could probably do this and figure it out, but if you were hoping to get that quick win of a good first issue. I don't think that's going to do it.

![GIF of Spongebob saying they made their point](https://media1.tenor.com/m/nSZU74yBJdMAAAAd/spongebob-there-i-think-i-made-my-point.gif)

This is all to say that quality good first issues are hard. We are really trying to make more and more good first issues that we can have some things for the folks in the [Black Python Devs Open Source Program](https://blackpythondevs.com/open-source-program) to work on. The reality is that, while you can make a lot of issues, if you aren't trying to actually create a valuable pipeline for new contributors, you likely won't get the results you're expecting.

Two things I would like to do:

- Have a recommendation that you can give that will help folks onboard into your system. This can be as simple as rewarding folks with contribution credit for triaging and verifying issues.

- Write issues for documentation updates where folks can learn about the software while fixing the documentation.

Lastly, I would accept that writing good issues can be as hard as solving them sometimes and if that person did some work and it gets you about 25-40% of the way there without doing any harm, maybe **merge the commit** and leave some comments and followup issues.

[gh issue]: https://github.com/blackpythondevs/blackpythondevs.github.io/issues/391
[3391-0001]: https://jekyllrb.com/
[Jinja2]: https://jinja.palletsprojects.com/en/3.0.x/

<!-- Report:
(47:31:19): [Jekyll](ruby jekyll) => https://jekyllrb.com/
(47:54:18): [Jinja](jinja2) => https://jekyllrb.com/
(0:54:18): Processed: 2 links, 0 errors.
-->