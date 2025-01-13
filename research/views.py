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
import re

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

# def purechain_view(request):
#     logger = logging.getLogger(__name__)
#     file_data = []  # List to hold all saved entries

#     if request.method == 'POST':
#         form = UserInputForm(request.POST, request.FILES)
#         if form.is_valid():
#             title = form.cleaned_data['title']
#             text_content = form.cleaned_data['text_content']
#             files = request.FILES.getlist('files')

#             sanitized_title = re.sub(r'[^\w\s-]', '', title).replace(' ', '_')  # Sanitize title
#             entry_data = {
#                 "title": title,
#                 "text_content": text_content,
#                 "files": [],
#                 "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
#             }

#             for file in files:
#                 unique_filename = f"{uuid.uuid4()}_{file.name}"
#                 file_path = f'uploads/{unique_filename}'
#                 try:
#                     default_storage.save(file_path, file)
#                     entry_data["files"].append({
#                         "filename": unique_filename,
#                         "url": default_storage.url(file_path),
#                     })
#                 except Exception as e:
#                     messages.error(request, f"Failed to save file {file.name}: {e}")

#             json_path = f'uploads/{sanitized_title}.json'
#             try:
#                 json_string = json.dumps(entry_data, ensure_ascii=False)
#                 default_storage.save(json_path, ContentFile(json_string))
#             except Exception as e:
#                 messages.error(request, f"Failed to save JSON metadata: {e}")

#             messages.success(request, "Files and metadata uploaded successfully.")
#             return redirect('research:purechain_view')
#     else:
#         form = UserInputForm()

#     # Fetch JSON files from storage
#     files = default_storage.listdir('uploads')[1]
#     logger.debug(f"Files in uploads: {files}")

#     for file in files:
#         if file.lower().endswith('.json'):
#             try:
#                 with default_storage.open(f'uploads/{file}', 'r') as f:
#                     entry_data = json.load(f)
#                     file_data.append(entry_data)
#             except json.JSONDecodeError:
#                 logger.error(f"Malformed JSON in file {file}. Skipping...")
#             except Exception as e:
#                 logger.error(f"Error reading JSON file {file}: {e}")

#     # Sort entries by timestamp (newest first)
#     file_data.sort(key=lambda x: x['timestamp'], reverse=True)
#     logger.debug(f"File data: {file_data}")

#     return render(request, 'research/purechain.html', {'form': form, 'files': file_data})

def generate_safe_filename(text):
    """Generate a filename safe string that preserves Korean characters"""
    # Convert spaces to underscores but preserve Korean
    filename = text.replace(' ', '_')
    # Remove unsafe characters but keep Korean
    filename = ''.join(char for char in filename 
                      if char.isalnum() 
                      or char in ('_', '-') 
                      or unicodedata.category(char).startswith(('Lo', 'Po')))
    return filename

