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
            form.save()
            return redirect('purechain_view')
    else:
        form = UserInputForm()

    # Fetch all user inputs and paginate
    data_list = UserInput.objects.all().order_by('-created_at')
    paginator = Paginator(data_list, 10)  # Show 10 items per page
    page_number = request.GET.get('page')
    data = paginator.get_page(page_number)

    context = {'form': form, 'data': data}
    return render(request, 'research/purechain.html', context)

def delete_entry(request, pk):
    entry = get_object_or_404(UserInput, pk=pk)
    entry.delete()
    return redirect('purechain_view')