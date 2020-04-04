import sys

project_home = u"/home/granthussey/ACNH-Fish-Database/webapp"
if project_home not in sys.path:
    sys.path = [project_home] + sys.path


from dashtable_app import app

application = app.server
