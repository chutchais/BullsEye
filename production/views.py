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
from .models import Family
from .models import Product
from .models import Station
from .models import WorkOrder
from .models import WorkOrderDetails
from django.contrib.auth.models import User
from .models import Performing
from .models import PerformingDetails
from .models import Parameter

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

        result=root.findtext('result')
        if result is None:
            result=root.findtext('parameters/parameter[@code="1101"]')

        updateResult = True if result == 'PASS' else  False

        

        #check Master data and create object
        #1)Family
        objFamily,created = Family.objects.get_or_create(name=model)
        #2)Bom
        objBom,created = Bom.objects.get_or_create(name=partnumber,model=partnumber,rev='00')
        #3)Product
        objProduct,created = Product.objects.get_or_create(name=partnumber,model=partnumber,rev='00',
            bom=objBom,family=objFamily)
        #4)Station/Operation
        objStation,created = Station.objects.get_or_create(station=operation,family=objFamily)
        #5)WorkOrder
        objWorkorder,created = WorkOrder.objects.get_or_create(name=workorder,product=objProduct)
        #6)User
        objUser,created = User.objects.get_or_create(username=employee,password=employee,
            email=("%s@fabrinet.co.th" % employee ))
        #7)Workorder and WorkorderDetail
        objWorkOrder,created = WorkOrder.objects.get_or_create(name=workorder,product=objProduct)
        objSnWoDetails,created = WorkOrderDetails.objects.update_or_create(sn=sn,workorder=objWorkorder,
            user=objUser,defaults={"current_staton":operation,"result":updateResult})

        #8)Performing
        import datetime
        d1 = datetime.datetime.strptime(datetimein,"%m/%d/%Y %H:%M:%S %p")
        datein=d1.strftime("%Y-%m-%d %H:%M:%S") # Store this!
        d2 = datetime.datetime.strptime(datetimeout,"%m/%d/%Y %H:%M:%S %p")
        dateout=d2.strftime("%Y-%m-%d %H:%M:%S") # Store this!
        objPerforming = Performing.objects.create(sn_wo=objSnWoDetails,station=operation,
            started_date=datein,finished_date=dateout,result=updateResult,user=objUser)

        #9)PerformingDetails
        #Fits details (parameter)
        for paramElement in root.findall('parameters/parameter'):
            code = paramElement.attrib['code']
            description = paramElement.attrib['desc']
            value = paramElement.text
            #9.1)Parameter
            objParam,created = Parameter.objects.get_or_create(name=code,description=description)
            objPerformingDetails =PerformingDetails.objects.create(performing=objPerforming,parameter=objParam,
                value_str=value,result=updateResult,created_date=datein,user=objUser)


        return ("Successful")

    except Exception as e:
        return "Failed : Unable to insert transaction %s" % e.args[0]