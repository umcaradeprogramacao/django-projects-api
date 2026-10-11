from django.test import TestCase

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Project


class ProjectAPITests(APITestCase):
    def setUp(self):
        self.project = Project.objects.create(
            name="Projeto de teste",
            description="Descrição para testes automatizados.",
        )
        self.list_url = "/api/projects/"
        self.detail_url = f"/api/projects/{self.project.id}/"

    def test_list_projects(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_create_project(self):
        data = {
            "name": "Novo projeto",
            "description": "Criado pelo teste automatizado.",
        }

        response = self.client.post(self.list_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Project.objects.filter(name="Novo projeto").exists()
        )

    def test_retrieve_project(self):
        response = self.client.get(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["name"], "Projeto de teste")

    def test_patch_project(self):
        response = self.client.patch(
            self.detail_url,
            {"name": "Nome alterado"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.project.refresh_from_db()
        self.assertEqual(self.project.name, "Nome alterado")
        self.assertEqual(
            self.project.description,
            "Descrição para testes automatizados.",
        )

    def test_delete_project(self):
        response = self.client.delete(self.detail_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Project.objects.filter(id=self.project.id).exists()
        )

# Create your tests here.
