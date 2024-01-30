from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from members.models import Bio
from .models import Serendipity
from .forms import SerendipityForm

# Create your views here.


def index(request):
    profs = Bio.objects.filter(position=1)
    context = {
        'profs': profs,
        'total': len(profs),
        }
    return render(request, 'pages/index.html', context)

def serendipity(request):
    serens = Serendipity.objects.order_by('-write_date')
    search = request.GET
    
    if 'subject' in search:
        subject = search['subject']
        if subject:
            serens = serens.filter(subject__icontains=subject)

    if 'year' in search:
        year = search['year']
        if year:
            serens = serens.filter(write_date__icontains=year)

    context = {
        'serens': serens
    }
    return render(request, 'pages/serendipity/serendipity.html', context)

@login_required(login_url="/members/login")
def serendipity_create(request):
    if request.method == 'POST':
        form = SerendipityForm(request.POST)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.writer = request.user
            form_instance.save()
            return redirect('pages:serendipity')
        
    else:
        form = SerendipityForm()
    
    return redirect('pages:serendipity')

@login_required(login_url="/members/login")
def serendipity_update(request, pk):
    serendipity = get_object_or_404(Serendipity, pk=pk)

    if request.method == 'POST':
        form = SerendipityForm(request.POST, instance=serendipity)
        if form.is_valid():
            form_instance = form.save(commit=False)
            form_instance.writer = request.user
            form_instance.save()
            return redirect('pages:serendipity')  # Redirect back to the view page
    else:
        form = Serendipity(instance=serendipity)

    return redirect('pages:serendipity') 



class SerendipityCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url="/members/login"
    model = Serendipity
    form_class = SerendipityForm  # Replace with your actual form
    template_name = ''  # Replace with your template name
    success_url = reverse_lazy('pages:serendipity')  # Replace with your success URL
    success_message =  "Serendipity added successfully"

    def form_valid(self, form):
        form.instance.writer = self.request.user  # Set the writer to the current user
        return super().form_valid(form)


class SerendipityUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = "/members/login/"
    model = Serendipity
    form_class = SerendipityForm
    template_name = ''
    success_url = reverse_lazy('pages:serendipity')
    success_message =  "Updated successfully"