# DB_FOLDER_AUTO

Requires:
Python 2.7 +
Pip

Set up dependencies:
virtualenv venv && source venv/bin/activate
pip install -r requirements.txt

The Dropbox CORE api work is authenticated via OAuth. 
A static business team token is required for so that non team admins may set up projects. 
The token is configured as an environment variable (OS, or Heroku) with: 

export DB_AUTH=YOURKEYHERE
(or a Heroku config variable called DB_AUTH)

Running:
python app.py runserver