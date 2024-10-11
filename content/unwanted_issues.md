---
date: 2024-08-24 07:51:00-04:00
description: I've learned that even questionable ideas in maintainers can lead to
  valuable insights and a better understanding of what truly matters.
title: '[Question] Writing Issues You Don''t Want to Implement'
---

Any maintainers in the past post issues that they don’t like purely to see if someone has a good reason that it should implemented?

Thinking about creating issues in render-engine around:

- flag to teardown output when the server is stopped
- flag to dry run and print output

The ideas aren’t bad. I just don't know the _why this should exist_.

In my head I was thinking it would be great for development and testing.

But that could be some custom stuff and not "YET ANOTHER FEATURE" that needs to be documented that won't be heavily used.

I also think there is some value in filing the issue and then explaining your case and then closing the issue. That way if the issue is brought up in the future you can reference it.

Again I'm more wondering if people have done this in the past (Creating issues that they don't think are great features but if they thought it could serve some good, then maybe it can?)