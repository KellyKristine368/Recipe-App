"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from recipe import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.recipes, name='home'),
    path('create/', views.create_recipe, name='create_recipe'),
    path("recipes/", views.recipe_list, name="recipe_list"),
    path("recipes/<int:recipe_id>/", views.recipe_detail, name="recipe_detail"),
    path("recipes/add/", views.create_recipe, name="create_recipe"),
    path('<int:id>/update/', views.update_recipe, name='update_recipe'),
    path('<int:id>/delete/', views.delete_recipe, name='delete_recipe'),
    path('categories/', views.category_list, name='categories'),
    path('categories/add/', views.add_category, name='add_category'),
    



]
