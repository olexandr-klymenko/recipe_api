from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserModel(AbstractUser):
    """AbstractUser with unique email field"""

    email = models.EmailField(_("email address"), unique=True, null=False, blank=False)

    def __str__(self):
        return self.email


class RecipeModel(models.Model):
    name = models.TextField(null=False, blank=False)
    user = models.ForeignKey(
        UserModel, on_delete=models.CASCADE, related_name="recipes"
    )

    def __str__(self):
        return f"The recipe for the user '{self.user.username}'"


class StepModel(models.Model):
    step_text = models.TextField(null=False, blank=False)
    recipe = models.ForeignKey(
        RecipeModel, on_delete=models.CASCADE, related_name="steps"
    )

    def __str__(self):
        return self.step_text


class IngredientModel(models.Model):
    text = models.TextField(null=False, blank=False)
    recipe = models.ForeignKey(
        RecipeModel, on_delete=models.CASCADE, related_name="ingredients"
    )

    def __str__(self):
        return self.text
