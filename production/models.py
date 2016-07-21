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

class Family(models.Model):
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=255)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)

	def __str__(self):
		return self.name

class Product(models.Model):
	name = models.CharField(max_length=50)
	model = models.CharField(verbose_name ='Model Name',max_length=50)
	rev = models.CharField(verbose_name ='Model Revision',max_length=50)
	customer_model = models.CharField(verbose_name ='Customer Model',max_length=50)
	customer_rev = models.CharField(verbose_name ='Customer Model revision',max_length=50)
	group = models.CharField(verbose_name ='Product Group',max_length=50)
	bom = models.ForeignKey('Bom' ,related_name='product_used')
	family = models.ForeignKey('Family' ,related_name='product_used',null=True)
	description = models.CharField(max_length=255)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)

	def __str__(self):
		return self.name


class Station(models.Model):
	"""docstring for ClassName"""
	station = models.CharField(verbose_name ='Station number',max_length=50)
	name = models.CharField(verbose_name ='Station name',max_length=50)
	description = models.CharField(max_length=255)
	family = models.ForeignKey('Family' ,related_name='station_used')
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
	QUAL='QUAL'
	BUILD_TYPE_CHOICES = (
        (PROD, 'Production'),
        (RMA, 'Repair'),
        (QUAL,'Qualification')
    )
	name = models.CharField(max_length=50)
	description = models.CharField(max_length=255)
	product = models.ForeignKey('Product' ,related_name='workorder_used')
	qty = models.IntegerField(default=1)
	build_type = models.CharField(max_length=10 ,choices=BUILD_TYPE_CHOICES,default=PROD)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)

	def __str__(self):
		return self.name


class WorkOrderDetails(models.Model):
	IN = 'IN'
	DONE = 'DONE'
	SHIPPED = 'SHIPPED'
	STATUS_CHOICES = (
        (IN, 'In Process'),
        (DONE, 'Completed Process'),
        (SHIPPED, 'Shipped'),
    )
	sn = models.CharField(max_length=50)
	workorder = models.ForeignKey('WorkOrder' ,related_name='sn_list')
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	current_staton = models.CharField(max_length=50)
	result = models.BooleanField(default=True) #Last Result Pass/Fail
	status = models.CharField(max_length=50,choices=STATUS_CHOICES,default=IN)
	user = models.ForeignKey('auth.User',blank=True,null=True)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	
	def __str__(self):
		return "%s on %s" % (self.sn,self.workorder)


class Performing(models.Model):
	sn_wo = models.ForeignKey('WorkOrderDetails' ,related_name='performing_list')
	station = models.CharField(max_length=50)
	loop = models.IntegerField(default=1)
	started_date = models.DateTimeField()
	finished_date = models.DateTimeField()
	result = models.BooleanField(default=True)
	dispose_code = models.CharField(max_length=100)
	user = models.ForeignKey('auth.User',blank=True,null=True)

	def __str__(self):
		return "%s" % self.sn_wo


class Parameter(models.Model):
	name = models.CharField(max_length=50)
	group = models.CharField(max_length=50)
	description = models.CharField(max_length=255)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)
	
	def __str__(self):
		return ("%s : %s" % (self.name,self.description))


class PerformingDetails(models.Model):
	S = 'String'
	N = 'Number'
	VALUE_CHOICES = (
        (S, 'String'),
        (N, 'Number'),
    )
	performing = models.ForeignKey('Performing' ,related_name='performingdetail_list')
	parameter = models.ForeignKey('Parameter' ,related_name='performing_used')
	value = models.FloatField(null=True, blank=True)
	value_str = models.CharField(max_length=50,null=True, blank=True)
	limit_min = models.FloatField(null=True, blank=True)
	limit_max = models.FloatField(null=True, blank=True)
	value_type = models.CharField(max_length=10,choices=VALUE_CHOICES,default=S)
	result = models.BooleanField(default=True)
	user = models.ForeignKey('auth.User',blank=True,null=True)
	created_date = models.DateTimeField()
	
	def __str__(self):
		return self.parameter.name

