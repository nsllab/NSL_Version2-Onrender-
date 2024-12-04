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
import logging

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
    logger = logging.getLogger(__name__)
    file_data = []  # List to hold all saved entries

    if request.method == 'POST':
        form = UserInputForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            text_content = form.cleaned_data['text_content']
            files = request.FILES.getlist('files')

            sanitized_title = re.sub(r'[^\w\s-]', '', title).replace(' ', '_')  # Sanitize title
            entry_data = {
                "title": title,
                "text_content": text_content,
                "files": [],
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }

            for file in files:
                unique_filename = f"{uuid.uuid4()}_{file.name}"
                file_path = f'uploads/{unique_filename}'
                try:
                    default_storage.save(file_path, file)
                    entry_data["files"].append({
                        "filename": unique_filename,
                        "url": default_storage.url(file_path),
                    })
                except Exception as e:
                    messages.error(request, f"Failed to save file {file.name}: {e}")

            json_path = f'uploads/{sanitized_title}.json'
            try:
                json_string = json.dumps(entry_data, ensure_ascii=False)
                default_storage.save(json_path, ContentFile(json_string))
            except Exception as e:
                messages.error(request, f"Failed to save JSON metadata: {e}")

            messages.success(request, "Files and metadata uploaded successfully.")
            return redirect('research:purechain_view')
    else:
        form = UserInputForm()

    # Fetch JSON files from storage
    files = default_storage.listdir('uploads')[1]
    logger.debug(f"Files in uploads: {files}")

    for file in files:
        if file.lower().endswith('.json'):
            try:
                with default_storage.open(f'uploads/{file}', 'r') as f:
                    entry_data = json.load(f)
                    file_data.append(entry_data)
            except json.JSONDecodeError:
                logger.error(f"Malformed JSON in file {file}. Skipping...")
            except Exception as e:
                logger.error(f"Error reading JSON file {file}: {e}")

    # Sort entries by timestamp (newest first)
    file_data.sort(key=lambda x: x['timestamp'], reverse=True)
    logger.debug(f"File data: {file_data}")

    return render(request, 'research/purechain.html', {'form': form, 'files': file_data})

def delete_file(request, filename):
    if request.method == 'POST':
        # Search for file with or without UUID
        files = default_storage.listdir('uploads')[1]
        file_to_delete = next((f for f in files if f.endswith(filename)), None)

        if not file_to_delete:
            messages.error(request, "File not found.")
            return redirect('research:purechain_view')

        file_path = f'uploads/{file_to_delete}'
        
        # Find and delete the associated JSON metadata file
        json_files = [f for f in files if f.lower().endswith('.json')]
        for json_file in json_files:
            try:
                with default_storage.open(f'uploads/{json_file}', 'r') as f:
                    entry_data = json.load(f)
                    # Check if this JSON file contains metadata for any of the deleted files
                    if any(file_info['filename'] == file_to_delete for file_info in entry_data.get('files', [])):
                        # Delete the JSON metadata file
                        json_path = f'uploads/{json_file}'
                        if default_storage.exists(json_path):
                            default_storage.delete(json_path)
            except Exception as e:
                messages.error(request, f"Error processing JSON file {json_file}: {e}")
                continue

        try:
            # Delete the actual file
            if default_storage.exists(file_path):
                default_storage.delete(file_path)
                messages.success(request, "File and associated metadata deleted successfully.")
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