---
title: SubCollections now available in Render Engine
date: 01 Jul 2020 14:43
category: Render Engine
tags: update
image: https://s3-us-west-2.amazonaws.com/kjaymiller/images/render-engine-subcollections.png
---

**Version Update: 2020.07.02**
I'm happy to announce that subcollections are now supported in render_engine

![subcollection-code](https://s3-us-west-2.amazonaws.com/kjaymiller/images/render-engine-subcollections.png)

**SubCollections** create a new collection from pages that has the specified value. SubCollections are of the same type as their parent so if you are using a `Blog` object , you will get access to feeds natively for each SubCollection.

### Other Minor Updates Include

- access to all collections and subcollections throughout the entire site template - e.g. `{% for page in collections['blog'].pages %}` or `{{subcollections['category']}}`
