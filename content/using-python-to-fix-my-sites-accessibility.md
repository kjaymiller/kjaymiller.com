---
date: 2023-09-10 23:17:55
description: I'll be updating the Render Engine template to include accessibility
  fixes for our website. I plan to focus on pages with existing issues, starting with
  this homepage. My goal is to make testing easier and ensure a better user experience.
title: Using Python to fix my Accessibility nightmare of a website
---

So earlier this year my colleague Pamela Fox gave a wonderful presentation on [using Playwright to test your accessibility](https://www.youtube.com/watch?v=J-4Qa6PSomM&pp=ygUUcGFtZWxhIGZveCBub3J0aCBiYXk%3D) with the help of [axe-core](https://github.com/dequelabs/axe-core). This led to the creation of her module (you guessed it!) - [axe-playwright-python](https://pypi.org/project/axe-playwright-python/).

My website is a hot-mess in terms of accessibility so in the name of accountability, I'm going to make sure that fix that hopefully by sharing how bad my site is.

## What I can't fix every single blog post I've written at least not easily

I don't write 100 blog posts a year (not even close) but I'm sure that I have some issues with my blog posts and here is why.

I write them with markdown2. This means that I'm limited to the extensions that are compatible with markdown2. While, yes I built the static site generator my site runs, making an extension that modifies the generated markdown is something that I personally don't recommend, especially now that markdown2 is getting a brand new extensibility format that should make doing that easier.

## How am I doing this

Steps to do

1. Install the module

```sh
python3 -m pip install -U axe-playwright-python
python3 -m playwright install --with-deps
```

2. Create a script testing your current website (You need to check against a running website. I could wrap this in a server instance and the )

I saved the script to my repo so you can [check that out over here](https://github.com/kjaymiller/kjaymiller.com).

### How bad is it?

The results show that there are 3 violations (well three types of violations. I didn't count the number of instances for each of those violations)

```md

Found 3 accessibility violations:
Rule Violated:
landmark-one-main - Ensures the document has a main landmark
 URL: https://dequeuniversity.com/rules/axe/4.4/landmark-one-main?application=axeAPI
 Impact Level: moderate
 Tags: ['cat.semantics', 'best-practice']
 Elements Affected:

 1) Target: html
  Snippet: <html lang="en">
  Messages:
  * Document does not have a main landmark
Rule Violated:
link-name - Ensures links have discernible text
 URL: https://dequeuniversity.com/rules/axe/4.4/link-name?application=axeAPI
 Impact Level: serious
 Tags: ['cat.name-role-value', 'wcag2a', 'wcag412', 'wcag244', 'section508', 'section508.22.a', 'ACT']
 Elements Affected:


 1) Target: .bg-gradient-to-br > .p-1:nth-child(3)
  Snippet: <a class="p-1" href="https://www.youtube.com/channel/UCjoJU65IbXkKXsNqydro05Q/">    <i class="text-red-700 text-2xl m-1 fa-brands fa-youtube"></i></a>
  Messages:
  * Element does not have text that is visible to screen readers
  * aria-label attribute does not exist or is empty
  * aria-labelledby attribute does not exist, references elements that do not exist or references elements that are empty
  * Element has no title attribute
  * Element is in tab order and does not have accessible text

 2) Target: .bg-gradient-to-br > .rounded-xl.opacity-50[href$="kjaymiller"]:nth-child(4)
  Snippet: <a class="rounded-xl opacity-50 p-1 hover:opacity-100" href="https://twitter.com/kjaymiller">    <i class=" text-blue-500 m-1 text-2xl fa-brands fa-twitter-square"></i></a>
  Messages:
  * Element does not have text that is visible to screen readers
  * aria-label attribute does not exist or is empty
  * aria-labelledby attribute does not exist, references elements that do not exist or references elements that are empty
  * Element has no title attribute
  * Element is in tab order and does not have accessible text

 3) Target: .rounded-xl.opacity-50.p-1:nth-child(5)
  Snippet: <a class="rounded-xl opacity-50  p-1 hover:opacity-100" href="https://linkedin.com/in/kjaymiller">    <i class=" text-blue-900 m-1 text-2xl fa-brands fa-linkedin"></i></a>
  Messages:
  * Element does not have text that is visible to screen readers
  * aria-label attribute does not exist or is empty
  * aria-labelledby attribute does not exist, references elements that do not exist or references elements that are empty
  * Element has no title attribute
  * Element is in tab order and does not have accessible text

 4) Target: a[href$="blog.rss"]
  Snippet: <a class="hover:underline" href="/blog.rss"><span class="icon"><i class="fas fa-rss" aria-hidden="true"></i></span></a>
  Messages:
  * Element does not have text that is visible to screen readers
  * aria-label attribute does not exist or is empty
  * aria-labelledby attribute does not exist, references elements that do not exist or references elements that are empty
  * Element has no title attribute
  * Element is in tab order and does not have accessible text

 5) Target: .p-1:nth-child(2)
  Snippet: <a class="p-1" href="https://www.youtube.com/channel/UCjoJU65IbXkKXsNqydro05Q/">    <i class="text-red-700 text-2xl m-1 fa-brands fa-youtube"></i></a>
  Messages:
  * Element does not have text that is visible to screen readers
  * aria-label attribute does not exist or is empty
  * aria-labelledby attribute does not exist, references elements that do not exist or references elements that are empty
  * Element has no title attribute
  * Element is in tab order and does not have accessible text

 6) Target: .rounded-xl.opacity-50[href$="kjaymiller"]:nth-child(3)
  Snippet: <a class="rounded-xl opacity-50 p-1 hover:opacity-100" href="https://twitter.com/kjaymiller">    <i class=" text-blue-500 m-1 text-2xl fa-brands fa-twitter-square"></i></a>
  Messages:
  * Element does not have text that is visible to screen readers
  * aria-label attribute does not exist or is empty
  * aria-labelledby attribute does not exist, references elements that do not exist or references elements that are empty
  * Element has no title attribute
  * Element is in tab order and does not have accessible text

 7) Target: .lg\:flex > div > .rounded-xl.opacity-50.p-1:nth-child(4)
  Snippet: <a class="rounded-xl opacity-50  p-1 hover:opacity-100" href="https://linkedin.com/in/kjaymiller">    <i class=" text-blue-900 m-1 text-2xl fa-brands fa-linkedin"></i></a>
  Messages:
  * Element does not have text that is visible to screen readers
  * aria-label attribute does not exist or is empty
  * aria-labelledby attribute does not exist, references elements that do not exist or references elements that are empty
  * Element has no title attribute
  * Element is in tab order and does not have accessible text
Rule Violated:
region - Ensures all page content is contained by landmarks
 URL: https://dequeuniversity.com/rules/axe/4.4/region?application=axeAPI
 Impact Level: moderate
 Tags: ['cat.keyboard', 'best-practice']
 Elements Affected:


 1) Target: .bg-gradient-to-br
  Snippet: <div class="  bg-gradient-to-br    from-purple-600to-indigo-800  flex  flex-wrap  items-baseline  px-5  py-2  ">
  Messages:
  * Some page content is not contained by landmarks

 2) Target: .flex-grow
  Snippet: <div class="flex-grow mx-2 md:mx-auto container">
  Messages:
  * Some page content is not contained by landmarks
```

This is just the homepage so we'll see if we can update the render-engine template and then shift our focus to other pages.

Because most of the template is in the render-engine theme my work will make it across many other pages quickly.

### How to keep on this

I definitely plan to take the work that Pamela has done and make it easy to test your pages with render engine. Because you have to test on the running site I'm not entirely sure the best way to go about this but as soon as I can, I will.

It will most likely be similar to how we test [relecloud cookiecutter generation with fastapi](https://github.com/kjaymiller/cookiecutter-relecloud/blob/5ca61f724202c533cd91e638131d6b96455578a6/%7B%7Bcookiecutter.__src_folder_name%7D%7D/src/tests/conftest.py#L44C1-L52C12).

I also don't need to ae my files all the time. I sat in a great talk by Randy Pegels on automating playwright testing and he mentioned taking the report and adding it to an artifact. I think that is a great idea and I'll be doing that as well. (More in a future post).

I may also catalog this in [livestreams](https://www.youtube.com/@KJayMiller/streams) and other things so stay tuned for that.
