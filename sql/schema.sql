-- Table: public.users
-- DROP TABLE IF EXISTS public.users;
CREATE TABLE IF NOT EXISTS public.users
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    public_id character varying(8) COLLATE pg_catalog."default",
    email character varying(32) COLLATE pg_catalog."default" NOT NULL,
    timezone character varying(64) COLLATE pg_catalog."default",
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone,
    CONSTRAINT users_pkey PRIMARY KEY (user_id, email),
    CONSTRAINT unique_email UNIQUE (email)
);
-- Index: idx_users_public_id
-- DROP INDEX IF EXISTS public.idx_users_public_id;
CREATE INDEX IF NOT EXISTS idx_users_public_id
    ON public.users USING btree
    (public_id COLLATE pg_catalog."default" ASC NULLS LAST);


-- Table: public.urls
-- DROP TABLE IF EXISTS public.urls;
CREATE TABLE IF NOT EXISTS public.urls
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    public_id character varying(8) COLLATE pg_catalog."default",
    destination_link text COLLATE pg_catalog."default" NOT NULL,
    destination_link_hash character varying(33) COLLATE pg_catalog."default" NOT NULL,
    qrcode_path character varying(128) COLLATE pg_catalog."default",
    created_at timestamp without time zone DEFAULT now(),
    updated_at timestamp without time zone DEFAULT now(),
    CONSTRAINT urls_pkey PRIMARY KEY (id)
);
-- Index: idx_public_id_user_id
-- DROP INDEX IF EXISTS public.idx_public_id_user_id;
CREATE INDEX IF NOT EXISTS idx_public_id_user_id_destination_link_hash
    ON public.urls USING btree
    (public_id COLLATE pg_catalog."default" ASC NULLS LAST, user_id ASC NULLS LAST, destination_link_hash ASC NULLS LAST)
    TABLESPACE pg_default;


-- DROP TABLE IF EXISTS public.url_aliases;
CREATE TABLE IF NOT EXISTS public.url_aliases
(
    url_public_id character varying(8) COLLATE pg_catalog."default" NOT NULL,
    alias_name character varying(64) COLLATE pg_catalog."default" NOT NULL,
    user_id integer,
    qrcode_path character varying(128) COLLATE pg_catalog."default",
    created_at timestamp without time zone,
    updated_at timestamp without time zone,
    CONSTRAINT url_aliases_pkey PRIMARY KEY (url_public_id, alias_name)
);

CREATE TABLE IF NOT EXISTS public.url_clicks
(
    id serial PRIMARY KEY,
    url_id integer REFERENCES public.urls(id),
    created_at timestamp without time zone DEFAULT now(),
    user_agent text,
    ip_address inet,
    referer text,
    alias_name character varying(64)
);

CREATE INDEX IF NOT EXISTS idx_url_clicks_url_id_created_at
    ON public.url_clicks
    (url_id ASC NULLS LAST, created_at ASC NULLS LAST);
