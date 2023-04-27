---
title: Create a Custom Query in the GitHub Issues Client
date: 2023-04-26 17:04:00-07:00

tags: [github, vscode, extensions, TIL]
---

Did you know that you can create a custom query for your GitHub issues and PRs?

The _GitHub Issues and Pull Requests extension_ allows you to interact with issues and PRs. While hovering over the "My Issues" label I noticed an edit marker with "Edit Query" in the tooltip.

![GitHub Issues and Pull Requests](https://kjaymiller.azureedge.net/media/GitHub%20Issues%20and%20Pull%20Requests.png)

When I clicked the icon, I noticed there was a list of queries that matched the entries. I figured I could create a custom entry so I did one for my current milestone.

```json
"githubIssues.queries" : [
    {
      "label": "Milestone",
      "query": "milestone:2023.5.x state:open repo:${owner}/${repository} sort:created-desc"
    }
    ... # The other queries
]
```

After entering the query, I immediately saw a new panel labelled _Milestone_ with all the issues in that milestone.

<video style="max-width: 100%;" src="https://kjaymiller.azureedge.net/media/Enable%20Github%20Issues%20and%20Pull%20Requests.mp4" controls>Enabling Github Issues and Pull Requests</video>
