
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from .models import Project


class ProjectAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="usuario_teste",
            password="senha_teste_123",
        )
        self.token = Token.objects.create(user=self.user)
        self.client.force_authenticate(user=self.user)

        self.project = Project.objects.create(
            name="Projeto de teste",
            description="Descrição para testes automatizados.",
            owner=self.user,
        )

        self.list_url = "/api/projects/"
        self.detail_url = f"/api/projects/{self.project.id}/"


    def test_user_cannot_retrieve_another_users_project(self):
        another_user = User.objects.create_user(
            username="outro_usuario",
            password="senha_teste_456",
        )

        another_project = Project.objects.create(
            name="Projeto de outra pessoa",
            description="Este projeto pertence a outro usuário.",
            owner=another_user,
        )

        response = self.client.get(
            f"/api/projects/{another_project.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

    def test_user_cannot_update_another_users_project(self):
        another_user = User.objects.create_user(
            username="outro_usuario_2",
            password="senha_teste_789",
        )

        another_project = Project.objects.create(
            name="Projeto protegido",
            description="Não deve ser alterado por outro usuário.",
            owner=another_user,
        )

        response = self.client.patch(
            f"/api/projects/{another_project.id}/",
            {"name": "Tentativa de alteração"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

        another_project.refresh_from_db()
        self.assertEqual(
            another_project.name,
            "Projeto protegido",
        )

    def test_anonymous_user_cannot_update_project(self):
        self.client.force_authenticate(user=None)

        response = self.client.patch(
            self.detail_url,
            {"name": "Alteração não autorizada"},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.project.refresh_from_db()
        self.assertEqual(self.project.name, "Projeto de teste")

    def test_anonymous_user_cannot_delete_project(self):
        self.client.force_authenticate(user=None)

        response = self.client.delete(self.detail_url)

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

        self.assertTrue(
            Project.objects.filter(id=self.project.id).exists()
        )

    def test_token_authentication_can_create_project(self):
        self.client.force_authenticate(user=None)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Token {self.token.key}"
        )

        response = self.client.post(
            self.list_url,
            {
                "name": "Projeto via token",
                "description": "Criado usando autenticação por token.",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_list_projects(self):
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_create_project(self):
        data = {
            "name": "Novo projeto",
            "description": "Criado pelo teste automatizado.",
        }

        response = self.client.post(
            self.list_url,
            data,
            format="json",
        )

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

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )
        self.assertFalse(
            Project.objects.filter(id=self.project.id).exists()
        )


    def test_anonymous_user_cannot_create_project(self):
        self.client.force_authenticate(user=None)

        data = {
            "name": "Projeto não autorizado",
            "description": "Este projeto não deve ser criado.",
        }

        response = self.client.post(
            self.list_url,
            data,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_403_FORBIDDEN,
        )

    
    def test_user_cannot_delete_another_users_project(self):
        another_user = User.objects.create_user(
            username="outro_usuario_3",
            password="senha_teste_987",
        )

        another_project = Project.objects.create(
            name="Projeto que deve ser protegido",
            description="Não deve ser excluído por outro usuário.",
            owner=another_user,
        )

        response = self.client.delete(
            f"/api/projects/{another_project.id}/"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_404_NOT_FOUND,
        )

        self.assertTrue(
            Project.objects.filter(id=another_project.id).exists()
        )