from django.db import models
from django.contrib.auth import get_user_model

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





class StudentDocument(models.Model):
	STATUS_CHOICES = (
		('RECEIVED','RECEIVED'),
		('NOT RECEIVED','NOT RECEIVED')
	)
	student = models.OneToOneField(Student,on_delete=models.CASCADE,related_name='documents')
	name = models.CharField(max_length=255)
	status = models.CharField(max_length=20,choices=STATUS_CHOICES)
