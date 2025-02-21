
CREATE SEQUENCE dashboard.seq_entidad_federativa
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 999
    CACHE 1;

ALTER SEQUENCE dashboard.seq_entidad_federativa
    OWNER TO dashboard;
	
CREATE TABLE dashboard.entidad_federativa
(
    id_entidad_federativa bigint NOT NULL DEFAULT nextval('dashboard.seq_entidad_federativa'::regclass),
    nombre character varying(80) NOT NULL,
    CONSTRAINT entidad_federativa_pkey PRIMARY KEY (id_entidad_federativa),
    CONSTRAINT entidad_federativa__un UNIQUE (nombre)
)
WITH (
    OIDS = FALSE
);

ALTER TABLE dashboard.entidad_federativa
    OWNER to dashboard;
