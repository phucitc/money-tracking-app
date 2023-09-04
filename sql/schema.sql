-- Table: public.users
-- DROP TABLE IF EXISTS public.users;
CREATE TABLE IF NOT EXISTS public.users
(
    id serial PRIMARY KEY,
    public_id character varying(8),
    email character varying(32) NOT NULL,
    timezone character varying(64),
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone,
    CONSTRAINT users_pkey PRIMARY KEY (user_id, email),
    CONSTRAINT unique_email UNIQUE (email)
);
-- Index: idx_users_public_id
-- DROP INDEX IF EXISTS public.idx_users_public_id;
CREATE INDEX IF NOT EXISTS idx_users_public_id
    ON public.users USING btree
    (public_id ASC NULLS LAST);


-- Table: public.urls
-- DROP TABLE IF EXISTS public.urls;
CREATE TABLE IF NOT EXISTS public.urls
(
    id serial,
    public_id character varying(8) COLLATE pg_catalog."default",
    destination_link text COLLATE pg_catalog."default" NOT NULL,
    destination_link_hash character varying(33) COLLATE pg_catalog."default" NOT NULL,
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now(),
    CONSTRAINT urls_pkey PRIMARY KEY (id)
)
-- Index: idx_public_id_user_id
-- DROP INDEX IF EXISTS public.idx_public_id_user_id;
CREATE INDEX IF NOT EXISTS idx_public_id_user_id_destination_link_hash
    ON public.urls USING btree
    (public_id ASC NULLS LAST, destination_link_hash ASC NULLS LAST)
    TABLESPACE pg_default;


-- DROP TABLE IF EXISTS public.url_aliases;
CREATE TABLE IF NOT EXISTS public.url_aliases
(
    id serial,
    url_id integer,
    alias_name character varying(64),
    user_id integer,
    qrcode_path character varying(128),
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now(),
    public_id character varying(8),
    cookie_uuid character varying(50),
    CONSTRAINT url_aliases_pkey PRIMARY KEY (id)
)
CREATE INDEX IF NOT EXISTS idx_url_aliases
    ON public.url_aliases
    (url_id ASC NULLS LAST, user_id ASC NULLS LAST, alias_name ASC NULLS LAST, public_id ASC NULLS LAST, cookie_uuid ASC NULLS LAST, created_at ASC NULLS LAST);


CREATE TABLE IF NOT EXISTS public.url_clicks
(
    id serial PRIMARY KEY,
    url_alias_id integer,
    created_at timestamp without time zone DEFAULT now(),
    user_agent text,
    ip_address inet,
    referer text,
    alias_name character varying(64)
);

CREATE INDEX IF NOT EXISTS idx_url_clicks_url_id_created_at
    ON public.url_clicks
    (url_alias_id ASC NULLS LAST, created_at ASC NULLS LAST);
