from project import db
from project.com.vo.CityVO import CityVO
from project.com.vo.ImageVO import ImageVO
from project.com.vo.StateVO import StateVO


class CityDAO:
    def insertCity(self, cityVO):
        db.session.add(cityVO)
        db.session.commit()

    def viewCity(self):
        cityList = db.session.query(CityVO, StateVO).join(StateVO, CityVO.city_StateId == StateVO.stateId).all()
        print(cityList, 'cityList')
        return cityList

    def deleteCity(self, cityVO):
        cityList = CityVO.query.get(cityVO.cityId)
        db.session.delete(cityList)
        db.session.commit()

    def editCity(self, cityVO):
        cityList = CityVO.query.filter_by(cityId=cityVO.cityId).all()

        return cityList

    def updateCity(self, cityVO):
        db.session.merge(cityVO)
        db.session.commit()

    def viewCityDetails(self):
        cityList = db.session.query(CityVO, ImageVO)\
            .join(ImageVO, CityVO.cityId == ImageVO.image_CityId).all()

        return cityList

    def viewCityDetailsByState(self,cityVO):

       cityList = db.session.query(CityVO.cityName) \
            .order_by(CityVO.cityName) \
            .filter(CityVO.city_StateId == cityVO.city_StateId)


       return cityList