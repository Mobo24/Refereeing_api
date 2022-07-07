from multiprocessing.dummy import Array
from numpy import infty, little_endian
from pydantic import BaseModel
from typing import Optional
from uuid import UUID, uuid4
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship
from database import Base

class Games(Base):
    __tablename__ = "Games"
    ID = Column(Integer, primary_key = True, index = True)
    GameID = Column(Integer)
    HomeTeam = Column(String)
    AwayTeam = Column(String)
    HomeTeamScore = Column(Integer)
    AwayTeamScore = Column(Integer)                                                                                                                                                                                                     
    TimePerHalf = Column(Integer)
    caution = relationship('Cautions', backref = 'author')

    def __Game__(self):
        return f"<Game ID: {self.GameID}"

class Cautions(Base):   
    
    __tablename__ = "Cautions"

    ID = Column(Integer, primary_key = True, index = True)
    HomeTeamYellow = Column(Integer) 
    HomeTeamRed = Column(Integer) 
    AwayTeamYellow = Column(Integer)   
    AwayTeamRed = Column(Integer) 
    GameID = Column(Integer, ForeignKey("Games.GameID"))

    def __Cautions__(self):
        return f"<Game ID {self.GameID}"   

Games_Cautions = Table('Games_cautions', Base.metadata,
    Column('Game_id', ForeignKey('Games.ID'), primary_key=True),
    Column('caution_id', ForeignKey('Cautions.ID'), primary_key=True)
)

   




