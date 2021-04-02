from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField


User = get_user_model()

# Create your models here.

class StudentQuerySet(models.QuerySet):
	def filter_by_assignee(self,user_id):
		return self.filter(assignee_id=user_id)

	def filter_by_file_opened(self):
		return self.filter(lead__status__icontains="FILE_OPENED")


class Student(models.Model):
	lead = models.OneToOneField('lead_management.Lead',on_delete=models.CASCADE,related_name='student')
	branch = models.ForeignKey('branch.Branch',on_delete=models.CASCADE)
	event = models.ForeignKey('lead_management.Event',on_delete=models.CASCADE)
	assignee = models.ForeignKey(User,on_delete=models.CASCADE)

	objects = StudentQuerySet.as_manager()

	# def has_documents_object(self):
	# 	return hasattr(self, 'documents')

	class Meta:
		verbose_name_plural = "1. Student"





class StudentDocument(models.Model):
	student = models.OneToOneField(Student,on_delete=models.CASCADE,related_name='documents')
	documents = RichTextField(null=True,blank=True)
	# name = models.CharField(max_length=255)
	# status = models.CharField(max_length=20,choices=STATUS_CHOICES)


	class Meta:
		verbose_name_plural = "2. Student Documents"



class StudentCredentials(models.Model):
	student = models.OneToOneField(Student,on_delete=models.CASCADE,related_name='credentials')
	credentials = RichTextField(null=True,blank=True)

	class Meta:
		verbose_name_plural = "3. Student Credentials"


class StudentApplicationStatus(models.Model):
	STATUS_CHOICES = (
		('PREPARING_DOCUMENTS','Preparing Documents'),
		('DOCUMENTS_PREPARED','Documents Prepared'),
		('APPLICATION_FEES_PAID','Application Fees Paid'),
		('APPLICATION_IN_PROGRESS','Application In-Progress'),
		('APPLICATION_DONE','Application Complete'),
		('CONDITIONAL_OFFER','Conditional Offer Letter Received'),
		('FINAL_OFFER','Final Offer Letter Received'),
		('TUITION_FEES_SENT','Tuition Fees Sent'),
		('APPLICATION_REJECTED','Application Rejected')
	)
	student = models.ForeignKey(Student,on_delete=models.CASCADE,related_name='application_status')
	title = models.CharField(max_length=255)
	status = models.CharField(max_length=40,choices=STATUS_CHOICES)

	class Meta:
		verbose_name_plural = "4. Student Application Status"



class StudentVisaStatus(models.Model):
	STATUS_CHOICES = (
		('READY_TO_APPLY','Ready to Apply for Visa'),
		('DOCUMENTS_PREPARED','Documents Prepared'),
		('APPLICATION_DONE','Application Complete'),
		('VISA_RECEIVED','Visa Received'),
		('VISA_REJECTED','Visa Rejected')
	)
	student = models.ForeignKey(Student,on_delete=models.CASCADE,related_name='visa_status')
	title = models.CharField(max_length=255)
	status = models.CharField(max_length=40,choices=STATUS_CHOICES)

	class Meta:
		verbose_name_plural = "4. Student Application Status"

