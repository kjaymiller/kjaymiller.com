---
date: 2025-05-28 17:12:53
description: I just learned the hard way that pgvectorscale needs explicit vector
  dimensions, even when it claims to support 16k. Three lines to add the extension,
  but forgetting `vector(768)` cost me my entire index.
tags:
- postgresql
- ai
- TIL
- development
- code
title: pgvectorscale is easy to add onto pgvector
---

I was surprised how easy it was to include [pgvectorscale](https://github.com/timescale/pgvectorscale) to your instance.

In order to add to my multi-collection AI app. It was three lines.

```sql
CREATE EXTENSION IF NOT EXISTS vectorscale CASCADE;
CREATE INDEX document_embedding_idx ON document_embedding
USING diskann (embedding vector_cosine_ops);
```

That is unless you do what I did and didn't hard specify your embedding limit in your vector data type.

My original setup

```sql
-- CREATE EXTENSION IF NOT EXISTS vector;
CREATE TABLE QuoteEmbeddings (
    id SERIAL PRIMARY KEY,
    content_item_id INTEGER NOT NULL,
    content_snippet TEXT NOT NULL,
    embedding vector NOT NULL,
    CONSTRAINT fk_content_item
      FOREIGN KEY(content_item_id)
   REFERENCES ContentItem(id)
      ON DELETE CASCADE
);
```

This would produce `Too many dimensions to index (max is 16000)` regardless of the size of the dimensions.

My fix was to be explicit.

```sql
-- Table 2: QuoteEmbeddings
 CREATE TABLE QuoteEmbeddings (
     id SERIAL PRIMARY KEY,
     content_item_id INTEGER NOT NULL,
     content_snippet TEXT NOT NULL,
     embedding vector(768) NOT NULL, -- NOTE the (768)
     CONSTRAINT fk_content_item
       FOREIGN KEY(content_item_id)
       REFERENCES ContentItem(id)
       ON DELETE CASCADE
 );
```

Too bad i realized that after I dropped all my tables and will need to reindex them.
