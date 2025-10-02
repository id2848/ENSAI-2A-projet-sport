-----------------------------------------------------
-- Insertion des utilisateurs
-----------------------------------------------------
INSERT INTO utilisateur (pseudo, mot_de_passe_hash, nom, prenom, date_de_naissance, sexe)
VALUES 
    ('johndoe', 'hash1', 'Doe', 'John', '1990-01-01', 'Homme'),
    ('janedoe', 'hash2', 'Doe', 'Jane', '1992-02-02', 'Femme'),
    ('samsmith', 'hash3', 'Smith', 'Sam', '1985-05-15', 'Homme'),
    ('emilyjones', 'hash4', 'Jones', 'Emily', '1995-03-20', 'Femme'),
    ('mikebrown', 'hash5', 'Brown', 'Mike', '1988-11-30', 'Homme');

-----------------------------------------------------
-- Insertion des activités
-----------------------------------------------------
INSERT INTO activite (id_utilisateur, sport, date_activite, distance, duree)
VALUES 
    (1, 'course', '2025-09-25', 5.0, 30.0),
    (2, 'natation', '2025-09-26', 2.5, 45.0),
    (3, 'velo', '2025-09-27', 20.0, 60.0),
    (4, 'randonnée', '2025-09-28', 10.0, 120.0),
    (5, 'course', '2025-09-29', 10.0, 50.0);

-----------------------------------------------------
-- Insertion des commentaires
-----------------------------------------------------
INSERT INTO commentaire (id_activite, id_auteur, commentaire, date_commentaire)
VALUES 
    (1, 2, "Super activité, j'ai bien aimé la course !", '2025-09-26'),
    (2, 3, "Natation relaxante, parfait pour se détendre.", '2025-09-27'),
    (3, 4, "J'adore le vélo, c'était un super parcours.", '2025-09-28'),
    (4, 5, "Randonnée incroyable avec des vues magnifiques.", '2025-09-29'),
    (5, 1, "Belle course, mais un peu fatiguant.", '2025-09-30');

-----------------------------------------------------
-- Insertion des likes (jaime)
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
    (2, 3),
    (3, 4),
    (4, 5),
    (5, 1);
