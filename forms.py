from flask_wtf import Form
from wtforms import StringField, SelectField, RadioField
from wtforms.validators import DataRequired

class AddAlarmForm(Form):
	time_as_tuple = lambda arr : map(lambda e : (e, str(e) if len(str(e)) == 2 else '0'+str(e)), arr)
	mode_as_tuple = lambda arr : map(lambda e : (e.lower(), e), arr)

	name = StringField("Name")
	hour = SelectField("Hour", choices=time_as_tuple(range(0, 24)))
	minute = SelectField("Minutes", choices=time_as_tuple([0,15,30,45]))
	mode = RadioField("Mode", choices=mode_as_tuple(["Weekdays", "Weekend", "All"]))
