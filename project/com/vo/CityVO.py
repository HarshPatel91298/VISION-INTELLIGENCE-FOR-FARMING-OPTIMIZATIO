from project import db
from project.com.vo.StateVO import StateVO


class CityVO(db.Model):
    __tablename__ = 'citymaster'
    cityId = db.Column('cityId', db.Integer, primary_key=True, autoincrement=True)
    cityName = db.Column('cityName', db.String(100), nullable=False)
    cityDescription = db.Column('cityDescription', db.String(300), nullable=False)
    city_StateId = db.Column('city_StateId', db.Integer, db.ForeignKey(StateVO.stateId))

    def as_dict(self):
        return {
            'cityId': self.cityId,
            'cityName': self.cityName,
            'cityDescription': self.cityDescription,
            'city_StateId': self.city_StateId
        }


db.create_all()
