
import os

from utils import calculate_co2, get_db_average, cast
from models import db, CompanyEmissions
from api import api_bp

from flask import Flask, request, redirect, render_template

from dotenv import load_dotenv
load_dotenv('.env', override=True)

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

    data = {
        'elec-bill': cast(request.form.get('elec-bill', 0), float, 0),
        'gas-bill': cast(request.form.get('gas-bill', 0), float, 0),
        'fuel-bill': cast(request.form.get('fuel-bill', 0), float, 0),
        'waste-kg': cast(request.form.get('waste-kg', 0), float, 0),
        'recycle-pct': cast(request.form.get('recycle-pct', 0), float, 0),
        'km-traveled': cast(request.form.get('km-traveled', 0), float, 0),
        'fuel-eff': cast(request.form.get('fuel-eff', 0), float, 0)
    }
    resp = calculate_co2(data)

    comp_emisson = CompanyEmissions(
        name=request.form.get('comp-name', 'Unknown'),
        elec_bill=data.get('elec-bill', 0),
        gas_bill=data.get('gas-bill', 0),
        fuel_bill=data.get('fuel-bill', 0),
        waste_kg=data.get('waste-kg', 0),
        recycle_pct=data.get('recycle-pct', 0),
        km_traveled=data.get('km-traveled', 0),
        fuel_eff=data.get('fuel-eff', 0),
        energy_co2=resp.get('energy-usage', 0),
        waste_co2=resp.get('waste', 0),
        travel_co2=resp.get('travel', 0),
        total_co2=resp.get('total', 0),
    )

    db.session.add(comp_emisson)
    db.session.commit()

    return redirect(f'/result/?result_id={comp_emisson.id}')


@app.route('/noresults/')
def noresults():
    return render_template('noresults.html')


@app.route('/result/')
def result():
    result_id = request.args.get('result_id', None, type=int)
    if result_id is None:
        redirect('index')

    data = CompanyEmissions.query.filter_by(id=result_id).first()
    if data is None:
        return redirect('/noresults')

    return render_template('result.html', data=data, averages=get_db_average())


@app.route('/results/')
def results():
    return render_template('results.html')


if __name__ == '__main__':
    app.run(port=8888)
