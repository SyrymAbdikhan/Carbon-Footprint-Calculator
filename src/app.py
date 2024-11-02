
from flask import Flask, request, session, redirect, render_template

from utils import calculate_co2, cast

app = Flask(__name__)
# store secret_key in .env file, this is only for testing purposes
app.secret_key = '!!r&W!D2pmyqBInQxRytHZh0aY+eGjWQtF&9Jg2P|dXN1cWv6Dza0S5Gak0AHQsZ'


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
    session['resp'] = calculate_co2(data)

    return redirect('/results')


@app.route('/noresults/')
def noresults():
    return render_template('noresults.html')


@app.route('/results/')
def results():
    data = session.get('resp')
    if data is None:
        return redirect('/noresults')
    return render_template('results.html', data=data)


if __name__ == '__main__':
    app.run(port=8888)
