-- The following table creation SQL queries are actually generated by pg_dump,
-- because data are loaded into Postgres by ogr2ogr through importing the KML
-- file that contains all the coordinates:
--
--      ogr2ogr -f PostgreSQL postgresql://localhost:5432 imgs.kml
CREATE TABLE public.home (
    ogc_fid integer NOT NULL,
    name character varying,
    description character varying,
    wkb_geometry public.geometry(PointZ,4326)
);
CREATE SEQUENCE public.home_ogc_fid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.home_ogc_fid_seq OWNED BY public.home.ogc_fid;

CREATE TABLE public.libraries (
    ogc_fid integer NOT NULL,
    name character varying,
    description character varying,
    wkb_geometry public.geometry(PointZ,4326)
);
CREATE SEQUENCE public.libraries_ogc_fid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.libraries_ogc_fid_seq OWNED BY public.libraries.ogc_fid;

CREATE TABLE public.waterworks (
    ogc_fid integer NOT NULL,
    name character varying,
    description character varying,
    wkb_geometry public.geometry(PointZ,4326)
);
CREATE SEQUENCE public.waterworks_ogc_fid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.waterworks_ogc_fid_seq OWNED BY public.waterworks.ogc_fid;

ALTER TABLE ONLY public.home ALTER COLUMN ogc_fid SET DEFAULT nextval('public.home_ogc_fid_seq'::regclass);
ALTER TABLE ONLY public.libraries ALTER COLUMN ogc_fid SET DEFAULT nextval('public.libraries_ogc_fid_seq'::regclass);
ALTER TABLE ONLY public.waterworks ALTER COLUMN ogc_fid SET DEFAULT nextval('public.waterworks_ogc_fid_seq'::regclass);

COPY public.home (ogc_fid, name, description, wkb_geometry) FROM stdin;
1	Home		01010000A0E610000061C43E0114925DC0888C839A030441400000000000000000
\.
COPY public.libraries (ogc_fid, name, description, wkb_geometry) FROM stdin;
1	Leavey		01010000A0E6100000848707581C925DC04BF64426C2024140A4703D0AD7433F40
2	G & T		01010000A0E61000005AD3BCE314925DC0E3787AF4680241400000000000000000
3	Helen Topping		01010000A0E6100000B119E0826C925DC0D2393FC5710241400000000000000000
4	Doheny		01010000A0E610000013684E2233925DC0D15CA79196024140736891ED7CBF2340
5	I & P Affairs		01010000A0E6100000E52A16BF29925DC0A68CF4F1B20241400000000000000000
6	Sci and Engr		01010000A0E610000019ED8FBB79925DC0FED64E94840241400000000000000000
\.
COPY public.waterworks (ogc_fid, name, description, wkb_geometry) FROM stdin;
1	Bloom Walk		01010000A0E6100000FFB730965A925DC07BBE66B96C0241400000000000000000
2	Viterbi		01010000A0E610000022CB20027F925DC0D5027B4CA40241404260E5D0226B4240
3	Prentiss		01010000A0E61000008AAE0B3F38925DC0447AC60DA1024140FCA9F1D24D423A40
4	Generations		01010000A0E61000006506C85B1F925DC0DE205A2BDA024140BE9F1A2FDD043740
5	Marshall		01010000A0E6100000882991442F925DC07CF2B0506B0241400000000000000000
6	P & F Shumway		01010000A0E61000006422A5D93C925DC0EB71DF6A9D0241400000000000000000
\.


SELECT pg_catalog.setval('public.home_ogc_fid_seq', 1, true);
SELECT pg_catalog.setval('public.libraries_ogc_fid_seq', 6, true);
SELECT pg_catalog.setval('public.waterworks_ogc_fid_seq', 6, true);

ALTER TABLE ONLY public.home
    ADD CONSTRAINT home_pkey PRIMARY KEY (ogc_fid);
ALTER TABLE ONLY public.libraries
    ADD CONSTRAINT libraries_pkey PRIMARY KEY (ogc_fid);
ALTER TABLE ONLY public.waterworks
    ADD CONSTRAINT waterworks_pkey PRIMARY KEY (ogc_fid);

-- Convex Hull
SELECT ST_AsText(ST_ConvexHull(ST_Collect(wkb_geometry)))
FROM (SELECT * FROM home UNION ALL SELECT * FROM libraries UNION ALL SELECT * FROM waterworks) AS t;

-- Nearest Neighbor
SELECT * FROM (SELECT * FROM libraries UNION ALL SELECT * FROM waterworks) AS t
ORDER BY wkb_geometry <-> (SELECT wkb_geometry FROM home) LIMIT 1;

-- Centroid
SELECT ST_AsText(ST_Centroid(ST_Collect(wkb_geometry)))
FROM (SELECT * FROM home UNION ALL SELECT * FROM libraries UNION ALL SELECT * FROM waterworks) AS t;