def purechain_view(request):
    logger = logging.getLogger(__name__)
    file_data = []

    if request.method == 'POST':
        form = UserInputForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                title = form.cleaned_data['title']
                text_content = form.cleaned_data['text_content']
                files = request.FILES.getlist('files')

                # Generate a unique ID for this entry
                entry_id = str(uuid.uuid4())
                
                entry_data = {
                    "id": entry_id,
                    "title": title,  # Store original title with Korean
                    "text_content": text_content,
                    "files": [],
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }

                # Handle file uploads
                for file in files:
                    try:
                        original_filename = file.name
                        safe_filename = generate_safe_filename(original_filename)
                        unique_filename = f"{entry_id}_{safe_filename}"
                        file_path = os.path.join('uploads', unique_filename)

                        # Save file with proper encoding
                        with default_storage.open(file_path, 'wb+') as destination:
                            for chunk in file.chunks():
                                destination.write(chunk)

                        entry_data["files"].append({
                            "filename": unique_filename,
                            "url": default_storage.url(file_path),
                            "original_name": original_filename,  # Keep original name with Korean
                            "size": f"{file.size / 1024 / 1024:.1f} MB"
                        })
                        messages.success(request, f"Successfully uploaded {original_filename}")
                    except Exception as e:
                        messages.error(request, f"Failed to save file {original_filename}: {str(e)}")
                        logger.error(f"File upload error: {str(e)}")
                        continue

                # Save metadata with Korean support
                json_filename = f"{entry_id}.json"
                json_path = os.path.join('uploads', json_filename)
                try:
                    json_string = json.dumps(entry_data, ensure_ascii=False, indent=2)
                    with default_storage.open(json_path, 'w', encoding='utf-8') as f:
                        f.write(json_string)
                    messages.success(request, "Entry saved successfully!")
                except Exception as e:
                    messages.error(request, f"Failed to save entry metadata: {str(e)}")
                    logger.error(f"Metadata save error: {str(e)}")

                return redirect('research:purechain_view')

            except Exception as e:
                messages.error(request, f"An unexpected error occurred: {str(e)}")
                logger.error(f"Unexpected error: {str(e)}")
    else:
        form = UserInputForm()

    # Fetch existing entries with proper encoding
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
    logger = logging.getLogger(__name__)
    file_data = []

    if request.method == 'POST':
        form = UserInputForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                title = form.cleaned_data['title']
                text_content = form.cleaned_data['text_content']
                files = request.FILES.getlist('files')

                # Generate a unique ID for this entry
                entry_id = str(uuid.uuid4())
                
                entry_data = {
                    "id": entry_id,
                    "title": title,  # Store original title with Korean
                    "text_content": text_content,
                    "files": [],
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }

                # Handle file uploads
                for file in files:
                    try:
                        original_filename = file.name
                        safe_filename = generate_safe_filename(original_filename)
                        unique_filename = f"{entry_id}_{safe_filename}"
                        file_path = os.path.join('ackuploads', unique_filename)

                        # Save file with proper encoding
                        with default_storage.open(file_path, 'wb+') as destination:
                            for chunk in file.chunks():
                                destination.write(chunk)

                        entry_data["files"].append({
                            "filename": unique_filename,
                            "url": default_storage.url(file_path),
                            "original_name": original_filename,  # Keep original name with Korean
                            "size": f"{file.size / 1024 / 1024:.1f} MB"
                        })
                        messages.success(request, f"Successfully uploaded {original_filename}")
                    except Exception as e:
                        messages.error(request, f"Failed to save file {original_filename}: {str(e)}")
                        logger.error(f"File upload error: {str(e)}")
                        continue

                # Save metadata with Korean support
                json_filename = f"{entry_id}.json"
                json_path = os.path.join('ackuploads', json_filename)
                try:
                    json_string = json.dumps(entry_data, ensure_ascii=False, indent=2)
                    with default_storage.open(json_path, 'w', encoding='utf-8') as f:
                        f.write(json_string)
                    messages.success(request, "Entry saved successfully!")
                except Exception as e:
                    messages.error(request, f"Failed to save entry metadata: {str(e)}")
                    logger.error(f"Metadata save error: {str(e)}")

                return redirect('research:acknowl_view')

            except Exception as e:
                messages.error(request, f"An unexpected error occurred: {str(e)}")
                logger.error(f"Unexpected error: {str(e)}")
    else:
        form = UserInputForm()

    # Fetch existing entries with proper encoding
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
        deletion_performed = False
        files = default_storage.listdir('uploads')[1]
        
        # Clean the filename
        filename = filename.replace('/', '')  # Remove any path separators
        
        # Try to find the actual file
        file_to_delete = next((f for f in files if filename in f), None)
        
        # Delete the actual file if it exists
        if file_to_delete:
            try:
                file_path = f'uploads/{file_to_delete}'
                if default_storage.exists(file_path):
                    default_storage.delete(file_path)
                    deletion_performed = True
            except Exception as e:
                messages.error(request, f"Error deleting file: {str(e)}")

        # Find and delete associated JSON metadata
        try:
            json_files = [f for f in files if f.endswith('.json')]
            for json_file in json_files:
                json_path = f'uploads/{json_file}'
                try:
                    if default_storage.exists(json_path):
                        with default_storage.open(json_path, 'r') as f:
                            data = json.load(f)
                            # Check if this JSON contains our file
                            if any(filename in str(file_info.get('filename', '')) 
                                  for file_info in data.get('files', [])):
                                default_storage.delete(json_path)
                                deletion_performed = True
                                break
                except json.JSONDecodeError:
                    continue
        except Exception as e:
            messages.error(request, f"Error processing JSON files: {str(e)}")

        if deletion_performed:
            messages.success(request, "Entry deleted successfully.")
        else:
            messages.warning(request, "No matching files found to delete.")

        return redirect('research:purechain_view')

def ackdelete_file(request, filename):
    if request.method == 'POST':
        deletion_performed = False
        files = default_storage.listdir('ackuploads')[1]
        
        # Clean the filename
        filename = filename.replace('/', '')  # Remove any path separators
        
        # Try to find the actual file
        file_to_delete = next((f for f in files if filename in f), None)
        
        # Delete the actual file if it exists
        if file_to_delete:
            try:
                file_path = f'ackuploads/{file_to_delete}'
                if default_storage.exists(file_path):
                    default_storage.delete(file_path)
                    deletion_performed = True
            except Exception as e:
                messages.error(request, f"Error deleting file: {str(e)}")

        # Find and delete associated JSON metadata
        try:
            json_files = [f for f in files if f.endswith('.json')]
            for json_file in json_files:
                json_path = f'ackuploads/{json_file}'
                try:
                    if default_storage.exists(json_path):
                        with default_storage.open(json_path, 'r') as f:
                            data = json.load(f)
                            # Check if this JSON contains our file
                            if any(filename in str(file_info.get('filename', '')) 
                                  for file_info in data.get('files', [])):
                                default_storage.delete(json_path)
                                deletion_performed = True
                                break
                except json.JSONDecodeError:
                    continue
        except Exception as e:
            messages.error(request, f"Error processing JSON files: {str(e)}")

        if deletion_performed:
            messages.success(request, "Entry deleted successfully.")
        else:
            messages.warning(request, "No matching files found to delete.")

        return redirect('research:acknowl_view')
    
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

def ackentry_details(request, title):
    file_data = None
    files = default_storage.listdir('ackuploads')[1]
    for file in files:
        if file.lower().endswith('.json'):
            try:
                with default_storage.open(f'ackuploads/{file}', 'r') as f:
                    entry_data = json.load(f)
                    if entry_data["title"] == title:
                        file_data = entry_data
                        break
            except Exception as e:
                print(f"Error reading JSON file {file}: {e}")
    
    if not file_data:
        messages.error(request, "Entry not found.")
        return redirect('research:acknowl_view')
    
    return render(request, 'research/ackentry_details.html', {'entry': file_data})