from typing import Dict

from django.test import TestCase
from rest_framework.test import RequestsClient


class RecipeTestCase(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = RequestsClient()
        super().setUpClass()

    def setUp(self) -> None:
        self.user1 = self._create_test_user(
            {
                "username": "joe_black",
                "password": "password",
                "first_name": "Joe",
                "last_name": "Black",
                "email": "jblack@example.com",
            }
        )
        self.user2 = self._create_test_user(
            {
                "username": "cliff_booth",
                "password": "password",
                "first_name": "Cliff",
                "last_name": "Booth",
                "email": "cbooth@example.com",
            }
        )

    def test_get_user(self):
        response = self.client.get("/v1/users/1/")

        user = response.json()
        assert user["email"] == "jblack@example.com"
        assert response.status_code == 200

    def test_get_user_not_found(self):
        response = self.client.get("/v1/users/1111/")

        assert response.status_code == 404

    def test_create_recipe(self):
        new_recipe = self._create_test_recipe(
            user_id=self.user1["id"], data={"name": "Test Recipe"}
        )
        assert new_recipe == {
            "id": 1,
            "name": "Test Recipe",
            "user_id": 1,
            "steps": [],
            "ingredients": [],
        }

    def test_get_recipes_by_user_id(self):
        self._create_test_recipe(user_id=self.user1["id"], data={"name": "Test Recipe"})
        self._create_test_recipe(
            user_id=self.user2["id"], data={"name": "Another Recipe"}
        )
        response = self.client.get("/v1/users/1/recipes")
        assert response.status_code == 200
        recipes = response.json()
        assert recipes == [
            {
                "id": 1,
                "name": "Test Recipe",
                "user_id": 1,
                "steps": [],
                "ingredients": [],
            }
        ]

    def test_get_all_recipes(self):
        self._create_test_recipe(user_id=self.user1["id"], data={"name": "Test Recipe"})
        self._create_test_recipe(
            user_id=self.user2["id"], data={"name": "Another Recipe"}
        )
        response = self.client.get("/v1/recipes")
        assert response.status_code == 200
        assert response.json() == [
            {
                "id": 1,
                "name": "Test Recipe",
                "user_id": 1,
                "steps": [],
                "ingredients": [],
            },
            {
                "id": 2,
                "name": "Another Recipe",
                "user_id": 2,
                "steps": [],
                "ingredients": [],
            },
        ]

    def test_update_recipe(self):
        self._create_test_recipe(user_id=self.user1["id"], data={"name": "Test Recipe"})
        response = self.client.put(
            "/v1/recipes/1", {"name": "New Recipe"}, content_type="application/json"
        )
        assert response.status_code == 200
        assert response.json() == {
            "id": 1,
            "name": "New Recipe",
            "user_id": 1,
            "steps": [],
            "ingredients": [],
        }

    def test_delete_recipe(self):
        self._create_test_recipe(user_id=self.user1["id"], data={"name": "Test Recipe"})
        response = self.client.delete("/v1/recipes/1")
        assert response.status_code == 204
        assert self.client.get("/v1/recipes").json() == []

    def _create_test_user(self, data: Dict) -> Dict:
        response = self.client.post("/v1/users/", data, content_type="application/json")
        assert response.status_code == 201
        return response.json()

    def _create_test_recipe(self, user_id: int, data: Dict) -> Dict:
        response = self.client.post(
            f"/v1/users/{user_id}/recipes", data, content_type="application/json"
        )
        assert response.status_code == 201
        return response.json()


# TODO: Create tasks.py file content
# TODO: Create docker-compose.yaml
# TODO: Create README.md file content
