import os
import uuid
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Project, History, BaseProject
from django.views.generic import CreateView, UpdateView, DetailView
from .forms import HistoryForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .choices import PROJECTS
from .models import UserInput
from .forms import UserInputForm
from django.core.paginator import Paginator
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime

def base_project(request):
    base_projects = BaseProject.objects.all()
    base_project = BaseProject.objects.first()
    
    projects = base_project.project_set.all()
    history_list = History.objects.filter(project__in=projects)
    
    

    context = {
        'base_project': base_project,
        'base_projects': base_projects,
        'history_list': history_list,
    }

    return render(request, 'research/projects.html', context)



def project_history(request, pk):
    base_projects = BaseProject.objects.all()
    project = get_object_or_404(Project, pk=pk)
    project_history = History.objects.filter(project=project).order_by('-write_date')
    context = {
        'project': project,
        'history_list': project_history,
        'base_projects': base_projects,
        # Other context variables...
    }
    return render(request, 'research/projects.html', context)



class HistoryCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url="/members/login"
    model = History
    form_class = HistoryForm
    template_name = 'research/create.html'  # Replace with your template name
    success_url = reverse_lazy("research:projects")  # Replace with your success URL
    success_message =  "Added successfully"

    def form_valid(self, form):
        form.instance.writer = self.request.user  # Set the writer to the current user
        return super().form_valid(form)

def purechain_view(request):
    file_data = []  # List to hold data for saved entries

    if request.method == 'POST':
        form = UserInputForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            text_content = form.cleaned_data['text_content']
            files = request.FILES.getlist('files')  # Get multiple files

            # Save text content as a .txt file
            if text_content:
                text_path = os.path.join('uploads', f"{uuid.uuid4()}_{title}.txt")
                try:
                    default_storage.save(text_path, text_content.encode('utf-8'))
                    file_data.append({
                        "url": default_storage.url(text_path),
                        "title": title,
                        "text_content": text_content,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    })
                except Exception as e:
                    messages.error(request, f"Failed to save text content: {e}")

            # Save uploaded files
            for file in files:
                file_path = os.path.join('uploads', f"{uuid.uuid4()}_{file.name}")
                try:
                    default_storage.save(file_path, file)
                    file_data.append({
                        "url": default_storage.url(file_path),
                        "title": title,
                        "text_content": text_content if file.name.lower().endswith(".txt") else None,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    })
                except Exception as e:
                    messages.error(request, f"Failed to save file {file.name}: {e}")

            messages.success(request, "Files uploaded successfully.")
            return redirect('research:purechain_view')
    else:
        form = UserInputForm()

    # Fetch file list from storage
    files = default_storage.listdir('uploads')[1]  # List all files in the 'uploads' directory
    for file in files:
        # Default metadata
        file_entry = {
            "url": default_storage.url(f'uploads/{file}'),
            "title": file.split("_")[1] if "_" in file else "Unknown Title",
            "text_content": None,
            "timestamp": "Unknown",
        }

        # Check if the file is a text file to read its content
        if file.lower().endswith('.txt'):
            try:
                with default_storage.open(f'uploads/{file}', 'r') as f:
                    file_entry["text_content"] = f.read()  # Read the content of the text file
            except Exception as e:
                print(f"Error reading file content for {file}: {e}")

        # Simulate adding a timestamp (since no timestamps are currently stored)
        file_entry["timestamp"] = datetime.fromtimestamp(
            os.path.getmtime(default_storage.path(f'uploads/{file}'))
        ).strftime("%Y-%m-%d %H:%M:%S")

        file_data.append(file_entry)

    return render(request, 'research/purechain.html', {'form': form, 'files': file_data})

def delete_file(request, filename):
    if request.method == 'POST':
        file_path = f'uploads/{filename}'
        if default_storage.exists(file_path):
            default_storage.delete(file_path)
            messages.success(request, "File deleted successfully.")
        else:
            messages.error(request, "File not found.")
        return redirect('research:purechain_view')