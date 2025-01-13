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
import unicodedata

logger = logging.getLogger(__name__)

def generate_safe_filename(text):
    """Generate a filename safe string that preserves Korean characters"""
    # Convert spaces to underscores but preserve Korean characters
    filename = text.replace(' ', '_')
    # Remove unsafe characters but keep Korean
    filename = ''.join(char for char in filename 
                      if char.isalnum() 
                      or char in ('_', '-') 
                      or unicodedata.category(char).startswith(('Lo', 'Po')))
    return filename

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
    }
    return render(request, 'research/projects.html', context)

class HistoryCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = "/members/login"
    model = History
    form_class = HistoryForm
    template_name = 'research/create.html'
    success_url = reverse_lazy("research:projects")
    success_message = "Added successfully"

    def form_valid(self, form):
        form.instance.writer = self.request.user
        return super().form_valid(form)

def save_uploaded_file(file, directory):
    """Helper function to save uploaded files"""
    try:
        original_filename = file.name
        safe_filename = generate_safe_filename(original_filename)
        unique_filename = f"{safe_filename}_{uuid.uuid4()}"
        file_path = os.path.join(directory, unique_filename)
        
        with default_storage.open(file_path, 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        return {
            "filename": unique_filename,
            "url": default_storage.url(file_path),
            "original_name": original_filename,
            "size": f"{file.size / 1024 / 1024:.1f} MB"
        }
    except Exception as e:
        logger.error(f"Error saving file {original_filename}: {str(e)}")
        raise

def save_entry_metadata(entry_data, directory, title):
    """Helper function to save entry metadata"""
    try:
        safe_title = generate_safe_filename(title)
        json_filename = f"{safe_title}_{uuid.uuid4()}.json"
        json_path = os.path.join(directory, json_filename)
        
        json_string = json.dumps(entry_data, ensure_ascii=False, indent=2)
        with default_storage.open(json_path, 'w', encoding='utf-8') as f:
            f.write(json_string)
        return json_path
    except Exception as e:
        logger.error(f"Error saving metadata: {str(e)}")
        raise

def purechain_view(request):
    file_data = []

    if request.method == 'POST':
        form = UserInputForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                title = form.cleaned_data['title']
                text_content = form.cleaned_data['text_content']
                files = request.FILES.getlist('files')

                entry_data = {
                    "id": str(uuid.uuid4()),
                    "title": title,
                    "text_content": text_content,
                    "files": [],
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }

                # Handle file uploads
                upload_dir = 'uploads'
                for file in files:
                    try:
                        file_info = save_uploaded_file(file, upload_dir)
                        entry_data["files"].append(file_info)
                        messages.success(request, f"Successfully uploaded {file_info['original_name']}")
                    except Exception as e:
                        messages.error(request, f"Failed to save file {file.name}: {str(e)}")
                        continue

                # Save metadata
                try:
                    save_entry_metadata(entry_data, upload_dir, title)
                    messages.success(request, "Entry saved successfully!")
                except Exception as e:
                    messages.error(request, f"Failed to save entry metadata: {str(e)}")
                
                return redirect('research:purechain_view')
                
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                messages.error(request, f"An unexpected error occurred: {str(e)}")
    else:
        form = UserInputForm()

    # Load existing entries
    try:
        _, files = default_storage.listdir('uploads')
        json_files = [f for f in files if f.endswith('.json')]
        
        for json_file in json_files:
            try:
                file_path = os.path.join('uploads', json_file)
                with default_storage.open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        entry_data = json.loads(content)
                        if isinstance(entry_data, dict):
                            file_data.append(entry_data)
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error for {json_file}: {str(e)}")
            except Exception as e:
                logger.error(f"Error reading file {json_file}: {str(e)}")

        file_data.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
    except Exception as e:
        logger.error(f"Error fetching files: {str(e)}")
        messages.error(request, "Error loading existing entries")

    context = {
        'form': form, 
        'files': file_data,
        'page_title': 'File Upload and Management',
        'has_files': bool(file_data)
    }
    
    return render(request, 'research/purechain.html', context)

def acknowl_view(request):
    file_data = []

    if request.method == 'POST':
        form = UserInputForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                title = form.cleaned_data['title']
                text_content = form.cleaned_data['text_content']
                files = request.FILES.getlist('files')

                entry_data = {
                    "id": str(uuid.uuid4()),
                    "title": title,
                    "text_content": text_content,
                    "files": [],
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }

                # Handle file uploads
                upload_dir = 'ackuploads'
                for file in files:
                    try:
                        file_info = save_uploaded_file(file, upload_dir)
                        entry_data["files"].append(file_info)
                        messages.success(request, f"Successfully uploaded {file_info['original_name']}")
                    except Exception as e:
                        messages.error(request, f"Failed to save file {file.name}: {str(e)}")
                        continue

                # Save metadata
                try:
                    save_entry_metadata(entry_data, upload_dir, title)
                    messages.success(request, "Entry saved successfully!")
                except Exception as e:
                    messages.error(request, f"Failed to save entry metadata: {str(e)}")
                
                return redirect('research:acknowl_view')
                
            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                messages.error(request, f"An unexpected error occurred: {str(e)}")
    else:
        form = UserInputForm()

    # Load existing entries
    try:
        _, files = default_storage.listdir('ackuploads')
        json_files = [f for f in files if f.endswith('.json')]
        
        for json_file in json_files:
            try:
                file_path = os.path.join('ackuploads', json_file)
                with default_storage.open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read().strip()
                    if content:
                        entry_data = json.loads(content)
                        if isinstance(entry_data, dict):
                            file_data.append(entry_data)
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error for {json_file}: {str(e)}")
            except Exception as e:
                logger.error(f"Error reading file {json_file}: {str(e)}")

        file_data.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        
    except Exception as e:
        logger.error(f"Error fetching files: {str(e)}")
        messages.error(request, "Error loading existing entries")

    context = {
        'form': form, 
        'files': file_data,
        'page_title': 'File Upload and Management',
        'has_files': bool(file_data)
    }
    
    return render(request, 'research/acknowl.html', context)

def delete_file(request, filename):
    if request.method == 'POST':
        try:
            files = default_storage.listdir('uploads')[1]
            
            # Clean the filename
            filename = generate_safe_filename(filename)
            
            # Delete the actual file
            file_path = os.path.join('uploads', filename)
            if default_storage.exists(file_path):
                default_storage.delete(file_path)
                messages.success(request, "File deleted successfully.")
            
            # Update or delete associated JSON metadata
            json_files = [f for f in files if f.endswith('.json')]
            for json_file in json_files:
                try:
                    json_path = os.path.join('uploads', json_file)
                    with default_storage.open(json_path, 'r', encoding='utf-8') as f:
                        entry_data = json.loads(f.read())
                    
                    # Remove the file from the entry's files list
                    entry_data['files'] = [
                        f for f in entry_data.get('files', [])
                        if f.get('filename') != filename
                    ]
                    
                    # If no files and no content, delete the entry
                    if not entry_data['files'] and not entry_data.get('text_content'):
                        default_storage.delete(json_path)
                    else:
                        # Update the JSON file
                        json_string = json.dumps(entry_data, ensure_ascii=False, indent=2)
                        with default_storage.open(json_path, 'w', encoding='utf-8') as f:
                            f.write(json_string)
                            
                except Exception as e:
                    logger.error(f"Error processing JSON file {json_file}: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error in delete_file: {str(e)}")
            messages.error(request, f"Error deleting file: {str(e)}")
        
        return redirect('research:purechain_view')

def ackdelete_file(request, filename):
    if request.method == 'POST':
        try:
            files = default_storage.listdir('ackuploads')[1]
            
            # Clean the filename
            filename = generate_safe_filename(filename)
            
            # Delete the actual file
            file_path = os.path.join('ackuploads', filename)
            if default_storage.exists(file_path):
                default_storage.delete(file_path)
                messages.success(request, "File deleted successfully.")
            
            # Update or delete associated JSON metadata
            json_files = [f for f in files if f.endswith('.json')]
            for json_file in json_files:
                try:
                    json_path = os.path.join('ackuploads', json_file)
                    with default_storage.open(json_path, 'r', encoding='utf-8') as f:
                        entry_data = json.loads(f.read())
                    
                    # Remove the file from the entry's files list
                    entry_data['files'] = [
                        f for f in entry_data.get('files', [])
                        if f.get('filename') != filename
                    ]
                    
                    # If no files and no content, delete the entry
                    if not entry_data['files'] and not entry_data.get('text_content'):
                        default_storage.delete(json_path)
                    else:
                        # Update the JSON file
                        json_string = json.dumps(entry_data, ensure_ascii=False, indent=2)
                        with default_storage.open(json_path, 'w', encoding='utf-8') as f:
                            f.write(json_string)
                            
                except Exception as e:
                    logger.error(f"Error processing JSON file {json_file}: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error in ackdelete_file: {str(e)}")
            messages.error(request, f"Error deleting file: {str(e)}")
        
        return redirect('research:acknowl_view')

def entry_details(request, title):
    try:
        _, files = default_storage.listdir('uploads')
        json_files = [f for f in files if f.endswith('.json')]
        
        for json_file in json_files:
            try:
                file_path = os.path.join('uploads', json_file)
                with default_storage.open(file_path, 'r', encoding='utf-8') as f:
                    entry_data = json.loads(f.read().strip())
                    if entry_data.get('title') == title:
                        return render(request, 'research/entry_details.html', {
                            'entry': entry_data
                        })
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error for {json_file}: {str(e)}")
            except Exception as e:
                logger.error(f"Error reading JSON file {json_file}: {str(e)}")
                continue
    
    except Exception as e:
        logger.error(f"Error in entry_details: {str(e)}")
        messages.error(request, f"Error retrieving entry: {str(e)}")
    
    messages.error(request, "Entry not found.")
    return redirect('research:purechain_view')

def ackentry_details(request, title):
    try:
        _, files = default_storage.listdir('ackuploads')
        json_files = [f for f in files if f.endswith('.json')]
        
        for json_file in json_files:
            try:
                file_path = os.path.join('ackuploads', json_file)
                with default_storage.open(file_path, 'r', encoding='utf-8') as f:
                    entry_data = json.loads(f.read().strip())
                    if entry_data.get('title') == title:
                        return render(request, 'research/ackentry_details.html', {
                            'entry': entry_data
                        })
            except json.JSONDecodeError as e:
                logger.error(f"JSON decode error for {json_file}: {str(e)}")
            except Exception as e:
                logger.error(f"Error reading JSON file {json_file}: {str(e)}")
                continue
    
    except Exception as e:
        logger.error(f"Error in ackentry_details: {str(e)}")
        messages.error(request, f"Error retrieving entry: {str(e)}")
    
    messages.error(request, "Entry not found.")
    return redirect('research:acknowl_view')