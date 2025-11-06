--
-- PostgreSQL Index Optimization for Content Editor TUI
-- Adds missing indexes for search and join operations
--
-- These indexes optimize the following queries:
-- - Search queries using ILIKE on title/content
-- - Tag filtering and counting (junction table joins)
-- - Pagination with ORDER BY date
--

-- Blog table: Add indexes on searchable text columns
-- These help with the search WHERE clause: WHERE title ILIKE %s OR slug ILIKE %s OR content ILIKE %s
CREATE INDEX IF NOT EXISTS idx_blog_title ON public.blog (title);
CREATE INDEX IF NOT EXISTS idx_blog_content ON public.blog (content);

-- Notes table: Add indexes on searchable text columns
CREATE INDEX IF NOT EXISTS idx_notes_title ON public.notes (title);
CREATE INDEX IF NOT EXISTS idx_notes_content ON public.notes (content);

-- Microblog table: Add index on content for search
CREATE INDEX IF NOT EXISTS idx_microblog_content ON public.microblog (content);

-- Junction table indexes: Speed up tag filtering and counts
-- These are crucial for:
-- - get_tag_post_count(): Counts posts per tag via the junction table
-- - get_posts_by_tag(): Filters posts by tag
-- - get_all_tags_with_counts(): Large JOIN with COUNT
-- Without these, every tag query does a full table scan of the junction table
CREATE INDEX IF NOT EXISTS idx_blog_tags_tag_id ON public.blog_tags (tag_id);
CREATE INDEX IF NOT EXISTS idx_blog_tags_blog_id ON public.blog_tags (blog_id);
CREATE INDEX IF NOT EXISTS idx_notes_tags_tag_id ON public.notes_tags (tag_id);
CREATE INDEX IF NOT EXISTS idx_notes_tags_notes_id ON public.notes_tags (notes_id);
CREATE INDEX IF NOT EXISTS idx_microblog_tags_tag_id ON public.microblog_tags (tag_id);
CREATE INDEX IF NOT EXISTS idx_microblog_tags_microblog_id ON public.microblog_tags (microblog_id);

-- Update query planner statistics
-- Run ANALYZE after adding indexes so the query planner knows about them
ANALYZE public.blog;
ANALYZE public.notes;
ANALYZE public.microblog;
ANALYZE public.tags;
ANALYZE public.blog_tags;
ANALYZE public.notes_tags;
ANALYZE public.microblog_tags;
