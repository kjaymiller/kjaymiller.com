---
title: pgvectorscale is easy to add onto pgvector
date: 2025-05-27T17:12:53
---

I was surprised how easy it was to include [pgvectorscale](https://github.com/timescale/pgvectorscale) to your instance.

In order to add to my multi-collection AI app. It was three lines.

```sql
CREATE EXTENSION IF NOT EXISTS vectorscale CASCADE;
CREATE INDEX document_embedding_idx ON document_embedding
USING diskann (embedding vector_cosine_ops);
```
