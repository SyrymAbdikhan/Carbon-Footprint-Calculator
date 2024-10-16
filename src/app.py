
from flask import Flask, request, session, redirect, render_template

from utils import calculate_co2, cast

app = Flask(__name__)
app.secret_key = '!!r&W!D2pmyqBInQxRytHZh0aY+eGjWQtF&9Jg2P|dXN1cWv6Dza0S5Gak0AHQsZ'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculator/', methods=['GET', 'POST'])
def calculator():
    if request.method == 'GET':
        return render_template('calculator.html')

    data = {
        'mo-elec-bill': cast(request.form.get('mo-elec-bill', 0), float, 0),
        'mo-gas-bill': cast(request.form.get('mo-gas-bill', 0), float, 0),
        'mo-fuel-bill': cast(request.form.get('mo-fuel-bill', 0), float, 0),
        'mo-waste-kg': cast(request.form.get('mo-waste-kg', 0), float, 0),
        'waste-rec-pct': cast(request.form.get('waste-rec-pct', 0), float, 0),
        'yr-travel-km': cast(request.form.get('yr-travel-km', 0), float, 0),
        '100km-eff-ltr': cast(request.form.get('100km-eff-ltr', 0), float, 0)
    }
    session['resp'] = calculate_co2(data)
    
    return redirect('/results')


@app.route('/results/')
def results():
    return render_template('results.html', data=session.get('resp'))


if __name__ == '__main__':
    app.run(port=8888)
