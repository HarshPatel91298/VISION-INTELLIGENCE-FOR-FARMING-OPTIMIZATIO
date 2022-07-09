from project import db
from project.com.vo.CityVO import CityVO
from project.com.vo.ImageVO import ImageVO
from project.com.vo.OutputVO import OutputVO
from project.com.vo.StateVO import StateVO


class ImageDAO:
    def insertImage(self, imageVO):
        db.session.add(imageVO)
        db.session.commit()

    def viewImage(self):
        imageList = db.session.query(ImageVO,CityVO, StateVO).join(CityVO, ImageVO.image_CityId == CityVO.cityId) \
                    .join(StateVO,ImageVO.image_StateId == StateVO.stateId).all()
        return imageList

    def deleteImage(self, imageId):
        imageList = ImageVO.query.get(imageId)
        db.session.delete(imageList)
        db.session.commit()
        return imageList

    def deleteOutput(self, imageId):
        outputList = db.session.query(OutputVO).filter(OutputVO.output_imageId == imageId).first()
        db.session.delete(outputList)
        db.session.commit()

    def editImage(self, imageVO):
        imageList = ImageVO.query.filter_by(imageId=imageVO.imageId)
        return imageList

    def updateImage(self, imageVO):
        db.session.merge(imageVO)
        db.session.commit()

    def viewOutput(self, outputVO):
        outputList = OutputVO.query.filter_by(output_imageId=outputVO.output_imageId).all()
        return outputList

    def viewImageByCityId(self,imageVO):
        imageList = ImageVO.query.filter_by(image_CityId=imageVO.image_CityId).all()
        return imageList

    def viewCityByCityName(self,cityVO):
        cityList = CityVO.query.filter_by(cityName=cityVO.cityName).all()
        return cityList
