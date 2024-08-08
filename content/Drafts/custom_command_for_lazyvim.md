---
title: Setting Marked 2 as my Previewer for Markdown Files in LazyVim
date:
---

I'm still trying to wrap my head around lua, but when it comes to configuring nvim:

> There is always a simple way to do it and a stupid complex way to do it.

For some reason AI wanted me to do it the complex way? WHY?

!["Really Tho" gif](https://tenor.com/view/why-why-tho-why-though-seriously-are-you-serious-gif-19807874)

> NOTE: I wanted to search for a gif here using tenor and then I used what I'm going to talk about to do just that.

In the end I needed to use the `vim.cmd("<THE SAME THING YOU WOULD PUT IN YOUR COMMAND>)`

Then you need to wrap it in the lua command `vim.api.nvim_create_user_comman()`

```lua
vim.api.nvim_create_user_command(
    "Marked", -- Command name
    function() -- Command implementation
        -- the marked application to the current buffer
        vim.cmd("! open -a Marked %")
    end,
    { -- Command options (optional)
        desc = "Opens the current file in Marked",
    }
)
```

```


All that stuff around it won't change but with this I was able to quickly create a new command.

### Bonus: That GIF Thing

gotcha
```
