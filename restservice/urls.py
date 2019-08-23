from django.urls import path, include
from rest_framework import routers

from restservice import views

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "users/<user_id>/recipes",
        views.RecipeViewSet.as_view({"get": "list", "post": "create"}),
    ),
    path("recipes", views.RecipeViewSet.as_view({"get": "list"})),
    path(
        "recipes/<pk>",
        views.RecipeViewSet.as_view({"delete": "destroy", "put": "update"}),
    ),
    path(
        "recipes/<recipe_id>/steps",
        views.StepViewSet.as_view({"get": "list", "post": "create"}),
    ),
    path(
        "recipes/<recipe_id>/ingredients",
        views.IngredientViewSet.as_view({"get": "list", "post": "create"}),
    ),
    path("steps/<pk>", views.StepViewSet.as_view({"delete": "destroy"})),
    path("steps", views.StepViewSet.as_view({"get": "list"})),
    path("ingredients/<pk>", views.IngredientViewSet.as_view({"delete": "destroy"})),
    path("ingredients", views.IngredientViewSet.as_view({"get": "list"})),
]
