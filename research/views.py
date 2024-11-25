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
    file_data = []  # Initialize file data list

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
                        "basename": title,  # Use title instead of file name
                        "text_content": text_content,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    })
                except Exception as e:
                    print(f"Error saving text file: {e}")
                    messages.error(request, "Failed to save text content.")

            # Save each uploaded file
            for file in files:
                file_path = os.path.join('uploads', f"{uuid.uuid4()}_{file.name}")
                try:
                    default_storage.save(file_path, file)
                    
                    # Attach metadata for each file
                    file_data.append({
                        "url": default_storage.url(file_path),
                        "basename": title,  # Use title instead of file name
                        "text_content": None,
                        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    })
                except Exception as e:
                    print(f"Error saving file: {e}")
                    messages.error(request, f"Failed to save file: {file.name}")

            messages.success(request, "Files uploaded successfully.")
            return redirect('research:purechain_view')
    else:
        form = UserInputForm()

    # Fetch file list and preprocess file data
    files = default_storage.listdir('uploads')[1]
    file_data.extend([
        {
            "url": default_storage.url(f'uploads/{file}'),
            "basename": os.path.splitext(file)[0],  # Use the file name without extension
            "text_content": None,  # Replace with actual text if available
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
        for file in files
    ])

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