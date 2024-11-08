
import os
import requests

from models import db, CompanyEmissions


def get_db_average():
    averages = db.session.query(
        db.func.avg(CompanyEmissions.energy_co2),
        db.func.avg(CompanyEmissions.waste_co2),
        db.func.avg(CompanyEmissions.travel_co2),
        db.func.avg(CompanyEmissions.total_co2)
    ).one()

    return {
        'energy_co2': averages[0],
        'waste_co2': averages[1],
        'travel_co2': averages[2],
        'total_co2': averages[3],
    }


def get_ai_suggestion(company: CompanyEmissions, averages: dict = None):
    if averages is None:
        averages = get_db_average()

    url = os.getenv('API_ENDPOINT')

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {os.getenv("API_KEY")}'
    }

    prompt = os.getenv('AI_PROMPT').format(
        elec_bill=company.elec_bill,
        gas_bill=company.gas_bill,
        fuel_bill=company.fuel_bill,
        waste_kg=company.waste_kg,
        recycle_pct=company.recycle_pct,
        km_traveled=company.km_traveled,
        fuel_eff=company.fuel_eff,
        energy_co2=company.energy_co2,
        waste_co2=company.waste_co2,
        travel_co2=company.travel_co2,
        total_co2=company.total_co2,
        avg_energy_co2=averages['energy_co2'],
        avg_waste_co2=averages['waste_co2'],
        avg_travel_co2=averages['travel_co2'],
        avg_total_co2=averages['total_co2']
    )

    data = {
        'model': 'gpt-4-1106-preview',
        'messages': [
            {
                'role': 'user',
                'content': prompt
            }
        ],
        # copied from old project
        'temperature': 0.3,
        'top_p': 1,
        'n': 1,
        'stream': False,
        'presence_penalty': 0,
        'frequency_penalty': 0.5,
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return {
            'status_code': 0,
            'suggestion': response.json()['choices'][0]['message']['content']
        }
    else:
        return {
            'status_code': 1,
            'suggestion': f'Error: {response.status_code=} {response.text=}'
        }


def calculate_co2(data: dict):
    total_energy_usage = (
        data.get('elec-bill', 0) * 12 * 0.0005 +
        data.get('gas-bill', 0) * 12 * 0.0053 +
        data.get('fuel-bill', 0) * 12 * 2.32
    )

    total_waste = (
        data.get('waste-kg', 0) * 12 *
        (1 - data.get('recycle-pct', 0)/100) * 0.57
        # changed ... * (0.57 - recycle-pct)
        # to ... * (1 - recycle-pct) * 0.57
    )

    total_travel = (
        data.get('km-traveled', 0) *
        (1 / data.get('fuel-eff', 0)) * 2.31
    )

    total_energy_usage = round(total_energy_usage, 2)
    total_waste = round(total_waste, 2)
    total_travel = round(total_travel, 2)

    total_co2 = total_energy_usage + total_waste + total_travel
    total_co2 = round(total_co2, 2)

    return {
        'energy-usage': total_energy_usage,
        'waste': total_waste,
        'travel': total_travel,
        'total': total_co2
    }


def cast(data, type, default=None):
    try:
        return type(data)
    except Exception:
        return default
