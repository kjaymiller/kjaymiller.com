---
date: 2023-09-11 13:43:01+00:00
description: Got a Mastodon account, but wish you could seamlessly follow new users?
  I recently discovered a browser hack that makes opening their profiles in Ivory
  a breeze.
title: Arc Boost for Opening in Ivory v0
---

> ❕ Note
> This only works for profiles. I hope to make it a little smarter and handle posts as well in the future.

In my question to find more folks (especially those that look kinda like me and have similar interests), I've been playing with some services that help me import a following of users.

While trying [followgraph for Mastodon](https://followgraph.vercel.app) - I wanted to automatically open a follow users account in [Ivory](https://apps.apple.com/us/app/ivory-for-mastodon-by-tapbots/id6444602274).

Arc (the browser I use) has this feature for making domain specific boosts that can inject css or javascript into a page. I do this to sometimes block adds for sites that are all fussy about me blocking their adds or that just have really annoying video things that I don't want to bother installing an extension for (Looking at you realtor.com).

You can't share boosts with javascript so here's what I did.

1. Go to the domain you wish to add the boost to. For us it's `https://mastodon.social`

2. Enable boosts in the url bar under settings
![Enable boosts in the url bar under settings]https://jmblogstorrage.blob.core.windows.net/media/Enable%20Boosts.png

3. Select the JS Button in the Boost Bar
![Select the JS Button in the Boost Bar](https://jmblogstorrage.blob.core.windows.net/media/boosts%20window.png)

4. Add code to grab the user name from the boost and open it in ivory using their [url_scheme](https://tapbots.com/support/ivory/tips/urlschemes).

![The javascript code window](https://jmblogstorrage.blob.core.windows.net/media/boosts-js-tab.png)

Here's the code I used for v1:

```js
const baseUrl=document.URL;
try {
const user=baseUrl.split("https://mastodon.social/@")[1];
const ivoryUrl=`ivory://acct/user_profile/${user}`;
console.log(`Opening ${ivoryUrl}`);
window.open(ivoryUrl);
}

catch (err) {
  console.log(err)
}
```

I also created [this gist](https://gist.github.com/kjaymiller/c356c81749b98d433b4b117737a8a4a5) that I'll try to update. 

In the next version, I'll likely try to edit the buttons for followgraph directly so that it open from there instead of loading the window and then opening the app (and closing the window).