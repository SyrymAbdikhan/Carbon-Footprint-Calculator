
def calculate_co2(data: dict):
    total_energy_usage = (
        data.get('mo-elec-bill', 0) * 12 * 0.0005 +
        data.get('mo-gas-bill', 0) * 12 * 0.0053 +
        data.get('mo-fuel-bill', 0) * 12 * 2.32
    )

    total_waste = (
        data.get('mo-waste-kg', 0) * 12 *
        (1 - data.get('waste-rec-pct', 0)/100) * 0.57
        # changed ... * (0.57 - waste-rec-pct)
        # to ... * (1 - waste-rec-pct) * 0.57
    )
    
    total_travel = (
        data.get('yr-travel-km', 0) *
        (1 / data.get('100km-eff-ltr', 0)) * 2.31
    )

    total_co2 = total_energy_usage + total_waste + total_travel

    return {
        'total_energy_usage': total_energy_usage,
        'total_waste': total_waste,
        'total_travel': total_travel,
        'total_co2': total_co2
    }


def cast(data, type, default=None):
    try:
        return type(data)
    except Exception:
        return default
