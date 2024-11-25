import os
import uuid

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
                except Exception as e:
                    print(f"Error saving text file: {e}")

            # Save each uploaded file
            for file in files:
                file_path = os.path.join('uploads', f"{uuid.uuid4()}_{file.name}")
                try:
                    default_storage.save(file_path, file)
                except Exception as e:
                    print(f"Error saving file: {e}")

            return redirect('purechain_view')
    else:
        form = UserInputForm()

    # Fetch file list
    files = default_storage.listdir('uploads')[1]
    file_urls = [default_storage.url(f'uploads/{file}') for file in files]

    return render(request, 'research/purechain.html', {'form': form, 'files': file_urls})