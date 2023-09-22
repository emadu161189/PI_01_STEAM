import pandas as pd
import numpy as np
import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/peliculas_idioma/{a}")
def prueba(a):
    return a



if __name__ == "__main__":
        uvicorn.run(app)