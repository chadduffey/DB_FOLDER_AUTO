from flask.ext.wtf import Form, widgets

from wtforms import StringField, SubmitField, SelectField, BooleanField, FormField
from wtforms.validators import Required

class AuthDBForm(Form):
	submit = SubmitField('Authorize Access to Dropbox')

class NewProjectForm(Form):
	user_id = SelectField('Team Member to Use', choices=[('a', 'a')])
	project_name = StringField('Project Name', validators=[Required()])
	project_rw_members = SelectField('Dropbox Group for read & write access', choices=[('a', 'a')])
	project_ro_members = SelectField('Dropbox Group for read only access', choices=[('a', 'a')])
	submit = SubmitField('Create New Project')

class TokenGatheringForm(Form):
	file_token = StringField("File Access Token", validators=[Required()], default='')
	member_mgmt_token = StringField("Member Management Token", validators=[Required()], default='')
	submit = SubmitField('Validate Tokens')