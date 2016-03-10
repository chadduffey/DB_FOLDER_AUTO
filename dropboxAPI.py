import json
import requests

#-------------------------
# Business API
#-------------------------

def get_info(token):
    dfbToken = "Bearer " + token
    try:
	    response = requests.post(url='https://api.dropboxapi.com/2/team/get_info',
	                    headers = ({ "Authorization" : dfbToken }))
    except:
    	return False
    
    if response.status_code == requests.codes.ok:
    	return response.json()

    return False

def get_team_members(token):
	#need to correct this for teams > 1000 in production version via the cursor.
	dfbToken = "Bearer " + token
	try:
	    response = requests.post(url='https://api.dropboxapi.com/2/team/members/list',
	                    headers = ({ "Authorization" : dfbToken }))
	except:
		return False

	if response.status_code == requests.codes.ok:
		return response.json()

	return False

def get_dropbox_groups(token):
	dfbToken = "Bearer " + token
	try:
	    response = requests.post(url='https://api.dropboxapi.com/2/team/groups/list',
	                    headers = ({ "Authorization" : dfbToken }))
	except:
		return False

	if response.status_code == requests.codes.ok:
		return response.json()

	return False

#-------------------------
# Core API
#-------------------------

def get_user_account_detail(token, dfb_id):
	userToken = "Bearer " + token
	try:
	    response = requests.post(url='https://api.dropboxapi.com/2/users/get_current_account',
	                    headers = ({ "Authorization" : userToken, "Dropbox-API-Select-User" : dfb_id }))
	except:
		return False

	if response.status_code == requests.codes.ok:
		return response.json()

	return False

def get_file_or_folder_metdata(token, folder_name, dfb_id):
	userToken = "Bearer " + token
	data="{\"path\": \"" + folder_name + "\"}"
	try:
	    response = requests.post(url='https://api.dropboxapi.com/2/files/get_metadata',
	    				data=data,
	                    headers = ({ "Authorization" : userToken, "Content-Type" : "application/json", "Dropbox-API-Select-User" : dfb_id }))
	except:
		return False

	if response.status_code == requests.codes.ok:
		return response.json()

	return False

def create_dropbox_folder(token, folder_name, dfb_id):
	userToken = "Bearer " + token
	data="{\"path\": \"" + folder_name + "\"}"
	try:
	    response = requests.post(url='https://api.dropboxapi.com/2/files/create_folder',
	    				data=data,
	                    headers = ({ "Authorization" : userToken, "Content-Type" : "application/json", "Dropbox-API-Select-User" : dfb_id }))
	except:
		return False

	if response.status_code == requests.codes.ok:
		return response.json()

	return False

def list_folder_content(token, folder_path, dfb_id):
	userToken = "Bearer " + token
	data="{\"path\": \"" + folder_path + "\",\"recursive\": true,\"include_media_info\": false,\"include_deleted\": false}"
	try:
	    response = requests.post(url='https://api.dropboxapi.com/2/files/list_folder',
	    				data=data,
	                    headers = ({ "Authorization" : userToken, "Content-Type" : "application/json" , "Dropbox-API-Select-User" : dfb_id }))
	except:
		return False

	if response.status_code == requests.codes.ok:
		return response.json()

	return False

def share_dropbox_folder(token, folder_path, dfb_id):
	userToken = "Bearer " + token
	data = "{\"path\": \"" + folder_path + "\",\"acl_update_policy\": \"editors\",\"force_async\": false}"
	try:
	    response = requests.post(url='https://api.dropboxapi.com/2/sharing/share_folder',
	    				data=data,
	                    headers = ({ "Authorization" : userToken, "Content-Type" : "application/json" , "Dropbox-API-Select-User" : dfb_id }))
	except:
		return False

	if response.status_code == requests.codes.ok:
		return response.json()

	return False

def add_dropbox_share_permissions(token, shared_folder_id, group_id, access_level, dfb_id):
	userToken = "Bearer " + token
	data="{\"shared_folder_id\": \"" + shared_folder_id + "\",\"members\": [{\"member\": {\".tag\": \"dropbox_id\",\"dropbox_id\": \"" + group_id + "\"},\"access_level\": {\".tag\": \"" + access_level +"\"}}]}"
	try:
	    response = requests.post(url='https://api.dropboxapi.com/2/sharing/add_folder_member',
	    				data=data,
	                    headers = ({ "Authorization" : userToken, "Content-Type" : "application/json" , "Dropbox-API-Select-User" : dfb_id }))
	except:
		return False

	if response.status_code == requests.codes.ok:
		return response.json()

	return False

#---------------------------
# Parsing Only (no api call)
#---------------------------

def get_folders_to_create(folder_information, template_folder, top_level_folder_to_create):
	folder_list = []
	for f in folder_information["entries"]:
		original_folder = str(f["path_lower"])
		new_folder = "/" + str(top_level_folder_to_create)
		folder_to_add = original_folder.replace(template_folder.lower(), new_folder)
		folder_list.append(folder_to_add)

	return folder_list

def create_folders(token, list_of_folder_names):
	for f in list_of_folder_names:
		create_dropbox_folder(token, str(f))





