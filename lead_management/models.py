from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model
from smart_selects.db_fields import ChainedForeignKey
from ckeditor.fields import RichTextField


User = get_user_model()

# Create your models here.


class EventQuerySet(models.QuerySet):
	def filter_by_query(self,query):
		return self.filter(name__icontains=query)

class Event(models.Model):
	name = models.CharField(max_length=255)
	description = models.TextField()
	event_date = models.DateField()
	active = models.BooleanField(default=True)

	objects = EventQuerySet.as_manager()

	def __str__(self):
		return self.name

	class Meta:
		verbose_name_plural = "2. Event"




class LeadQuerySet(models.QuerySet):
    def filter_by_event(self,event_id):
        return self.filter(event__id=event_id)

    def filter_by_status(self,status):
        return self.filter(status__exact=status)

    def filter_query(self,query):
        return self.filter(Q(name__icontains=query) | Q(email__icontains=query) | Q(phone_number__icontains=query) |  Q(event__name__icontains=query))


    def filter_by_is_assigned(self,bool):
    	return self.filter(assigned=bool)



class Lead(models.Model):
    LEAD_STATUS_CHOICE = [
        ('Not Available', (
            ('PHONE_OFF', 'Phone Off'),
            ('NO ANSWER', 'No Answer'),
            ('CALL_FORWARDED', 'Call Forwarded'),
            ('INCORREET_NUMBER', 'Incorrect Number'),
            ('OTHER', 'Other'),
        )
        ),
        ('Positive Response', (
                ('EVENT_CONFIRMED', 'Event Confirmed'),
                ('FUTURE_INTEREST', 'Future Interest'),
                ('DECISION_PENDING', 'Decision Pending'),
                ('OTHER', 'Other'),
            )
        ),
        ('Negative Response', (
                ('NOT_INTERESTED', 'Not Interested'),
                ('UNINFORMED', 'Uninformed'),
                ('NOT_QUALIFIED', 'Not Qualified'),
                ('SELF_APPLIED', 'Self-Applied'),
                ('OTHER', 'Other'),
            )
        ),
        ('FILE_OPENED', 'File Opened'),
        ('NEW', 'New'),
    ]

    created_by = models.ForeignKey(User,on_delete=models.CASCADE,related_name="leads")
    event = models.ForeignKey(Event,on_delete=models.CASCADE,related_name="leads")
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)
    phone_number = models.CharField(max_length=255)
    present_address = models.CharField(max_length=255)
    country_of_interest = models.CharField(max_length=255)
    last_completed_education = models.CharField(max_length=255)
    ielts = models.CharField(max_length=255)
    remarks = models.CharField(max_length=255,null=True,blank=True)
    created_at = models.DateField(auto_now_add=True)
    assigned = models.BooleanField(default=False)
    status = models.CharField(max_length=20,choices=LEAD_STATUS_CHOICE,default='NEW')
    note =  RichTextField(null=True,blank=True)

    objects = LeadQuerySet.as_manager()

    def __str__(self):
    	return self.name

    class Meta:
        verbose_name_plural = '1. Leads'
        ordering = ['id']



class TaskAssignQuerySet(models.QuerySet):
    def filter_by_event(self,event_id):
        return self.filter(event__id=event_id)

    def filter_by_assignee(self,user_id):
        return self.filter(assignee_id=user_id)


class TaskAssign(models.Model):
    branch = models.ForeignKey('branch.Branch',on_delete=models.CASCADE)
    event = models.ForeignKey(Event,on_delete=models.CASCADE,related_name='event_tasks')
    lead = models.OneToOneField(Lead,on_delete=models.CASCADE,related_name='lead_task')
    assignee = ChainedForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='user_tasks',
        chained_field="branch",
        chained_model_field="branch_users",
        show_all=False,
        auto_choose=True,
        sort=True)

    objects = TaskAssignQuerySet.as_manager()

    def __str__(self):
        return self.lead.name

    class Meta:
        verbose_name_plural = '1. Task'



class Student(models.Model):
    pass
