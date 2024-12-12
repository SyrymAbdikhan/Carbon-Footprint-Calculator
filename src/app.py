
import os

from dotenv import load_dotenv
load_dotenv('.env', override=True)

from api import api_bp
from models import db
from utils import funcs
from utils import db_funcs

from flask import Flask, request, redirect, render_template, url_for

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

app.register_blueprint(api_bp, url_prefix='/api')

app.secret_key = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculator/', methods=['GET', 'POST'])
def calculator():
    if request.method == 'GET':
        return render_template('calculator.html')

    data = request.form.to_dict()
    result_id = funcs.process_data(data)

    return redirect(url_for('result', result_id=result_id))


@app.route('/noresults/')
def noresults():
    return render_template('noresults.html')


@app.route('/result/')
@app.route('/result/<int:result_id>')
def result(result_id=None):
    if result_id is None:
        redirect(url_for('index'))

    data = db_funcs.get_results(result_id)
    if data is None:
        return redirect(url_for('noresults'))

    return render_template('result.html', data=data, averages=db_funcs.get_average())


@app.route('/results/')
def results():
    return render_template('results.html')


@app.errorhandler(404)
def error_404(e):
    return render_template('error.html')


if __name__ == '__main__':
    app.run(port=8888)
