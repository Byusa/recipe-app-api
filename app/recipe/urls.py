"""
URL mappings for the recipe app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from recipe import views

# Create a router and register our viewsets with it.
router = DefaultRouter()
# this will create a URL for the recipe list and detail views
router.register('recipes', views.RecipeViewSet)

# app_name will help us do reverse lookups
app_name = 'recipe'

# urlpatterns will be used by the Django router
urlpatterns = [
    path('', include(router.urls)),
]
