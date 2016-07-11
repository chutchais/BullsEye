from django.shortcuts import render
from .forms import StationModelForm

from django.http import HttpResponseRedirect
from django.views.generic import CreateView

from .forms import BomDetailsFormSet, BomForm
from .models import Bom

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


class RecipeCreateView(CreateView):
    template_name = 'bom_add.html'
    model = Bom
    form_class = BomForm
    success_url = 'success/'

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        bomdetail_form = BomDetailsFormSet()
        return self.render_to_response(
        	self.get_context_data(
        		form=form,bomdetail_form=bomdetail_form))

    # def post(self, request, *args, **kwargs):
    #     """
    #     Handles POST requests, instantiating a form instance and its inline
    #     formsets with the passed POST variables and then checking them for
    #     validity.
    #     """
    #     self.object = None
    #     form_class = self.get_form_class()
    #     form = self.get_form(form_class)
    #     bomdetail_form = BomDetailsFormSet(self.request.POST)
    #     #instruction_form = InstructionFormSet(self.request.POST)
    #     if (form.is_valid() and bomdetail_form.is_valid()):
    #         return self.form_valid(form, bomdetail_form)
    #     else:
    #         return self.form_invalid(form, bomdetail_form)

    # def form_valid(self, form, bomdetail_form):
    #     """
    #     Called if all forms are valid. Creates a Recipe instance along with
    #     associated Ingredients and Instructions and then redirects to a
    #     success page.
    #     """
    #     self.object = form.save()
    #     bomdetail_form.instance = self.object
    #     bomdetail_form.save()
    #     #instruction_form.instance = self.object
    #     #instruction_form.save()
    #     return HttpResponseRedirect(self.get_success_url())

    # def form_invalid(self, form, bomdetail_form):
    #     """
    #     Called if a form is invalid. Re-renders the context data with the
    #     data-filled forms and errors.
    #     """
    #     return self.render_to_response(
    #         self.get_context_data(form=form,
    #                               bomdetail_form=bomdetail_form))