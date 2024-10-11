---
date: 2023-11-17 02:29:21+00:00
description: 'Here''s a subtle description to encourage the reader to read the blog
  post:


  "Want to make your code snippets shine in your blog posts? Learn how I''m using
  four game-changing tools - bat, termshot, vhs, and more - to create visually stunning
  and engaging code examples that will take your writing to the next level.'
summary: Here are some of the tools I'm using to create code snippets for my blog
  posts
title: Using bat, termshot, and vhs to create snippets of code for blog posts
---

When I'm sharing my code in a blog post, I have a few tools to get the job done.

Of course I can use an extension in VS Code like [polacode](https://marketplace.visualstudio.com/items?itemName=pnp.polacode) but sometimes I'm doing my terminal thing in either the VS Code terminal or in [Warp](https://www.warp.dev/).

### Step 0: Installing the tools

We're going to talk about four tools that you can install via homebrew (or chocolatey I hope. Thank you WSL).

```shell
brew install \
bat \
ripgrep \
bat-extras \
homeport/tap/termshot\
vhs 
```

### Getting code snippets with bat, batgrep

[bat](https://github.com/sharkdp/bat) is like cat but better. Basically it's cat with some good features like line-numbering and a lot of things to help you find exactly what you're looking for. I'm probably underutilizing it.

The easiest way of getting all of the code for a specific file is to run `bat` and the filename. You can even limit which lines you pull using the range command

```shell
bat pyproject.toml 0:5
```

![bat pyproject.toml 0:5](https://kjaymiller.azureedge.net/media/bat_pyproject_toml.gif)

But what if you don't know the file name. This is where you can use [batgrep](https://github.com/eth-p/bat-extras/tree/master). batgrep uses bat and [ripgrep](https://github.com/BurntSushi/ripgrep) to search for a portion of the code. You can also use `B` and `A` to count how many lines you want to add around it.

The following command shows ALL areas where dependencies are called in the pyproject.toml with the following 10 lines.

```shell
batgrep "dependencies" pyproject.toml -A=10
```

![batgrep](https://jmblogstorrage.blob.core.windows.net/media/batgrep.gif)

With both of these you can append `| pbcopy` to your command to save the output to your clipboard.

### Capturing the output as a screenshot

We've been showing the contents of files but what about the output of commands? You can use [termshot](https://github.com/homeport/termshot) to run a command and capture the output as a screenshot. 

Here's a capture of the help for `render-engine serve`

```shell
termshot -c -- render-engine serve --help
```

![render-engine serve --help](https://jmblogstorrage.blob.core.windows.net/media/render-engine-serve-help.png)

### Recording Commands and output

Earlier I created some gifs of commands being ran. For that I'm using one of the coolest products I've discovered in the last few years and that's [vhs](https://vhs.charm.sh).

vhs allows you to run a command and create a `tape` file that can be used to generate a gif or video of the command being ran.

You can manually create the file using the syntax but I prefer to use the record feature. This creates a new shell where your commands can be recorded. It can also record things like backspaces and Enter keypresses. When you're done type `exit` and then you are given a `tape` file. This file can be edited to fix any mistakes and even add some configuration for your output file. 

![vhs record doing "hello world"](https://jmblogstorrage.blob.core.windows.net/media/hello_world_vhs.gif)

Lastly when you are ready you can run `vhs < <YOUR TAPE FILE>` to convert it to a gif or mp4 (default is gif).

They also have a server that you can use to upload your tapes to and share them with others.