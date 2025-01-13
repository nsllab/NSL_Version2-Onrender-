# views.py
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth import login, logout, authenticate, login
from .forms import MemberCreationForm, LoginForm, MemberUpdateForm, BioUpdateForm
from django.contrib import messages
from .models import Bio, Member
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import LoginRequiredMixin

def register_user(request):
    if request.method == 'POST':
        form = MemberCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # login(request, user)  # Log in the user after registration
            messages.add_message(request, messages.SUCCESS, f'Thanks for registering {user.username}. Contact admin to activate your account')
            return redirect('members:login')  # Redirect to the home page or any other page you want
    else:
        form = MemberCreationForm()

    return render(request, 'members/registration/registration.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                # Change the redirect to our new dashboard
                messages.add_message(request, messages.SUCCESS, f'Welcome back {user.username}')
                return redirect('members:dashboard')  # We'll create this URL pattern
            else:
                messages.add_message(request, messages.ERROR, 'Invalid Credentials. Login Unsuccessful. Contact Admin')
    else:
        form = LoginForm()

    return render(request, 'members/registration/login.html', {'form': form})

def logout_user(request):
    logout(request)
    messages.add_message(request, messages.SUCCESS, f'See you soon {request.user.username}')
    return redirect('publications:journals')


class MemberUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Member
    form_class = MemberUpdateForm
    template_name = 'members/registration/update_profile.html'  # Your template for updating profile
    success_url = reverse_lazy('pages:index')  # Redirect to the user's profile page
    success_message = "Profile successfully updated."

    def get_object(self, queryset=None):
        return self.request.user  # Get the currently logged-in user

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        existing_user = Member.objects.exclude(pk=self.request.user.pk).filter(username=username).exists()
        
        if existing_user:
            messages.add_message(self.request, messages.ERROR, 'Username already exists. Please choose a different username.')
            return self.form_invalid(form)
        
        return super().form_valid(form)

class MemberChangePasswordView(LoginRequiredMixin, SuccessMessageMixin, PasswordChangeView):
    template_name = 'members/registration/change_password.html'  # Your template for changing password
    success_url = reverse_lazy('pages:index')  # Redirect to the user's profile page
    success_message = "Your password was successfully updated."

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

# def professors_list(request):

#     bio = Bio.objects.filter(position=1)
#     context = {
#         'bios': bio,
#         'total': len(bio)
#         }
#     return render(request, 'members/professors.html', context)

class DashboardView(LoginRequiredMixin, DetailView):
    model = Member
    template_name = 'members/personal_account/dashboard.html'
    context_object_name = 'user'
    
    def get_object(self, queryset=None):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['bio'] = Bio.objects.filter(member=self.request.user).first()
        return context

class ProfessorsListView(ListView):
    model = Bio
    template_name = 'members/people/professors.html'
    context_object_name = 'bios'

    def get_queryset(self):
        return Bio.objects.filter(position=1).order_by('display_order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total'] = self.get_queryset().count()
        return context


class PostDocsListView(ListView):
    model = Bio
    template_name = 'members/people/post_docs.html'
    context_object_name = 'bios'

    def get_queryset(self):
        return Bio.objects.filter(position=2).order_by('display_order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total'] = self.get_queryset().count()
        return context

class PostDocDetailView(DetailView):
    model = Bio
    template_name = 'members/people/post_doc_detail.html'
    context_object_name = 'post_doc'



class FullTimeListView(ListView):
    model = Bio
    template_name = 'members/people/full_time.html'
    context_object_name = 'bios'

    def get_queryset(self):
        return Bio.objects.filter(position=3).order_by('display_order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total'] = self.get_queryset().count()
        return context


class FullTimeDetailView(DetailView):
    model = Bio
    template_name = 'members/people/full_time_detail.html'
    context_object_name = 'full_time'


class PartTimeListView(ListView):
    model = Bio
    template_name = 'members/people/part_time.html'
    context_object_name = 'bios'

    def get_queryset(self):
        return Bio.objects.filter(position=4).order_by('display_order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total'] = self.get_queryset().count()
        return context


class VisitingListView(ListView):
    model = Bio
    template_name = 'members/people/visiting.html'
    context_object_name = 'bios'

    def get_queryset(self):
        return Bio.objects.filter(position=9).order_by('display_order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total'] = self.get_queryset().count()
        return context

class AlumniPostDocListView(ListView):
    model = Bio
    template_name = 'members/people/post_doc_alumni.html'
    context_object_name = 'bios'

    def get_queryset(self):
        return Bio.objects.filter(position=7).order_by('display_order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total'] = self.get_queryset().count()
        return context

class AlumniGraduateListView(ListView):
    model = Bio
    template_name = 'members/people/graduate_alumni.html'
    context_object_name = 'bios'

    def get_queryset(self):
        return Bio.objects.filter(position=6).order_by('display_order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total'] = self.get_queryset().count()
        return context

class AdvisersListView(ListView):
    model = Bio
    template_name = 'members/people/advisers.html'
    context_object_name = 'bios'

    def get_queryset(self):
        return Bio.objects.filter(position=5).order_by('display_order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total'] = self.get_queryset().count()
        return context

class UnderGraduateListView(ListView):
    model = Bio
    template_name = 'members/people/undergraduate.html'
    context_object_name = 'bios'

    def get_queryset(self):
        return Bio.objects.filter(position=8).order_by('display_order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total'] = self.get_queryset().count()
        return context


class BioUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = "/members/login/"
    model = Bio
    form_class = BioUpdateForm
    template_name = 'members/bios/bio_update.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Updated successfully")
        return response

    def get_success_url(self):
        # Get the previous page from the session or default to some URL
        previous_page = self.request.session.get('previous_page', '/members/full_time/')
        return previous_page

    def get(self, request, *args, **kwargs):
        # Store the current page in the session before displaying the form
        self.request.session['previous_page'] = request.META.get('HTTP_REFERER', '/members/full_time/')
        return super().get(request, *args, **kwargs)