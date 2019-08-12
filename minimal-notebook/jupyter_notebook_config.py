##################################
# Default Notebook configuration #
##################################

import os

c = get_config()

c.NotebookApp.ip = '0.0.0.0'
c.NotebookApp.port = 8080
c.NotebookApp.open_browser = False
c.NotebookApp.quit_button = False

password = os.environ.get('JUPYTER_NOTEBOOK_PASSWORD')
if password:
    import notebook.auth
    c.NotebookApp.password = notebook.auth.passwd(password)
    del password
    del os.environ['JUPYTER_NOTEBOOK_PASSWORD']

image_config_file = '/opt/app-root/src/.jupyter/jupyter_notebook_config.py'

if os.path.exists(image_config_file):
    with open(image_config_file) as fp:
        exec(compile(fp.read(), image_config_file, 'exec'), globals())


#######################
# Directories mapping #
#######################
import boto3
from s3contents import S3ContentsManager
from pgcontents.hybridmanager import HybridContentsManager
from notebook.services.contents.filemanager import FileContentsManager

# We use HybridContentsManager (https://github.com/quantopian/pgcontents),
# FileContentsManager for accessing local volumes
# and S3ContentsManager (https://github.com/danielfrg/s3contents) to connect to the datalake
c.NotebookApp.contents_manager_class = HybridContentsManager

# Intialize Hybrid Contents Manager with local filesystem
c.HybridContentsManager.manager_classes = {
    # Associate the root directory with a FileContentsManager.
    # This manager will receive all requests that don't fall under any of the
    # other managers.
    '': FileContentsManager
}

# Get S3 credentials from environment variables
aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
endpoint_url = os.environ.get("S3_ENDPOINT_URL")

# Add datalake connection information
if (aws_access_key_id and aws_access_key_id!='none'): # Make sure we have usable S3 informations are there before configuring
    # Initialize S3 connection (us-east-1 seems to be needed even when it is not used, in Ceph for example)
    s3 = boto3.resource('s3','us-east-1',
                        endpoint_url=endpoint_url,
                        aws_access_key_id = aws_access_key_id,
                        aws_secret_access_key = aws_secret_access_key,
                        use_ssl = True if 'https' in endpoint_url else False ) # Provides for test environment with no https
    # Enumerate all accessible buckets and create a folder entry in HybridContentsManager
    for bucket in s3.buckets.all():
        c.HybridContentsManager.manager_classes.update({'datalake/'+bucket.name: S3ContentsManager})

# Initalize arguments for local filesystem
c.HybridContentsManager.manager_kwargs = {
    # Args for the FileContentsManager mapped to /directory
    '': {
        'root_dir': '/users'
    }
}

# Add datalake connections arguments
if (aws_access_key_id and aws_access_key_id!='none'):
    # We don't have to reinitialize the connection, thanks for previous "for" not being scoped
    # Enumerate all buckets and configure access
    for bucket in s3.buckets.all():
        c.HybridContentsManager.manager_kwargs.update({'datalake/'+bucket.name: {
            'access_key_id': aws_access_key_id,
            'secret_access_key': aws_secret_access_key,
            'endpoint_url': endpoint_url,
            'bucket': bucket.name
        } })




