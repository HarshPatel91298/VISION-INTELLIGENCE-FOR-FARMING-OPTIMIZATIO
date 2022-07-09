from project import db
from project.com.vo.CityVO import CityVO
from project.com.vo.RegisterVO import RegisterVO


class PredictionVO(db.Model):
    __tablename__ = 'predictionmaster'
    predictionId = db.Column('predictionId', db.Integer, primary_key=True, autoincrement=True)
    predictionCrop = db.Column('predictionCrop', db.String(100), nullable=False)
    predictionDate = db.Column('predictionDate', db.Date, nullable=False)
    predictionYear = db.Column('predictionYear', db.Integer, nullable=False)
    predictionArea = db.Column('predictionArea', db.Float, nullable=False)
    predictionProduction = db.Column('predictionProduction', db.Float, nullable=False)
    predictionYield = db.Column('predictionYield', db.Float)
    predictionPrice = db.Column('predictionPrice', db.Float)
    prediction_CityId = db.Column('prediction_CityId', db.Integer, db.ForeignKey(CityVO.cityId))
    prediction_RegisterId = db.Column('prediction_RegisterId', db.Integer, db.ForeignKey(RegisterVO.registerId))

    def as_dict(self):
        return {
            'predictionId': self.predictionId,
            'predictionCrop': self.predictionCrop,
            'predictionDate': self.predictionDate,
            'predictionYear': self.predictionYear,
            'predictionArea': self.predictionArea,
            'predictionProduction': self.predictionProduction,
            'predictionYield': self.predictionYield,
            'predictionPrice': self.predictionPrice,
            'prediction_CityId': self.prediction_CityId,
            'prediction_RegisterId': self.prediction_RegisterId

        }


db.create_all()
