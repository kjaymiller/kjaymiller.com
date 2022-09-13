---
title: asdf, direnv and the upgrade to python 3.10
date: 06 Oct 2021 07:16
tags: python, code
image: https://kjaymiller.s3-us-west-2.amazonaws.com/images/python_3_10_asdf_errors_python_versions.png
---

Recently [Python Bytes][6937-0001] a post mentioned using [asdf][6937-0002] and direnv to manage Python versions.

I've always looked for a good way to have auto-setting environments and while `virtualenvwrapper` did a lot for that. I feel like using pyenv via Homebrew was a step backward, having to initialize `pyenv-virtualenvwrapper` every time I opened the terminal felt like I was doing something wrong. _I probably was_.

That said asdf gives you pyenv-like[^1] simplicity for running multiple versions of Python (and nvm, and ruby, and other things).

## My Installation

### Pre-Requisites

**Install [Homebrew][2889-0001]**. We aren't removing it from our setup, just liberating it from programming language version management responsibilities.

**Install [direnv][2889-0002]**. Using the `layout` command is how we'll create that auto-environment control. layout will create a _shim_ of our requested Python version in the `.direnv` directory of our project[^2].

**[Optional]** - This blog post is using [zsh][2889-0003] and [ohmyzsh][2889-0004] as the environment. It's not required but this post will explain the setup using that.

## Install asdf and Python

Run `brew install asdf`. If running ohmyzsh, you can add asdf to the list of plugins, otherwise be sure to follow any setup instructions.

![zsh plugins](https://kjaymiller.s3-us-west-2.amazonaws.com/images/python_3_10_asdf_errors_omz_plugins.png).

You'll also need the [asdf-python plugin][2889-0005] with `asdf plugin-add python`

Next you'll need to install Python through asdf. I recommend completely [uninstalling Python via Homebrew](https://dev.to/therealdarkmage/clean-up-and-remove-a-python3-homebrew-install-21ai). Once that is done you can re-install Python using the command `asdf install python <PYTHON VERSION>` you can also use `latest` for the Python version if you aren't sure with version is the latest one.

You can verify the python versions installed using `asdf list python`. You can verify that asdf installed version of python is default by running `which python`.

If you have multiple versions installed, you can select the version similar to `pyenv` using `asdf global python <PYTHON VERSION>`

You can tell which one is set using `python --version`.

![asdf python versions](https://kjaymiller.s3-us-west-2.amazonaws.com/images/python_3_10_asdf_errors_python_versions.png)

## Register a Python Environment for Your Project

When you want to create a new project make the directory for that project. Then create a .envrc file and add `layout python <PYTHON VERSION>`

I had a recent issue with the <PYTHON VERSION> part of this[^3]. If you drop this then it will use the latest version by default.

Then you will need to activate direnv using `direnv allow`.

[^1]: If I remember correctly it's actually using pyenv to manage the version. I'm too lazy to check.
[^2]: Also thanks to [Jeff Triplett](https://jefftriplett.com) who got me into direnv for directory based environment variables a while ago.
[^3]: To be fair, at the time of writing the version I was trying to use was less than 24 hours old so things may not have been updated yet. I just tried again before releasing this and the problem has been fixed.

[2889-0001]: https://brew.sh/ "The Missing Package Manager for macOS (or Linux) — Homebrew"
[2889-0002]: https://direnv.net/ "direnv – unclutter your .profile - direnv"
[2889-0003]: https://www.zsh.org/ "Zsh"
[2889-0004]: https://ohmyz.sh/ "Oh My Zsh - a delightful & open source framework for Zsh"
[2889-0005]: https://github.com/danhper/asdf-python "GitHub - danhper/asdf-python"
[6937-0001]: https://pythonbytes.fm/episodes/show/249/all-of-linux-as-a-python-api
[6937-0002]: https://asdf-vm.com/ "Home - asdf"
