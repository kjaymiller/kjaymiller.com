---
date: 2025-01-21 02:03:45.848219+00:00
title: Bambu Lab, You aren't Apple
description: BambuLabs latest moves are scaring a lot of users, but My hope is the backlash will keep them from going too far.
---

Two of my colleagues convinced me to make the switch from Creality[^1] to Bambu Lab. One of the big talking points was that the company had really invested in user experience. The setup was easy and I've had no problems with my A1 or the AMS since I got it in November. I was just telling a friend today that I was considering starting to save for the P1S.

It wasn't until I went to look for some videos for that friend, whom I had convinced to dive into the Bambu Lab ecosystem as well, that I found [a video by Louis Rossmann](https://www.youtube.com/watch?v=aIyaDD8onIE) saying that Bambu Lab was locking their printers to use their software.

## What do I know

First of all, I'm an enthusiast that hasn't been in the space for that long (approx 1 year). You shouldn't be relying on me as the sole source of information around 3d printing.

That said, here's what I got.

A few days ago, Bambu Lab [released a post on their blog](https://blog.bambulab.com/firmware-update-introducing-new-authorization-control-system-2/) that would require authorization controls to do many things with your Bambu Lab X-series printers (with P and A series happening in the future). This was done in the name of security.

They also announced they were no longer supporting the open-source networking plugin for third-party slicers and would require a new beta plugin called [Bambu Connect](https://wiki.bambulab.com/en/software/bambu-connect?ref=blog.bambulab.com).

Today (of writing), they responded to the large outcry from the community in an [update](https://blog.bambulab.com/updates-and-third-party-integration-with-bambu-connect/). This update provided more details about the update and Bambu Connect. It also took a very defensive position saying that "misinformation" was being spread. I don't have examples and the videos that I've seen don't state what Bambu **IS** doing but talk about what they **COULD** do under the same security stances.

<iframe src="https://www.youtube.com/embed/gFotkmlPAT4?si=MHVNmYyOMbvZPBue" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

## Bambu seems to be making decisions like their previous employer

It's interesting that Bambu Lab was founded by former DJI employees. This explains a lot given that DJI is known for quality hardware with excellent user experience. It's also interesting that a few days before this Bambu Lab update, DJI make a questionable move in removing their geofence restrictions in No-Fly Zones.

> Areas previously defined as Restricted Zones (also known as No-Fly Zones) will be displayed as Enhanced Warning Zones, aligning with the FAA's designated areas. In these zones, in-app alerts will notify operators flying near FAA designated controlled airspace, placing control back in the hands of the drone operators, in line with regulatory principles of the operator bearing final responsibility.

The **operator** bearing final responsibility...

Bambu Lab at first glance may seem to be doing the opposite, by bringing their code in house, but I think they are doing everything in their power to say "We did what we could".

There have been an increase of attacks on 3d printers. AnyCubic, another 3D printer company, [shared last year](https://store.anycubic.com/blogs/news/security-issue-of-Anycubic-cloud) that thousands of their printers were subject to a MQ Telemetry Transport (MQTT) vulnerability.

It seems Bambu Lab also has seen their share of [MQTT Related incidents](https://forum.bambulab.com/t/bambu-lab-mqtt-limitations/83440). But there are also [other products](https://biqu.equipment/products/bigtreetech-panda-touch-5-display-for-bambu-lab-printers) that rely on MQTT.

This is where I think the truth may start to be found.

Bambu Lab doesn't want to support another product. I also expect they will release their own competitor in the future. But also if there is an issue introduced by a third party, they want to say, they did everything they could to keep you safe. This sounds a lot like a Apple.

## Apple vs Open Source vs the world

This examination was mostly formed by one of the same people that convinced me to buy a Bambu Lab printer.

Apple is perhaps the biggest example where a walled-garden is a benefit. I'm an Mac and iPhone user and our home for over a decade has been heavily an Apple-first ecosystem. The biggest reason is convenience. The second is something that my friend Jacob once mentioned [in a talk](https://youtu.be/qphoNm9LiXM?si=Mc8yRvJD9tNELY4n&t=2031).

> Google's (or in this case Apple's) security team is better than yours.

I understand that Apple is a large target these days. And in the printer world I would think that Bambu Lab, Prusa, and Creality, and AnyCubic are probably the biggest names in printing. That said Apple has stood on the backs of giants and uses a ton of open source software, polished behind 100% Recycled ALUMINIUM.

My guess is that Bambu Lab is building off of open source technology with some proprietary changes and ultimately saying, "we think between our skills, not being out in the open, and a bug bounty program, we'll be fine". They might be. I'm not against closed-source software... I'm more against the, changing your mind on things and I think that's the problem most people have and they will want to prove that you are indeed, not fine.

## Bambu have fun being a target

If you thought the target of being the darling of the non-hacky consumer 3d printing market put a target on your back. Now you done pissed off the open-source purists...

[Bambu Connect has already been reverse engineered](https://www.reddit.com/r/OrcaSlicer/comments/1i2t6l8/comment/m7tuf2i/). Just like the TikTok ban, people are going to side with pettiness until they get their way. I expect there to be a fun game of cat and mouse until one of the parties gets board. Considering Bambu is doing this in the name of liability, I mean security. They will probably patch as fast as they find which means that it will boil down to how much the those that like to exploit will want the glory (or the Bug bounty money).

## Where does that leave me

None of this answers the $0.000100 question, "Jay, are you going to ditch Bambu Lab?" The honest answer is, I don't know. I'm a creature of convenience. Bambu didn't win me over with their printer... They did with the autodetection QR code stuff that get's detected in Orca slicer. Other filament companies do this but I haven't seen it from anyone other than them sooooooooo.

Honestly, the update will not affect me in the long run. I don't want to tinker with my 3d printer. I want to print things for myself and my friends. There's a chance that I'll look at other options for my first Core-XY printer, but the reality is. THESE PRINTERS ARE 90% the same and you're paying for brand + User Experience and a little bit of Made in the <COUNTRY YOU CARE ABOUT> or Saved X dollars compared to the Prusa whatever their cheapest printer is which is still like twice what I paid for my printers.

[^1]: Considering my Creality V3 KE is still down due to some weird extrusion failure, It wasn't that hard to do.
