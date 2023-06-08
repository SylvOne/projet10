from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics
from .models import Project, Contributor, Issue, Comment
from .serializers import ProjectSerializer, ContributorSerializer, IssueSerializer, CommentSerializer
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied
import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_email



class SignupView(APIView):
    """
    Vue permettant de créer un nouvel utilisateur.

    La classe `SignupView` hérite de la classe `APIView` de Django Rest Framework.
    Elle est utilisée pour inscrire de nouveaux utilisateurs en fournissant des informations de base, telles que le nom d'utilisateur, le mot de passe, le prénom, le nom et l'e-mail. 
    Des contrôles de validation sont effectués pour vérifier la complexité du mot de passe et la validité de l'adresse e-mail.

    Méthodes:
    - `post` : Crée un nouvel utilisateur avec les informations fournies. 

    Attributs:
    - `permission_classes` : Spécifie les classes de permission à utiliser pour déterminer l'accès à la vue. Dans ce cas, l'accès est autorisé à tous.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        email = request.data.get("email")

        if not username or not password or not first_name or not last_name or not email:
            return Response({'error': 'Username, password, first name, last name and email are required'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Vérification de la complexité du mot de passe
        if not re.match(r'^(?=.*[A-Z])(?=.*[!@#$&*])(?=.*[0-9])(?=.*[a-z]).{8,}$', password):
            return Response({'error': 'Password is not complex enough'}, status=status.HTTP_400_BAD_REQUEST)

        # Validation email
        try:
            validate_email(email)
        except ValidationError:
            return Response({'error': 'Invalid email address'}, status=status.HTTP_400_BAD_REQUEST)

        # Création de l'utilisateur
        user = User.objects.create_user(username=username, password=password, first_name=first_name, last_name=last_name, email=email)
        
        if user:
            return Response({'message': 'User created'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Failed to create user'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProjectList(generics.ListCreateAPIView):
    """
    Vue permettant de manipuler les projets d'un utilisateur.

    La classe `ProjectList` hérite de la classe `ListCreateAPIView` de Django Rest Framework.
    Elle est utilisée pour créer et récupérer les projets d'un utilisateur spécifique.

    Méthodes:
    - `perform_create` : Ajoute l'auteur à un projet lors de sa création.
    - `get_queryset` : Récupère les projets pour l'utilisateur connecté.

    Attributs:
    - `serializer_class` : Spécifie le sérialiseur à utiliser pour le traitement des données.
    - `permission_classes` : Spécifie les classes de permission à utiliser pour déterminer l'accès à la vue.
    """
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_queryset(self):
        return Project.objects.filter(author=self.request.user)


class ProjectDetail(APIView):
    """
    Vue permettant de manipuler un projet spécifique.

    La classe `ProjectDetail` hérite de la classe `APIView` de Django Rest Framework.
    Elle est utilisée pour récupérer, mettre à jour et supprimer un projet spécifique.

    Méthodes:
    - `get` : Récupère un projet spécifique.
    - `put` : Met à jour un projet spécifique. L'utilisateur doit être l'auteur du projet.
    - `delete` : Supprime un projet spécifique. L'utilisateur doit être l'auteur du projet.

    Attributs:
    - `serializer_class` : Spécifie le sérialiseur à utiliser pour le traitement des données.
    - `permission_classes` : Spécifie les classes de permission à utiliser pour déterminer l'accès à la vue.
    """
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Project.objects.filter(Q(author=user) | Q(contributors__user=user))
        return queryset

    def get_project(self):
        return get_object_or_404(Project, pk=self.kwargs['pk'])

    def check_author(self, user, project):
        if project.author != user:
            raise PermissionDenied('You are not allowed.')

    def get_object(self):
        obj = self.get_project()
        if not self.get_queryset().filter(pk=obj.pk).exists():
            raise PermissionDenied('You are not allowed.')
        return obj

    def get(self, request, *args, **kwargs):
        project = self.get_object()
        serializer = self.serializer_class(project)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        project = self.get_project()
        self.check_author(request.user, project)
        # Je récupère les données de la requête
        data = request.data
        # Je m'assure que certains champs ne soient pas modifiés
        data['id'] = project.id
        data['author'] = project.author
        serializer = self.serializer_class(project, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        project = self.get_project()
        self.check_author(request.user, project)
        project.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContributorsProjectDetail(generics.RetrieveAPIView):
    """
    Vue permettant de manipuler les contributeurs d'un projet spécifique.

    La classe `ContributorsProjectDetail` hérite de la classe `RetrieveAPIView` de Django Rest Framework.
    Elle est utilisée pour récupérer, ajouter et supprimer les contributeurs d'un projet spécifique.

    Méthodes:
    - `get` : Récupère tous les contributeurs du projet spécifié.
    - `post` : Ajoute un nouveau contributeur au projet spécifié. L'utilisateur doit être l'auteur du projet.
    - `delete` : Supprime un contributeur spécifique du projet. L'utilisateur doit être l'auteur du projet.

    Attributs:
    - `serializer_class` : Spécifie le sérialiseur à utiliser pour le traitement des données.
    - `permission_classes` : Spécifie les classes de permission à utiliser pour déterminer l'accès à la vue.
    """
    serializer_class = ContributorSerializer
    permission_classes = [IsAuthenticated]
    
    def get_contributors(self):
        project = self.get_project()
        contributors = Contributor.objects.filter(project=project)
        return contributors

    def get_project(self):
        return get_object_or_404(Project, pk=self.kwargs['pk'])

    def check_author(self, user, project):
        if project.author != user:
            raise PermissionDenied('You are not allowed.')

    def get(self, request, *args, **kwargs):
        contributors = self.get_contributors()
        serializer = self.serializer_class(contributors, many=True)
        user_ids = [contributor['user'] for contributor in serializer.data]
        return Response(user_ids)

    def post(self, request, *args, **kwargs):
        project = self.get_project()
        self.check_author(request.user, project)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(project=project)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        project = self.get_project()
        self.check_author(request.user, project)
        user = get_object_or_404(User, pk=self.kwargs['u_id'])
        contributors = Contributor.objects.filter(project=project, user=user)
        if contributors.exists():
            contributors.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "Error with your request."}, status=status.HTTP_404_NOT_FOUND)

    

class IssuesProjectDetail(APIView):
    """
    Vue permettant de manipuler les problèmes (issues) associés à un projet spécifique.

    La classe `IssuesProjectDetail` hérite de la classe `APIView` de Django Rest Framework.
    Elle est utilisée pour créer, récupérer, mettre à jour et supprimer des problèmes pour un projet spécifique.

    Méthodes:
    - `post` : Crée un nouveau problème pour le projet spécifié. L'utilisateur doit être l'auteur du projet ou un de ses contributeurs.
    - `get` : Récupère tous les problèmes liés au projet spécifié.
    - `put` : Met à jour un problème spécifique lié au projet. L'utilisateur doit être l'auteur du problème.
    - `delete` : Supprime un problème spécifique lié au projet. L'utilisateur doit être l'auteur du problème.
    
    Attributs:
    - `serializer_class` : Spécifie le sérialiseur à utiliser pour le traitement des données.
    - `permission_classes` : Spécifie les classes de permission à utiliser pour déterminer l'accès à la vue.
    """
    serializer_class = IssueSerializer
    permission_classes = [IsAuthenticated]

    def check_author_or_contributor(self, user, project):
        if project.author != user and not project.contributors.filter(user=user).exists():
            raise PermissionDenied("You are not allowed.")
    
    def check_author_issue(self, user, issue):
        if issue.author != user:
            raise PermissionDenied("You are not allowed.")

    def post(self, request, *args, **kwargs):
            project = get_object_or_404(Project, pk=self.kwargs['pk'])
            # Je vérifie si l'utilisateur est contributeur ou auteur du projet
            self.check_author_or_contributor(request.user, project)
            # Je récupère les données de la requête
            data = request.data
            # J'ajoute l'ID du projet aux données de la requête
            data['project'] = project.id
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save(project=project, author=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get_issues(self, project):
        issues = Issue.objects.filter(project=project)
        return issues
    
    def get_issue(self, project, id_issue):
        issue = Issue.objects.get(project=project, pk=id_issue)
        return issue

    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        # Je vérifie si l'utilisateur est contributeur ou auteur du projet
        self.check_author_or_contributor(request.user, project)
        issues = self.get_issues(project)
        serializer = self.serializer_class(issues, many=True)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        issue = self.get_issue(project, self.kwargs['id_issue'])
        self.check_author_issue(request.user, issue)
        # Je récupère les données de la requête
        data = request.data
        # Je m'assure que certains champs ne soient pas modifiés
        data['id'] = issue.id
        data['project'] = project.id
        data['author'] = issue.author
        serializer = self.serializer_class(issue, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        issue = self.get_issue(project, self.kwargs['id_issue'])
        self.check_author_issue(request.user, issue)
        issue.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
       

class CommentProjectDetail(APIView):
    """
    Vue permettant de manipuler les commentaires associés à un problème spécifique dans un projet.

    La classe `CommentProjectDetail` hérite de la classe `APIView` de Django Rest Framework.
    Elle est utilisée pour créer et récupérer les commentaires d'un problème spécifique d'un projet.

    Méthodes:
    - `post` : Crée un nouveau commentaire pour le problème spécifié dans un projet. L'utilisateur doit être l'auteur du projet ou un de ses contributeurs.
    - `get` : Récupère tous les commentaires liés au problème spécifié dans un projet.

    Attributs:
    - `serializer_class` : Spécifie le sérialiseur à utiliser pour le traitement des données.
    - `permission_classes` : Spécifie les classes de permission à utiliser pour déterminer l'accès à la vue.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def check_author_or_contributor(self, user, project):
        if project.author != user and not project.contributors.filter(user=user).exists():
            raise PermissionDenied("You are not allowed.")
    
    def check_issue_of_project(self, project, issue):
        if issue.project != project:
            raise PermissionDenied("You are not allowed.")

    def post(self, request, *args, **kwargs):
            project = get_object_or_404(Project, pk=self.kwargs['pk'])
            issue = get_object_or_404(Issue, pk=self.kwargs['id_issue'])
            # Je vérifie si l'utilisateur est contributeur ou auteur du projet
            # Je vérifie également si le problème fait bien parti du projet donné
            self.check_author_or_contributor(request.user, project)
            self.check_issue_of_project(project, issue)
            # Je récupère les données de la requête
            data = request.data
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save(issue=issue, author=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_comments(self, issue):
        issues = Comment.objects.filter(issue=issue)
        return issues
    
    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        issue = get_object_or_404(Issue, pk=self.kwargs['id_issue'])
        # Je vérifie si l'utilisateur est contributeur ou auteur du projet
        # Je vérifie également si le problème fait bien parti du projet donné
        self.check_author_or_contributor(request.user, project)
        self.check_issue_of_project(project, issue)
        comments = self.get_comments(issue)
        serializer = self.serializer_class(comments, many=True)
        return Response(serializer.data)


class CommentUpdateDelete(APIView):
    """
    Vue permettant de manipuler un commentaire spécifique associé à un problème dans un projet.

    La classe `CommentUpdateDelete` hérite de la classe `APIView` de Django Rest Framework.
    Elle est utilisée pour récupérer, mettre à jour et supprimer un commentaire spécifique d'un problème dans un projet.

    Méthodes:
    - `get` : Récupère un commentaire spécifique lié à un problème dans un projet.
    - `put` : Met à jour un commentaire spécifique lié à un problème dans un projet. L'utilisateur doit être l'auteur du commentaire.
    - `delete` : Supprime un commentaire spécifique lié à un problème dans un projet. L'utilisateur doit être l'auteur du commentaire.

    Attributs:
    - `serializer_class` : Spécifie le sérialiseur à utiliser pour le traitement des données.
    - `permission_classes` : Spécifie les classes de permission à utiliser pour déterminer l'accès à la vue.
    """
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def check_author_or_contributor(self, user, project):
        if project.author != user and not project.contributors.filter(user=user).exists():
            raise PermissionDenied("You are not allowed.")
    
    def check_issue_of_project(self, project, issue):
        if issue.project != project:
            raise PermissionDenied("You are not allowed.")
    
    def check_comment_of_issue(self, issue, comment):
        if comment.issue != issue:
            raise PermissionDenied("You are not allowed.")

    def check_author_of_comment(self, user, comment):
        if comment.author != user:
            raise PermissionDenied("You are not allowed.")

    def get_comments(self, issue):
        issues = Comment.objects.filter(issue=issue)
        return issues
    
    def get(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        issue = get_object_or_404(Issue, pk=self.kwargs['id_issue'])
        comment = get_object_or_404(Comment, pk=self.kwargs['id_comment'])
        # Je vérifie si l'utilisateur est contributeur ou auteur du projet
        # Je vérifie également si le problème fait bien parti du projet donné
        self.check_author_or_contributor(request.user, project)
        self.check_issue_of_project(project, issue)
        self.check_comment_of_issue(issue, comment)
        serializer = self.serializer_class(comment)
        return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        issue = get_object_or_404(Issue, pk=self.kwargs['id_issue'])
        comment = get_object_or_404(Comment, pk=self.kwargs['id_comment'])
        # Je vérifie si l'utilisateur est contributeur ou auteur du projet
        # Je vérifie également si le problème fait bien parti du projet donné
        self.check_author_or_contributor(request.user, project)
        self.check_author_of_comment(request.user, comment)
        self.check_issue_of_project(project, issue)
        self.check_comment_of_issue(issue, comment)
        # Je récupère les données de la requête
        # et je m'assure qu'on ne change que la description
        data = request.data
        data['id'] = comment.id
        data['author'] = comment.author
        data['issue'] = comment.issue
        data['created_time'] = comment.created_time
        serializer = self.serializer_class(comment, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        project = get_object_or_404(Project, pk=self.kwargs['pk'])
        issue = get_object_or_404(Issue, pk=self.kwargs['id_issue'])
        comment = get_object_or_404(Comment, pk=self.kwargs['id_comment'])
        # Je vérifie si l'utilisateur est contributeur ou auteur du projet
        # Je vérifie également si le problème fait bien parti du projet donné
        self.check_author_or_contributor(request.user, project)
        self.check_author_of_comment(request.user, comment)
        self.check_issue_of_project(project, issue)
        self.check_comment_of_issue(issue, comment)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
        