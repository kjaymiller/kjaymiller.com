---
title: How I Made My Twitch Player Appear on My Site Only When I'm Live
slug: twitch-player-live-only
category: Code
tags: twitch, javascript, KISS
image: https://kjaymiller.s3-us-west-2.amazonaws.com/images/purple-background-twitch-embed.png
date: 12 Aug 2020 11:27
---

I wanted to write this to show that the easiest answer can often elude us. 

If I asked you to add a twitch frame to a website and make it only appear when you were live, how would you do it?

## Embedding the Twitch Frame

Following the [documentation](https://dev.twitch.tv/docs/embed/everything) from Twitch, I copied the example code, adjusted the width and the height[^1], and changed the `channel-id` to my Twitch username.

## Checking the Live Status

After spending an hour on stream trying to build a twitch app, I opted for the more low-tech solution. 

```javascript
if (player.getPlayerState().currentTime != 0) {
    document.querySelector('#twitch-block').style.display = 'initial';
  }

  else {
    document.querySelector('#twitch-block').style.display="None";
  }
```

There were a few reasons:

- The javascript was easy.
- The authentication stuff is hard to stream (in a secure way)
- RateLimits and things
- THE JAVASCRIPT WAS EASY

The hardest part about building this listener was keeping it simple. You could add event listeners and things and you could use webhooks and all that stuff. Another option is to look at the `currentTime` value. When you are not streaming, `player.getPlayerState().currentTime == 0`[^2]. This means that I can set  `display="None"` on the element that holds the twitch player. Allowing my website to act like the embed was never there[^3]. 

Don't forget to add an amazing purple background so it looks fantastic!

![embed with a beautiful background](https://kjaymiller.s3-us-west-2.amazonaws.com/images/purple-background-twitch-embed.png)

[^1]: Which I still a little confused on how that present in a responsive way
[^2]: I don't know if this is the case if you are hosting someone sooooo... Your mileage may vary.
[^3]: There could be some performance issues with this, but ultimately if there is the player would not load which means that the block wouldn't take up any space.

