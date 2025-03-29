--
-- PostgreSQL database dump
--

-- Dumped from database version 13.16 (Debian 13.16-1.pgdg120+1)
-- Dumped by pg_dump version 17.0 (Debian 17.0-1.pgdg120+1)

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
-- Name: public; Type: SCHEMA; Schema: -; Owner: username
--

-- *not* creating schema, since initdb creates it


ALTER SCHEMA public OWNER TO username;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: apostador; Type: TABLE; Schema: public; Owner: username
--

CREATE TABLE public.apostador (
    id integer NOT NULL,
    nombre character varying NOT NULL,
    mail character varying NOT NULL,
    clave bytea NOT NULL,
    balance_apuestas double precision NOT NULL,
    es_admin boolean NOT NULL
);


ALTER TABLE public.apostador OWNER TO username;

--
-- Name: apostador_id_seq; Type: SEQUENCE; Schema: public; Owner: username
--

CREATE SEQUENCE public.apostador_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.apostador_id_seq OWNER TO username;

--
-- Name: apostador_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: username
--

ALTER SEQUENCE public.apostador_id_seq OWNED BY public.apostador.id;


--
-- Name: apuesta; Type: TABLE; Schema: public; Owner: username
--

CREATE TABLE public.apuesta (
    id integer NOT NULL,
    fecha timestamp without time zone NOT NULL,
    monto double precision NOT NULL,
    apostador_id integer NOT NULL,
    carrera_id integer NOT NULL,
    caballo_id integer NOT NULL
);


ALTER TABLE public.apuesta OWNER TO username;

--
-- Name: apuesta_id_seq; Type: SEQUENCE; Schema: public; Owner: username
--

CREATE SEQUENCE public.apuesta_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.apuesta_id_seq OWNER TO username;

--
-- Name: apuesta_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: username
--

ALTER SEQUENCE public.apuesta_id_seq OWNED BY public.apuesta.id;


--
-- Name: caballo; Type: TABLE; Schema: public; Owner: username
--

CREATE TABLE public.caballo (
    id integer NOT NULL,
    nombre character varying NOT NULL,
    peso double precision NOT NULL
);


ALTER TABLE public.caballo OWNER TO username;

--
-- Name: caballo_id_seq; Type: SEQUENCE; Schema: public; Owner: username
--

CREATE SEQUENCE public.caballo_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.caballo_id_seq OWNER TO username;

--
-- Name: caballo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: username
--

ALTER SEQUENCE public.caballo_id_seq OWNED BY public.caballo.id;


--
-- Name: carrera; Type: TABLE; Schema: public; Owner: username
--

CREATE TABLE public.carrera (
    id integer NOT NULL,
    fecha timestamp without time zone NOT NULL,
    caballo_ganador_id integer
);


ALTER TABLE public.carrera OWNER TO username;

--
-- Name: carrera_id_seq; Type: SEQUENCE; Schema: public; Owner: username
--

CREATE SEQUENCE public.carrera_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.carrera_id_seq OWNER TO username;

--
-- Name: carrera_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: username
--

ALTER SEQUENCE public.carrera_id_seq OWNED BY public.carrera.id;


--
-- Name: carreracaballolink; Type: TABLE; Schema: public; Owner: username
--

CREATE TABLE public.carreracaballolink (
    carrera_id integer NOT NULL,
    caballo_id integer NOT NULL
);


ALTER TABLE public.carreracaballolink OWNER TO username;

--
-- Name: apostador id; Type: DEFAULT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.apostador ALTER COLUMN id SET DEFAULT nextval('public.apostador_id_seq'::regclass);


--
-- Name: apuesta id; Type: DEFAULT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.apuesta ALTER COLUMN id SET DEFAULT nextval('public.apuesta_id_seq'::regclass);


--
-- Name: caballo id; Type: DEFAULT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.caballo ALTER COLUMN id SET DEFAULT nextval('public.caballo_id_seq'::regclass);


--
-- Name: carrera id; Type: DEFAULT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.carrera ALTER COLUMN id SET DEFAULT nextval('public.carrera_id_seq'::regclass);


--
-- Data for Name: apostador; Type: TABLE DATA; Schema: public; Owner: username
--

COPY public.apostador (id, nombre, mail, clave, balance_apuestas, es_admin) FROM stdin;
3	pepe	pepe@gmail.com	\\x2432622431322464614e58642e634b58774473335041525a567246782e376665694850797668682e487a2f5a69773572524d7161716d6a5648434e4f	-1000	f
1	nahuel	nahuelcarro@gmail.com	\\x243262243132246633527169626e64524c79756a344e6e31426a77756537737045664e3934634b2f55726c4558704742636344787159784769776f69	-2500	t
2	jose	jose@gmail.com	\\x2432622431322445704f71694439643563446c58633873367969516a2e3578714c634d3348633164334a436f386e346147395035385763536d4f3365	3000	f
4	nahuel	nahuel@gmail.com	\\x243262243132244a704c586a716b74575a75752f5666374e58456e327555483836435132625975766e2f2f683069337954693256586a2f737a4b494b	0	f
\.


--
-- Data for Name: apuesta; Type: TABLE DATA; Schema: public; Owner: username
--

