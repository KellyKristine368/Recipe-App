from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from recipe import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.recipes, name='home'),

    path('recipes/', views.recipe_list, name='recipe_list'),
    path('recipes/add/', views.create_recipe, name='create_recipe'),
    path('recipes/<int:id>/', views.recipe_detail, name='recipe_detail'),
    path('recipes/<int:id>/update/', views.update_recipe, name='update_recipe'),
    path('recipes/<int:id>/delete/', views.delete_recipe, name='delete_recipe'),

    path('categories/', views.category_list, name='categories'),
    path('categories/add/', views.add_category, name='add_category'),
    path('categories/<int:id>/edit/', views.edit_category, name='edit_category'),
    path('categories/<int:id>/delete/', views.delete_category, name='delete_category'),
    path('categories/<int:id>/', views.category_detail, name='category_detail'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
