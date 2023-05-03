from django.shortcuts import render

from form_creator.forms import SuperForm
from form_creator.utils import get_forms_example

# Create your views here.

def v_form(request):
    if request.method == 'POST': # how to load forms: https://stackoverflow.com/a/59442810
        print(request.POST)
    return render(request, 'base.html', context = {'forms':get_forms_example()})