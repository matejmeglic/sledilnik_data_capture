from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime

from HOS.forms import ReportHOSForm
from HOS.models import ReportHOS


# from HOS.models import ReportHOS, Hospital
# from django.views import generic
# from django.shortcuts import get_object_or_404

# Create your views here.



def index(request):
    """View function for home page of site."""

    context = {
        'num_books': 'empty'
    }

    return render(request, 'index.html', context=context)

def HOS_form(request):
    """View function for home page of site."""

    form = ReportHOSForm() 

    # If this is a POST request then process the Form data
    if request.method == 'POST':


        

        # Create a form instance and populate it with data from the request (binding):
        form = ReportHOSForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)

            HOSobject = ReportHOS()
            HOSobject.date_reporting = form.date_reporting,
            HOSobject.hospital = form.hospital,
            HOSobject.total_hospitalized = form.total_hospitalized,
            HOSobject.total_hospitalized_ICU = form.total_hospitalized_ICU,
            HOSobject.total_released = form.total_released,
            HOSobject.total_deaths = form.total_deaths,
            HOSobject.deaths_info = form.deaths_info,
            HOSobject.remark = form.remark

            HOSobject.save()

            # redirect to a new URL:
            return HttpResponseRedirect('/')

    # If this is a GET (or any other method) create the default form.
   
        

    context = {
        'form': form,
        'HOSobject': HOSobject,
    }

    return render(request, 'HOS_form.html', context)