from project import db
from project.com.vo.CropRatioVO import CropRatioVO


class CropRatioDAO:
    def insertCropRatio(self, rise_cropRatioVO, jowar_cropRatioVO):
        db.session.add(rise_cropRatioVO)
        db.session.add(jowar_cropRatioVO)
        db.session.commit()

    def viewCropName(self):
        cropNameList = db.session.query(CropRatioVO.cropName).distinct().all()
        return cropNameList

    def ajaxAreaRationByCropName(self, cropRatioVO):
        ajaxAreaRatioList = CropRatioVO.query.filter_by(cropName=cropRatioVO.cropName,
                                                        cropRatio_ImageId=cropRatioVO.cropRatio_ImageId).all()
        return ajaxAreaRatioList

    def cropDetailsByCropRatioId(self, cropRatioVO):
        cropRatioList = CropRatioVO.query.filter_by(cropRatioId=cropRatioVO.cropRatioId).all()
        return cropRatioList
