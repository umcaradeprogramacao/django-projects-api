import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from .models import Project
from rest_framework import generics
from .serializers import ProjectSerializer


def home(request):
    return HttpResponse("Minha primeira aplicação Django!")


def project_list(request):
    projects = Project.objects.all()

    data = [
        {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "created_at": project.created_at.isoformat(),
        }
        for project in projects
    ]

    return JsonResponse(data, safe=False)

@require_http_methods(["POST"])
def project_create(request):
    try:
        data = json.loads(request.body)

        name = data.get("name", "").strip()
        description = data.get("description", "").strip()

        if not name or not description:
            return JsonResponse(
                {"error": "Nome e descricao sao obrigatorios."},
                status=400,
            )
        project = Project.objects.create(
            name=name,
            description=description,
        )

        return JsonResponse(
            {
                "id": project.id,
                "name": project.name,
                "description": project.description,
            },
            status=201,
        )

    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse(
            {"error": "Json Invalido."},
            status=400,
        )

@require_http_methods(["GET", "PUT", "PATCH", "DELETE"])
def project_detail(request, project_id):
    project = get_object_or_404(Project, id=project_id)

    if request.method == "DELETE":
        project.delete()
        return JsonResponse({
            "message": "Projeto excluído com sucesso."
        })

    if request.method in ["PUT", "PATCH"]:
        try:
            data = json.loads(request.body)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return JsonResponse(
                {"error": "JSON inválido."},
                status=400,
            )

        if not isinstance(data, dict):
            return JsonResponse(
                {"error": "Envie um objeto JSON."},
                status=400,
            )

        if request.method == "PUT":
            if "name" not in data or "description" not in data:
                return JsonResponse(
                    {"error": "PUT exige name e description."},
                    status=400,
                )

        fields = ["name", "description"]
        updated = False

        for field in fields:
            if field in data:
                value = data[field]

                if not isinstance(value, str) or not value.strip():
                    return JsonResponse(
                        {"error": f"{field} deve ser um texto não vazio."},
                        status=400,
                    )

                setattr(project, field, value.strip())
                updated = True

        if not updated:
            return JsonResponse(
                {"error": "Nenhum campo válido para atualizar."},
                status=400,
            )

        project.save()

    return JsonResponse({
        "id": project.id,
        "name": project.name,
        "description": project.description,
        "created_at": project.created_at.isoformat(),
    })

class ProjectListCreateAPIView(generics.ListCreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

class ProjectDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer