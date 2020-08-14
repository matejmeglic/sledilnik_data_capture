from django.shortcuts import render
from django.shortcuts import redirect

from .forms import ReportHOSForm


def index(request):
<<<<<<< HEAD
    return render(request, "index.html", {})


def hos_form(request):

    if request.method == "POST":
=======
    return render(request, 'index.html', {})


def hos_form(request):
    form = ReportHOSForm()

    if request.method == 'POST':
>>>>>>> 53ff0b61ab45b4d824041869d3a70fc388e32b20
        form = ReportHOSForm(request.POST)

        if form.is_valid():
            report = form.save(commit=False)
            report.submitted_by = request.user
            report.save()
<<<<<<< HEAD
            return redirect("HOS:index")
    else:
        form = ReportHOSForm()

    return render(request, "HOS_form.html", {"form": form})
=======
            return redirect('HOS:index')

    return render(request, 'HOS_form.html', {
        'form': form
    })
>>>>>>> 53ff0b61ab45b4d824041869d3a70fc388e32b20
