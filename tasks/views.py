from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .models import Task
from .forms import TaskForm

# API REST (DRF)
from rest_framework import viewsets, status, filters, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import TaskSerializer

@login_required
def task_list(request: HttpRequest) -> HttpResponse:
    qs = Task.objects.filter(owner=request.user).order_by("-created_at")
    paginator = Paginator(qs, 10) # 10 tasks por pagina
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "tasks/task_list.html", {"page_obj":page_obj})

@login_required
def task_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.owner = request.user
            task.save()
            messages.success(request, "Task created with success.")
            return redirect("task_list")
        return render(request, "tasks/task_create_html", {"form":form})
    return render(request, "tasks/task_create.html", {"form":TaskForm()})

@login_required
def task_edit(request: HttpRequest, pk: int) -> HttpResponse:
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated with success.")
            return redirect("task_list")
        return render(request, "tasks/task_edit.html", {"form": form, "task": task})
    form = TaskForm(instance=task)
    return render(request, "tasks/task_edit.html", {"form": form, "task": task})

@login_required
def task_delete(request: HttpRequest, pk: int) -> HttpResponse:
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    if request.method == "POST":
        task.delete()
        messages.success(request, "Task excluded with success.")
        return redirect("task_list")
    # confirmação simples
    return render(request, "tasks/task_delete_confirm.html", {"task": task})

@login_required
def task_toggle_status(request: HttpRequest, pk: int) -> HttpResponse:
    task = get_object_or_404(Task, pk=pk, owner=request.user)
    task.status = "Completed" if task.status != "Completed" else "Pending"
    task.save(update_fields=["status"])
    messages.info(request, f"Status updated to: {task.status}.")
    return redirect("task_list")


class IsOwner(permissions.BasePermission):
    """
    Possible access the object just if the request.user is the owner
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner_id == request.user.id


class TaskViewSet(viewsets.ModelViewSet):
    """
    Endpoints REST:
    GET /api/tasks/
    POST /api/tasks/
    GET /api/tasks/{id}/
    PUT /api/tasks{id}/
    PATCH /api/tasks/{id}/
    DELETE /api/tasks/{id}/
    POST /api/tasks/{id}/toogle/
    """

    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'title']
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        qs = Task.objects.filter(owner=self.request.user).order_by('-created_at')

        done = self.request.query_params.get('done')
        if done is not None:
            val = str(done).lower()
            if val in ('true', '1'):
                qs = qs.filter(status='Completed')
            elif val in ('false', '0'):
                qs = qs.filter(status='Pending')
        return qs
    
    def perform_create(self, serializer):
        """
        Fill in the owner when creating
        """
        serializer.save(owner=self.request.user)


    @action(detail=True, methods=['post'])
    def toggle(self, request, pk=None):
        task = self.get_object()
        task.status = 'Pending' if task.status == 'Completed' else 'Completed'
        task.save(update_fields=['status'])
        serializer = self.get_serializer(task)
        return Response(serializer.data, status=status.HTTP_200_OK)