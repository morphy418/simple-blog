from  flask import Flask, render_template, request
import requests
import smtplib

posts = requests.get("https://api.npoint.io/2d878b86d0155b984396").json()

OWN_EMAIL = YOUR OWN EMAIL ADDRESS
OWN_PASSWORD = YOUR EMAIL ADDRESS PASSWORD

app = Flask(__name__)

@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)

@app.route('/about')
def about_page():
    return render_template("about.html")

@app.route("/post/<int:blog_id>")
def get_post(blog_id):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == blog_id:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)

@app.route('/contact', methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        data = request.form
        print(data["name"])
        print(data["email"])
        print(data["phone"])
        print(data["message"])
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
    else:
        return render_template("contact.html", msg_sent=False)

def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(OWN_EMAIL, OWN_PASSWORD)
        connection.sendmail(OWN_EMAIL, OWN_EMAIL, email_message)

if __name__ == "__main__":
    app.run(debug=True)