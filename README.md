# Créez une API sécurisée RESTful en utilisant Django REST

## Scénario

SoftDesk, une société d'édition de logiciels de développement et de collaboration, a décidé de publier une application permettant de remonter et suivre des problèmes techniques (issue tracking system). Cette solution s’adresse à des entreprises clientes, en B2B.

SoftDesk a mis en place une nouvelle équipe chargée de ce projet, et vous avez été embauché comme ingénieur logiciel (back-end) pour créer un back-end performant et sécurisé, devant servir les applications sur toutes les plateformes.

Pour ce projet je dois alors réaliser une API REST en utilisant le framework Django REST conforme à ces points :

1. Authentification des utilisateurs (inscription/connexion) :
> Remarque : Utiliser l'authentification JWT pour authentifier les utilisateurs.<br><br>
  
2. Concernant les objets de type projet, les utilisateurs doivent avoir accès aux actions basiques de type CRUD (de l'anglais Create, Read, Update, Delete, signifiant “créer, lire, actualiser, supprimer”) sur des projets. Chaque projet doit avoir un titre, une description, un type (back-end, front-end, iOS ou Android), et un author_user_id.
> Remarque : Un projet peut être défini comme une entité ayant plusieurs collaborateurs (utilisateurs), et chaque projet peut contenir plusieurs problèmes.<br><br>

3. Chaque projet peut se voir associer des problèmes qui lui sont liés ; l'utilisateur ne doit pouvoir appliquer le processus CRUD aux problèmes du projet que si il ou elle figure sur la liste des contributeurs.
  > Remarque : Un projet ne doit être accessible qu'à son responsable et aux contributeurs. Seuls les contributeurs sont autorisés à créer ou à consulter les problèmes d'un projet.<br><br>

4. Chaque problème doit avoir un titre, une description, un assigné (l’assigné par défaut étant l'auteur lui-même), une priorité (FAIBLE, MOYENNE ou ÉLEVÉE), une balise (BUG, AMÉLIORATION ou TÂCHE), un statut (À faire, En cours ou Terminé), le project_id auquel il est lié et un created_time (horodatage), ainsi que d'autres attributs mentionnés dans le diagramme de classe.
> Remarque : Seuls les contributeurs peuvent créer (Create) et lire (Read) les commentaires relatifs à un problème. En outre, ils ne peuvent les actualiser (Update) et les supprimer (Delete) que s'ils en sont les auteurs.<br><br>

5. Les problèmes peuvent faire l'objet de commentaires de la part des contributeurs au projet auquel ces problèmes appartiennent. Chaque commentaire doit être assorti d'une description, d'un author_user_id, d'un issue_id, et d'un comment_id.
> Remarque : Un commentaire doit être visible par tous les contributeurs du projet, mais il ne peut être actualisé ou supprimé que par son auteur.<br><br>

6. Il est interdit à tout utilisateur autorisé autre que l'auteur d'émettre des requêtes d'actualisation et de suppression d'un problème/projet/commentaire.
> Remarque : Autorisation d'actualisation et de suppression.<br><br>

Il faudra également prendre en compte une liste de vérifications de sécurité OWASP que voici :

    1. Authentification : utilisez JWT (JSON Web Token) pour le back-end d'authentification du framework Django REST. Cela vise à couvrir les cas d'utilisation de JWT les plus répandus, en offrant par défaut un jeu de fonctionnalités prudent.
   
    2. Autorisation : la deuxième étape est l'autorisation, dans laquelle le back-end décide si l'utilisateur authentifié est autorisé à accéder à une ressource. Dans notre application, un utilisateur ne doit pas être autorisé à accéder à un projet pour lequel il n'est pas ajouté en tant que contributeur. De même, un contributeur ou un utilisateur doit toujours être connecté pour accéder à une fonctionnalité.
   
    3. Accès : même après que l'utilisateur a été authentifié et autorisé à accéder à une ressource, la ressource elle-même peut nécessiter des autorisations spéciales, par exemple pour actualiser ou supprimer un commentaire.
        - Les commentaires doivent être visibles par tous les contributeurs au projet et par le responsable du projet, mais seul leur auteur peut les actualiser ou les supprimer.
        - Un problème ne peut être actualisé ou supprimé que par son auteur, mais il doit rester visible par tous les contributeurs au projet.
        - Il est interdit à tout utilisateur autre que l'auteur de demander une mise à jour et de supprimer des demandes sur une un projet/problème/un commentaire. 

## Installation

1. Clonez le dépôt avec la commande `git clone https://github.com/SylvOne/projet10.git`.
2. Placez vous dans le dossier projet10 avec la commande `cd projet10`.
3. Créez un environnement virtuel avec la commande `python -m venv venv` sur Windows ou `python3 -m venv venv` sur Linux/Mac.
4. Activez l'environnement virtuel avec la commande `source venv/bin/activate` sur Linux/Mac ou `.\venv\scripts\activate` sur Windows.
5. Installez les dépendances avec `pip install -r requirements.txt`.

## Lancement du serveur

- Vous pouvez maintenant lancer le serveur localement<br>
avec la commande `python manage.py runserver`.
  ATTENTION : Il faudra garder le terminal qui a servi au lancement du serveur, ouvert.
  (Vous pourrez stopper le serveur en effectuant un Ctrl + C dans ce même terminal)

## Utilisation

- L'API est désormais accessible à l'adresse suivante : `http://127.0.0.1:8000`
  
- Pour utiliser cette API veuillez vour référer à la documentation disponible ici :<br>
  [Voir la documentation de l'API](https://documenter.getpostman.com/view/17650939/2s93sZ8F2h#5ca65989-4f0e-4cb0-bf73-9433af48f6e4)
  
## Rapport Flake8-HTML

1. Générez un rapport Flake8-HTML avec la commande suivante :
`flake8 --exclude=.git,__pycache__,venv,migrations --max-line-length=119 --format=html --htmldir=flake8_rapport`.
2. Ouvrez le fichier `flake8_rapport/index.html` pour voir le rapport.