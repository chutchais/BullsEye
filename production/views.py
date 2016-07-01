from django.shortcuts import render
from .forms import StationModelForm

# Create your views here.
def post_list(request):
# if this is a POST request we need to process the form data
	title ="Welcome"
	form = StationModelForm(request.POST or None)
	context ={
		"title": title,
		"form" : form
	}
	if form.is_valid():
		instance = form.save(commit=False)
		station = form.cleaned_data["station"]
		instance.save()
		context ={
			"title": "Sign up successful!!"
		}	
		# if not station :
		# 	station = "new station"
		# 	instance.station = station
		# 	instance.save()
		# 	context ={
		# 	"title": "Sign up successful!!",
		# 	}

	return render(request, 'production/post_list.html',context)

		# if form.is_valid():
		# 	instance = form.save(commit=False)
		# 	station = form.cleaned_data["station"]
		# 	if not station:
		# 		station = "new station"
		# 		instance.station = station
		# 		instance.save()
		# 		context ={
		# 		"title": "Sign up successful!!",
		# 		}

    # if a GET (or any other method) we'll create a blank form
    # else:
    #     form = StationModelForm()

    