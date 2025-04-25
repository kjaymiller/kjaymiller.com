---
category: code
date: 2021-03-24 20:21:00
description: 'I recently rediscovered a simple yet often-overlooked method for securing
  my online presence: using CertBot with NGINX. Here''s how I do it.'
tags:
- certbox
- nginx
title: How to enable certs with CertBot and NGINX
---

I always forget this so I'm adding it to my website instead of my notes (since I apparently don't check those.[^1])

`sudo certbot --nginx -d your_domain -d www.your_domain`

[^1]: I also added it to my archive in Drafts (it was in the inbox with 800 other items)
