from os.path import join, dirname
from os import environ
from dotenv import load_dotenv # pip install python-dotenv
import dropbox # pip install dropbox
import sys

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

APP_KEY = environ.get('DROPBOX_APP_KEY')
APP_SECRET = environ.get('DROPBOX_APP_SECRET')

auth_flow = dropbox.oauth.DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)

authorize_url = auth_flow.start()

print '1. Go to: ' + authorize_url
print '2. Click "Allow" (you might have to log in first)'
print '3. Copy the authorization code.'

auth_code = raw_input('Enter the authorization code here: ').strip()

try:
    oauth_result = auth_flow.finish(auth_code)
except Exception, error:
    sys.exit(error)

dbx = dropbox.Dropbox(oauth_result.access_token)

try:
    account = dbx.users_get_account(oauth_result.account_id)
    print 'Email: ' + account.email
    print 'Access token: ' + oauth_result.access_token
except Exception, error:
    sys.exit(error)
