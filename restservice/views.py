from typing import Optional
from django.db.models.base import Model
from rest_framework import viewsets
from rest_framework.response import Response

from .models import UserModel, RecipeModel, StepModel, IngredientModel
from .serializers import (
    UserSerializer,
    RecipeSerializer,
    StepSerializer,
    IngredientSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    """Class for CRUD operations for User model."""

    http_method_names = ["get", "delete", "post", "put"]
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()


class BaseOneToManyViewSet(viewsets.ModelViewSet):
    """Base class for CRUD operations for models which have many to one foreign key."""

    _model: Optional[Model] = None
    _relation_primary_key: Optional[str] = None

    def create(self, request, *args, **kwargs):
        request.data[self._relation_primary_key] = kwargs[self._relation_primary_key]
        return super().create(request, *args, **kwargs)

    def list(self, request, *args, **kwargs):
        if self._relation_primary_key in kwargs:
            queryset = self._model.objects.filter(
                **{self._relation_primary_key: kwargs[self._relation_primary_key]}
            )
        else:
            queryset = self._model.objects.all()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class RecipeViewSet(BaseOneToManyViewSet):
    """Class for CRUD operations for Recipe model."""

    _model = RecipeModel
    _relation_primary_key = "user_id"
    queryset = _model.objects.all()
    serializer_class = RecipeSerializer

    def update(self, request, *args, **kwargs):
        instance = self._model.objects.get(pk=kwargs["pk"])
        request.data[self._relation_primary_key] = instance.user_id
        return super().update(request, *args, **kwargs)


class StepViewSet(BaseOneToManyViewSet):
    """Class for CRUD operations for Step model."""

    _model = StepModel
    _relation_primary_key = "recipe_id"
    queryset = _model.objects.all()
    serializer_class = StepSerializer


class IngredientViewSet(BaseOneToManyViewSet):
    """Class for CRUD operations for Ingredient model."""

    _model = IngredientModel
    _relation_primary_key = "recipe_id"
    queryset = _model.objects.all()
    serializer_class = IngredientSerializer
