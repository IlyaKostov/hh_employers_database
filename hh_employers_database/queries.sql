--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET default_tablespace = '';

SET default_with_oids = false;

---
--- drop tables
---

DROP TABLE IF EXISTS employers;
DROP TABLE IF EXISTS vacancies;


--
-- Name: employers; Type: TABLE; Schema: public; Owner: -; Tablespace:
--

CREATE TABLE employers (
    employer_id serial PRIMARY KEY,
    employer_name varchar(40),
    employer_site_url varchar(200),
    employer_hh_url varchar(100)
);


--
-- Name: customers; Type: TABLE; Schema: public; Owner: -; Tablespace:
--

CREATE TABLE vacancies (
    vacancy_id serial PRIMARY KEY,
    vacancy_title varchar(100),
    employer_id int REFERENCES employers(employer_id),
    city varchar(100),
    salary_from int,
    salary_to int,
    currency varchar(5),
    published_date date,
    requirement text,
    responsibility text,
    experience varchar(100),
    vacancy_url varchar(100)
);

--
-- PostgreSQL database dump complete
--