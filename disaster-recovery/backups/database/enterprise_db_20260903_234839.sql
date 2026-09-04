--
-- PostgreSQL database dump
--

\restrict VpEzX037GCprcI2HnhpuYYSYhttGSw2iLceHtLs3zGDEg2EDCXNtLPJ8NQKRZfw

-- Dumped from database version 16.15
-- Dumped by pg_dump version 16.15

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: task_records; Type: TABLE; Schema: public; Owner: enterprise_user
--

CREATE TABLE public.task_records (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    status character varying(50) NOT NULL,
    created_at timestamp with time zone
);


ALTER TABLE public.task_records OWNER TO enterprise_user;

--
-- Name: task_records_id_seq; Type: SEQUENCE; Schema: public; Owner: enterprise_user
--

CREATE SEQUENCE public.task_records_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.task_records_id_seq OWNER TO enterprise_user;

--
-- Name: task_records_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: enterprise_user
--

ALTER SEQUENCE public.task_records_id_seq OWNED BY public.task_records.id;


--
-- Name: task_records id; Type: DEFAULT; Schema: public; Owner: enterprise_user
--

ALTER TABLE ONLY public.task_records ALTER COLUMN id SET DEFAULT nextval('public.task_records_id_seq'::regclass);


--
-- Data for Name: task_records; Type: TABLE DATA; Schema: public; Owner: enterprise_user
--

COPY public.task_records (id, name, status, created_at) FROM stdin;
1	generate-enterprise-report	queued	2026-08-29 18:10:18.402346+00
2	docker-compose-full-stack-test	queued	2026-08-29 18:52:05.8651+00
3	Enterprise DevSecOps Integration Test	queued	2026-08-30 09:23:33.33261+00
4	CI Integration Test Task	queued	2026-08-31 15:34:15.005326+00
5	CI Integration Test Task	queued	2026-08-31 15:43:28.827434+00
\.


--
-- Name: task_records_id_seq; Type: SEQUENCE SET; Schema: public; Owner: enterprise_user
--

SELECT pg_catalog.setval('public.task_records_id_seq', 5, true);


--
-- Name: task_records task_records_pkey; Type: CONSTRAINT; Schema: public; Owner: enterprise_user
--

ALTER TABLE ONLY public.task_records
    ADD CONSTRAINT task_records_pkey PRIMARY KEY (id);


--
-- Name: ix_task_records_id; Type: INDEX; Schema: public; Owner: enterprise_user
--

CREATE INDEX ix_task_records_id ON public.task_records USING btree (id);


--
-- PostgreSQL database dump complete
--

\unrestrict VpEzX037GCprcI2HnhpuYYSYhttGSw2iLceHtLs3zGDEg2EDCXNtLPJ8NQKRZfw

