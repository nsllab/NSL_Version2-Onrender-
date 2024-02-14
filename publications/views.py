from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Journal, Conference, Patent, Book
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import JournalForm, JournalUpdateForm, ConferenceForm, PatentForm, ConferenceUpdateForm, BookForm
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DetailView
from .choices import PAPER_STATUS, PAPER_TYPE
from django.urls import reverse_lazy
from django.contrib import messages

# Create your views here.
def journals(request):
    # query = request.GET.get('q')
    # print(f"QUery ########### {query}")
    journals = Journal.objects.order_by('-write_date')
    search = request.GET
    
    if 'title' in search:
        title = search['title']
        if title:
            journals = journals.filter(title__icontains=title)

    if 'year' in search:
        year = search['year']
        if year:
            journals = journals.filter(write_date__icontains=year)


    if 'journal_type' in search:
        journal_type = search['journal_type']
        if journal_type:
            journals = journals.filter(journal_type__iexact=journal_type)

    if 'status' in search:
        status = search['status']
        if status:
            journals = journals.filter(status__iexact=status)

    # if query:
    #     journals = journals.filter(
    #         Q(title__icontains=query) | Q(write_date__icontains=query)
    #     )
    
    paginator = Paginator(journals, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'journals': page_obj,
        'journal_type': PAPER_TYPE,
        'status': PAPER_STATUS,
    }
    return render(request, 'publications/journals/journals.html', context)

class JournalCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url = "/members/login/"
    model = Journal
    form_class = JournalForm  # Replace with your actual form
    template_name = ''  # publications/journals/create.html
    success_url = reverse_lazy('publications:journals')  # Replace with your success URL
    success_message =  "%(journal_name)s created successfully"

    def form_valid(self, form):
        form.instance.writer = self.request.user  # Set the writer to the current user
        return super().form_valid(form)


class JournalUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = "/members/login/"
    model = Journal
    form_class = JournalUpdateForm
    template_name = 'publications/journals/update.html'
    success_url = reverse_lazy('publications:journals')
    success_message =  "Updated successfully"

    def form_valid(self, form):
        form.instance.writer = self.request.user
        return super().form_valid(form)

# @login_required(login_url="/members/login")
# def journal_update(request, pk):
#     journal = get_object_or_404(Journal, pk=pk)

#     if request.method == 'POST':
#         form = JournalUpdateForm(request.POST, request.FILES, instance=journal)
        
#         if form.is_valid():
#             form.save()
#             messages.add_message(request, messages.SUCCESS, 'Update Successful')
#             return redirect('publications:journals')
#     else:
#         form = JournalUpdateForm(instance=journal)

#     context = {
#         'form': form,
#     }

#     return render(request, 'publications/journals/update.html', context)


class JournalDetailView(DetailView):
    model = Journal
    template_name = 'publications/journals/journal_details.html'
    context_object_name = 'journal'


def conferences(request):
    conferences = Conference.objects.order_by('-write_date')
    search = request.GET
    
    if 'title' in search:
        title = search['title']
        if title:
            conferences = conferences.filter(title__icontains=title)

    if 'writer' in search:
        writer = search['writer']
        print(f"{writer}gggg")
        if writer:
            conferences = conferences.filter(writer__iexact=writer)

    if 'year' in search:
        year = search['year']
        if year:
            conferences = conferences.filter(write_date__icontains=year)


    if 'conference_type' in search:
        conference_type = search['conference_type']
        if conference_type:
            conferences = conferences.filter(conference_type__iexact=conference_type)

    if 'status' in search:
        status = search['status']
        if status:
            conferences = conferences.filter(status__iexact=status)

    paginator = Paginator(conferences, 50)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'conferences': page_obj,
        'conference_type': PAPER_TYPE,
        'status': PAPER_STATUS,
    }
    return render(request, 'publications/conferences/conferences.html', context)



class ConferenceCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url="/members/login"
    model = Conference
    form_class = ConferenceForm  # Replace with your actual form
    template_name = 'publications/conferences/create.html'  # Replace with your template name
    success_url = reverse_lazy('publications:conferences')  # Replace with your success URL
    success_message =  "Conference added successfully"

    def form_valid(self, form):
        form.instance.writer = self.request.user  # Set the writer to the current user
        return super().form_valid(form)


class ConferenceUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = "/members/login/"
    model = Conference
    form_class = ConferenceUpdateForm
    template_name = 'publications/conferences/update.html'
    success_url = reverse_lazy('publications:conferences')
    success_message =  "Updated successfully"

    def form_valid(self, form):
        form.instance.writer = self.request.user
        return super().form_valid(form)

class ConferenceDetailView(DetailView):
    model = Conference
    template_name = 'publications/conferences/conference_details.html'
    context_object_name = 'conference'

# @login_required(login_url="/members/login")
# def conference_update(request, pk):
#     conference = get_object_or_404(Conference, pk=pk)

#     if request.method == 'POST':
#         form = ConferenceUpdateForm(request.POST, request.FILES, instance=conference)
        
#         if form.is_valid():
#             form.save()
#             messages.add_message(request, messages.SUCCESS, 'Update Successful')
#             return redirect('publications:conferences')
#     else:
#         form = ConferenceUpdateForm(instance=conference)

#     context = {
#         'form': form,
#     }

#     return render(request, 'publications/conferences/update.html', context)


def patents(request):
    patents = Patent.objects.order_by('-write_date')
    search = request.GET

    if 'subject' in search:
        subject = search['subject']
        if subject:
            patents = patents.filter(subject__icontains=subject)

    if 'year' in search:
        year = search['year']
        if year:
            patents = patents.filter(write_date__icontains=year)

    if 'patent_type' in search:
        patent_type = search['patent_type']
        if patent_type:
            patents = patents.filter(patent_type__iexact=patent_type)

    # international_patents = patents.filter(patent_type=1)
    # domestic_patents = patents.filter(patent_type=2)

    context = {
        'patents': patents,
        'patent_type': PAPER_TYPE
        # 'dom_pats': domestic_patents,
    }

    return render(request, 'publications/patents/patent_lists.html', context)



class PatentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url="/members/login"
    model = Patent
    form_class = PatentForm  # Replace with your actual form
    template_name = ''  # Replace with your template name
    success_url = reverse_lazy('publications:patents')  # Replace with your success URL
    success_message =  "Patent added successfully"

    def form_valid(self, form):
        form.instance.writer = self.request.user  # Set the writer to the current user
        return super().form_valid(form)


class PatentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = "/members/login/"
    model = Patent
    form_class = PatentForm
    template_name = ''
    success_url = reverse_lazy('publications:patents')
    success_message =  "Updated successfully"

# class PatentDetailView(DetailView):
#     model = Patent
#     template_name = ''
#     # template_name = 'publications/conferences/conference_details.html'
#     context_object_name = 'patent'


def books(request):
    books = Book.objects.order_by('-write_date')
    search = request.GET

    if 'title' in search:
        title = search['title']
        if title:
            books = books.filter(title__icontains=title)

    if 'year' in search:
        year = search['year']
        if year:
            books = books.filter(write_date__icontains=year)

    if 'book_type' in search:
        book_type = search['book_type']
        if book_type:
            books = books.filter(book_type__iexact=book_type)

    # international_patents = patents.filter(book_type=1)
    # domestic_patents = patents.filter(book_type=2)
    paginator = Paginator(books, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'books': page_obj,
        'book_type': PAPER_TYPE
        # 'dom_pats': domestic_patents,
    }

    return render(request, 'publications/books/book_lists.html', context)

class BookCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    login_url="/members/login"
    model = Book
    form_class = BookForm  # Replace with your actual form
    template_name = ''  # Replace with your template name
    success_url = reverse_lazy('publications:books')  # Replace with your success URL
    success_message =  "Book added successfully"

    def form_valid(self, form):
        form.instance.writer = self.request.user  # Set the writer to the current user
        return super().form_valid(form)

class BookUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    login_url = "/members/login/"
    model = Book
    form_class = BookForm
    template_name = 'publications/books/update.html'
    success_url = reverse_lazy('publications:books')
    success_message =  "Updated successfully"

    def form_valid(self, form):
        form.instance.writer = self.request.user  # Set the writer to the current user
        return super().form_valid(form)