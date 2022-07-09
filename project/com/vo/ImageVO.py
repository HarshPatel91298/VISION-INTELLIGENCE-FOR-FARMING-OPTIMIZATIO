from project import db
from project.com.vo.CityVO import CityVO
from project.com.vo.StateVO import StateVO


class ImageVO(db.Model):
    __tablename__ = 'imagemaster'
    imageId = db.Column('imageId', db.Integer, primary_key=True, autoincrement=True)
    imageFileName = db.Column('imageFileName', db.String(100), nullable=False)
    imageFilePath = db.Column('imageFilePath', db.String(100), nullable=False)
    imageUploadDate = db.Column('imageUploadDate', db.Date, nullable=False)
    imageUploadTime = db.Column('imageUploadTime', db.Time, nullable=False)
    image_StateId = db.Column('image_StateId', db.Integer, db.ForeignKey(StateVO.stateId))
    image_CityId = db.Column('image_CityId', db.Integer, db.ForeignKey(CityVO.cityId))

    def as_dict(self):
        return {
            'imageId': self.imageId,
            'imageFileName': self.imageFileName,
            'imageFilePath': self.imageFilePath,
            'imageUploadDate': self.imageUploadDate,
            'imageUploadTime': self.imageUploadTime,
            'image_StateId': self.image_StateId,
        }


db.create_all()
