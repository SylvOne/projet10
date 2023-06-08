"""
URL configuration for drfprojet10 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from api.views import (
    SignupView,
    ProjectList,
    ProjectDetail,
    ContributorsProjectDetail,
    IssuesProjectDetail,
    CommentProjectDetail,
    CommentUpdateDelete
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('signup/', SignupView.as_view(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('projects/', ProjectList.as_view(), name='projects_list'),
    path('projects/<int:pk>/', ProjectDetail.as_view(), name='projects_detail'),
    path('projects/<int:pk>/users/', ContributorsProjectDetail.as_view(), name='contributors_project_detail'),
    path(
        'projects/<int:pk>/users/<int:u_id>/',
        ContributorsProjectDetail.as_view(),
        name='contributors_project_detail'
    ),
    path('projects/<int:pk>/issues/', IssuesProjectDetail.as_view(), name='issues_project_detail'),
    path('projects/<int:pk>/issues/<int:id_issue>/', IssuesProjectDetail.as_view(), name='issues_project_detail'),
    path(
        'projects/<int:pk>/issues/<int:id_issue>/comments/',
        CommentProjectDetail.as_view(),
        name='comment_project_detail'
    ),
    path(
        'projects/<int:pk>/issues/<int:id_issue>/comments/<int:id_comment>/',
        CommentUpdateDelete.as_view(),
        name='comment_update_delete'
    ),
]
