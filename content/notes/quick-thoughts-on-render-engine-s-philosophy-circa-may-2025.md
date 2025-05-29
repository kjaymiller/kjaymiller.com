---
date: 2025-05-29 07:42:05
description: Just shared my thoughts on Render Engine's core philosophy and why I
  built it the way I did. From Django-inspired class-based objects to plugin autonomy,
  these architectural decisions shape everything we do.
tags:
- render-engine
- python
- development
- community
- static-site-generator
- projects
title: Quick Thoughts on Render Engine's Philosophy (circa May 2025)
---

In our [discord](https://discord.gg/2xMQ4j4d8m) we had a wonderful question about Render Engine's Philosophy.

Reminder that Render Engine started as a way for me to learn Python on the job so there are places where this philosophy is inconsistent with how and where code lives but we're
working to make it more consistent.

Here are some notes from that chat.

## Core philosophy

The framework architecture is maintained with three foundational principles that guide all architectural decisions:

### 1. Ease of contribution

Since Render Engine is not anyone's full-time job, the codebase prioritizes simplicity and clarity to enable community contributions while minimizing maintenance overhead.

Since is was meant to be a way to learn we also hope that it can be a place where people new to contributing to open source can begin their OSS journey. We prioritize readability
over micro-performance optimizations.

#### Where we need to improve

This also means that comments that explain the why's (not the what's) should exist.

### 2. Separation of concerns based on interaction points

Components are organized around where and how they interact with the system, creating clear boundaries and responsibilities. More on this later.

All of the foundational components of Render Engine live in the primary repo - [render-engine/render-engine](https://github.com/render-engine/render-engine) with the one exception being parsers.
There is a render-engine-parser repo and that is because the parsers **can** be used independently from Render Engine itself (Perhaps you want an easy way to convert data from one
type to HTML).

This separation of concerns is meant to keep the core lightweight and help with [Extensibility](#3-extensibility). A great example is with `render-engine init`. With our template
being in a separate repo and served via cookiecutter, this allows you to easily swap the default base template with your own, if you have your own preference in what you want in
your site.

### 3. Extensibility

The framework is designed to be highly extensible through a plugin and theme system that allows for controlled customization.

Render-Engine uses pluggy (the same system used in tools like PyTest and django-simple-deploy). This allows for great extensibility that can be brought into projects without our
involvement. We want you to be able to extend Render Engine for your needs without our interceding.

## Architectural influences

### Django inspiration

Render Engine draws heavily from Django in two key areas:

- **Class-Based Objects**: Each generated page is treated as an object that can be modified, inspired by Django's Class-Based Views. Collections and Sites are also classes that
  can be modified and managed as independent objects. This means that you should (in theory) Create multiple websites with similar components and have them look similar but
  different based on configurations and settings
- **Component Registration**: The extensibility system uses Django's approach to registering components, enabling multi-site management with controlled access to plugins, themes,
  and settings per site from a single configuration file. This means that your extensibility is by choice and there are no surprises that come from installed packages.

### Flask philosophy

Like Flask, Render Engine tries to avoid a "batteries-included". This supports the core principles of ease of contribution and separation of concerns.

## Core Components

The Render Engine architecture consists of four primary components, each with distinct responsibilities:

### Parser

**Responsibility**: Converting data from one format to output markup language (usually HTML)

Parsers handle the transformation of content from various input formats into the final rendered output.

### Page

**Responsibility**: Rendering a single page object

Pages represent individual content items and manage their own customization to the rendering process, including which plugins, templates, and parsers they utilize.

### Collection

**Responsibility**: Rendering multiple page objects with shared base configuration

Collections manage groups of related pages that share common settings and rendering rules.

### Site

**Responsibility**: Managing the overall rendering process for Pages & Collections

The Site component orchestrates the entire rendering workflow and maintains the registry of available plugins and themes with their default settings. While the Site manages what's available, individual Pages and Collections determine what they actually use.

## Design Principles in Practice

### Component Autonomy

Pages and Collections have autonomy in choosing:

- Which plugins to use
- Which templates to apply
- Which parsers to employ
- Individual settings for parsers and plugins

This autonomy operates within the framework provided by the Site's available resources.

This modular, principle-driven approach ensures Render Engine remains both accessible to contributors and powerful enough for complex static site generation needs.
