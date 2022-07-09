from project import db
from project.com.vo.ImageVO import ImageVO
from project.com.vo.StateVO import StateVO


class OutputVO(db.Model):
    __tablename__ = 'outputmaster'
    outputId = db.Column('outputId', db.Integer, primary_key=True, autoincrement=True)
    outputCrop = db.Column('outputCrop', db.String(20), nullable=False)
    outputFileName = db.Column('outputFileName', db.String(100), nullable=False)
    outputFilePath = db.Column('outputFilePath', db.String(100), nullable=False)
    outputUploadDate = db.Column('outputUploadDate', db.Date, nullable=False)
    outputUploadTime = db.Column('outputUploadTime', db.Time, nullable=False)
    output_imageId = db.Column('output_imageId', db.Integer, db.ForeignKey(ImageVO.imageId))
    output_stateId = db.Column('output_stateId', db.Integer, db.ForeignKey(StateVO.stateId))

    def as_dict(self):
        return {
            'outputId': self.outputId,
            'outputCrop': self.outputCrop,
            'outputFileName': self.outputFileName,
            'outputFilePath': self.outputFilePath,
            'outputUploadDate': self.outputUploadDate,
            'outputUploadTime': self.outputUploadTime,
            'output_imageId': self.output_imageId,
            'output_stateId': self.output_stateId

        }


db.create_all()
