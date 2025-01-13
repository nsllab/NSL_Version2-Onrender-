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
import unicodedata  # For Korean character handling

def safe_file_operation(operation, *args, **kwargs):
    """Wrapper for safe file operations with proper error handling"""
    try:
        return operation(*args, **kwargs)
    except OSError as e:
        logger.error(f"File operation error: {str(e)}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error in file operation: {str(e)}")
        raise

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
    if not text:
        return str(uuid.uuid4())
        
    # Convert spaces to underscores but preserve Korean
    filename = str(text).replace(' ', '_')
    # Remove unsafe characters but keep Korean and numbers
    filename = ''.join(char for char in filename 
                      if char.isalnum() 
                      or char in ('_', '-', '.')  # Added dot for file extensions
                      or unicodedata.category(char).startswith(('Lo', 'Po')))
    
    # Ensure the filename isn't empty after cleaning
    return filename if filename else str(uuid.uuid4())

def save_entry_metadata(entry_data, directory, title):
    """Helper function to save entry metadata"""
    try:
        # Generate unique filename
        entry_id = str(uuid.uuid4())
        json_filename = f"{entry_id}.json"
        json_path = os.path.join(directory, json_filename)
        
        # Convert to JSON string with Korean character support
        json_string = json.dumps(entry_data, ensure_ascii=False, indent=2)
        
        # Convert string to bytes with UTF-8 encoding
        json_bytes = json_string.encode('utf-8')
        
        # Create ContentFile with the encoded bytes
        content_file = ContentFile(json_bytes)
        
        # Save using default_storage
        default_storage.save(json_path, content_file)
        
        return json_path
    except Exception as e:
        logger.error(f"Error saving metadata: {str(e)}")
        raise

def read_entry_metadata(file_path):
    """Helper function to read entry metadata"""
    try:
        # Read file content as bytes
        with default_storage.open(file_path, 'rb') as f:
            content_bytes = f.read()
            
        # Decode bytes to string using UTF-8
        content_string = content_bytes.decode('utf-8')
        
        # Parse JSON
        if content_string.strip():
            return json.loads(content_string)
        return None
    except Exception as e:
        logger.error(f"Error reading metadata: {str(e)}")
        return None

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
                for file in files:
                    try:
                        original_filename = file.name
                        safe_filename = generate_safe_filename(original_filename)
                        unique_filename = f"{entry_data['id']}_{safe_filename}"
                        file_path = os.path.join('uploads', unique_filename)

                        # Save file
                        default_storage.save(file_path, file)

                        entry_data["files"].append({
                            "filename": unique_filename,
                            "url": default_storage.url(file_path),
                            "original_name": original_filename,
                            "size": f"{file.size / 1024 / 1024:.1f} MB"
                        })
                        messages.success(request, f"Successfully uploaded {original_filename}")
                    except Exception as e:
                        messages.error(request, f"Failed to save file {original_filename}: {str(e)}")
                        logger.error(f"File upload error: {str(e)}")
                        continue

                # Save metadata
                try:
                    save_entry_metadata(entry_data, 'uploads', title)
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

    # Load existing entries
    try:
        _, files = default_storage.listdir('uploads')
        json_files = [f for f in files if f.endswith('.json')]
        
        for json_file in json_files:
            try:
                file_path = os.path.join('uploads', json_file)
                entry_data = read_entry_metadata(file_path)
                if entry_data and isinstance(entry_data, dict):
                    file_data.append(entry_data)
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

def entry_details(request, title):
    try:
        _, files = default_storage.listdir('uploads')
        json_files = [f for f in files if f.endswith('.json')]
        
        for json_file in json_files:
            try:
                file_path = os.path.join('uploads', json_file)
                entry_data = read_entry_metadata(file_path)
                if entry_data and entry_data.get('title') == title:
                    return render(request, 'research/entry_details.html', {
                        'entry': entry_data
                    })
            except Exception as e:
                logger.error(f"Error reading JSON file {json_file}: {str(e)}")
                continue
    
    except Exception as e:
        logger.error(f"Error in entry_details: {str(e)}")
        messages.error(request, f"Error retrieving entry: {str(e)}")
    
    messages.error(request, "Entry not found.")
    return redirect('research:purechain_view')


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
                for file in files:
                    try:
                        original_filename = file.name
                        safe_filename = generate_safe_filename(original_filename)
                        unique_filename = f"{entry_data['id']}_{safe_filename}"
                        file_path = os.path.join('ackuploads', unique_filename)

                        # Save file
                        default_storage.save(file_path, file)

                        entry_data["files"].append({
                            "filename": unique_filename,
                            "url": default_storage.url(file_path),
                            "original_name": original_filename,
                            "size": f"{file.size / 1024 / 1024:.1f} MB"
                        })
                        messages.success(request, f"Successfully uploaded {original_filename}")
                    except Exception as e:
                        messages.error(request, f"Failed to save file {original_filename}: {str(e)}")
                        logger.error(f"File upload error: {str(e)}")
                        continue

                # Save metadata
                try:
                    save_entry_metadata(entry_data, 'ackuploads', title)
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

    # Load existing entries
    try:
        _, files = default_storage.listdir('ackuploads')
        json_files = [f for f in files if f.endswith('.json')]
        
        for json_file in json_files:
            try:
                file_path = os.path.join('ackuploads', json_file)
                entry_data = read_entry_metadata(file_path)
                if entry_data and isinstance(entry_data, dict):
                    file_data.append(entry_data)
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
                    entry_data = read_entry_metadata(json_path)
                    
                    if entry_data:
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
                            save_entry_metadata(entry_data, 'ackuploads', entry_data.get('title', ''))
                            
                except Exception as e:
                    logger.error(f"Error processing JSON file {json_file}: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error in ackdelete_file: {str(e)}")
            messages.error(request, f"Error deleting file: {str(e)}")
        
        return redirect('research:acknowl_view')

def ackentry_details(request, title):
    try:
        _, files = default_storage.listdir('ackuploads')
        json_files = [f for f in files if f.endswith('.json')]
        
        for json_file in json_files:
            try:
                file_path = os.path.join('ackuploads', json_file)
                entry_data = read_entry_metadata(file_path)
                if entry_data and entry_data.get('title') == title:
                    return render(request, 'research/ackentry_details.html', {
                        'entry': entry_data
                    })
            except Exception as e:
                logger.error(f"Error reading JSON file {json_file}: {str(e)}")
                continue
    
    except Exception as e:
        logger.error(f"Error in ackentry_details: {str(e)}")
        messages.error(request, f"Error retrieving entry: {str(e)}")
    
    messages.error(request, "Entry not found.")
    return redirect('research:acknowl_view')

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
                    entry_data = read_entry_metadata(json_path)
                    
                    if entry_data:
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
                            save_entry_metadata(entry_data, 'uploads', entry_data.get('title', ''))
                            
                except Exception as e:
                    logger.error(f"Error processing JSON file {json_file}: {str(e)}")
                    continue
                    
        except Exception as e:
            logger.error(f"Error in delete_file: {str(e)}")
            messages.error(request, f"Error deleting file: {str(e)}")
        
        return redirect('research:purechain_view')


    


