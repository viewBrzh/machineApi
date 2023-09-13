from fastapi import APIRouter, HTTPException
from database import db_cursor, db_connection
from models.tictactoe import Tictactoe, TictactoeCreate, TictactoeUpdate

router = APIRouter()
@router.get("/tictactoe/", response_model=list[Tictactoe])
def read_all_tictactoe():
    query = "SELECT * FROM tictactoe order by id desc limit 20"
    db_cursor.execute(query)
    rows = db_cursor.fetchall()

    tictactoe = []
    column_names = [column[0] for column in db_cursor.description]
    for row in rows:
        tictactoe_dict = dict(zip(column_names, row))
        tictactoe.append(Tictactoe(**tictactoe_dict))

    return tictactoe

@router.get("/tictactoe/{data_id}", response_model=Tictactoe)
def read_tictactoe(data_id: int):
    query = "SELECT * FROM tictactoe WHERE id = %s"
    db_cursor.execute(query, (data_id,))
    row = db_cursor.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="data not found")

    tictactoe_dict = dict(zip(db_cursor.column_names, row))
    return Tictactoe(**tictactoe_dict)

@router.post("/tictactoe/", response_model=Tictactoe)
def create_tictactoe(data: TictactoeCreate):
    query = """
    INSERT INTO tictactoe (
        `top_left_square`, `top_middle_square`, `top_right_square`, `middle_left_square`, 
        `middle_middle_square`, `middle_right_square`, `bottom_left_square`, `bottom_middle_square`, 
        `bottom_right_square`, `class_`
    )
    VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
    )
    """
    values = (
        data.top_left_square, data.top_middle_square, data.top_right_square,
        data.middle_left_square, data.middle_middle_square, data.middle_right_square,
        data.bottom_left_square, data.bottom_middle_square, data.bottom_right_square,
        data.class_
    )
    
    db_cursor.execute(query, values)
    db_connection.commit()
    
    tictactoe_id = db_cursor.lastrowid  # Get the auto-generated id
    return Tictactoe(id=tictactoe_id, **data.dict())

@router.put("/tictactoe/{data_id}", response_model=Tictactoe)
def update_tictactoe(data_id: int, updated_data: TictactoeUpdate):
    query = """
        UPDATE tictactoe
        SET 
            `top_left_square` = %s, 
            `top_middle_square` = %s, 
            `top_right_square` = %s, 
            `middle_left_square` = %s,
            `middle_middle_square` = %s, 
            `middle_right_square` = %s, 
            `bottom_left_square` = %s,
            `bottom_middle_square` = %s, 
            `bottom_right_square` = %s,
            `class_` = %s
        WHERE id = %s
    """
    values = (
        updated_data.top_left_square, 
        updated_data.top_middle_square, 
        updated_data.top_right_square,
        updated_data.middle_left_square, 
        updated_data.middle_middle_square, 
        updated_data.middle_right_square,
        updated_data.bottom_left_square, 
        updated_data.bottom_middle_square, 
        updated_data.bottom_right_square,
        updated_data.class_,
        data_id
    )

    
    db_cursor.execute(query, values)
    db_connection.commit()
    
    updated_data_dict = updated_data.dict()
    updated_data_dict["id"] = data_id
    return Tictactoe(**updated_data_dict)

@router.delete("/tictactoe/{data_id}", response_model=Tictactoe)
def delete_tictactoe(data_id: int):
    query = "SELECT * FROM tictactoe WHERE id = %s"
    db_cursor.execute(query, (data_id,))
    row = db_cursor.fetchone()

    if row is None:
        raise HTTPException(status_code=404, detail="Data not found")
    
    deleted_tictactoe = dict(zip(db_cursor.column_names, row))
    
    delete_query = "DELETE FROM tictactoe WHERE id = %s"
    db_cursor.execute(delete_query, (data_id,))
    db_connection.commit()
    
    return deleted_tictactoe