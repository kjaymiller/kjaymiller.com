---
date: 2023-04-16 13:09:00-07:00
series: Render Engine DevLog
tags:
- render-engine
- devlog
title: Breaking Changes Around Date Handling
---

In our push to reduce the complexity of the system prior to our "1.0" stable release. I've made the decision to reduce the number of mandatory attributes reduce confusion in what is required and what isn't.

Over the last week of thought one of the areas this is most obvious is around date handling.

There were two breaking changes introduced in the 2024.2.1a2 update. Both of these changes are only focused around the `Blog` Collection Type object.

### removal of `date_published` and `date_modified` in favor of `date`

In previous versions, `Blog` objects required a `date_published` and had code for handling both `date_published`/`date_modified`. We've changed this to just `date`.

####  Before

>
> ```yaml
> ---
> title: my page title
> date_published: 16 Apr 2023 13:31 -07:00
> # date_modified: 16 Apr 2023 14:31 -07:00 # date_modified is optional but built-in logic is looking for it.
> ---
> ```

#### After

> ```yaml
> # example.md
> ---
> title: my page title
> date: 2023-04-16 13:31 -07:00
> # date_modified can exist but no built-in logic for it exists
> ---
> ```
>
Originally we wanted to distinguish between the date the object was created and if any updates were made. However there is no standardized way of specifying this.

Render Engine has a liberal approach to how custom attributes are handled and we can do that because we only work to modify code that is required. The custom code that was introduced was designed to handle inconsistencies with naming. There was much concern in detecting the right values and making them consistent behind the scenes. Changing `date_published` to `date` and removing `date_modified` removes the need for correcting naming.

### Better handling of `datetime` objects by forcing iso8691 format

Render Engine heavily relies on [python-frontmatter](https://pypi.org/project/python-frontmatter/). Frontmatter uses PyYaml to handle many parsing features including parsing iso8601 to `date` or `datetime` formatting based on what information is provided.

Since the beginning there was a lot of concern on how to detect and parse datetime objects. This included looking for optional attributes. These implementations were always inconsistent and even led to issues with parsing values and slowing down build-times.

Date-based aggregation is common. For this reason, it benefits us to let that datetime parsing of PyYAML to handle all file-based `datetime` assignments and we can leverage pythons built-in `datetime` parsing. This creates consistency on detection of `datetime` values that were already being detected. Making for clearer documentation and less custom code.

#### Before

> ```yaml
> # example.md
> ---
> title: my page title
> date: 16 Apr 2023 13:31
> ---

#### After
>
> ```yaml
> # example.md
> ---
> title: my page title
> date: 2023-04-16 13:31 -07:00
> ---

This opens the door for people to add custom dates and provide a simple way to standardize on all datetime objects using the new `{{format_datetime}}` jinja2 custom filter provided and the `site_var['DATETIME_FORMAT']`

## The decision not to deprecate

We are being aggressive in our development as we get closer to our most stable release. The deprecation would require us to add more code to handle all three values in multiple areas as well as pass the burden onto extensions such as `render-engine-microblog`. It's better to make a clean break while we can.

## Concerns

There is always an issue when dealing with time-zone naive or aware dates. I've create [a gist that will look for some common date-attributes and convert them to iso8601 format](https://gist.github.com/kjaymiller/83175df30291c885508ffa1129ee85c4)

## Future Removals

The hope is that if breaking changes are required they can be documented with steps to remediate any issues caused by it.
