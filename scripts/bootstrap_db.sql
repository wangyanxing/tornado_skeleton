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
    video_size integer,
    rate integer
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