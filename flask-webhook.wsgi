import sys
import os
sys.path.insert(0, "/var/www/flask-webhook/")
sys.stdout = open(os.devnull, 'w')

from api import app as application
if __name__ == "__main__":
   application.run()
