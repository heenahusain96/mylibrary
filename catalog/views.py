from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from .models import Book, Author, Genre, Language
from .models import BookInstance
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse
from catalog.forms import AddBookForm, SignUpForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import Group
# Create your views here.
# from catalog.models import Book, Author, BookInstance, Genre

def landing_page(request):
    """
    Landing Page will contain signup form
    """
    if request.method=='POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user_obj = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            group = Group.objects.get(name="Library Members")
            user_obj.groups.add(group)
            ## USer Authentication Part
            # user = authenticate(username=username, password=password)
            # login(request, user)
            # return redirect('login')
            return HttpResponseRedirect(reverse('login'))

    else:
        form = SignUpForm(initial ={})
    return render(request, 'landing_page.html', {'form': form})
    # return render(request, 'landing_page.html', context=context)

@login_required
def home_page(request):
    context = {}
    ## Number of visits to this view as counted by the session object
    num_visits = request.session.get("num_visits",0)
    request.session["num_visits"] = num_visits + 1
    context = {
        "num_visits" : num_visits
    }
    return render(request, 'index.html', context=context)

class BookListView(PermissionRequiredMixin,LoginRequiredMixin, generic.ListView):
    login_url = '/accounts/login/'
    permission_required = 'catalog.can_add_book'
    # redirect_field_name = "/home/"
    model = BookInstance
    template_name ='catalog/book_list.html'
    paginate_by = 9
    def get_queryset(self):
        return BookInstance.objects.filter(book_owner=self.request.user).order_by('added_on')


class BookDetailView(generic.DetailView):
    model = BookInstance
    # model = Book
    template_name ='catalog/book_detail.html'
    def get_queryset(self):
        return BookInstance.objects.filter(book_owner=self.request.user)

@permission_required('catalog.can_add_book')
def add_book_collection(request):
    # import pdb; pdb.set_trace()
    # If this is a POST request then process the Form data
    # If the method is post that means the form is submitted
    # If the method is get then the form is being called for the first time
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = AddBookForm(request.POST)
        if form.is_valid():
            # add the book to database
            ## Step 1 - Check if the book object exists # NOTE: For now i am using isbn as unique key to
            ## identify if a book object exists. It can be changed later.
            # import pdb; pdb.set_trace()
            isbn_no = form.cleaned_data["isbn"]
            summary = form.cleaned_data["summary"]
            if not Book.objects.filter(isbn=isbn_no):
                ## If the book object does not exists, then create a new book and author objects and save them
                book_title = form.cleaned_data["book_title"]
                author_fname =  form.cleaned_data["author_firstname"]
                author_lname = form.cleaned_data["author_lastname"]
                ## Ifthe author object exists then get the author name
                if Author.objects.filter(first_name=author_fname, last_name=author_lname).first():
                    author_obj =  Author.objects.get(first_name=author_fname, last_name=author_lname)
                else:
                    ## else create a new author object and save it
                    author_obj = Author.objects.create(first_name=author_fname, last_name=author_lname)
                    author_obj.save()
                ## Now create a new book object
                book_obj = Book.objects.create(title=book_title,author=author_obj,isbn=isbn_no, language=form.cleaned_data["language"])
                book_obj.save()
                book_obj.genre.set(form.cleaned_data["genre"])
            else:
                ## if the book object exists, then get the book object
                book_obj = Book.objects.get(isbn=isbn_no)

            ## Now create a book instance object using the book object for a given user
            bookinst_obj = BookInstance.objects.create(book=book_obj,summary=summary,book_owner=request.user)
            bookinst_obj.save()
            # redirect to a new URL:
            return HttpResponseRedirect(reverse('books'))
    else:
        form = AddBookForm(initial = {})
    # import pdb; pdb.set_trace()
    context = {'form': form,}
    return render(request, 'catalog/add_book_form.html', context)


@permission_required('catalog.can_delete_book')
def delete_book(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)
    context = {'book_instance':book_instance}
    ## if request method is post then delete the book instance
    if request.method == 'POST':
        book_instance.delete()
        return HttpResponseRedirect(reverse('books'))

    return render(request, 'catalog/delete_book_confirm.html',context)