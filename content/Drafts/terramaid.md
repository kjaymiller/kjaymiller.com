---
title: Visualizing Terraform using Mermaidjs with Terramaid
date: 2025-03-21 13:46:00.342848+00:00
description: Terraform graph is cool but I prefer mermaid and this tool helps with that!
---

Working on a blog post at work and wanted to diagram my terraform post.

Terraform has `terraform graph` which makes a GraphViz - <https://developer.hashicorp.com/terraform/cli/commands/graph#generating-images>

2. My dev world has standardized on mermaid which there is a request for support - <https://github.com/hashicorp/terraform/issues/30519>
   a. It's been two years with this request open...
   b. I wonder if OpenTofu will support this.
   c. OpenTofu's issue template gave me anxiety and didn't add the issue.

![OpenTofu's issue template]

The tf issue suggested using terramaid and I'm happy to say... **IT JUST WORKS**

1. Install Terramaid (On MacOS):

```shell
brew install terramaid
```

2. navigate to the terraform folder
3. run `terramaid run`

## Complaints

You get terraform but it feels backwards in it's breakdown
