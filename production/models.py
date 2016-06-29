from django.db import models

# Create your models here.
#Master data
class Bom(models.Model):
	name = models.CharField(max_length=50)
	model = models.CharField(verbose_name ='Model Name',max_length=50)
	rev = models.CharField(verbose_name ='Model Revision',max_length=50)
	description = models.CharField(max_length=255)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)

	def __str__(self):
		return self.name


class BomDetails(models.Model):
	bom = models.ForeignKey('Bom',
		on_delete = models.CASCADE, related_name='bom_details')
	pn = models.CharField(verbose_name ='Part Number',max_length=50)
	customer_pn = models.CharField(verbose_name ='Customer Part number' ,max_length=50)
	rd = models.CharField(verbose_name ='Reference Destination' , max_length=50)
	description = models.CharField(max_length=255)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)

	def __str__(self):
		return self.pn


class Product(models.Model):
	name = models.CharField(max_length=50)
	model = models.CharField(verbose_name ='Model Name',max_length=50)
	rev = models.CharField(verbose_name ='Model Revision',max_length=50)
	customer_model = models.CharField(verbose_name ='Customer Model',max_length=50)
	customer_rev = models.CharField(verbose_name ='Customer Model revision',max_length=50)
	group = models.CharField(verbose_name ='Product Group',max_length=50)
	bom = models.ForeignKey('Bom' ,related_name='product_used')
	description = models.CharField(max_length=255)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)

	def __str__(self):
		return self.name


class Station(models.Model):
	"""docstring for ClassName"""
	station = models.CharField(max_length=50)
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=255)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)
	
	def __str__(self):
		return self.name


class Routing(models.Model):
	"""docstring for ClassName"""
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=255)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)
	
	def __str__(self):
		return self.name


class RoutingDetails(models.Model):
	"""docstring for ClassName"""
	route = models.ForeignKey('Routing' ,related_name='route_details')
	station = models.ForeignKey('Station' ,related_name='route_used')
	description = models.CharField(max_length=255)
	next_pass = models.ForeignKey('Station' ,related_name='route_used_next_pass')
	next_fail = models.ForeignKey('Station' ,related_name='route_used_next_fail')
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)
	
	def __str__(self):
		return self.station.name

#Configuration data
class WorkOrder(models.Model):
	PROD = 'PROD'
	RMA='RMA'
	BUILD_TYPE_CHOICES = (
        (PROD, 'Production'),
        (RMA, 'Repair'),
    )
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=255)
	product = models.ForeignKey('Product' ,related_name='workorder_used')
	qty = models.IntegerField()
	build_type = models.CharField(max_length=10 ,choices=BUILD_TYPE_CHOICES)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)

	def __str__(self):
		return self.name


class WorkOrderDetails(models.Model):
	IN = 'IN'
	DONE = 'DONE'
	STATUS_CHOICES = (
        (IN, 'In Process'),
        (DONE, 'Completed Process'),
    )
	sn = models.CharField(max_length=50)
	workorder = models.ForeignKey('WorkOrder' ,related_name='sn_list')
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	current_staton = models.CharField(max_length=50)
	result = models.BooleanField(default=True) #Last Result Pass/Fail
	status = models.CharField(max_length=50,choices=STATUS_CHOICES)
	user = models.ForeignKey('auth.User',blank=True,null=True)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)
	
	def __str__(self):
		return self.sn


class Performing(models.Model):
	sn_wo = models.ForeignKey('WorkOrderDetails' ,related_name='performing_list')
	station = models.CharField(max_length=50)
	started_date = models.DateTimeField(auto_now_add=True)
	finished_date = models.DateTimeField(auto_now_add=True)
	result = models.BooleanField(default=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)

	def __str__(self):
		return self.WorkOrderDetails.sn

