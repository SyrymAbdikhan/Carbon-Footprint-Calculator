
import os
import requests

from models import CompanyEmissions
from utils import db_funcs

URL = os.getenv('API_ENDPOINT')
HEADERS = {'Content-Type': 'application/json',
           'Authorization': f'Bearer {os.getenv("API_KEY")}'}
PROMPT = os.getenv('AI_PROMPT')
data = {
    'model': 'gpt-4-1106-preview',
    'messages': [
        {
            'role': 'user',
            'content': ''
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


def get_suggestion(company: CompanyEmissions, averages: dict = None):
    if averages is None:
        averages = db_funcs.get_average()

    prompt = PROMPT.format(
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

    data['messages'][0]['content'] = prompt
    response = requests.post(URL, headers=HEADERS, json=data)

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
