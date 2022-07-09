from project import db
from project.com.vo.ImageVO import ImageVO


class CropRatioVO(db.Model):
    __tablename__ = 'cropratiomaster'
    cropRatioId = db.Column('cropRatioId', db.Integer, primary_key=True, autoincrement=True)
    cropName = db.Column('cropName', db.String(100))
    cropAreaRatio = db.Column('cropAreaRatio',db.VARCHAR(10))
    cropRatio_ImageId = db.Column('cropRatio_ImageId', db.Integer, db.ForeignKey(ImageVO.imageId))

    def as_dict(self):
        return {
            'cropRatioId': self.cropRatioId,
            'cropName': self.cropName,
            'cropAreaRatio': self.cropAreaRatio,
            'cropRatio_ImageId': self.cropRatio_ImageId,
        }


db.create_all()
