# justfile for kjaymiller.com static site generator
# Built with render-engine and PostgreSQL

set shell := ["zsh", "-cu"]

# Default target - show help
default:
    @just --list

# Install dependencies using uv
install:
    uv sync

upgrade:
    uv sync --upgrade --prerelease=allow

# Build the static site
build:
    uv run --no-dev --prerelease=allow render-engine build

# Start development server with live reload
serve:
    uv run --no-dev --prerelease=allow render-engine serve

# Create a new blog entry
new-entry collection:
    uv run --no-dev --prerelease=allow render-engine new-entry {{ collection }}

tui:
    uv run --no-dev --prerelease=allow render-engine-tui

publish:
    gh workflow run Publish

# generate read and insert queries
gen-queries:
    uv run --no-dev --prerelease=allow render-engine-pg  schema.sql

# Build the database schema (PostgreSQL)
build-schema:
    @echo "Building PostgreSQL schema..."
    psql $CONNECTION_STRING -f schema.sql

# Populate database from markdown files
populate-db BLOG CONTENT:
    uv run python populate_db.py {{BLOG}} {{CONTENT}} --ignore-pk

# Truncate blog tables (blog, tags, blog_tags)
truncate-blog:
    psql $CONNECTION_STRING -c "TRUNCATE TABLE blog_tags, blog, tags CASCADE;"

# Run pre-commit checks
pre-commit:
    uv run pre-commit run --all-files

# Clean build artifacts
clean:
    rm -rf output/
    rm -rf build/
