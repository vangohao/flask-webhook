from flask import Flask,request,json
import json
import requests

app = Flask(__name__)

f = open("url")
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

def parse_labels(labels):
    labels_list = []
    colors_list = []
    for label in labels:
        labels_list.append(label["name"])
        colors_list.append(label["color"])
    
    label_string = ""
    for label in labels_list:
        label_string = label_string + "**" + label + "** "
    return label_string

def remove_cr(text):
    return "\n".join(text.splitlines())

@app.route('/')
def hello():
    return 'Webhooks with Python'

@app.route('/github',methods=['POST'])
def github():
    data = request.json
    event = request.headers["X-Github-Event"]

    flag = True
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
    elif event == "issues":
        event_type = "issue"
        event_action = data["action"]

        event_created_at = data[event_type]["created_at"]
        event_updated_at = data[event_type]["updated_at"]
        event_url = data[event_type]["url"]
        repo_name = data["repository"]["name"]
        event_number = data[event_type]["number"]
        event_title = data[event_type]["title"]
        event_user = data[event_type]["user"]["login"]
        event_labels = data[event_type]["labels"]
        event_body = data[event_type]["body"]

        result = get_template(event_type)
        result["elements"][0]["text"]["content"] = "**Title: **[" + event_title + "]("+event_url+")"
        result["elements"][1]["text"]["content"] = "labels: " + parse_labels(event_labels)
        result["elements"][2]["text"]["content"] = remove_cr(event_body)
        result["header"]["title"]["content"]= "@" + event_user + " " + event_action + " issue #" + str(event_number) + " in " + repo_name

        
        if (event_created_at == event_updated_at) and event_action != "opened":
            flag = False

    elif event == "pull_request":
        event_type = "pull_request"
        event_action = data["action"]

        event_created_at = data[event_type]["created_at"]
        event_updated_at = data[event_type]["updated_at"]
        event_url = data[event_type]["url"]
        repo_name = data["repository"]["name"]
        event_number = data[event_type]["number"]
        event_title = data[event_type]["title"]
        event_user = data[event_type]["user"]["login"]
        event_labels = data[event_type]["labels"]
        event_body = data[event_type]["body"]

        head_branch = data[event_type]["head"]["label"]
        base_branch = data[event_type]["base"]["label"]


        result = get_template(event_type)
        result["elements"][0]["text"]["content"] = "**Title: **[" + event_title + "]("+event_url+")"
        result["elements"][1]["text"]["content"] = "labels: " + parse_labels(event_labels)
        result["elements"][2]["text"]["content"] = remove_cr(event_body)

        result["elements"][3]["fields"][0]["text"]["content"] = "**From**\n" + head_branch
        result["elements"][3]["fields"][1]["text"]["content"] = "**To**\n" + base_branch

        result["header"]["title"]["content"]= "@" + event_user + " " + event_action + " pull request #" + str(event_number) + " in " + repo_name

        
        if (event_created_at == event_updated_at) and event_action != "opened":
            flag = False
    

    print( json.dumps(result))
    if flag:
        send(result)
    return json.dumps(result)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
