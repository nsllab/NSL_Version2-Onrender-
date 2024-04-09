from django.shortcuts import render
from .models import WeeklyReport, PostDocReport, Seminar, Review
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DetailView, ListView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import WeeklyReportForm, PostDocReportForm, SeminarForm, ReviewForm

# Create your views here.


def weekly_reports(request):
    wr = WeeklyReport.objects.all().order_by('-fr_dt')
    context = {
        'reports': wr
    }
    return render(request, 'works/weeklyreport/reports.html', context)

class WeeklyReportCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url="/members/login"
    model = WeeklyReport
    form_class = WeeklyReportForm  # Replace with your actual form
    template_name = 'works/weeklyreport/create.html'  # Replace with your template name
    success_url = reverse_lazy('works:weekly_reports')  # Replace with your success URL
    success_message =  "Report added successfully"

    def form_valid(self, form):
        form.instance.writer = self.request.user  # Set the writer to the current user
        return super().form_valid(form)

class WeeklyReportDetailView(DetailView):
    model = WeeklyReport
    template_name = 'works/weeklyreport/details.html'
    context_object_name = 'report'

class WeeklyReportUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = "/members/login/"
    model = WeeklyReport
    form_class = WeeklyReportForm
    template_name = 'works/weeklyreport/update.html'
    success_url = reverse_lazy('works:weekly_reports')
    success_message =  "Updated successfully"

    def form_valid(self, form):
        form.instance.writer = self.request.user
        return super().form_valid(form)


def post_doc_reports(request):
    wr = PostDocReport.objects.all().order_by('-fr_dt')
    context = {
        'reports': wr
    }
    return render(request, 'works/weeklyreport/post_doc_reports.html', context)

class PostDocReportCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url="/members/login"
    model = PostDocReport
    form_class = PostDocReportForm  # Replace with your actual form
    template_name = 'works/weeklyreport/post_doc_create.html'  # Replace with your template name
    success_url = reverse_lazy('works:post_doc_reports')  # Replace with your success URL
    success_message =  "Report added successfully"

    def form_valid(self, form):
        form.instance.writer = self.request.user  # Set the writer to the current user
        return super().form_valid(form)

class PostDocReportDetailView(DetailView):
    model = PostDocReport
    template_name = 'works/weeklyreport/post_doc_details.html'
    context_object_name = 'report'

class PostReportUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = "/members/login/"
    model = PostDocReport
    form_class = PostDocReportForm
    template_name = 'works/weeklyreport/post_doc_update.html'
    success_url = reverse_lazy('works:post_doc_reports')
    success_message =  "Updated successfully"

    def form_valid(self, form):
        form.instance.writer = self.request.user
        return super().form_valid(form)


def seminars(request):
    seminars = Seminar.objects.all().order_by('-write_date')
    context = {
        'seminars': seminars
    }
    return render(request, 'works/seminars/seminars.html', context)

class SeminarCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url="/members/login"
    model = Seminar
    form_class = SeminarForm  # Replace with your actual form
    template_name = 'works/seminars/create.html'  # Replace with your template name
    success_url = reverse_lazy('works:seminars')  # Replace with your success URL
    success_message =  "Seminar added successfully"

    def form_valid(self, form):
        form.instance.writer = self.request.user  # Set the writer to the current user
        return super().form_valid(form)

class SeminarUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url="/members/login"
    model = Seminar
    form_class = SeminarForm  # Replace with your actual form
    template_name = 'works/seminars/update.html'  # Replace with your template name
    success_url = reverse_lazy('works:seminars')  # Replace with your success URL
    success_message =  "Seminar updated successfully"

    def form_valid(self, form):
        form.instance.writer = self.request.user  # Set the writer to the current user
        return super().form_valid(form)

class ReviewListView(LoginRequiredMixin, ListView):
    model = Review
    context_object_name = 'reviews'
    template_name = 'works/reviews/review_list.html'
    # paginate_by = 10
   
    def get_queryset(self):
        return Review.objects.order_by('-write_date')




class ReviewCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url="/members/login"
    model = Review
    form_class = ReviewForm  # Replace with your actual form
    template_name = 'works/reviews/create.html'  # Replace with your template name
    success_url = reverse_lazy('works:reviews')  # Replace with your success URL
    success_message =  "Review added successfully"

    def form_valid(self, form):
        form.instance.writer = self.request.user  # Set the writer to the current user
        return super().form_valid(form)


class ReviewUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url="/members/login"
    model = Review
    form_class = ReviewForm  # Replace with your actual form
    template_name = 'works/reviews/update.html'  # Replace with your template name
    success_url = reverse_lazy('works:reviews')  # Replace with your success URL
    success_message =  "Review updated successfully"

    def form_valid(self, form):
        form.instance.writer = self.request.user  # Set the writer to the current user
        return super().form_valid(form)
