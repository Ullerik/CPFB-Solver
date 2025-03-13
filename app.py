from flask import Flask, render_template, request
from backend.solver import process_scramble  # Import the function if it's in your backend

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    image_url = None
    output_list = None
    scramble = None
    rotation = None

    if request.method == "POST":
        scramble = request.form["scramble"]
        rotation = request.form["rotation"]  # Get the rotation value
        output_list = process_scramble(scramble, rotation)  # Pass both scramble and rotation

    return render_template("index.html", output_list=output_list, scramble=scramble, rotation=rotation, image_url=image_url)

if __name__ == "__main__":
    app.run(debug=True)
