import uvicorn
from fastapi import FastAPI, HTTPException
import asyncio
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache
import joblib
from pydantic import BaseModel, validator, ValidationError, Extra
import numpy as np
from datetime import datetime

class DataInputCheck(BaseModel):
    class Config:
        extra = Extra.forbid

    MedInc: list
    HouseAge: list
    AveRooms: list
    AveBedrms: list
    Population: list
    AveOccup: list
    Latitude: list
    Longitude: list


    @validator('MedInc', 'Population','HouseAge', 'AveRooms', 'AveBedrms', 'Population', 'AveOccup')
    def valid_med(cls, v):

        assert isinstance(v[0], float), "Data must be a float"
        if v[0] < 0:
          raise ValueError('Must be positive')
        return v


    class DataOutputCheck(BaseModel):
        output: list

        @validator('output')
        def valid_pred(cls, v):
            #assert len(v)==len(MedInc), "Number of output predictions must be equal to the number of inputs"
            assert isinstance(v[0], float), "Prediction must be a float"
            if v[0] < 0:
                raise ValueError('Must be positive')
            return v



model = joblib.load("model_pipeline.pkl")
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


@app.post("/predict", response_model=DataInputCheck.DataOutputCheck)
@cache(expire=30)
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
        data_loaded = np.array(data_loaded)
        dt = data_loaded.reshape(data_loaded.shape[2], 8)  # convert to numpy & reshape (8 is the number of features)
        final_val =  model.predict(dt).tolist()
        try:
            final = {"output": final_val}
            await asyncio.sleep(5)
            return final
        except ValidationError as e:
            raise HTTPException(status_code=400, detail=str(e))
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))



@app.on_event('startup')
async def startup():
    redis = aioredis.from_url('redis://redis', encoding = 'utf8', decode_responses = True)
    FastAPICache.init(RedisBackend(redis), prefix = 'fastapi-cache')


@app.get("/health")
async def health():
    return {"Current Date/Time": datetime.now().isoformat()}

if __name__=="__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


'''
{
  "MedInc": [10.0, 10.0],
  "HouseAge": [10.0, 10.0],
  "AveRooms": [10.0, 10.0],
  "AveBedrms": [10.0, 10.0],
  "Population": [10.0, 10.0],
  "AveOccup": [10.0, 10.0],
  "Latitude": [10.0, 10.0],
  "Longitude": [10.0, 10.0]
}
'''

'''
curl -X 'POST' \
  'http://localhost:8000/predict' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "MedInc": [10.0, 10.0],
  "HouseAge": [10.0, 10.0],
  "AveRooms": [10.0, 10.0],
  "AveBedrms": [10.0, 10.0],
  "Population": [10.0, 10.0],
  "AveOccup": [10.0, 10.0],
  "Latitude": [10.0, 10.0],
  "Longitude": [10.0, 10.0]
}'
'''
