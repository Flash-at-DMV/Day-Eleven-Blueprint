from flask import Flask, render_template, request, redirect
from scrapper import aggregate_subreddits, get_status_by_subreddit

app = Flask("RedditNews")

subreddits = [
    "javascript",
    "reactjs",
    "reactnative",
    "programming",
    "css",
    "golang",
    "flutter",
    "rust",
    "django"
]

@app.route("/")
def home():
  return render_template("home.html", subreddits=subreddits)

@app.route("/read")
def read():
  selected = []
  for subreddit in subreddits:
    if subreddit in request.args:
      selected.append(subreddit)
  posts = aggregate_subreddits(selected)
  posts.sort(key=lambda post: post['votes'], reverse=True)
  return render_template("read.html", selected=selected, posts=posts)

@app.route("/add", methods=["POST"])
def add():
  new_subreddit = request.form["new-subreddit"]

  error_msg = ""

  if "/r/" in new_subreddit:
    error_msg = "Write the name without /r/"
  elif new_subreddit in subreddits:
    error_msg = "Already exists"
  else:
    status_code = get_status_by_subreddit(new_subreddit)

    if status_code == 404:
      error_msg = "That subreddit does not exist."
    else:
      subreddits.append(new_subreddit)
      return redirect("/")

  return render_template("add.html", error_msg = error_msg)

app.run(host="0.0.0.0")