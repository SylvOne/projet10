from django.db import models
from django.contrib.auth.models import User

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    type = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')

class Contributor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

class Issue(models.Model):
    PRIORITY_CHOICES = [('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')]
    TAG_CHOICES = [('BUG', 'Bug'), ('TASK', 'Task'), ('ENHANCEMENT', 'Enhancement')]
    STATUS_CHOICES = [('TODO', 'To do'), ('ONGOING', 'Ongoing'), ('DONE', 'Done')]

    title = models.CharField(max_length=200)
    description = models.TextField()
    assignee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assigned_issues')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES)
    tag = models.CharField(max_length=15, choices=TAG_CHOICES)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='issues')
    created_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_issues')

class Comment(models.Model):
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='comments')
    created_time = models.DateTimeField(auto_now_add=True)
