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
from .models import UserInput, UserFile
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
    if request.method == 'POST':
        form = UserInputForm(request.POST)
        if form.is_valid():
            user_input = form.save()  # Save the main entry
            
            # Handle multiple file uploads manually
            files = request.FILES.getlist('files')  # Fetch the list of files
            for file in files:
                UserFile.objects.create(user_input=user_input, file=file)
            
            messages.success(request, "Entry and files saved successfully!")
            return redirect('research:purechain_view')
        else:
            messages.error(request, "Failed to save the entry. Please check the form.")

    # Fetch entries with their files
    entries = UserInput.objects.prefetch_related('files').order_by('-created_at')
    form = UserInputForm()
    return render(request, 'research/purechain.html', {'form': form, 'entries': entries})

def delete_file(request, filename):
    # Delete file associated with an entry
    if request.method == 'POST':
        entry = get_object_or_404(UserInput, file=f'uploads/{filename}')
        if entry.file:
            entry.file.delete()
        entry.delete()
        messages.success(request, "Entry deleted successfully.")
        return redirect('research:purechain_view')