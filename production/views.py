from django.shortcuts import render
from .forms import StationModelForm

# Create your views here.
def post_list(request):
# if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = StationModelForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = StationModelForm()

    return render(request, 'production/post_list.html', {'form': form})