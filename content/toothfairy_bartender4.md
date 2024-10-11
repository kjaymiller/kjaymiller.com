---
category: development
date: 2021-02-15 16:43:00-08:00
description: 'Here is a subtle description to encourage the reader to read the blog
  post:


  "I recently discovered a clever way to automatically show my ToothFairy icon in
  macOS only when my AirPods Pro are connected. Want to see how I did it?"


  This description aims to pique the reader''s interest by highlighting a specific
  feature and hinting at the solution, without using clickbait phrases or making exaggerated
  claims.'
image: https://kjaymiller.s3-us-west-2.amazonaws.com/images/ToothFairy%20Toggle.png
tags: shell, apps, macOS, automation
title: Showing the Toothfairy Icon only when my Airpods Pro are Connected
---

Recently [Bartender 4][Bartender] released with a couple of features that I was super stoked about. 

One of those updates was the ability to add custom rules for showing/hiding icons based. Wanting to play with this more I created a watcher shell script for showing/hiding the [ToothFairy][ToothFairy] icon.

![Bartender Showing Toothfairy](https://kjaymiller.s3-us-west-2.amazonaws.com/images/ToothFairy%20Toggle.png)

The end result of this script is that when my Airpods Pro are connected to the device, the toothfairy icon will appear in the menu bar. Once the Airpods Pro are disconnected the icon will go back to being hidden. This means that I can quickly tell when my AirPods Pro are connected to my machine (even if they are also connected to my phone or iPad).

![Airpods are not connected and the icon is in the secondary Bartender Bar](https://kjaymiller.s3-us-west-2.amazonaws.com/images/bartender-toothfairy-disabled.png)

## The Script
I found the command for getting your Bluetooth settings just tabbing through terminal commands. 

`AP_STAT=$(system_profiler SPBluetoothDataType | grep -A9 "Jay’s AirPods Pro:")`

This saves the information for any bluetooth device named _Jay's AirPods Pro_ to `AP_STAT` (Airpods Status).

I got help from this similar idea from [Godbout's Alfred Workflow](https://github.com/godbout/alfred-airpodspro-battery). 

`echo $AP_STAT | awk '/Connected: Yes/{print 1}'`

echo prints the data and awk is a _text manipulation_ command. It looks for the pattern `Connnected: Yes` and returns a 1 if it is found (otherwise it returns nothing).

Bartender looks for a _True_ value which `1` is. 

![Airpods are Enabled and the icon is showing in the main menubar](https://kjaymiller.s3-us-west-2.amazonaws.com/images/toothfairy-bartender-enabled.png)


Here's the whole script

```
AP_STAT=$(system_profiler SPBluetoothDataType | grep -A9 "Jay’s AirPods Pro:")
echo $AP_STAT | awk '/Connected: Yes/{print 1}'
```

Both [ToothFairy][ToothFairy] and [Bartender 4][Bartender] (available on Big Sur ONLY) are both a part of [SetApp (Affiliate Link)](https://go.setapp.com/invite/6bcd77a8-3223-482b-bcd2-ff337999765d)

[Bartender]: https://macbartender.com
[ToothFairy]: https://c-command.com/toothfairy/