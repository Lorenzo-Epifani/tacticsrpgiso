BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "abilita" (
	"id"	VARCHAR NOT NULL,
	"nome"	VARCHAR NOT NULL,
	"p_ab"	INTEGER NOT NULL,
	"effect"	VARCHAR(6) NOT NULL,
	PRIMARY KEY("id"),
	UNIQUE("nome")
);
CREATE TABLE IF NOT EXISTS "attiva" (
	"id"	VARCHAR NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY("id") REFERENCES "abilita"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "classe" (
	"id"	VARCHAR NOT NULL,
	"nome"	VARCHAR NOT NULL,
	"requisiti"	VARCHAR,
	PRIMARY KEY("id"),
	UNIQUE("nome")
);
CREATE TABLE IF NOT EXISTS "classe_equip_cat" (
	"classe_id"	VARCHAR NOT NULL,
	"equip_cat_id"	VARCHAR NOT NULL,
	PRIMARY KEY("classe_id","equip_cat_id"),
	FOREIGN KEY("classe_id") REFERENCES "classe"("id") ON DELETE CASCADE,
	FOREIGN KEY("equip_cat_id") REFERENCES "equip_cat"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "equip" (
	"id"	VARCHAR NOT NULL,
	"nome"	VARCHAR NOT NULL,
	"stats"	VARCHAR NOT NULL,
	"equip_cat_id"	VARCHAR NOT NULL,
	PRIMARY KEY("id"),
	UNIQUE("nome"),
	FOREIGN KEY("equip_cat_id") REFERENCES "equip_cat"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "equip_abilita" (
	"equip_id"	VARCHAR NOT NULL,
	"abilita_id"	VARCHAR NOT NULL,
	PRIMARY KEY("equip_id","abilita_id"),
	FOREIGN KEY("abilita_id") REFERENCES "abilita"("id") ON DELETE CASCADE,
	FOREIGN KEY("equip_id") REFERENCES "equip"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "equip_cat" (
	"id"	VARCHAR NOT NULL,
	"nome"	VARCHAR NOT NULL,
	"tipo"	VARCHAR(11) NOT NULL,
	PRIMARY KEY("id"),
	UNIQUE("nome")
);
CREATE TABLE IF NOT EXISTS "innata" (
	"id"	VARCHAR NOT NULL,
	"trigger"	VARCHAR(8) NOT NULL,
	"razza_id"	VARCHAR NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY("id") REFERENCES "abilita"("id") ON DELETE CASCADE,
	FOREIGN KEY("razza_id") REFERENCES "razza"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "passiva" (
	"id"	VARCHAR NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY("id") REFERENCES "abilita"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "razza" (
	"id"	VARCHAR NOT NULL,
	"nome"	VARCHAR NOT NULL,
	PRIMARY KEY("id"),
	UNIQUE("nome")
);
CREATE TABLE IF NOT EXISTS "razza_classe" (
	"razza_id"	VARCHAR NOT NULL,
	"classe_id"	VARCHAR NOT NULL,
	PRIMARY KEY("razza_id","classe_id"),
	FOREIGN KEY("classe_id") REFERENCES "classe"("id") ON DELETE CASCADE,
	FOREIGN KEY("razza_id") REFERENCES "razza"("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "reazione" (
	"id"	VARCHAR NOT NULL,
	"trigger"	VARCHAR(12) NOT NULL,
	PRIMARY KEY("id"),
	FOREIGN KEY("id") REFERENCES "abilita"("id") ON DELETE CASCADE
);
INSERT INTO "abilita" VALUES ('6aaa0f9b-9bcb-415e-84db-4aa50733653b','Salto del Drago',10,'DANNO');
INSERT INTO "abilita" VALUES ('1a633bfb-4ca5-4b51-b4ec-bfd704169fa3','Taglio Potente',8,'DANNO');
INSERT INTO "abilita" VALUES ('afb43756-4561-4d33-bd9e-8432bb51ec99','Meteorite',12,'DANNO');
INSERT INTO "abilita" VALUES ('e7837f3a-1df3-4d63-9eb2-3e1922361c42','Cura Suprema',10,'CURA');
INSERT INTO "abilita" VALUES ('a2b651ad-fe49-49d6-a35c-042dfb2ad266','Pelle Dura',0,'BUFF');
INSERT INTO "abilita" VALUES ('6585a105-c01a-4745-bb87-2e7811da7ee2','Magia Potenziata',0,'BUFF');
INSERT INTO "abilita" VALUES ('d35134f7-1554-408f-b086-1a54951cdac2','Contrattacco',0,'DANNO');
INSERT INTO "abilita" VALUES ('7e8ddef7-19f0-40c9-80bf-43240a3adf92','Risveglio Magico',0,'BUFF');
INSERT INTO "abilita" VALUES ('24d44fd9-b7b8-4b5e-9999-18ff56606b15','Forza Bangaa',0,'BUFF');
INSERT INTO "abilita" VALUES ('fd5e9d08-59bb-442b-84fa-cb924782514a','Mana Innato',0,'BUFF');
INSERT INTO "attiva" VALUES ('6aaa0f9b-9bcb-415e-84db-4aa50733653b');
INSERT INTO "attiva" VALUES ('1a633bfb-4ca5-4b51-b4ec-bfd704169fa3');
INSERT INTO "attiva" VALUES ('afb43756-4561-4d33-bd9e-8432bb51ec99');
INSERT INTO "attiva" VALUES ('e7837f3a-1df3-4d63-9eb2-3e1922361c42');
INSERT INTO "classe" VALUES ('494bd3cc-73d0-4a99-8ac1-3d7d17144a6b','Dragone','{}');
INSERT INTO "classe" VALUES ('bb2c5f2e-0e64-4cd4-88de-c2d92bd18600','Gladiatore','{}');
INSERT INTO "classe" VALUES ('739e48a4-809b-4fae-ab5a-63e728595016','Mago Nero','{}');
INSERT INTO "classe" VALUES ('e54d1c40-a817-4ce0-876d-8c9961cb2cdc','Mago Bianco','{}');
INSERT INTO "equip" VALUES ('552e4ff6-a152-4785-893e-7407fd9e794f','Lancia del Drago','{"attacco": 25}','f93d3686-e16c-4be5-a86a-8b41e5d1b128');
INSERT INTO "equip" VALUES ('ef5962a3-1b2c-4908-8e8a-e1f90248dcfe','Spada Gladiatore','{"attacco": 20}','f93d3686-e16c-4be5-a86a-8b41e5d1b128');
INSERT INTO "equip" VALUES ('ce0874fc-382c-494c-b51d-821be034012f','Verga del Fuoco','{"magia": 30}','f93d3686-e16c-4be5-a86a-8b41e5d1b128');
INSERT INTO "equip" VALUES ('50d78f0d-f1eb-4036-ba3c-a4e793e51eb8','Bastone della Luce','{"magia": 28}','f93d3686-e16c-4be5-a86a-8b41e5d1b128');
INSERT INTO "equip" VALUES ('3d8241e7-1efc-4733-b780-929726be8dd6','Ascia Pesante','{"attacco": 35}','f93d3686-e16c-4be5-a86a-8b41e5d1b128');
INSERT INTO "equip" VALUES ('375dfcb3-983d-4418-8044-02e9c7aabe7a','Armatura di Mithril','{"difesa": 20}','d3c8a20a-aaaf-421e-8648-003af0389c2d');
INSERT INTO "equip" VALUES ('120c29f6-125d-4535-b00e-6825880e1769','Veste del Mago','{"difesa": 15, "mana": 10}','d3c8a20a-aaaf-421e-8648-003af0389c2d');
INSERT INTO "equip" VALUES ('4e4f62fe-c205-4064-93f5-78b411572b03','Scudo Sacro','{"difesa": 25}','d3c8a20a-aaaf-421e-8648-003af0389c2d');
INSERT INTO "equip" VALUES ('e2660d23-f940-429d-a437-14c99500859a','Elmo del Drago','{"difesa": 18}','d3c8a20a-aaaf-421e-8648-003af0389c2d');
INSERT INTO "equip" VALUES ('abca353d-5e9f-40e4-9784-3d1c046c2b5c','Mantello Oscuro','{"evasione": 12}','d3c8a20a-aaaf-421e-8648-003af0389c2d');
INSERT INTO "equip_cat" VALUES ('f93d3686-e16c-4be5-a86a-8b41e5d1b128','Arma','ARMA');
INSERT INTO "equip_cat" VALUES ('d3c8a20a-aaaf-421e-8648-003af0389c2d','Armatura','ARMATURA');
INSERT INTO "innata" VALUES ('24d44fd9-b7b8-4b5e-9999-18ff56606b15','BORN','cb6a947b-79c8-4e1b-b6c9-4a404fcd4a75');
INSERT INTO "innata" VALUES ('fd5e9d08-59bb-442b-84fa-cb924782514a','BORN','a483069b-1b46-427c-bfaa-f456e0416b69');
INSERT INTO "passiva" VALUES ('a2b651ad-fe49-49d6-a35c-042dfb2ad266');
INSERT INTO "passiva" VALUES ('6585a105-c01a-4745-bb87-2e7811da7ee2');
INSERT INTO "razza" VALUES ('cb6a947b-79c8-4e1b-b6c9-4a404fcd4a75','Bangaa');
INSERT INTO "razza" VALUES ('a483069b-1b46-427c-bfaa-f456e0416b69','Nu Mou');
INSERT INTO "reazione" VALUES ('d35134f7-1554-408f-b086-1a54951cdac2','DANNO_SUBITO');
INSERT INTO "reazione" VALUES ('7e8ddef7-19f0-40c9-80bf-43240a3adf92','MAGIA');
COMMIT;
