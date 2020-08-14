from django.shortcuts import render
from django.shortcuts import redirect

from .forms import ReportHOSForm


def index(request):
    return render(request, "index.html", {})


def hos_form(request):

    if request.method == "POST":
        form = ReportHOSForm(request.POST)

        if form.is_valid():
            report = form.save(commit=False)
            report.submitted_by = request.user
            report.save()
            return redirect("HOS:index")
    else:
        form = ReportHOSForm()

    return render(request, "HOS_form.html", {"form": form})
