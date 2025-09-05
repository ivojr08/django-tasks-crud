from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Task
from .forms import TaskForm

def task_list(request: HttpRequest) -> HttpResponse:
    qs = Task.objects.all().order_by("-created_at")
    paginator = Paginator(qs, 10) # 10 tasks por pagina
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    tasks = Task.objects.all().order_by("-created_at")
    return render(request, "tasks/task_list.html", {"page_obj": page_obj})

def task_create(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Task criada com sucesso.")
            return redirect("task_list")
        # POST inválido -> volta o form com erros
        return render(request, "tasks/task_create.html", {"form": form})

    # GET -> sempre retorna o formulário
    form = TaskForm()
    return render(request, "tasks/task_create.html", {"form": form})

def task_edit(request: HttpRequest, pk: int) -> HttpResponse:
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            messages.success(request, "Task updated with success.")
            return redirect("task_list")
        return render(request, "tasks/task_edit.html", {"form": form, "task": task})
    form = TaskForm(instance=task)
    return render(request, "tasks/task_edit.html", {"form": form, "task": task})

def task_delete(request: HttpRequest, pk: int) -> HttpResponse:
    task = get_object_or_404(Task, pk=pk)
    if request.method == "POST":
        task.delete()
        messages.success(request, "Task excluded with success.")
        return redirect("task_list")
    # confirmação simples
    return render(request, "tasks/task_delete_confirm.html", {"task": task})

def task_toggle_status(request: HttpRequest, pk: int) -> HttpResponse:
    task = get_object_or_404(Task, pk=pk)
    task.status = "Completed" if task.status != "Completed" else "Pending"
    task.save(update_fields=["status"])
    messages.info(request, f"Status updated to: {task.status}.")
    return redirect("task_list")
