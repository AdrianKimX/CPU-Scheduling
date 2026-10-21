
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    name = "Alex"
    return render_template("index.html", username=name)

if __name__ == "__main__":
    app.run(debug=True)



from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        num1 = float(request.form["num1"])
        num2 = float(request.form["num2"])
        result = num1 + num2

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
