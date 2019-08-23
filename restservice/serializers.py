from typing import Optional
from django.db.models.base import Model
from rest_framework import serializers

from .models import StepModel, IngredientModel, RecipeModel, UserModel


class BaseSerializer(serializers.ModelSerializer):
    """Base serializer class for models which have many to one foreign key."""

    _related_model: Optional[Model] = None
    _related_model_filed: Optional[str] = None
    _related_primary_key: Optional[str] = None

    def create(self, validated_data):
        validated_data[self._related_model_filed] = self._related_model.objects.get(
            pk=self.initial_data[self._related_primary_key]
        )
        return super().create(validated_data)


class StepSerializer(BaseSerializer):
    _related_model = RecipeModel
    _related_model_filed = "recipe"
    _related_primary_key = "recipe_id"

    recipe_id = serializers.IntegerField(source="recipe.id", read_only=True)

    class Meta:
        model = StepModel
        fields = ("id", "step_text", "recipe_id")


class IngredientSerializer(BaseSerializer):
    _related_model = RecipeModel
    _related_model_filed = "recipe"
    _related_primary_key = "recipe_id"

    recipe_id = serializers.IntegerField(source="recipe.id", read_only=True)

    class Meta:
        model = IngredientModel
        fields = ("id", "text", "recipe_id")


class RecipeSerializer(BaseSerializer):
    _related_model = UserModel
    _related_model_filed = "user"
    _related_primary_key = "user_id"

    id = serializers.IntegerField(read_only=True)
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    steps = StepSerializer(many=True, read_only=True)
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = RecipeModel
        fields = ("id", "name", "user_id", "steps", "ingredients")

    def update(self, instance, validated_data):
        validated_data["user"] = UserModel.objects.get(pk=self.initial_data["user_id"])
        return super().update(instance, validated_data)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        extra_kwargs = {"password": {"write_only": True}}
        fields = ("id", "username", "password", "first_name", "last_name", "email")
