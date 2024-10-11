---
date: 2023-01-05 11:30:00-08:00
description: Learn a handy Vim trick to enclose text in parentheses and other characters
  without relying on plugins. Discover how to customize your workflow for maximum
  efficiency.
image: https://kjaymiller.azureedge.net/media/vim_encap_parens.gif
link: https://superuser.com/questions/875095/adding-parenthesis-around-highlighted-text-in-vim
tags: vim
title: Enclose text in Parentheses (and Other Characters) in VIM WITHOUT PLUGINS
---

Whether I'm creating a backlink or adding a url or a comment I often need to wrap text in parenteses or other characters. I've been a VIM (or VIM mode) user for a while and I never committed how to do this to memory. Let's change that.

## How to do it

```vim
#  In VISUAL Mode with the text selected
c()<Esc>P
```

## For those not in the VIM world

c - changes the text and puts the previous text in the buffer (think clipboard)
() - creates brackets. You can replace with braces, brackert or single/double quotes. You can also add as many of these as you wish.
<Esc> - escape back into Normal Mode
P - Paste one character back which pulls from the buffer returning the last bit of text. If your cursor is not in the correct spot. You will need to move it.

## That sounds like a lot

It kinda is (especially if VIM isn't your thing) which is why if you do this a lot you are better off mapping those steps in your config file to a command. 

```vim
vnoremap <C-(> c()<esc>P
```

Most of the commands are the same. The `vnoremap` ensures that this only runs in VISUAL Mode (When you select text) and `<C-(>` is the command for `ctrl+(`.

![Running the Command in VIM](https://kjaymiller.azureedge.net/media/vim_encap_parens.gif)

[SuperUser post]: https://superuser.com/questions/875095/adding-parenthesis-around-highlighted-text-in-vim