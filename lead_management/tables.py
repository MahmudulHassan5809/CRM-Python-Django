import django_tables2 as tables
from .models import TaskAssign,Lead
from django_tables2.utils import AttributeDict
from django.utils.safestring import mark_safe



class TaskAssignTable(tables.Table):
	selection = tables.CheckBoxColumn(accessor='pk')

	def render_selection(self, value, bound_column, record):
		if record.assigned:
			default = {"type": "checkbox", "name": bound_column.name, "value": record.id,"checked":"" }
		else:
			default = {"type": "checkbox", "name": bound_column.name, "value": record.id,}
		general = self.attrs.get("input")
		specific = self.attrs.get("td__input")
		attrs = AttributeDict(default, **(specific or general or {}))
		return mark_safe(f"<input  %s/>" % attrs.as_html())
	
	class Meta:
		model = Lead
		template_name = "django_tables2/bootstrap.html"
		fields = ('name','email','phone_number','selection')
		