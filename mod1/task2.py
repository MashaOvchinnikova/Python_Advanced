from flask import Flask

app = Flask(__name__)
cars_list = ['Chevrolet', 'Renault', 'Ford', 'Lada']


@app.route('/cars')
def cars():
    return ', '.join(cars_list)


if __name__ == "__main__":
    app.run(debug=True)
