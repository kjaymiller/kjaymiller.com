---
title: Getting text from websites using Keyboard Maestro
date: 03 Mar 2021 22:15
tags: productivity, keyboard maestro, automation
YouTube: https://youtube.com/embed/U_VHfB9b9oE
image: https://kjaymiller.s3-us-west-2.amazonaws.com/images/Keyboard%20Maestro%20Get%20Text%20from%20Website/execute%20javascript-squashed.png
---

In a [similar post](https://kjaymiller.com/how-to-automate-form-filling-with-keyboard-maestro-for-big-sur) I showed how to input information into a browser using [Keyboard Maestro](https://keyboardmaestro.com). 

In this post I want to show another integration with your browser and show you how you can get content from your browser to do whatever you want with.

This technique uses Javascript to return the text of an HTML element and then it can be manipulated using Keyboard Maestro.

## Enable Javascript from Apple Events ##

This setting (off by default prevents rogue applications from taking control of your browser). In most cases this is a great security measure but in our case, it breaks the Keyboard Maestro functionality.

### For Safari ###
With Safari open go to **Preferences** and select the advanced column.

Check the box _Show Develop menu in menu bar_

![check the box show develop menu in menu bar](https://kjaymiller.s3-us-west-2.amazonaws.com/images/Keyboard%20Maestro%20Form%20Automation/Safari%20Show%20Develop%20Menu%20from%20MenuBar.png)
 
In the menu bar select the _Develop_ menu and select the option _Allow Javascript from Apple Events_.

![Enable Javascript from Apple Events](https://kjaymiller.s3-us-west-2.amazonaws.com/images/Keyboard%20Maestro%20Form%20Automation/Safari%20Allow%20Javascript%20from%20Apple%20Events.png)

### For Chrome

Chrome makes this a little easier. In the menu bar select _View_, then _Develop_ (already visible) and select _Allow Javascript from Apple Events_.

In both cases, you will see a check mark that indicates you are ready to Automate!

## Navigate to the page you wish to get data from ##

You can use Keyboard Maestro's **New Safari/Chrome Tab with URL**. If you do this make sure that you wait until the page is fully loaded or data may not be collectable. Luckily there is a _Wait for Safari/Chrome to Finish Loading_ action you can use.

![New Safari/Chrome Tab](https://kjaymiller.s3-us-west-2.amazonaws.com/images/Keyboard%20Maestro%20Get%20Text%20from%20Website/New%20Tab%20with%20URL.png)

## Find the element that you wish to get the text of ##

Highlight the selected text on the page. Right Click and select _Inspect Element_ (or _Inspect_ for Chrome). This will open the developer console with that selected element highlighted.

![Inspect Element](https://kjaymiller.s3-us-west-2.amazonaws.com/images/Keyboard%20Maestro%20Get%20Text%20from%20Website/inspect%20element-squashed.png)
Right click the element and hover over copy and choose the _Selector Path_ (in Chrome choose _copy selector_)

![Copy Selector](https://kjaymiller.s3-us-west-2.amazonaws.com/images/Keyboard%20Maestro%20Get%20Text%20from%20Website/copy%20selector-squashed.png)

## Use the _querySelector_ method and _innerText_ attribute ##

Add the **Execute Javascript in Safari/Chrome** action and enter the following code.

```html
document.querySelector("<PASTE YOUR COPIED TEXT>").innerText`
```

`document.querySelector` tells the browser to find the first element that matches your passed selection. Since you highlighted the text it will give you the most unique possible selection, so the first choice should be the correct one[^1].

This however, `document.querySelector` gives you the full HTML element. So a paragraph would be

```html
<p>Lorem ipsum dolor sit amet..</p>`
```

We don't need the `<p></p>` parts. Luckily we can use the `innerText` attribute. As [Mozilla](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/innerText) explains it:

>  	The innerText property of the HTMLElement interface represents the "rendered" text content of a node and its descendants. As a getter, it approximates the text the user would get if they highlighted the contents of the element with the cursor and then copied it to the clipboard.

To test this you can paste your code into the console of your browser (a tab in the developer console.) or you can set the action to display the results. When you have the right element you can pass that information as a variable to use later in your Keyboard Maestro workflow or you can save it to your clipboard to paste into another window. 

![Execute Javascript](https://kjaymiller.s3-us-west-2.amazonaws.com/images/Keyboard%20Maestro%20Get%20Text%20from%20Website/execute%20javascript-squashed.png)

[Keyboard Maestro]: https://keyboardmaestro.com 

[^1]: If you do need to get another version you can use `querySelectorAll(<Your Element>)` and choose the index that you're looking for.

