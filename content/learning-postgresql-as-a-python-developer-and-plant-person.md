---
date: 2025-09-11 10:07:00
title: Mistakes In Learning PostgreSQL as a Python Developer (and Plant Person)
tags: ["postgresql"]
description: "A reflection on common mistakes made while learning PostgreSQL as a non-traditional database developer, including schema design pitfalls and overconfidence from ORM usage that masked fundamental knowledge gaps."
---

On September 9th, I spoke (virtually) at the [San Francisco Bay Area PostgreSQL User Group][sf pug]. My presentation was packed with a lot of history for me. Trying to learn more about PostgreSQL has been challenging and here's why.

- I'm not a software engineer
- I'm not a DBA

These two things mean that if I'm learning about something, I'm likely building it. For good reason, I can't just poke around the Aiven PostgreSQL servers.

I'm also a massive fan of static sites which means that I'm not hosting and building a lot of databases _just 'cause_.

I made a [list of database projects](./postgresql-project-ideas-for-beginners.html) that you could build. One of them was my [plant-tracker]. This Django app has been a fun but challenging situation for me. My goal was to let AI handle as much of the Python development as possible while I serve as the DBA.

Not a lot is happening in my little database, but I still made the mistakes and I want to talk about them.

## Mistake 1 - I didn't do a full on design

Designing your schema is challenging as a solo dev because it is extremely hard to bounce from developer, designer, and dba.

If you are like me, you skip the designing. You build base functionality, you build your schema based on that functionality, you design based on that functionality, then you iterate.

In this pattern you keep altering and altering. This can build muscle memory but it's only going to give you so much. You also run the risk of developing your schema or your codebase into a corner.

While I was at PGDataDay Chicago, I sat in [Lætitia Avrot's](https://www.linkedin.com/in/l%C3%A6titia-avrot/) workshop on the "Merise" modeling methodology. That said, I was eager to get started and began building tables based on what I had in mind for this app. I trusted claude code to blindly start building a tracker based on my DB's schema.

This blind trust in building [^1] was important because I wanted a realistic experience for the DBAs that would normally not be consulted on the application itself. This worked fine but ultimately found myself altering the database more than I wanted to.


## Mistake 2 - I knew less than I thought I did and I blame ORMs

This isn't meant to be an _ORMs are bad_ section. Object Relational Mappers (ORMs) are designed to interact with your database in your preferred language. This is great, however much of the work you do with an ORM is initial table management and queries that won't change very much.

There is a difference in interacting with your PostgreSQL data, and understanding your PostgreSQL ecosystem.

As a web developer, I spend a lot of time in the former. Much of my LLM queries were questions looked similar to "Is it better to use direct queries or build views?". Of course the answer is _it depends_ and I knew that. What I didn't know was the context required to make the best decision.

## Conclusions

When I think of PostgreSQL, the ceiling and floor feel incredibly vast. If you are building things and you don't want to think about PG outside of how your app adds and retrieves data, you can likely do so for a long time with no trouble.

If you want to optimize your work load, you can likely do so. If you want to optimize your database to work beyond the singular app experience, you have countless things you can do but also need to understand that you can accomplish this overtime, learning as you go. Best thing you can do, whether building your app or database, is make a plan and try to think about your development before you start building.


[sf pug]: https://www.meetup.com/postgresql-1/
[plant-tracker]: https://github.com/kjaymiller/plant-tracker

[^1]: My prompt did instruct them to use Python, UV, Django, and HTMX
