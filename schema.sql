--
-- PostgreSQL database dump
--

\restrict UTd3hReNLdHRCO3mBfvVYu3DKQ7yrpEhu86nim8ZnWzA6r7JgwFgD8ppKLSP3fH

-- Dumped from database version 18.0
-- Dumped by pg_dump version 18.0 (Debian 18.0-1.pgdg13+3)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: unaccent; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS unaccent WITH SCHEMA public;


--
-- Name: EXTENSION unaccent; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION unaccent IS 'text search dictionary that removes accents';


--
-- Name: set_slug(); Type: FUNCTION; Schema: public; Owner: avnadmin
--

CREATE FUNCTION public.set_slug() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN
  IF NEW.slug IS NULL OR NEW.slug = '' THEN
    NEW.slug := slugify(NEW.title);
  END IF;
  RETURN NEW;
END
$$;


ALTER FUNCTION public.set_slug() OWNER TO avnadmin;

--
-- Name: slugify(text); Type: FUNCTION; Schema: public; Owner: avnadmin
--

CREATE FUNCTION public.slugify(value text) RETURNS text
    LANGUAGE plpgsql IMMUTABLE STRICT
    AS $_$
BEGIN
  RETURN regexp_replace(
           regexp_replace(
             lower(unaccent("value")), -- Lowercase and remove accents in one step
             '[^a-z0-9\\-_]+', '-', 'gi' -- Replace non-alphanumeric characters with hyphens
           ),
           '(^-+|-+$)', '', 'g' -- Remove leading and trailing hyphens
         );
END
$_$;


ALTER FUNCTION public.slugify(value text) OWNER TO avnadmin;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: blog; Type: TABLE; Schema: public; Owner: avnadmin
--

CREATE TABLE public.blog (
    id integer NOT NULL,
    slug character varying(255) NOT NULL,
    title character varying(255) NOT NULL,
    content text NOT NULL,
    description text,
    external_link character varying(500),
    image_url character varying(500),
    date timestamp without time zone NOT NULL
);


ALTER TABLE public.blog OWNER TO avnadmin;

--
-- Name: blog_id_seq; Type: SEQUENCE; Schema: public; Owner: avnadmin
--

CREATE SEQUENCE public.blog_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.blog_id_seq OWNER TO avnadmin;

--
-- Name: blog_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: avnadmin
--

ALTER SEQUENCE public.blog_id_seq OWNED BY public.blog.id;


--
-- Name: blog_tags; Type: TABLE; Schema: public; Owner: avnadmin
--

