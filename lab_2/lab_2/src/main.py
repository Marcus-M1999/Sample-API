import uvicorn
from fastapi import FastAPI, HTTPException
import joblib
from pydantic import BaseModel, validator, ValidationError, Extra
import numpy as np
import json
from datetime import datetime


class DataInputCheck(BaseModel):
    class Config:
        extra = Extra.forbid

    MedInc: float
    HouseAge: float
    AveRooms: float
    AveBedrms: float
    Population: float
    AveOccup: float
    Latitude: float
    Longitude: float


    @validator('MedInc', 'Population','HouseAge', 'AveRooms', 'AveBedrms', 'Population', 'AveOccup')
    def valid_med(cls, v):
        assert isinstance(v, float), "Data must be a float"
        if v < 0:
          raise ValueError('Must be positive')
        return v


class DataOutputCheck(BaseModel):
    output: list

    @validator('output')
    def valid_pred(cls, v):
        assert isinstance(v[0][0], float), "Prediction must be a float"
        if v[0][0] < 0:
            raise ValueError('Must be positive')
        return v


model = joblib.load("../model_pipeline.pkl")
app = FastAPI()

#all HTTP code justifications were taken from this website: https://developer.mozilla.org/en-US/docs/Web/HTTP/Status#server_error_responses

#HTTP response 422 means "The request was well-formed but was unable to be followed due to semantic errors."
#ie: not filling in the name parameter
@app.get("/hello")
async def hello(name):
    if not name:
        raise HTTPException(status_code=422, detail="Bad Request: Invalid or missing name.")
    return {"name": "Hello " + name}

#501 is the "Not Implemented" error that all server are require to support
@app.get("/")
async def root():
    raise HTTPException(status_code=501, detail="not implemented")


@app.post("/predict", response_model=DataOutputCheck)
async def prediction(data: DataInputCheck):

    data_loaded = [
         [data.MedInc,
         data.HouseAge,
         data.AveRooms,
         data.AveBedrms,
         data.Population,
         data.AveOccup,
         data.Latitude,
         data.Longitude]
    ]
    try:
        dt = np.array(data_loaded).reshape(-1,8)  # convert to numpy & reshape (8 is the number of features
        final_val = model.predict(dt).tolist()
        final = {"output": [final_val]}
        try:
            return final
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))


@app.get("/health")
async def health():
    return {"Current Date/Time": datetime.now().isoformat()}

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)