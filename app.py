from flask import Flask, render_template, request
app=Flask(__name__)
@app.route("/", methods=["GET", "POST"])

def home():
    result=None
    if request.method == "POST":
        num_process= int(request.form['num_process'])
        result= num_process

    return render_template("test.html", result=result)
if __name__ == "__main__":
    app.run(debug=True)