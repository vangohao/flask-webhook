import sys
sys.path.insert(0, "/var/www/flask-webhook/")
sys.stdout = sys.stderr

from api import app as application
if __name__ == "__main__":
   application.run()
