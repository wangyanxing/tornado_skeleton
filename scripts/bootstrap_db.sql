--
-- Titles
--

CREATE TABLE titles (
    id integer NOT NULL,
    uuid uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    title_id character varying(10) NOT NULL,
    title text NOT NULL,
    video_path character varying(128) NOT NULL,
    file_names character varying(128) NOT NULL,
    description text,
    maker character varying(32),
    video_size integer,
    stars integer,
    rate integer,
    length numeric,
    published_date timestamp
);

CREATE SEQUENCE title_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE title_id_seq OWNED BY titles.id;
ALTER TABLE ONLY titles ALTER COLUMN id SET DEFAULT nextval('title_id_seq'::regclass);

ALTER TABLE ONLY titles ADD CONSTRAINT titles_uuid_pkey PRIMARY KEY (uuid);

CREATE INDEX ix_titles_uuid ON titles USING btree (uuid);
CREATE INDEX ix_titles_id ON titles USING btree (id);
CREATE INDEX ix_titles_title_id ON titles USING btree (title_id);
CREATE INDEX ix_titles_updated_at ON titles USING btree (updated_at);


--
-- Stars
--

CREATE TABLE stars (
    id integer NOT NULL,
    uuid uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    raw_name character varying(32) NOT NULL,
    hiragana character varying(32) NOT NULL,
    english_id character varying(32) NOT NULL,
    pronunciation character varying(32),
    other_names character varying(64),
    num_titles integer
);

CREATE SEQUENCE star_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE star_id_seq OWNED BY stars.id;
ALTER TABLE ONLY stars ALTER COLUMN id SET DEFAULT nextval('star_id_seq'::regclass);

ALTER TABLE ONLY stars ADD CONSTRAINT stars_uuid_pkey PRIMARY KEY (uuid);

CREATE INDEX ix_stars_uuid ON stars USING btree (uuid);
CREATE INDEX ix_stars_id ON stars USING btree (id);
CREATE INDEX ix_stars_english_id ON stars USING btree (english_id);
CREATE INDEX ix_stars_raw_name ON stars USING btree (raw_name);
CREATE INDEX ix_stars_updated_at ON stars USING btree (updated_at);


--
-- Users
--
CREATE TABLE users (
    id integer NOT NULL,
    uuid uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    user_name character varying(20) NOT NULL,
    password character varying(128) NOT NULL,
    email character varying(320) NOT NULL
);

CREATE SEQUENCE user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE user_id_seq OWNED BY users.id;
ALTER TABLE ONLY users ALTER COLUMN id SET DEFAULT nextval('user_id_seq'::regclass);

ALTER TABLE ONLY users ADD CONSTRAINT user_uuid_pkey PRIMARY KEY (uuid);

CREATE INDEX ix_users_uuid ON users USING btree (uuid);
CREATE INDEX ix_users_id ON users USING btree (id);
CREATE INDEX ix_users_user_name ON users USING btree (user_name);
CREATE INDEX ix_users_updated_at ON users USING btree (updated_at);


--
-- Tags
--
CREATE TABLE tags (
    id integer NOT NULL,
    uuid uuid NOT NULL,
    created_at timestamp with time zone NOT NULL,
    updated_at timestamp with time zone NOT NULL,
    name text NOT NULL
);

CREATE SEQUENCE tag_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE tag_id_seq OWNED BY tags.id;
ALTER TABLE ONLY tags ALTER COLUMN id SET DEFAULT nextval('tag_id_seq'::regclass);

ALTER TABLE ONLY tags ADD CONSTRAINT tag_uuid_pkey PRIMARY KEY (uuid);

CREATE INDEX ix_tags_uuid ON tags USING btree (uuid);
CREATE INDEX ix_tags_id ON tags USING btree (id);
CREATE INDEX ix_tags_name ON tags USING btree (name);
CREATE INDEX ix_tags_updated_at ON tags USING btree (updated_at);
