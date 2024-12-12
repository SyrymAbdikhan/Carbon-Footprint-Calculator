
from models import db, CompanyEmissions, ReductionSuggestions


def get_results(result_id: int):
    return CompanyEmissions.query.filter_by(id=result_id).first()


def get_average():
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


def save_results(name: str, input_data: dict, result_data: dict):
    comp_emisson = CompanyEmissions(
        name=name,
        elec_bill=input_data.get('elec-bill', 0),
        gas_bill=input_data.get('gas-bill', 0),
        fuel_bill=input_data.get('fuel-bill', 0),
        waste_kg=input_data.get('waste-kg', 0),
        recycle_pct=input_data.get('recycle-pct', 0),
        km_traveled=input_data.get('km-traveled', 0),
        fuel_eff=input_data.get('fuel-eff', 0),
        energy_co2=result_data.get('energy-usage', 0),
        waste_co2=result_data.get('waste', 0),
        travel_co2=result_data.get('travel', 0),
        total_co2=result_data.get('total', 0),
    )

    db.session.add(comp_emisson)
    db.session.commit()

    return comp_emisson.id


def save_suggestion(result_id, suggestion):
    suggestion = ReductionSuggestions(
        result_id=result_id,
        suggestion=suggestion
    )
    db.session.add(suggestion)
    db.session.commit()
