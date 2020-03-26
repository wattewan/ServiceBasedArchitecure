from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class PiltoverChampion(Base):
    """ Piltover Champion """

    __tablename__ = "piltover_champion"

    id = Column(Integer, primary_key=True)
    champ_id = Column(String(25), nullable=False)
    champ_name = Column(String(25), nullable=False)
    technology_used = Column(String(100), nullable=False)
    city = Column(String(25), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, champ_id, champ_name, technology_used, city):
        """ Initializes a piltover champions info reading """
        self.champ_id = champ_id
        self.champ_name = champ_name
        self.date_created = datetime.datetime.now()
        self.technology_used = technology_used
        self.city = city

    def to_dict(self):
        """ Dictionary Representation of a piltover champion """
        dict = {}
        dict['id'] = self.id
        dict['champ_id'] = self.champ_id
        dict['champ_name'] = self.champ_name
        dict['technology_used'] = self.technology_used
        dict['city'] = self.city

        return dict