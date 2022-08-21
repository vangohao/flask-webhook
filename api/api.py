from flask import Flask,request,json
import json
import requests

app = Flask(__name__)

f = open("url");
url = f.read()
f.close()

def get_template(event):
    f = open("template/%s.json" % event);
    s = f.read()
    f.close()
    return json.loads(s)

def send(data):
    result = {
        "msg_type": "interactive",
        "card": data
    }
    response = requests.post(url, json=result)
    print("response code: ", response.status_code)

@app.route('/')
def hello():
    return 'Webhooks with Python'

@app.route('/github',methods=['POST'])
def github():
    data = request.json
    event = request.headers["X-Github-Event"]
    if event == "ping":
        return "ping"
    elif event == "push":
        branch = data["ref"].split("/")[-1]
        repo_name = data["repository"]["name"]
        pusher = data["pusher"]["name"]
        head_commit_id = data["head_commit"]["id"]
        head_commit_message = data["head_commit"]["message"]
        head_commit_author_name = data["head_commit"]["author"]["name"]
        head_commit_author_email = data["head_commit"]["author"]["email"]

        result = get_template("push")
        result["elements"][0]["text"]["content"] = head_commit_message
        result["elements"][1]["fields"][0]["text"]["content"] = "**head commit id**\n" + head_commit_id
        result["elements"][1]["fields"][1]["text"]["content"] = "**head commit author**\n" + head_commit_author_name
        result["header"]["title"]["content"] = "@" + pusher + " pushed to " + repo_name + "/" + branch
    # print(f'Issue {data["issue"]["title"]} {data["action"]}')
    # print(f'{data["issue"]["body"]}')
    # print(f'{data["issue"]["url"]}')
    print( json.dumps(result))
    send(result)
    return json.dumps(result)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
