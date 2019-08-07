import os

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


# S3 configuration
from s3contents import S3ContentsManager

c = get_config()

# Tell Jupyter to use S3ContentsManager for all storage.
if os.environ.get("AWS_ACCESS_KEY_ID")!='none':
    c.NotebookApp.contents_manager_class = S3ContentsManager
    c.S3ContentsManager.access_key_id = os.environ.get("AWS_ACCESS_KEY_ID")
    c.S3ContentsManager.secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY")
    c.S3ContentsManager.endpoint_url = os.environ.get("S3_ENDPOINT_URL")
    c.S3ContentsManager.bucket = 'valeria-users-' + os.environ.get("JUPYTERHUB_USER")
