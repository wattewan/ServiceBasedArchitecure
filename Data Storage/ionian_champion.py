from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class IonianChampion(Base):
    """ Ionian Champion """

    __tablename__ = "ionian_champion"

    id = Column(Integer, primary_key=True)
    champ_id = Column(String(25), nullable=False)
    champ_name = Column(String(25), nullable=False)
    weapon = Column(String(25), nullable=False)
    role = Column(String(25), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, champ_id, champ_name, weapon, role):
        """ Initializes a ionian champions info reading """
        self.champ_id = champ_id
        self.champ_name = champ_name
        self.weapon = weapon
        self.date_created = datetime.datetime.now()
        self.role = role

    def to_dict(self):
        """ Dictionary Representation of a ionian champion """
        dict = {}
        dict['id'] = self.id
        dict['champ_id'] = self.champ_id
        dict['champ_name'] = self.champ_name
        dict['weapon'] = self.weapon
        dict['role'] = self.role



        return dict