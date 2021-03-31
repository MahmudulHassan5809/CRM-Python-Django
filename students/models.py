from django.db import models
from django.contrib.auth import get_user_model
from ckeditor.fields import RichTextField


User = get_user_model()

# Create your models here.

class StudentQuerySet(models.QuerySet):
	def filter_by_assignee(self,user_id):
		return self.filter(assignee_id=user_id)


class Student(models.Model):
	lead = models.OneToOneField('lead_management.Lead',on_delete=models.CASCADE,related_name='student')
	branch = models.ForeignKey('branch.Branch',on_delete=models.CASCADE)
	event = models.ForeignKey('lead_management.Event',on_delete=models.CASCADE)
	assignee = models.ForeignKey(User,on_delete=models.CASCADE)

	objects = StudentQuerySet.as_manager()

	# def has_documents_object(self):
	# 	return hasattr(self, 'documents')





class StudentDocument(models.Model):
	student = models.OneToOneField(Student,on_delete=models.CASCADE,related_name='documents')
	documents = RichTextField(null=True,blank=True)
	# name = models.CharField(max_length=255)
	# status = models.CharField(max_length=20,choices=STATUS_CHOICES)



class StudentCredentials(models.Model):
	student = models.OneToOneField(Student,on_delete=models.CASCADE,related_name='credentials')
	credentials = RichTextField(null=True,blank=True)


class StudentApplicationStatus(models.Model):
	STATUS_CHOICES = (
		('Documents_Prepared','Documents Prepared'),
		('Application_Done','Application Done')
	)
	student = models.ForeignKey(Student,on_delete=models.CASCADE,related_name='status')
	university_name = models.CharField(max_length=255)
	status = models.CharField(max_length=40,choices=STATUS_CHOICES)



