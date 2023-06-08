from rest_framework import serializers
from .models import Project, Contributor, Issue, Comment


class ProjectSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle `Project`.

    Attributs:
    - `model` : Définit le modèle qui doit être sérialisé/désérialisé.
    - `fields` : Définit les champs du modèle qui doivent être inclus dans la forme sérialisée.
    - `read_only_fields` : Définit les champs qui ne doivent pas être modifiés lors des opérations de mise à jour.
    """
    class Meta:
        model = Project
        fields = ['id', 'title', 'description', 'type', 'author', 'created_time']
        read_only_fields = ['created_time', 'author']

class ContributorSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle `Contributor`.

    Attributs:
    - `model` : Définit le modèle qui doit être sérialisé/désérialisé.
    - `fields` : Définit les champs du modèle qui doivent être inclus dans la forme sérialisée.
    - `read_only_fields` : Définit les champs qui ne doivent pas être modifiés lors des opérations de mise à jour.
    """
    class Meta:
        model = Contributor
        fields = ['id', 'user', 'project']
        read_only_fields = ['project']

class IssueSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle `Issue`.

    Attributs:
    - `model` : Définit le modèle qui doit être sérialisé/désérialisé.
    - `fields` : Définit les champs du modèle qui doivent être inclus dans la forme sérialisée.
    - `read_only_fields` : Définit les champs qui ne doivent pas être modifiés lors des opérations de mise à jour.
    """
    class Meta:
        model = Issue
        fields = ['id', 'title', 'description', 'assignee', 'priority', 'tag', 'status', 'project', 'created_time', 'author']
        read_only_fields = ['created_time', 'author']

class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer pour le modèle `Comment`.

    Attributs:
    - `model` : Définit le modèle qui doit être sérialisé/désérialisé.
    - `fields` : Définit les champs du modèle qui doivent être inclus dans la forme sérialisée.
    - `read_only_fields` : Définit les champs qui ne doivent pas être modifiés lors des opérations de mise à jour.
    """
    class Meta:
        model = Comment
        fields = ['id', 'description', 'author', 'issue', 'created_time']
        read_only_fields = ['created_time', 'author', 'issue']