CREATE TABLE public.blog_tags (
    blog_id integer NOT NULL,
    tag_id integer NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.blog_tags OWNER TO avnadmin;

--
-- Name: conferences; Type: TABLE; Schema: public; Owner: avnadmin
--

CREATE TABLE public.conferences (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    date timestamp without time zone NOT NULL,
    location character varying(255),
    latitude numeric(10,8),
    longitude numeric(11,8),
    url character varying(500),
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.conferences OWNER TO avnadmin;

--
-- Name: conferences_id_seq; Type: SEQUENCE; Schema: public; Owner: avnadmin
--

CREATE SEQUENCE public.conferences_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.conferences_id_seq OWNER TO avnadmin;

--
-- Name: conferences_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: avnadmin
--

ALTER SEQUENCE public.conferences_id_seq OWNED BY public.conferences.id;


--
-- Name: microblog; Type: TABLE; Schema: public; Owner: avnadmin
--

CREATE TABLE public.microblog (
    id integer NOT NULL,
    slug character varying(255) NOT NULL,
    content text NOT NULL,
    external_link character varying(500),
    image_url character varying(500),
    date timestamp without time zone NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.microblog OWNER TO avnadmin;

--
-- Name: microblog_id_seq; Type: SEQUENCE; Schema: public; Owner: avnadmin
--

CREATE SEQUENCE public.microblog_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.microblog_id_seq OWNER TO avnadmin;

--
-- Name: microblog_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: avnadmin
--

ALTER SEQUENCE public.microblog_id_seq OWNED BY public.microblog.id;


--
-- Name: microblog_tags; Type: TABLE; Schema: public; Owner: avnadmin
--

CREATE TABLE public.microblog_tags (
    microblog_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE public.microblog_tags OWNER TO avnadmin;

--
-- Name: notes; Type: TABLE; Schema: public; Owner: avnadmin
--

CREATE TABLE public.notes (
    id integer NOT NULL,
    slug character varying(255) NOT NULL,
    title character varying(255) NOT NULL,
    content text NOT NULL,
    description text,
    external_link character varying(500),
    image_url character varying(500),
    date timestamp without time zone NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.notes OWNER TO avnadmin;

--
-- Name: notes_id_seq; Type: SEQUENCE; Schema: public; Owner: avnadmin
--

CREATE SEQUENCE public.notes_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.notes_id_seq OWNER TO avnadmin;

--
-- Name: notes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: avnadmin
--

ALTER SEQUENCE public.notes_id_seq OWNED BY public.notes.id;


--
-- Name: notes_tags; Type: TABLE; Schema: public; Owner: avnadmin
--

CREATE TABLE public.notes_tags (
    notes_id integer NOT NULL,
    tag_id integer NOT NULL
);


ALTER TABLE public.notes_tags OWNER TO avnadmin;

--
-- Name: tags; Type: TABLE; Schema: public; Owner: avnadmin
--

CREATE TABLE public.tags (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    created_at timestamp without time zone DEFAULT CURRENT_TIMESTAMP
);


ALTER TABLE public.tags OWNER TO avnadmin;

--
-- Name: tags_id_seq; Type: SEQUENCE; Schema: public; Owner: avnadmin
--

CREATE SEQUENCE public.tags_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.tags_id_seq OWNER TO avnadmin;

--
-- Name: tags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: avnadmin
--

ALTER SEQUENCE public.tags_id_seq OWNED BY public.tags.id;


--
-- Name: blog id; Type: DEFAULT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.blog ALTER COLUMN id SET DEFAULT nextval('public.blog_id_seq'::regclass);


--
-- Name: conferences id; Type: DEFAULT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.conferences ALTER COLUMN id SET DEFAULT nextval('public.conferences_id_seq'::regclass);


--
-- Name: microblog id; Type: DEFAULT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.microblog ALTER COLUMN id SET DEFAULT nextval('public.microblog_id_seq'::regclass);


--
-- Name: notes id; Type: DEFAULT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.notes ALTER COLUMN id SET DEFAULT nextval('public.notes_id_seq'::regclass);


--
-- Name: tags id; Type: DEFAULT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.tags ALTER COLUMN id SET DEFAULT nextval('public.tags_id_seq'::regclass);


--
-- Name: blog blog_pkey; Type: CONSTRAINT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.blog
    ADD CONSTRAINT blog_pkey PRIMARY KEY (id);


--
-- Name: blog blog_slug_key; Type: CONSTRAINT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.blog
    ADD CONSTRAINT blog_slug_key UNIQUE (slug);


--
-- Name: blog_tags blog_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.blog_tags
    ADD CONSTRAINT blog_tags_pkey PRIMARY KEY (blog_id, tag_id);


--
-- Name: conferences conferences_pkey; Type: CONSTRAINT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.conferences
    ADD CONSTRAINT conferences_pkey PRIMARY KEY (id);


--
-- Name: microblog microblog_pkey; Type: CONSTRAINT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.microblog
    ADD CONSTRAINT microblog_pkey PRIMARY KEY (id);


--
-- Name: microblog microblog_slug_key; Type: CONSTRAINT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.microblog
    ADD CONSTRAINT microblog_slug_key UNIQUE (slug);


--
-- Name: microblog_tags microblog_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.microblog_tags
    ADD CONSTRAINT microblog_tags_pkey PRIMARY KEY (microblog_id, tag_id);


--
-- Name: notes notes_pkey; Type: CONSTRAINT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.notes
    ADD CONSTRAINT notes_pkey PRIMARY KEY (id);


--
-- Name: notes notes_slug_key; Type: CONSTRAINT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.notes
    ADD CONSTRAINT notes_slug_key UNIQUE (slug);


--
-- Name: notes_tags notes_tags_pkey; Type: CONSTRAINT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.notes_tags
    ADD CONSTRAINT notes_tags_pkey PRIMARY KEY (notes_id, tag_id);


--
-- Name: tags tags_name_key; Type: CONSTRAINT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_name_key UNIQUE (name);


--
-- Name: tags tags_pkey; Type: CONSTRAINT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.tags
    ADD CONSTRAINT tags_pkey PRIMARY KEY (id);


--
-- Name: idx_blog_date; Type: INDEX; Schema: public; Owner: avnadmin
--

CREATE INDEX idx_blog_date ON public.blog USING btree (date DESC);


--
-- Name: idx_blog_slug; Type: INDEX; Schema: public; Owner: avnadmin
--

CREATE INDEX idx_blog_slug ON public.blog USING btree (slug);


--
-- Name: idx_conferences_date; Type: INDEX; Schema: public; Owner: avnadmin
--

CREATE INDEX idx_conferences_date ON public.conferences USING btree (date);


--
-- Name: idx_microblog_date; Type: INDEX; Schema: public; Owner: avnadmin
--

CREATE INDEX idx_microblog_date ON public.microblog USING btree (date);


--
-- Name: idx_microblog_slug; Type: INDEX; Schema: public; Owner: avnadmin
--

CREATE INDEX idx_microblog_slug ON public.microblog USING btree (slug);


--
-- Name: idx_notes_date; Type: INDEX; Schema: public; Owner: avnadmin
--

CREATE INDEX idx_notes_date ON public.notes USING btree (date);


--
-- Name: idx_notes_slug; Type: INDEX; Schema: public; Owner: avnadmin
--

CREATE INDEX idx_notes_slug ON public.notes USING btree (slug);


--
-- Name: idx_tags_name; Type: INDEX; Schema: public; Owner: avnadmin
--

CREATE INDEX idx_tags_name ON public.tags USING btree (name);


--
-- Name: blog_tags blog_tags_blog_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.blog_tags
    ADD CONSTRAINT blog_tags_blog_id_fkey FOREIGN KEY (blog_id) REFERENCES public.blog(id) ON DELETE CASCADE;


--
-- Name: blog_tags blog_tags_tag_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.blog_tags
    ADD CONSTRAINT blog_tags_tag_id_fkey FOREIGN KEY (tag_id) REFERENCES public.tags(id) ON DELETE CASCADE;


--
-- Name: microblog_tags microblog_tags_microblog_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.microblog_tags
    ADD CONSTRAINT microblog_tags_microblog_id_fkey FOREIGN KEY (microblog_id) REFERENCES public.microblog(id) ON DELETE CASCADE;


--
-- Name: microblog_tags microblog_tags_tag_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.microblog_tags
    ADD CONSTRAINT microblog_tags_tag_id_fkey FOREIGN KEY (tag_id) REFERENCES public.tags(id) ON DELETE CASCADE;


--
-- Name: notes_tags notes_tags_notes_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.notes_tags
    ADD CONSTRAINT notes_tags_notes_id_fkey FOREIGN KEY (notes_id) REFERENCES public.notes(id) ON DELETE CASCADE;


--
-- Name: notes_tags notes_tags_tag_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: avnadmin
--

ALTER TABLE ONLY public.notes_tags
    ADD CONSTRAINT notes_tags_tag_id_fkey FOREIGN KEY (tag_id) REFERENCES public.tags(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

\unrestrict UTd3hReNLdHRCO3mBfvVYu3DKQ7yrpEhu86nim8ZnWzA6r7JgwFgD8ppKLSP3fH
