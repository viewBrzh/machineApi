from pydantic import BaseModel

class TictactoeBase(BaseModel):
    top_left_square: str
    top_middle_square: str
    top_right_square: str
    middle_left_square: str
    middle_middle_square: str
    middle_right_square: str
    bottom_left_square: str
    bottom_middle_square: str
    bottom_right_square: str
    class_: str  

class TictactoePredictBase(BaseModel):
    top_left_square: str
    top_middle_square: str
    top_right_square: str
    middle_left_square: str
    middle_middle_square: str
    middle_right_square: str
    bottom_left_square: str
    bottom_middle_square: str
    bottom_right_square: str

class TictactoeCreate(TictactoeBase):
    pass

class TictactoeUpdate(TictactoeBase):
    pass

class Tictactoe(TictactoeBase):
    id: int

    class Config:
        orm_mode = True

