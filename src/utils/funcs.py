
from utils import db_funcs


def process_data(data: dict):
    fields = ['elec-bill', 'gas-bill', 'fuel-bill',
              'waste-kg', 'recycle-pct', 'km-traveled', 'fuel-eff']
    for field in fields:
        data[field] = cast(data.get(field, 0), float, 0)

    resp = calculate_co2(data)
    result_id = db_funcs.save_results(data.get('comp-name', 'Unknown'), data, resp)

    return result_id


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
        data.get('km-traveled', 0) * data.get('fuel-eff', 0) * 2.31
        # changed ... * (1 / fuel-eff)
        # to ... * fuel-eff
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
