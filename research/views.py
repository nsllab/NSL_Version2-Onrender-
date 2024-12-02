import os
import uuid
import json
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
from django.core.files.base import ContentFile

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

            # Check for duplicate titles
            existing_files = [
                os.path.splitext(file_entry["filename"])[0].split("_")[1]
                for file_entry in file_data
            ]
            if title in existing_files:
                messages.error(
                    request, f"An entry with the title '{title}' already exists."
                )
                return redirect("research:purechain_view")

            # Create a unique record for title, text content, and associated files
            entry_data = {
                "title": title,
                "text_content": text_content,
                "files": [],
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

            # Save each uploaded file and associate it with this entry
            for file in files:
                file_path = f'uploads/{uuid.uuid4()}_{file.name}'
                try:
                    default_storage.save(file_path, file)
                    entry_data["files"].append({
                        "filename": os.path.basename(file_path),
                        "url": default_storage.url(file_path)
                    })
                except Exception as e:
                    messages.error(request, f"Failed to save file {file.name}: {e}")

            # Save text content as part of JSON for this entry
            json_path = f'uploads/{uuid.uuid4()}_{title}.json'
            try:
                json_string = json.dumps(entry_data, ensure_ascii=False)  # Ensure non-ASCII characters
                default_storage.save(json_path, ContentFile(json_string))
                entry_data["json_url"] = default_storage.url(json_path)
                file_data.append(entry_data)
            except Exception as e:
                messages.error(request, f"Failed to save JSON content: {e}")

            messages.success(request, "Files and metadata uploaded successfully.")
            return redirect('research:purechain_view')
    else:
        form = UserInputForm()

    # Fetch file list from storage
    files = default_storage.listdir('uploads')[1]  # List all files in the 'uploads' directory
    for file in files:
        if file.lower().endswith('.json'):
            try:
                with default_storage.open(f'uploads/{file}', 'r') as f:
                    entry_data = json.load(f)
                    # Append JSON data (title, text content, files) to file_data
                    file_data.append(entry_data)
            except Exception as e:
                print(f"Error reading JSON file {file}: {e}")

    # Sort file data by timestamp
    file_data.sort(key=lambda x: x['timestamp'], reverse=True)

    return render(request, 'research/purechain.html', {'form': form, 'files': file_data})



def delete_file(request, filename):
    if request.method == 'POST':
        file_path = f'uploads/{filename}'
        try:
            if default_storage.exists(file_path):
                default_storage.delete(file_path)
                messages.success(request, "File deleted successfully.")
            else:
                messages.error(request, "File not found.")
        except Exception as e:
            messages.error(request, f"An error occurred while deleting the file: {e}")
        return redirect('research:purechain_view')
    
def entry_details(request, title):
    file_data = None
    files = default_storage.listdir('uploads')[1]
    for file in files:
        if file.lower().endswith('.json'):
            try:
                with default_storage.open(f'uploads/{file}', 'r') as f:
                    entry_data = json.load(f)
                    if entry_data["title"] == title:
                        file_data = entry_data
                        break
            except Exception as e:
                print(f"Error reading JSON file {file}: {e}")
    
    if not file_data:
        messages.error(request, "Entry not found.")
        return redirect('research:purechain_view')
    
    return render(request, 'research/entry_details.html', {'entry': file_data})