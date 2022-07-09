from project import db
from project.com.vo.CityVO import CityVO
from project.com.vo.LoginVO import LoginVO
from project.com.vo.PredictionVO import PredictionVO
from project.com.vo.RegisterVO import RegisterVO


class PredictionDAO:
    def insertPrediction(self, predictionVO):
        db.session.add(predictionVO)
        db.session.commit()

    def viewPrediction(self, predictionVO):
        predictionList = db.session.query(PredictionVO, CityVO) \
            .join(CityVO, PredictionVO.prediction_CityId == CityVO.cityId) \
            .filter(PredictionVO.prediction_RegisterId == predictionVO.prediction_RegisterId) \
            .all()

        return predictionList

    def adminViewPrediction(self):
        predictionList = db.session.query(PredictionVO, CityVO, RegisterVO, LoginVO) \
            .join(CityVO, PredictionVO.prediction_CityId == CityVO.cityId) \
            .join(RegisterVO, PredictionVO.prediction_RegisterId == RegisterVO.registerId) \
            .join(LoginVO, RegisterVO.register_LoginId == LoginVO.loginId) \
            .all()

        return predictionList

    def viewPredictionCrops(self, predictionVO):
        predictionList = db.session.query(PredictionVO.predictionCrop) \
            .distinct(PredictionVO.predictionCrop) \
            .filter(PredictionVO.prediction_RegisterId == predictionVO.prediction_RegisterId) \
            .all()
        return predictionList

    def userAjaxGetGraphData(self, predictionVO):
        predictionList = db.session.query(PredictionVO.predictionId, PredictionVO.predictionYear,
                                          PredictionVO.predictionYield, PredictionVO.predictionPrice) \
            .filter(PredictionVO.prediction_RegisterId == predictionVO.prediction_RegisterId) \
            .filter(PredictionVO.predictionCrop == predictionVO.predictionCrop) \
            .all()
        return predictionList

    def userdeletePrediction(self, predictionVO):
        predictionlist = PredictionVO.query.get(predictionVO.predictionId)
        db.session.delete(predictionlist)
        db.session.commit()
