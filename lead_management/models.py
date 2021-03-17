from django.db import models
from django.contrib.auth import get_user_model 


User = get_user_model()

# Create your models here.


class Event(models.Model):
	name = models.CharField(max_length=255)
	description = models.TextField()
	event_date = models.DateField()
	active = models.BooleanField(default=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = "2. Event"




class LeadQuerySet(models.QuerySet):
    def filter_by_event(self,event_id):
        return self.filter(event__id=event_id)

    


class Lead(models.Model):
	created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="leads")
	event = models.ForeignKey(Event,on_delete=models.CASCADE,related_name="leads")
	name = models.CharField(max_length=255)
	email = models.EmailField(max_length=254)
	phone_number = models.CharField(max_length=255)
	present_address = models.CharField(max_length=255)
	country_of_interest = models.JSONField()
	last_completed_education = models.CharField(max_length=255)
	ielts = models.CharField(max_length=255)
	created_at = models.DateField(auto_now_add=True)

	objects = LeadQuerySet.as_manager()

	def __str__(self):
		return self.name 

	class Meta:
		verbose_name_plural = '1. Leads'

