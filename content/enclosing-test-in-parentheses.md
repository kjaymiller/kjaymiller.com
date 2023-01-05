---
title: Enclose text in Parentheses (and Other Characters) in VIM WITHOUT PLUGINS
link: https://superuser.com/questions/875095/adding-parenthesis-around-highlighted-text-in-vim
tags: vim 
---

> I learned this from this [SuperUser post].


```vim
# In Normal Mode
v$
c()<Esc>P
```

## For those not in the VIM world

v - switch to visual mode which allows you to select text
$ - jumps to the end of the line, selecting all the text. This can also be swapped to select as much as you like.

c - changes the text and puts the previous text in the buffer (think clipboard)
() - creates brackets. You can replace with braces, brackert or single/double quotes. You can also add as many of these as you wish.
<Esc> - escape back into Normal Mode
P - Paste one character back which pulls from the buffer returning the last bit of text. If your cursor is not in the correct spot. You will need to move it.

## That sounds like a lot.

It is which is why if you do this a lot you are better off mapping those steps in your config file to a command. 

```vim
vnoremap <C-(> c()<esc>P
```

Most of the commands are the same. The `vnoremap` ensures that this only runs in VISUAL Mode (When you select text) and `<C-(>` is the command for `ctrl+(`.


[SuperUser post]: https://superuser.com/questions/875095/adding-parenthesis-around-highlighted-text-in-vim