COPY public.apuesta (id, fecha, monto, apostador_id, carrera_id, caballo_id) FROM stdin;
1	2024-11-09 15:54:18.274952	1000	1	2	6
2	2024-11-09 15:54:40.27136	1000	2	2	6
3	2024-11-09 15:55:09.641594	1000	3	2	3
4	2024-11-09 15:59:55.065605	1500	1	1	2
5	2024-11-09 16:04:43.942964	1500	1	3	1
6	2024-11-09 16:05:07.837901	2000	2	3	5
\.


--
-- Data for Name: caballo; Type: TABLE DATA; Schema: public; Owner: username
--

COPY public.caballo (id, nombre, peso) FROM stdin;
1	Relampago	450.5
2	Tormenta	480
3	Fuego	490
4	Trueno	500
5	Rafaga	510
6	Viento	520
\.


--
-- Data for Name: carrera; Type: TABLE DATA; Schema: public; Owner: username
--

COPY public.carrera (id, fecha, caballo_ganador_id) FROM stdin;
1	2024-12-01 19:00:00	\N
2	2024-11-09 16:00:00	4
4	2024-11-09 16:08:00	\N
3	2024-11-09 16:10:00	5
5	2024-11-14 19:00:00	\N
\.


--
-- Data for Name: carreracaballolink; Type: TABLE DATA; Schema: public; Owner: username
--

COPY public.carreracaballolink (carrera_id, caballo_id) FROM stdin;
1	6
2	6
2	3
2	4
1	2
3	5
3	1
\.


--
-- Name: apostador_id_seq; Type: SEQUENCE SET; Schema: public; Owner: username
--

SELECT pg_catalog.setval('public.apostador_id_seq', 4, true);


--
-- Name: apuesta_id_seq; Type: SEQUENCE SET; Schema: public; Owner: username
--

SELECT pg_catalog.setval('public.apuesta_id_seq', 6, true);


--
-- Name: caballo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: username
--

SELECT pg_catalog.setval('public.caballo_id_seq', 6, true);


--
-- Name: carrera_id_seq; Type: SEQUENCE SET; Schema: public; Owner: username
--

SELECT pg_catalog.setval('public.carrera_id_seq', 5, true);


--
-- Name: apostador apostador_mail_key; Type: CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.apostador
    ADD CONSTRAINT apostador_mail_key UNIQUE (mail);


--
-- Name: apostador apostador_pkey; Type: CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.apostador
    ADD CONSTRAINT apostador_pkey PRIMARY KEY (id);


--
-- Name: apuesta apuesta_pkey; Type: CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.apuesta
    ADD CONSTRAINT apuesta_pkey PRIMARY KEY (id);


--
-- Name: caballo caballo_nombre_key; Type: CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.caballo
    ADD CONSTRAINT caballo_nombre_key UNIQUE (nombre);


--
-- Name: caballo caballo_pkey; Type: CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.caballo
    ADD CONSTRAINT caballo_pkey PRIMARY KEY (id);


--
-- Name: carrera carrera_pkey; Type: CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.carrera
    ADD CONSTRAINT carrera_pkey PRIMARY KEY (id);


--
-- Name: carreracaballolink carreracaballolink_pkey; Type: CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.carreracaballolink
    ADD CONSTRAINT carreracaballolink_pkey PRIMARY KEY (carrera_id, caballo_id);


--
-- Name: ix_apuesta_id; Type: INDEX; Schema: public; Owner: username
--

CREATE INDEX ix_apuesta_id ON public.apuesta USING btree (id);


--
-- Name: ix_caballo_id; Type: INDEX; Schema: public; Owner: username
--

CREATE INDEX ix_caballo_id ON public.caballo USING btree (id);


--
-- Name: ix_carrera_id; Type: INDEX; Schema: public; Owner: username
--

CREATE INDEX ix_carrera_id ON public.carrera USING btree (id);


--
-- Name: apuesta apuesta_apostador_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.apuesta
    ADD CONSTRAINT apuesta_apostador_id_fkey FOREIGN KEY (apostador_id) REFERENCES public.apostador(id);


--
-- Name: apuesta apuesta_caballo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.apuesta
    ADD CONSTRAINT apuesta_caballo_id_fkey FOREIGN KEY (caballo_id) REFERENCES public.caballo(id);


--
-- Name: apuesta apuesta_carrera_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.apuesta
    ADD CONSTRAINT apuesta_carrera_id_fkey FOREIGN KEY (carrera_id) REFERENCES public.carrera(id);


--
-- Name: carrera carrera_caballo_ganador_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.carrera
    ADD CONSTRAINT carrera_caballo_ganador_id_fkey FOREIGN KEY (caballo_ganador_id) REFERENCES public.caballo(id);


--
-- Name: carreracaballolink carreracaballolink_caballo_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.carreracaballolink
    ADD CONSTRAINT carreracaballolink_caballo_id_fkey FOREIGN KEY (caballo_id) REFERENCES public.caballo(id);


--
-- Name: carreracaballolink carreracaballolink_carrera_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: username
--

ALTER TABLE ONLY public.carreracaballolink
    ADD CONSTRAINT carreracaballolink_carrera_id_fkey FOREIGN KEY (carrera_id) REFERENCES public.carrera(id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: username
--

REVOKE USAGE ON SCHEMA public FROM PUBLIC;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

