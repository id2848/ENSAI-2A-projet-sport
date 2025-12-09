-----------------------------------------------------
-- Insertion des utilisateurs
-----------------------------------------------------
INSERT INTO utilisateur (pseudo, nom, prenom, date_de_naissance, sexe)
VALUES 
    ('johndoe', 'Doe', 'John', '1990-01-01', 'Homme'),
    ('janedoe', 'Doe', 'Jane', '1992-02-02', 'Femme'),
    ('samsmith', 'Smith', 'Sam', '1985-05-15', 'Homme'),
    ('emilyjones', 'Jones', 'Emily', '1995-03-20', 'Femme'),
    ('mikebrown', 'Brown', 'Mike', '1988-11-30', 'Homme');

-----------------------------------------------------
-- Insertion des credentials (identifiants)
-- Les hashs et sels seront remplacés dynamiquement par reset_database.py
-----------------------------------------------------
INSERT INTO credentials (id_utilisateur, mot_de_passe_hash, sel)
VALUES
    (1, 'mdp1', ''),
    (2, 'mdp2', ''),
    (3, 'mdp3', ''),
    (4, 'mdp4', ''),
    (5, 'mdp5', '');

-----------------------------------------------------
-- Insertion des activités
-----------------------------------------------------
INSERT INTO activite (id_utilisateur, sport, date_activite, distance, duree)
VALUES 
    (1, 'course', '2025-09-25', 5.0, 30.0),
    (2, 'natation', '2025-09-26', 2.5, 45.0),
    (3, 'vélo', '2025-09-27', 20.0, 60.0),
    (4, 'randonnée', '2025-09-28', 10.0, 120.0),
    (5, 'course', '2025-09-29', 10.0, 50.0),
    (1, 'natation', '2025-09-27', 1.0, 30.0),
    (1, 'vélo', '2025-10-25', 15.0, 60.0);;

-----------------------------------------------------
-- Insertion des commentaires
-----------------------------------------------------
INSERT INTO commentaire (id_activite, id_auteur, contenu, date_commentaire)
VALUES 
    (1, 2, 'Super activité !', '2025-09-26'),
    (2, 3, 'Je trouve la natation relaxante, c''est parfait pour se détendre.', '2025-09-27'),
    (3, 4, 'J''adore le vélo !', '2025-09-28'),
    (4, 4, 'Randonnée incroyable avec des vues magnifiques.', '2025-09-29');

-----------------------------------------------------
-- Insertion des jaimes
-----------------------------------------------------
INSERT INTO jaime (id_activite, id_auteur)
VALUES 
    (1, 3),
    (2, 4),
    (3, 1),
    (4, 2),
    (5, 3);

-----------------------------------------------------
-- Insertion des abonnements
-----------------------------------------------------
INSERT INTO abonnement (id_utilisateur_suiveur, id_utilisateur_suivi)
VALUES 
    (1, 2),
    (2, 1),
    (2, 3),
    (2, 4),
    (3, 4),
    (4, 5),
    (5, 1);
