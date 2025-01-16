---
date: 2023-03-28 22:36:00-07:00
description: I recently learned a crucial lesson setting up testing for my Postgres
  Django app - and you can too. Here's how I did it.
tags: gh-actions
title: Lesson Learned from Setting Up Testing for a Postgres Django App (Crash Course)
---

> NOTE:  This is a quick write... I'll probably come back and edit it later.
## Quick Steps

1. Use the base from <https://docs.github.com/en/actions/using-containerized-services/creating-postgresql-service-containers>.
2. Swap the node stuff for python stuff.
3. Set default info for your postgres connection. _Don't worry you aren't loading any data other than the test data and you aren't connecting to anything in production. You can also set these as repo secrets (That's probably the best way to do it)_
4. Configure the python app to install requirements, apply migrations, and run the test

## Why Do This

My project runs in containers which means that sometimes development may mean that I'm operating without a connection to the database. It's nice to be able to run GitHub Actions and let it build an image and test for me using a postgres DB.

## Where to Find an Example

The relecloud repo: <https://github.com/Azure-Samples/azure-django-postgres-aca/>

## Considerations

I don't know how much this costs in resources but I don't think it would be too bad.

Another consideration is that I'm not using my actual docker image to test which means configurations may need to be maintained in multiple places. You can use your image but it will need to be hosted in DockerHub.
