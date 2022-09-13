---
title: Fresh Builds Daily
date: 07 Dec 2021 13:19
tags: development, github, gh actions
---

One of the challenges faced with faced with static site generation is not having to be on top of things. When [Conduit](!g conduit relay.fm) releases, if I would like my website to update, this would require me to run a script to rebuild my site[^1]. 

Yesterday I took a look at my GitHub action for triggering [render engine] to run. I was surprised to see a handful of issues that had been keeping it from running as expected for almost a year!

![This didn't run for 12 months](https://kjaymiller.s3-us-west-2.amazonaws.com/images/GH%20Action%2012%20months%20inactive.png)

After fixing what was out dated code, I added the `cron` build step to my Github action.

```python
 schedule:
   - cron: "0 8,12,16,20 * * *" 
```

This gave me the ability to run my script 4x each day. Also after fixing an issue with my folder not overwriting (still not sure as to why but this [Remove Folder](https://github.com/JesseTG/rm) action did solve the issue) this mean that I would have a clean build of my site every four hours, fixing a duplication issue that I'm still unsure of why it's happening.

I'm not happy that I have some bugs that aren't solved but I am happy that I have a nice little fix to make sure that my site is always within 4 hours of being up to day with what I'm doing.

[^1]: The [script](https://github.com/kjaymiller/kjaymiller/blob/main/podreader.py) actually pulls the latest episode from our rss feed

