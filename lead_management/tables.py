import django_tables2 as tables
from .models import TaskAssign,Lead
from django_tables2.utils import AttributeDict
from django.utils.safestring import mark_safe



class TaskAssignTable(tables.Table):
	selection = tables.CheckBoxColumn(accessor='pk')
	assignee = tables.Column(accessor='pk')

	# def render_selection(self, value, bound_column, record):
	# 	if record.assigned:
	# 		default = {"type": "checkbox", "name": bound_column.name, "value": record.id,"checked":"" }
	# 	else:
	# 		default = {"type": "checkbox", "name": bound_column.name, "value": record.id,}
	# 	general = self.attrs.get("input")
	# 	specific = self.attrs.get("td__input")
	# 	attrs = AttributeDict(default, **(specific or general or {}))
	# 	return mark_safe(f"<input  %s/>" % attrs.as_html())

	def render_assignee(self, value, bound_column, record):
		try:
			return record.lead_task.assignee.username.title
		except:
			return 'Not Assigned'
		# print(record.lead_task)
        # default = {"type": "text", "name": bound_column.name, "value": record.id}
        # general = self.attrs.get("input")
        # specific = self.attrs.get("td__input")
        # attrs = AttributeDict(default, **(specific or general or {}))
        # return mark_safe("<input %s/>" % attrs.as_html())

	
	class Meta:
		model = Lead
		template_name = "django_tables2/bootstrap.html"
		fields = ('name','email','phone_number','assignee','selection')
		