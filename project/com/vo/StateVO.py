from project import db


class StateVO(db.Model):
    __tablename__ = 'statemaster'
    stateId = db.Column('stateId', db.Integer, primary_key=True, autoincrement=True)
    stateName = db.Column('stateName', db.String(100))
    stateDescription = db.Column('stateDescription', db.String(100))

    def as_dict(self):
        return {
            'stateId': self.stateId,
            'stateName': self.stateName,
            'stateDescription': self.stateDescription
        }


db.create_all()
