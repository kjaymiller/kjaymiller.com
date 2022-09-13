---
title: DiversityOrgs.Tech (Beta 2)
date: 29 June 2022
tags: diversity, azure, technology
---



> **TLDR**: 
> The latest update to Diversityorgs.Tech returns to the original URL and brings more information to each organization, map-based searching, and organizer access to keep organizations up to date, and a basic API for programmatic access.

Two years ago, I started working on [Diversityorgs.Tech](https://diversityorgs.tech) as a project to learn new tools and create a resource for underrepresented folks in tech everywhere. Today I'm happy to announce some amazing new features thanks to the entire project being rebuilt using [Django 4](https://djangoproject.org).

Let’s start with exploring some of the new features.

## Map Based Searching:

![Map showing locations for Black Girls Code](https://jmblogstorrage.blob.core.windows.net/media/bgh-map.png)  

It’s good to know what’s in your area. Not only are we indexing city-level locations of these orgs, but you can now find them on a map. Pages with organizations in different locations will present a map so you can view the results in that area. This is powered by Azure Maps for geocoding, and map display.

## Focused Searching and Filtering
We’ve all had the painful experience of looking for similar results and the service you’re using forces you to reapply all the previous settings manually. For Example, you are looking at PyLadies Atlanta and you want more groups focused on women. You select the women tag and the site will first return orgs in Atlanta with the same tag. On that page there is an option to expand to all orgs with that tag or that location.

![Select a Diversity Focus will lead to more results with the same focus in the same location](https://jmblogstorrage.blob.core.windows.net/media/pyladies-atl-tags.png)
 
## Better Organization Management
One of the biggest barriers to further development previously was that it was very impractical to add/update content. I’ve added two new features to make organization management easier.

First, organizers can create an account and request moderator rights to an org. Once reviewed and approved, they can make updates to their org’s location, links, logo and more.

Second, anyone can suggest changes to an organization. These changes will be reviewed, and updates can be made by organizers or administrators
 
![The Suggest Edit link allow for access to request updates to the view](https://jmblogstorrage.blob.core.windows.net/media/suggests-update.png)
 

## Learn More Than Just a Name
Joining an organization as a member is one of the first steps in getting more involved in the developer community. That said many of those foundational experiences can impact future decisions. This site highlights important things like having a publicly available code of conduct.

![An organization page will show if it has a public link to the code of conduct](https://jmblogstorrage.blob.core.windows.net/media/suggests-update.png) 

Speaking of good intentions, we’ve also added the ability to report any organization for removal by ANYONE. Each report is taken seriously and investigated.

## The API
The REST API is generally available in limited scope with more endpoints available with an API Key. The hope is organizations and municipalities can use the data collected.
 
![API results of orgs in Atlanta](https://jmblogstorrage.blob.core.windows.net/media/api-atl.png) 

Organizers can even manage the organizations they are responsible for providing easy updates and automation.

## Information Freedom and Data Privacy
This site aims to ensure that folks find helpful information to determine if an organization is right for them. All information for each organization is available for free with no need to create an account unless you are an organizer. The site doesn’t collect or sell personal identifying data nor share information with organizations.

Simply put, your data is just that, **YOURS**.

I’ll be working with my team at Microsoft to highlight some of the specifics of deploying and maintaining this app in the Azure ecosystem. You'll be able to see those posts in the future on the [Microsoft Azure Dev.To Channel](https://dev.to/azure).


This was a big undertaking that took much of the last few months to get to this point. There are likely bugs and some of the interfaces will undergo some changes. If you spot an issue, please let me know by submitting an issue over on the GitHub Repo. Lastly, this project is open-source project and accepting contributions from folks at all skill-levels.
I hope that you'll enjoy using Diversityorgs.Tech and that you point underrepresented folks to this as a resource in their tech career at all stages.
