from uuid import uuid4
from uuid import UUID
from fastapi import FastAPI, HTTPException,Depends
from typing import List
import models
from pydantic import UUID4, Field, BaseModel
from models import Cautions, Games;
from database import engine, SessionLocal
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(bind = engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# db : List[Games] = [ Games(
#     ID = UUID('b49c4c77-e426-4ece-aeb5-d75f4c711bf9'),
#     GameID = 1, 
#     HomeTeam = " United FC",
#     AwayTeam = "Rising",
#     HomeTeamScore = 0,
#     AwayTeamScore = 0,
#     HomeTeamYellow = [],
#     HomeTeamred = [],
#     AwayTeamYellow = [],
#     AwayTeamRed = [],
#     TimePerHalf = 35
# ), Games(
#     ID = UUID("b49c4c77-e426-4ece-aeb5-d75f4c711bf9"),
#     GameID = 2, 
#     HomeTeam = " Arsenal",
#     AwayTeam = "United",
#     HomeTeamScore = 2,
#     AwayTeamScore = 1,
#     HomeTeamYellow = [],
#     HomeTeamred = [],
#     AwayTeamYellow = [],
#     AwayTeamRed = [],
#     TimePerHalf = 35
# )]


class GamesBase(BaseModel):
    GameID :int = Field(gt=-1, lt =200000)
    HomeTeam :str = Field(min_length=1, max_length = 100)
    AwayTeam :str = Field(min_length=1, max_length = 100)
    HomeTeamScore: int = Field(gt=-1, lt =200000)
    AwayTeamScore: int = Field(gt=-1, lt =200000)
    TimePerHalf : int = Field(gt= 5, lt = 45)

class CautionsBase(BaseModel):
    GameID : int = Field(gt=-1, lt =200000)
    HomeTeamYellow : int = Field(gt=-1, lt =200000)
    HomeTeamRed : int = Field(gt=-1, lt =200000)
    AwayTeamYellow : int = Field(gt=-1, lt =200000)
    AwayTeamRed : int = Field(gt=-1, lt =200000)

    class Config:
        orm_mode = True
# # class Gamesorig(GamesBase):
# #     id: int

# #     class Config:
# #         orm_mode = True
# # class CautionsOrig(CautionsBase):
# #     id: int

# #     class Config:
# #         orm_mode = True
# class GameSchema(GamesBase):
#     Games: List[GamesBase]

# class CautionSchema(CautionsBase):
#     Cautions: List[CautionsBase]


# @app.get("/") 

# async def root():
#     return {"Hello World"}

@app.get("/fetchgames") 
async def fetch_games(db: Session = Depends(get_db)):
    return db.query(models.Games).all()

@app.get("/fetchCautions") 
async def fetch_cautions(db: Session = Depends(get_db)):
    return db.query(models.Cautions).all()

# @app.get("/Games", response_model=List[GameSchema])
# async def get_Games(db: Session = Depends(get_db)):
#     return db.query(models.Games).all()


@app.post("/postGames")
async def Add_games(game: GamesBase, db: Session = Depends(get_db)):
    games_model = models.Games()
    games_model.GameID = game.GameID
    games_model.HomeTeam = game.HomeTeam
    games_model.AwayTeam = game.AwayTeam
    games_model.HomeTeamScore = game.HomeTeamScore
    games_model.AwayTeamScore = game.AwayTeamScore
    games_model.TimePerHalf = game.TimePerHalf
    db.add(games_model)
    db.commit()

    return game

@app.post("/postCautions")
async def Add_Cautions(caution: CautionsBase, db: Session = Depends(get_db)):
    caution_model = models.Cautions()
    caution_model.GameID = caution.GameID
    caution_model.HomeTeamYellow = caution.HomeTeamYellow
    caution_model.HomeTeamRed = caution.HomeTeamRed
    caution_model.AwayTeamYellow = caution.AwayTeamYellow
    caution_model.AwayTeamRed = caution.AwayTeamRed
    db.add(caution_model)
    db.commit()

    return caution

# @app.delete("/api/v1/Games/{GameID}")
# async def Delete_games(GameID: int):
#     for game in db:
#         if game.GameID == GameID:
#             db.remove(game)
#             return{"Succesfully removed"}
#     raise HTTPException(status_code =404, detail=f" user with id: {GameID} does not exist")
        

    