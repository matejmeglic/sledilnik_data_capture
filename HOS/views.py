from django.shortcuts import render
# from HOS.models import ReportHOS, Hospital
# from django.views import generic
# from django.shortcuts import get_object_or_404

# Create your views here.



def index(request):
    """View function for home page of site."""

    # # Generate counts of some of the main objects
    # num_books = Book.objects.all().count()
    # num_instances = BookInstance.objects.all().count()
    
    # # Available books (status = 'a')
    # num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    
    # # The 'all()' is implied by default.    
    # num_authors = Author.objects.count()
    
    # # Number of visits to this view, as counted in the session variable.
    # num_visits = request.session.get('num_visits', 0)
    # request.session['num_visits'] = num_visits + 1

    context = {
        'num_books': 'empty'
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def HOS_form(request):
    """View function for home page of site."""
    context = {"context":"empty"}
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'HOS_form.html', context=context)
