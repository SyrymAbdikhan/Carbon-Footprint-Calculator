
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

db = SQLAlchemy()


class CompanyEmissions(db.Model):
    __tablename__ = 'company_emissions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, server_default=func.now())

    elec_bill = db.Column(db.Float)
    gas_bill = db.Column(db.Float)
    fuel_bill = db.Column(db.Float)

    waste_kg = db.Column(db.Float)
    recycle_pct = db.Column(db.Float)  # from 0 to 100

    km_traveled = db.Column(db.Float)
    fuel_eff = db.Column(db.Float)  # from 0 to 100

    energy_co2 = db.Column(db.Float)
    waste_co2 = db.Column(db.Float)
    travel_co2 = db.Column(db.Float)
    total_co2 = db.Column(db.Float)

    def __repr__(self):
        return f"<Company '{self.name}' {self.created_at}>"
