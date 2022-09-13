---
title: How to Automate Form Filling with Keyboard Maestro (For Big Sur)
date: 03 Mar 2021 11:12
tags: Keyboard Maestro, automation, productivity
image: https://kjaymiller.s3-us-west-2.amazonaws.com/images/Keyboard%20Maestro%20Form%20Automation/Keyboard%20Maestro%20Set%20Safari%20Field.png
---

Working to help a friend automate some form entry I went to look back into how I had automated a similar task a few years ago with [Keyboard Maestro](https://keyboardmastro.com). I was surprised at how I remembered the steps to input form fields (Big props to the KM team for making it so easy to do.)

But when I went to test adding value to the field, I got nothing. If you're trying to automate this form filling, you may run into the same steps so hopfully this will serve as a quick guide to troubleshoot the problems you may have run into or to start automating your own form fields.

**NOTE: This guide uses Safari but you can use the Chrome actions to complete the same tasks.**

---

## Step 1: 🚨 Make sure Javascript can Be Ran FROM System Events 🚨

Ultimately this was the issue I ran into. This setting (off by default prevents rogue applications from taking control of your browser). In most cases this is a great security measure but in our case, it breaks the Keyboard Maestro functionality.

### For Safari ###
With Safari open go to **Preferences** and select the advanced column.

Check the box _Show Develop menu in menu bar_

![check the box show develop menu in menu bar](https://kjaymiller.s3-us-west-2.amazonaws.com/images/Keyboard%20Maestro%20Form%20Automation/Safari%20Show%20Develop%20Menu%20from%20MenuBar.png)
 
In the menu bar select the _Develop_ menu and select the option _Allow Javascript from Apple Events_.

![Enable Javascript from Apple Events](https://kjaymiller.s3-us-west-2.amazonaws.com/images/Keyboard%20Maestro%20Form%20Automation/Safari%20Allow%20Javascript%20from%20Apple%20Events.png)

### For Chrome

Chrome makes this a little easier. In the menu bar select _View_, then _Develop_ (already visible) and select _Allow Javascript from Apple Events_.

In both cases, you will see a check mark that indicates you are ready to Automate!
[Keyboard Maestro]: https://keyboardmaestro.com 

## Step 2: Find the XPath of the field you want to Enter ##

This is where the magic happens 🧙🏾‍♂️. Finding the right field to target with information can be a challenge as websites come in many different sizes and accesssibility forms.That said you can use the tools built into Keyboard Maestro or the browser to find the correct XPath.

Don't worry too much about what an [XPath](https://developer.mozilla.org/en-US/docs/Web/XPath) is. You just need to know how to find it. 

### Using Keyboard Maestro  ###

In Keyboard Maestro, when you select the _Set Safari Field to Text_ the _Safari ˇ_ will look for forms on the active tab of in your browswer and show all of the input fields available. Find the field that you want to automate with text and select it. Enter the text you wish to fill in. 

![Choosing the XPath from Keyboard Maestro](https://kjaymiller.s3-us-west-2.amazonaws.com/images/Keyboard%20Maestro%20Form%20Automation/Keyboard%20Maestro%20Set%20Safari%20Field.png)

**NOTE: There is also a checkbox version of this that works exclusively for checkboxes**

### Using Safari/Chrome  ###

If you have a lot of fields that you want need to identify you can figure out the exact text field you want to add to by right-clicking the field in your browser and selecting _Inspect Element_ (_Inspect_ for Chrome) to view the source code. 

![inspect element](https://kjaymiller.s3-us-west-2.amazonaws.com/images/Keyboard%20Maestro%20Form%20Automation/Safari%20Inspect%20Element.png)

Then in the inspector you can right click the highlighted code-block and hover over _copy_ and select _XPath_.

![copy XPath](https://kjaymiller.s3-us-west-2.amazonaws.com/images/Keyboard%20Maestro%20Form%20Automation/Copy%20XPath.png)


Repeat this step as many times as you like for each field. Finally, add a submit field.

![Submit Form](https://kjaymiller.s3-us-west-2.amazonaws.com/images/Keyboard%20Maestro%20Form%20Automation/Keyboard%20Maestro%20Submit%20Safari%20Form.png)

