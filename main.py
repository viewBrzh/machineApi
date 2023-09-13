from fastapi import FastAPI
import api.tictactoe as tictactoe
import api.tictactoe_view as tictactoe_view
import api.tictactoe_train as tictactoe_train

app = FastAPI()
app.include_router(tictactoe.router)
app.include_router(tictactoe_view.router)
app.include_router(tictactoe_train.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
