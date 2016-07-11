from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
import xml.etree.cElementTree as ET

from .serializers import BomSerializer

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




@api_view(['GET', 'POST'])
def getBOM(request):
    """
    Get, all BOM data
    """
    try:
        bomData = Bom.objects.all ()

    except bomData.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BomSerializer(bomData, many=True)
        return Response(serializer.data )


@api_view(['GET', 'POST'])
def upload_fits(request):

    if True :
        xml = request.body
        return Response(execute_transaction(xml))
    else:
        return Response("Accept only xml (ODC/SPC compatible)" )

def execute_transaction(xml):
    try:
        root = ET.fromstring(xml)
        #Main data
        sn = root.findtext('serialnumber')
        trans_seq = root.findtext('trans_seq')
        sn_attr_code = root.findtext('sn_attr_code')
        operation = root.findtext('operation')
        employee = root.findtext('employee')
        shift = root.findtext('shift')
        buildtype= root.findtext('buildtype')
        runtype= root.findtext('runtype')
        partnumber= root.findtext('partnumber')
        model= root.findtext('model')
        datetimein= root.findtext('datetimein')
        datetimeout= root.findtext('datetimeout')
        workorder= root.findtext('workorder')
        #SPC details (child)
        for paramElement in root.findall('parameters/parameter'):
            code = paramElement.attrib['code']
            description = paramElement.attrib['desc']
            value = paramElement.text


        return ("serial %s on %s of %s -- value is : %s" % (sn,operation,shift,value ))

    except Exception as e:
        return "Failed : Unable to insert transaction %s" % e.args[0]



#         #Modify by Chutchai on April 20,2016
#         #To not accect VALIDATE transaction while ActionRequire flag is True
#         if data_type == 'VALIDATE':
#             ps = PerformSetting.objects.get(tester_name= testername)
#             if ps.require_actions:
#                 return "Not allow to execute data, found action is pending"


#         #insert to model
#         #xmltrack = PerformingTracking(sn='' , model='', station='', tester_name='', ticket=ticket, type='')
#         xmltrack = PerformingTracking()
#         xmltrack.sn = sn
#         xmltrack.model = model
#         xmltrack.station = station
#         xmltrack.tester_name = testername
#         xmltrack.location= location
#         xmltrack.ticket = ticket
#         xmltrack.type = data_type
#         xmltrack.user_id = user
#         xmltrack.result = True if result == 'P' else False
#         import datetime
#         from django.utils import timezone
#         date_in = datetime.datetime.strptime(datetime_in, '%d-%m-%Y %H:%M:%S')
#         xmltrack.datetime = timezone.make_aware(date_in, timezone.get_default_timezone())
#         xmltrack.save()


#         vtrack_id = xmltrack.perform_id

#         #SPC details (child)
#         for paramElement in root.findall('spc/summary_result/parameter'):
#             parameter = paramElement.attrib['name']
#             param_result = paramElement.findtext('result')
#             min_value = paramElement.findtext('min')
#             max_value = paramElement.findtext('max')
#             param_unit = paramElement.findtext('unit')
#             lower_limit = paramElement.findtext('lowerlimit')
#             upper_limit = paramElement.findtext('upperlimit')

#             xmlDetail = PerformingDetail()
#             xmlDetail.perform_id = xmltrack
#             xmlDetail.param_name = parameter
#             xmlDetail.result = True if param_result == 'P' else False
#             xmlDetail.min_value = min_value
#             xmlDetail.max_value = max_value
#             xmlDetail.unit_name = param_unit
#             xmlDetail.lower_limit = lower_limit
#             xmlDetail.upper_limit = upper_limit
#             xmlDetail.spc_required = xmlDetail.is_master_required()
#             xmlDetail.datetime = xmltrack.datetime
#             xmlDetail.save()
#             if data_type == 'VALIDATE':
#                 xmlDetail.excecute_spc()

#         if data_type == 'VALIDATE':
#             #Update Perform Setting
#             pd = PerformingDetail.objects.filter(perform_id=vtrack_id,spc_required=True,spc_result=False)
#             ps = PerformSetting.objects.get(tester_name= testername)

#             ps.last_perform_datetime = timezone.now()
#             ps.last_perform_result = True if result == 'P' else False
#             ps.perform_id = vtrack_id
#             ps.last_spc_result = True if pd.count() == 0 else False
#             #update action log. (if there is SPC failed, it requires Action log
#             if pd.count() > 0 and ps.tester_name.control  :
#                 ps.require_actions = True
#             ps.save()
#             #End Update

#         return "Successful"

#     except Exception as e:
#         return "Failed : Unable to insert transaction %s" % e.args[0]