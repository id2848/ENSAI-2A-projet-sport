-----------------------------------------------------
-- Utilisateur 
-----------------------------------------------------
DROP TABLE IF EXISTS utilisateur CASCADE ;

CREATE TABLE utilisateur (
    id_utilisateur          SERIAL PRIMARY KEY,
    pseudo                  VARCHAR(30) UNIQUE,
    mot_de_passe_hash       VARCHAR(256),
    nom                     VARCHAR(50),
    prenom                  VARCHAR(30),
    date_de_naissance       DATE,
    sexe                    VARCHAR(10)
);

-----------------------------------------------------
-- Activite
-----------------------------------------------------
DROP TABLE IF EXISTS activite CASCADE ;

CREATE TYPE sport AS ENUM ('course', 'natation', 'velo', 'randonnée');  -- Définition de l'énumération

CREATE TABLE activite (
    id_activite             SERIAL PRIMARY KEY,
    id_utilisateur          INTEGER,  -- Change SERIAL en INTEGER car ce sera une clé étrangère
    sport                   sport,    -- Utilisation de l'ENUM sport
    date_activite           DATE,
    distance                FLOAT,
    duree                   FLOAT,
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id_utilisateur)  -- Définition de la clé étrangère
);

-----------------------------------------------------
-- Commentaire
-----------------------------------------------------
DROP TABLE IF EXISTS commentaire CASCADE ;

CREATE TABLE commentaire (
    id_commentaire          SERIAL PRIMARY KEY,
    id_activite             INTEGER,  -- Id de l'activité
    id_auteur               INTEGER,  -- Id de l'auteur
    commentaire             VARCHAR(300),
    date_commentaire        DATE,
    FOREIGN KEY (id_activite) REFERENCES activite(id_activite),  -- Clé étrangère vers activite
    FOREIGN KEY (id_auteur) REFERENCES utilisateur(id_utilisateur)  -- Clé étrangère vers utilisateur
);

-----------------------------------------------------
-- Jaime
-----------------------------------------------------
DROP TABLE IF EXISTS jaime CASCADE ;

CREATE TABLE jaime (
    id_jaime                SERIAL PRIMARY KEY,
    id_activite             INTEGER,  -- Id de l'activité
    id_auteur               INTEGER,  -- Id de l'auteur
    FOREIGN KEY (id_activite) REFERENCES activite(id_activite),  -- Clé étrangère vers activite
    FOREIGN KEY (id_auteur) REFERENCES utilisateur(id_utilisateur)  -- Clé étrangère vers utilisateur
);

-----------------------------------------------------
-- Abonnement
-----------------------------------------------------
DROP TABLE IF EXISTS abonnement CASCADE ;

CREATE TABLE abonnement (
    id_utilisateur_suiveur INTEGER,  -- Id de l'utilisateur qui suit
    id_utilisateur_suivi   INTEGER,  -- Id de l'utilisateur suivi
    PRIMARY KEY (id_utilisateur_suiveur, id_utilisateur_suivi),  -- Clé primaire composée
    FOREIGN KEY (id_utilisateur_suiveur) REFERENCES utilisateur(id_utilisateur),  -- Clé étrangère vers utilisateur
    FOREIGN KEY (id_utilisateur_suivi) REFERENCES utilisateur(id_utilisateur)   -- Clé étrangère vers utilisateur
);
