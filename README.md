DJANGO PROJECTS API

API REST para gerenciamento de projetos,desenvolvida com Python,Django e Django REST Framework.

REST API for project management, developed with Python, Django, and Django REST Framework.

Funcionalidades:
- CRIAR E LISTAR PROJETOS
- CONSULTAR DETALHES DE UM PROJETO
- ATUALIZAR PROJETOS COM PUT E PATCH
- EXCLUIR PROJETOS
- VALIDAR DADOS RECEBIDOS
- TESTES AUTOMATIZADOS

Features:
- Create and list projects
- View project details
- Update projects using PUT and PATCH
- Delete projects
- Validate incoming data
- Automated tests

Tecnologias:
- Python
- Django
- Django REST Framework
- SQLite
- Django Test Framework

Tecnologies:
- Python
- Django
- Django REST Framework
- SQLite
- Django Test Framework

Requisitos:
- Python instalado
- Git

Requirements:
- Python installed
- Git

Instalação:

Clone o repositório:

git clone URL_DO_SEU_REPOSITORIO
cd django-project

Crie e ative um ambiente virtual:

python -m venv venv
source venv/bin/activate

Instale as dependências:

python -m pip install -r requirements.txt

Aplique as migrações:

python manage.py migrate

Inicie o servidor:

python manage.py runserver.

Installation:

Clone the repository:

git clone YOUR_REPOSITORY_URL
cd django-project

Create and activate a virtual environment:

python -m venv venv
source venv/bin/activate

Install the dependencies:

python -m pip install -r requirements.txt

Apply migrations:

python manage.py migrate

Start the server:

python manage.py runserver

Endpoints principais:

Método	Endpoint	Descrição
GET	/api/projects/	Listar projetos
POST	/api/projects/	Criar projeto
GET	/api/projects/{id}/	Consultar projeto
PUT	/api/projects/{id}/	Atualizar projeto
PATCH	/api/projects/{id}/	Atualizar campos específicos
DELETE	/api/projects/{id}/	Excluir projeto

Key endpoints:

Method	Endpoint	Description
GET	/api/projects/	List projects
POST	/api/projects/	Create project
GET	/api/projects/{id}/	Retrieve project
PUT	/api/projects/{id}/	Update project
PATCH	/api/projects/{id}/	Update specific fields
DELETE	/api/projects/{id}/	Delete project

Documentação:

Com o servidor em execução, acesse:

Swagger: /api/docs/
Esquema OpenAPI: /api/schema/

Documentation:

With the server running, access:

Swagger: /api/docs/
OpenAPI schema: /api/schema/

Testes

Execute os testes automatizados:

python manage.py test projects

Tests

Run the automated tests:

Objetivo

Este projeto faz parte do meu aprendizado em desenvolvimento backend com Python e Django, com foco na construção de APIs REST, organização de código, testes automatizados e documentação.

