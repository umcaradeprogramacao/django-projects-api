"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
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

from django.urls import path
from django.contrib import admin
from projects import views
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="home"),

    path("projects/", views.project_list,name="project-list"),
    path("projects/create/", views.project_create, name="project-create"),
    path("projects/<int:project_id>/",
    views.project_detail,
    name="project-detail",
    ),
    path(
        "api/projects/",
        views.ProjectListCreateAPIView.as_view(),
        name="api-project-list-create",
    ),
    path(
        "api/projects/<int:pk>/", 
        views.ProjectDetailAPIView.as_view(),
        name="api-project-detail",
    ),
    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    ]   
