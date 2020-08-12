"""Views"""
from django.shortcuts import render
from django.http import HttpResponseRedirect
from HOS.forms import ReportHOSForm
from HOS.models import ReportHOS

# Create your views here.

def index(request):
    """View function for home page of site."""

    context = {
        'num_books': 'empty'
    }

    return render(request, 'index.html', context=context)

def hos_form(request):
    """View function for home page of site."""

    form = ReportHOSForm()

    if request.method == 'POST':

        form = ReportHOSForm(request.POST)

        if form.is_valid():

            hos_object = ReportHOS()
           # hos_object.submitted_by = request.user,
            hos_object.date_reporting = form['date_reporting'],
            hos_object.hospital = form.cleaned_data['hospital'],
            hos_object.total_hospitalized = form['total_hospitalized'],
            hos_object.total_hospitalized_ICU = form['total_hospitalized_ICU'],
            hos_object.total_released = form['total_released'],
            hos_object.total_deaths = form['total_deaths'],
            hos_object.deaths_info = form['deaths_info'],
            hos_object.remark = form['remark']

            hos_object.save()

            return HttpResponseRedirect('/')

    context = {
        'form': form,
    }

    return render(request, 'HOS_form.html', context)
    