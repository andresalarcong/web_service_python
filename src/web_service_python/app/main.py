from fastapi import FastAPI
from ..controller import product_controller
from .lifespan import lifespan
from .exception_handlers import add_exception_handlers
app = FastAPI(lifespan=lifespan)

add_exception_handlers(app)

app.include_router(product_controller.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Product API"}