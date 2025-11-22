-----------------------------------------------------
-- Insertion des utilisateurs
-----------------------------------------------------
INSERT INTO utilisateur (id_utilisateur, pseudo, nom, prenom, date_de_naissance, sexe)
VALUES 
    (991, 'johndoe', 'Doe', 'John', '1990-01-01', 'Homme'),
    (992, 'janedoe', 'Doe', 'Jane', '1992-02-02', 'Femme'),
    (993, 'samsmith', 'Smith', 'Sam', '1985-05-15', 'Homme'),
    (994, 'emilyjones', 'Jones', 'Emily', '1995-03-20', 'Femme'),
    (995, 'mikebrown', 'Brown', 'Mike', '1988-11-30', 'Homme');

-----------------------------------------------------
-- Insertion des credentials (identifiants)
-- Les hashs et sels seront remplacés dynamiquement par reset_database.py
-----------------------------------------------------
INSERT INTO credentials (id_utilisateur, mot_de_passe_hash, sel)
VALUES
    (991, 'mdp1', ''),
    (992, 'mdp2', ''),
    (993, 'mdp3', ''),
    (994, 'mdp4', ''),
    (995, 'mdp5', '');

-----------------------------------------------------
-- Insertion des activités
-----------------------------------------------------
INSERT INTO activite (id_activite, id_utilisateur, sport, date_activite, distance, duree)
VALUES 
    (991, 991, 'course', '2025-09-25', 5.0, 30.0),
    (992, 992, 'natation', '2025-09-26', 2.5, 45.0),
    (993, 993, 'vélo', '2025-09-27', 20.0, 60.0),
    (994, 994, 'randonnée', '2025-09-28', 10.0, 120.0),
    (995, 995, 'course', '2025-09-29', 10.0, 50.0),
    (996, 991, 'natation', '2025-09-27', 1.0, 30.0),
    (997, 991, 'vélo', '2025-10-25', 15.0, 60.0);;

-----------------------------------------------------
-- Insertion des commentaires
-----------------------------------------------------
INSERT INTO commentaire (id_commentaire, id_activite, id_auteur, contenu, date_commentaire)
VALUES 
    (991, 991, 992, 'Super activité !', '2025-09-26'),
    (992, 992, 993, 'Je trouve la natation relaxante, c''est parfait pour se détendre.', '2025-09-27'),
    (993, 993, 994, 'J''adore le vélo !', '2025-09-28'),
    (994, 994, 994, 'Randonnée incroyable avec des vues magnifiques.', '2025-09-29');

-----------------------------------------------------
-- Insertion des jaimes
-----------------------------------------------------
INSERT INTO jaime (id_activite, id_auteur)
VALUES 
    (991, 993),
    (992, 994),
    (993, 991),
    (994, 992),
    (995, 993);

-----------------------------------------------------
-- Insertion des abonnements
-----------------------------------------------------
INSERT INTO abonnement (id_utilisateur_suiveur, id_utilisateur_suivi)
VALUES 
    (991, 992),
    (992, 991),
    (992, 993),
    (992, 994),
    (993, 994),
    (994, 995),
    (995, 991);
