import base64
import os
import requests
import urllib

from flask import Flask, render_template, session, redirect, url_for, flash, request, abort
from flask_wtf.csrf import CsrfProtect

from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment

from forms import NewProjectForm, TokenGatheringForm

from dropboxAPI import (get_info, get_team_members, get_dropbox_groups, get_user_account_detail,
						get_file_or_folder_metdata, create_dropbox_folder, list_folder_content,
						get_folders_to_create, create_folders, share_dropbox_folder, add_dropbox_share_permissions)

app = Flask(__name__)
app.config['SECRET_KEY'] = "w3xkIaP5nF6a8Ndq79J4rK5nK4MI/HMakUJTB3PWa8cxmiqrxQZ/+hgp/d+gcV7e"
app.config['DEBUG'] = True

manager = Manager(app)
bootstrap = Bootstrap(app)
moment = Moment(app)

csrf = CsrfProtect()

#Dropbox App
APP_KEY = 'k543xq496hfjkqw'
APP_SECRET = '6u1exxfq1aydw4m'

#Static template folder till we get some front end code to do this:
template_folder = "/Project_Automation_Template"

csrf_token = base64.urlsafe_b64encode(os.urandom(18))


@app.route('/')
def index():
	session['csrf_token'] = csrf_token
	return render_template('index.html')

@app.route('/obtain_auth_tokens', methods=['GET', 'POST'])
def auth_tokens():
	try:
		if session['dropbox_file_token']:
			return render_template('tokens_validated.html', 
									mgmt_token=session['basic_mgmt_token_check'], 
									file_token=session['basic_file_token_check'])
	except:
		form = TokenGatheringForm()
		if form.validate_on_submit():
			basic_mgmt_token_check = get_info(form.member_mgmt_token.data.strip())
			if basic_mgmt_token_check == False:
				flash('There is an issue with your Team Management Token')
				return render_template('auth_tokens.html', form=form)
			team_members = get_team_members(form.member_mgmt_token.data.strip())
			basic_file_token_check = get_user_account_detail(form.file_token.data.strip(), team_members["members"][0]["profile"]["team_member_id"])
			if basic_file_token_check == False:
				flash('There is an issue with your File Access Token')
				return render_template('auth_tokens.html', form=form) 
			#we trust the tokens from here. add them to session object. 
			session['dropbox_file_token'] = form.file_token.data.strip()
			session['dropbox_mgmt_token'] = form.member_mgmt_token.data.strip()
			session['basic_mgmt_token_check'] = basic_mgmt_token_check
			session['basic_file_token_check'] = basic_file_token_check
			return render_template('tokens_validated.html', 
									mgmt_token=session['basic_mgmt_token_check'], 
									file_token=session['basic_file_token_check'])
		return render_template('auth_tokens.html', form=form)


@app.route('/complete_sf_create', methods=['GET', 'POST'])
def complete_sf_create(form=None):
	if form == None:
		return internal_server_error()

	template_folder_info = get_file_or_folder_metdata(session['dropbox_file_token'], template_folder, form.user_id.data)
	if template_folder_info == False:
			create_dropbox_folder(session['dropbox_file_token'], template_folder, form.user_id.data)
	session['account_id'] = form.user_id.data
	
	top_level_folder_to_create = form.project_name.data
	rw_group = form.project_rw_members.data
	ro_group = form.project_ro_members.data
	folder_content = list_folder_content(session['dropbox_file_token'], template_folder, session['account_id'])
	folders_to_create = get_folders_to_create(folder_content, template_folder, top_level_folder_to_create)
	create_folders(session['dropbox_file_token'], folders_to_create, session['account_id'])
	shared_folder_detail = share_dropbox_folder(session['dropbox_file_token'], folders_to_create[0], session['account_id'])
	perms_change_status_rw = add_dropbox_share_permissions(session['dropbox_file_token'], shared_folder_detail['shared_folder_id'], 
															rw_group, "editor", session['account_id'])
	perms_change_status_ro = add_dropbox_share_permissions(session['dropbox_file_token'], shared_folder_detail['shared_folder_id'], 
															ro_group, "viewer", session['account_id'])
	return render_template('complete.html', folder_content=folders_to_create, project_name=top_level_folder_to_create)


@app.route('/tokens_validated', methods=['GET', 'POST'])
def tokens_validated():
	return render_template('tokens_validated.html')

@app.route('/not_yet')
def not_yet():
	flash('cough... feature still under development.. cough...')
	return redirect(url_for("index"))


@app.route('/main', methods=['GET', 'POST'])
def main():
	newProjectForm = NewProjectForm()
	
	dropbox_users = get_team_members(session['dropbox_mgmt_token'])
	newProjectForm.user_id.choices = ( 
										[ (u['profile']['team_member_id'], u['profile']['email'] 
										if u['profile']['status']['.tag'] == "active" else "(inactive) " + u['profile']['email']) 
										for u in dropbox_users['members'] ] 
										)

	dropbox_groups = get_dropbox_groups(session['dropbox_mgmt_token'])
	newProjectForm.project_rw_members.choices = [ (g['group_id'], g['group_name']) for g in dropbox_groups['groups']]
	newProjectForm.project_ro_members.choices = [ (g['group_id'], g['group_name']) for g in dropbox_groups['groups']]

	if newProjectForm.validate_on_submit():
		return complete_sf_create(newProjectForm)

	return render_template('main.html', db_auth=True, newProjectForm=newProjectForm)

@app.route("/logout")
def logout():
    session.clear()
    flash('You have been logged out')
    return redirect(url_for("index"))


@app.errorhandler(404)
def page_not_found(e):
	return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
	return render_template('500.html'), 500


if __name__ == '__main__':
	app.run()
	csrf.init_app(app)

