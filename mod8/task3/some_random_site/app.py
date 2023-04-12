import os
from flask import Flask, render_template


root_dir = os.path.dirname(os.path.abspath(__file__))
template_folder = os.path.join(root_dir, 'templates')
js_directory = os.path.join(template_folder, 'static/js')
app = Flask(__name__, template_folder=template_folder)


@app.route('/')
def index():
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug=True)
