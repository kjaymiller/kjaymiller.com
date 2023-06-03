---
title: Render Engine Update June 2023 Patch
tags: [render-engine]
date: 2023-06-01 10:07:00-07:00
---

Here are the changes available in `render-engine 2023.6.1`

## [REMOVED]:

### BlogPost PageObject:
There is no difference between the BlogPost Page Object and the Standard Page Object. All of the Blog like logic exists in the Blog Collection Object. This simplifies design and reduces the number of object types that Custom Object Builders need to choose from.

## [CHANGED]:

### `site._route_list` reverted to `site.route_list`
Made `site.route_list` public again and is now the main way that pages are access outside of their creation.

This sets the standard that if you need to reference an object. You can find the instance that will build the html file in the site's route list. This removes the need to call `site.page` or `site.collection` outside of the decorator.

```python
site = Site()

# previously to access Page1 in your build you had to call `site.page(Page1)` or create an out-of-site instance of the page.
# class Page1(Page):  
#    pass
#
# out_of_site_page =  site.page(Page1)

# now you can access the page instance from the route list
@site.page
class Page1(Page):
    pass

@site.page
class PageCallingPage1Instance(Page):
    page1 = site.route_list['page1']
```

### Methods `site.page()` and `site.collection()` now return `None`

To reinforce how to access instances of pages and collections.

### Registering Plugins for Pages and Collections happen when `Site.collection()` and `Site.page()` is called _(previously from `Collection.__init__()` and `Page.__init__()`)_

This creates a little more consistency in how plugins operate as referenced.

### `render_content` hookspec is called in `site.render()` for Page objects and `site.render_partial_collection`/`site.render_full_collection` for collection objects.

**SIDE EFFECT**: If you are calling the content from one page into another the `render_content` hookspec is not called. This should be fixed in future updates (perhaps with an extension to render pages as partials) 

**SIDE EFFECT**: `render_content` is now called on parsed content and not preparsed content. This means that you are looking for the rendered html and not the pre-existing content. This ensures that plugin developers don't need to think about the content's base type and instead can focus on the ensured HTML-formatted string.

**TODO**: Move the logic of page creation from site objects simple to a `site.render_page()` method that is called by all pages written to file.
