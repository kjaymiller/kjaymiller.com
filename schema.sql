-- Enable PostGIS extension
CREATE EXTENSION IF NOT EXISTS postgis;

-- Tags table (shared between blog and microblog)
CREATE TABLE IF NOT EXISTS tags (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Blog posts table
-- @collection
CREATE TABLE IF NOT EXISTS blog (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(255) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    description TEXT,
    external_link VARCHAR(500),
    image_url VARCHAR(500),
    date TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Blog to tags relationship
-- @junction
CREATE TABLE IF NOT EXISTS blog_tags (
    blog_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (blog_id, tag_id),
    FOREIGN KEY (blog_id) REFERENCES blog(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

-- Microblog posts table (no title, no description)
-- @collection
CREATE TABLE IF NOT EXISTS microblog (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(255) UNIQUE NOT NULL,
    content TEXT NOT NULL,
    external_link VARCHAR(500),
    image_url VARCHAR(500),
    date TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Microblog to tags relationship
-- @junction
CREATE TABLE IF NOT EXISTS microblog_tags (
    microblog_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (microblog_id, tag_id),
    FOREIGN KEY (microblog_id) REFERENCES microblog(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

-- Notes table (similar to blog but for /notes collection)
-- @collection
CREATE TABLE IF NOT EXISTS notes (
    id SERIAL PRIMARY KEY,
    slug VARCHAR(255) UNIQUE NOT NULL,
    title VARCHAR(255) NOT NULL,
    content TEXT NOT NULL,
    description TEXT,
    external_link VARCHAR(500),
    image_url VARCHAR(500),
    date TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Notes to tags relationship
-- @junction
CREATE TABLE IF NOT EXISTS notes_tags (
    notes_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (notes_id, tag_id),
    FOREIGN KEY (notes_id) REFERENCES notes(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

-- Conferences table (with PostGIS support)
-- @page
CREATE TABLE IF NOT EXISTS conferences (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    date TIMESTAMP NOT NULL,
    location VARCHAR(255),
    location_geom GEOGRAPHY(POINT, 4326),
    url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for better query performance
CREATE INDEX IF NOT EXISTS idx_blog_slug ON blog(slug);
CREATE INDEX IF NOT EXISTS idx_blog_date ON blog(date);
CREATE INDEX IF NOT EXISTS idx_microblog_slug ON microblog(slug);
CREATE INDEX IF NOT EXISTS idx_microblog_date ON microblog(date);
CREATE INDEX IF NOT EXISTS idx_notes_slug ON notes(slug);
CREATE INDEX IF NOT EXISTS idx_notes_date ON notes(date);
CREATE INDEX IF NOT EXISTS idx_tags_name ON tags(name);
CREATE INDEX IF NOT EXISTS idx_conferences_location ON conferences USING GIST(location_geom);
