import sys
sys.path.insert(0, "/root/flask-webhook/api/")
from api import app as application

if __name__ == "__main__":
   application.run()