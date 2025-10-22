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

CREATE TYPE sport AS ENUM ('course', 'natation', 'vélo', 'randonnée');  

CREATE TABLE activite (
    id_activite             SERIAL PRIMARY KEY,
    id_utilisateur          INTEGER,  
    sport                   sport,   
    date_activite           DATE,
    distance                FLOAT,
    duree                   FLOAT,
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateur(id_utilisateur) 
);

-----------------------------------------------------
-- Commentaire
-----------------------------------------------------
DROP TABLE IF EXISTS commentaire CASCADE ;

CREATE TABLE commentaire (
    id_commentaire          SERIAL PRIMARY KEY,
    id_activite             INTEGER, 
    id_auteur               INTEGER, 
    commentaire             VARCHAR(300),
    date_commentaire        DATE,
    FOREIGN KEY (id_activite) REFERENCES activite(id_activite),  
    FOREIGN KEY (id_auteur) REFERENCES utilisateur(id_utilisateur) 
);

-----------------------------------------------------
-- Jaime
-----------------------------------------------------
DROP TABLE IF EXISTS jaime CASCADE ;

CREATE TABLE jaime (
    id_activite             INTEGER,  
    id_auteur               INTEGER, 
    PRIMARY KEY (id_activite, id_auteur),  
    FOREIGN KEY (id_activite) REFERENCES activite(id_activite),  
    FOREIGN KEY (id_auteur) REFERENCES utilisateur(id_utilisateur) 
);

-----------------------------------------------------
-- Abonnement
-----------------------------------------------------
DROP TABLE IF EXISTS abonnement CASCADE ;

CREATE TABLE abonnement (
    id_utilisateur_suiveur INTEGER,  
    id_utilisateur_suivi   INTEGER,  
    PRIMARY KEY (id_utilisateur_suiveur, id_utilisateur_suivi),  
    FOREIGN KEY (id_utilisateur_suiveur) REFERENCES utilisateur(id_utilisateur),  
    FOREIGN KEY (id_utilisateur_suivi) REFERENCES utilisateur(id_utilisateur)   
);
