---
date: 2025-10-25 13:54:13.020335
slug: swapping-from-ssh-to-https-and-back-in-git
title: swapping from ssh to https (and back) in git
---

According to Claude:

Yes, you can change Git's protocol from SSH to HTTPS (or vice versa). Here are the main ways to do it:

**For a specific repository:**

If you have a repository cloned with SSH and want to switch to HTTPS, you can change the remote URL:

```bash
git remote set-url origin https://github.com/username/repo.git
```

To verify the change worked:
```bash
git remote -v
```

**For all repositories globally:**

You can configure Git to automatically use HTTPS for all GitHub (or other Git hosting) URLs:

```bash
git config --global url."https://github.com/".insteadOf git://github.com/
```

This tells Git to replace `git://` protocol with HTTPS.

**If you're switching from SSH to HTTPS:**

```bash
git config --global url."https://github.com/".insteadOf ssh://git@github.com/
```

**To check your current configuration:**

```bash
git config --list
```

This will show all your Git settings, including any URL rewrites.

**Note:** When using HTTPS, you may be prompted for credentials (username/password or a personal access token). If you want to avoid entering credentials repeatedly, you can:
- Use a personal access token instead of a password
- Configure Git credential caching with `git config --global credential.helper cache`
- Or on macOS, use `osxkeychain` as the credential helper

Is there a specific Git hosting service you're working with, or are you trying to solve a particular issue with your current setup?

## And switching back

To switch back from HTTPS to SSH:

**For a specific repository:**

```bash
git remote set-url origin git@github.com:username/repo.git
```

Verify the change:
```bash
git remote -v
```

**For all repositories globally (undo the config):**

If you set a global URL rewrite to use HTTPS, you can remove it:

```bash
git config --global --unset url."https://github.com/".insteadOf
```

Or if you had configured it the other way:

```bash
git config --global --unset url."https://github.com/".insteadOf ssh://git@github.com/
```

**To view and manually edit all global configs:**

```bash
git config --global --list
```

This shows all your global settings, so you can identify any URL rewrites you've set up.

**Note:** When using SSH, make sure you have your SSH keys set up properly and added to your SSH agent:

```bash
ssh-add ~/.ssh/id_rsa
```

You can test your SSH connection with:

```bash
ssh -T git@github.com
```
