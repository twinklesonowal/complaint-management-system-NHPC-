from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>IT Asset Complaint & Service Management System</h1>
    <h3>Internship Project</h3>
    <p>Developed for the IT Department</p>
    """

if __name__ == "__main__":
    app.run(debug=True)