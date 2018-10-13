from django.shortcuts import render

# Create your views here.

from catalog.models import Book, Author, BookInstance, Genre

def index(request):
    #View function for home page of site.

    #Generate counts of some the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    mystery_count = Genre.objects.filter(name__icontains='mystery').count
    the_count = Book.objects.filter(title__icontains='the').count



    #Available Books
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    #The 'all()' is implied by default.
    num_authors = Author.objects.count()

    #Number of visits to this view, as counted in the session variable
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'mystery_count': mystery_count,
        'the_count': the_count,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)



from django.views import generic

class BookListView(generic.ListView):
    model = Book
    paginate_by = 5
    context_object_name = 'book_list' # your own name for the list as a template variable
    book_list = Book.objects.all # Get 5 books containing the title war
    template_name = 'catalog/book_list.html' # Specify your own template name/location

'''
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        print(context)
        return context

    def get_queryset(self):
        return Book.objects.filter(title__icontains='the')[:5]
'''


    #render(request, 'book_list.html', context=context)





class AuthorListView(generic.ListView):
    model = Author
    paginate_by = 5
    context_object_name = 'author_list' # your own name for the list as a template variable
    author_list = Author.objects.all # Get 5 books containing the title war

    template_name = 'catalog/author_list.html' # Specify your own template name/location

'''
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(AuthorListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['some_data'] = 'This is just some data'
        print(context)
        return context

    def get_queryset(self):
        return Book.objects.filter(title__icontains='the')[:5]
'''


    #render(request, 'book_list.html', context=context)



class BookDetailView(generic.DetailView):
    model = Book
    template_name = 'catalog/book_detail.html'

class AuthorDetailView(generic.DetailView):

    model = Author
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['book_list'] = Book.objects.filter(author__pk__exact='1')
        return context
    template_name = 'catalog/author_detail.html'
