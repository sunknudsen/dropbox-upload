from os.path import join, dirname, isfile, getsize, basename
from os import environ
from dotenv import load_dotenv # pip install python-dotenv
import sys
import dropbox # pip install dropbox

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

ACCESS_TOKEN = environ.get('DROPBOX_ACCESS_TOKEN')
CHUNK_SIZE = 4 * 1024 * 1024

if len(sys.argv) == 1 or not isfile(sys.argv[1]):
    sys.exit('usage: python dropbox-upload.py path_to_file')

file_path = sys.argv[1]
file_size = getsize(file_path)
file_name = basename(file_path)
file = open(file_path)
destination_path = '/' + file_name
dbx = dropbox.Dropbox(ACCESS_TOKEN)

if file_size <= CHUNK_SIZE:
	try:
	    dbx.files_upload(file.read(), destination_path, mode=dropbox.files.WriteMode.overwrite)
	    print 'done'
	except Exception, error:
		sys.exit(error.error)
else:
    try:
        upload_session_start_result = dbx.files_upload_session_start(file.read(CHUNK_SIZE))
        cursor = dropbox.files.UploadSessionCursor(upload_session_start_result.session_id, file.tell())
        commit = dropbox.files.CommitInfo(destination_path, dropbox.files.WriteMode.overwrite)
        while file.tell() < file_size:
            if ((file_size - file.tell()) <= CHUNK_SIZE):
                dbx.files_upload_session_finish(file.read(CHUNK_SIZE), cursor, commit)
                print 'done'
            else:
                dbx.files_upload_session_append(file.read(CHUNK_SIZE), cursor.session_id, cursor.offset)
                cursor.offset = file.tell()
    except Exception, error:
        sys.exit(error.error)
