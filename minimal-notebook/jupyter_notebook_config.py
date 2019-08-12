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


# Directories configuration
import boto3
from s3contents import S3ContentsManager
from pgcontents.hybridmanager import HybridContentsManager
from notebook.services.contents.filemanager import FileContentsManager

HCM_mg = {
    # Associate the root directory with a FileContentsManager.
    # This manager will receive all requests that don't fall under any of the
    # other managers.
    '': FileContentsManager
}

# Get S3 creds from environment
aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
endpoint_url = os.environ.get("S3_ENDPOINT_URL")

# Check if S3 informations are there
if (aws_access_key_id and aws_access_key_id!='none'):
    # Initialize S3 connection (us-east-1 seems to be needed even when it is not used, in Ceph for example)
    # Last line to provide for test environment with no https
    s3 = boto3.resource('s3','us-east-1',
                        endpoint_url=endpoint_url,
                        aws_access_key_id = aws_access_key_id,
                        aws_secret_access_key = aws_secret_access_key,
                        use_ssl = True if 'https' in endpoint_url else False )
    for bucket in s3.buckets.all():
        HCM_mg.update({'datalake/'+bucket.name: S3ContentsManager})


# Intialize Hybrid Contents Manager with local silesystem
c.HybridContentsManager.manager_classes = HCM_mg

HCM_mk = {
    # Args for the FileContentsManager mapped to /directory
    'directory': {
        'root_dir': '/users'
    }
}

if (aws_access_key_id and aws_access_key_id!='none'):
    # We don't have to reinitialize the connection, thanks for "for" not being scoped
    for bucket in s3.buckets.all():
        HCM_mk.update({'datalake/'+bucket.name: {
            'access_key_id': aws_access_key_id,
            'secret_access_key': aws_secret_access_key,
            'endpoint_url': endpoint_url,
            'bucket': bucket.name
        } })

c.HybridContentsManager.manager_kwargs = HCM_mk




