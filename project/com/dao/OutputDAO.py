from project import db


class OutputDAO:
    def insertOutput(self, rise_outputVO, jowar_outputVO):
        db.session.add(rise_outputVO)
        db.session.add(jowar_outputVO)
        db.session.commit()
