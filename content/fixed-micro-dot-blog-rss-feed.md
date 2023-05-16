---
title: Fixing my Micro.blog RSS Feed (A Love Letter to Micro.Blog)
date: 2023-05-15 22:45:00-04:00
---

> !!! Note disclaimer: This is a praise piece of Micro.blog and they deserve it. That said, they have given me money before so I want to be transparent about that. They did not pay me to write this and I will not earn any revenue as a direct result of this post.

I was using [micro.blog](https://microblog.kjaymiller) as a way to share my microblog and blog posts to awesome folks.

One day it stopped working. Sadly I didn't notice at the time and wasn't aware of how to fix it.

## Why not Twitter/Mastodon/BlueSky/LinkedIn

That's the problem! They all have their ups and downs.

The world is divided and to be honest, I'm on social media to work both in consumption and production. I want to share the things that I'm making, my opinions and, importantly, communicate with my developer friends and maintain fantastic relationships with them but with everyone being in multiple places. I feel as if I'm connecting with new people on deeper levels in different formats using Private Discord Servers and Signal/Messages which means. I'm consuming less and less and not sharing the things that I've been doing.

![Chart of my social media user based on previous consumption and production ](https://kjaymiller.azureedge.net/media/What%20I%20Was%20Doing%3F.png)

I'd like to share to all the services I look at (and more) and I believe Micro.blog can help with that.

![Chart of my projected social media usage](https://kjaymiller.azureedge.net/media/What%20I%20(Hope)%20to%20Be%20Doing.png)

## Micro.blog allows you to post your RSS to multiple timelines

Micro.blog will allow you to connect your personal blog for free using RSS. If you provide a title it will share your post and link to it. Without a title, the contents will be displayed in a _tweet-like_ format for the first 280 characters. Beyond that, the post will be auto truncated and a link to your post will be sent.

This does require you to have your own blog/microblog but if you don't have one, you can get one from Micro.blog (at time of writing you can go to [micro.blog/summer](https://micro.blog/summer) to get your first 4 months for $1.

Micro.blog also gives you the ability to post to other social media channels. This means that my blog/microblog is the place where I publish my content and thoughts and that post gets distributed out by Micro.blog shortly later.

![Micro.Blog's cross-posting options](https://jmblogstorrage.blob.core.windows.net/media/micro_dot_blog_crossposts.png)

## Micro.blog wasn't working earlier

I mentioned that I was doing this before and it wasn't working. Luckily for me, they have logs available to you when things don't go right. This mean that once I added the new [rssFeed](https://kjaymiller.com/allposts.rss) from my new [AggregationFeed](https://github.com/kjaymiller/render-engine-aggregators) page, I could look at the logs and see that it wasn't working since my feeds didn't use guids which micro.blog requires.

![View Micro.blog posting Logs](https://kjaymiller.azureedge.net/media/micro_dot_blog_view_logs.png)

I was able to [change the code](https://github.com/kjaymiller/render_engine/commit/8ed5f8938cf80e8c040e0345d8dbee20630124bc) for my blog to provide a guid and things immediately began working.

![Logs showing no GUID present](https://kjaymiller.azureedge.net/media/micro_dot_blog_no_guids.png)

I know that I just spent 500 words fawning over this service that I've been using again for one day. Micro.blog is a small team of independent developers that focus on this full time and believe that there is something special about social media when you have a well moderated, niche service that is funded by its users. The audience may be small, but the service works to ensure that you have the ability to share your content the way that you wish while retaining ownership of it.
