from pydantic import BaseModel, validator
import numpy as np


class DataInputCheck(BaseModel):
    data: object
    target: object
    feature_names: list

    @validator('data')
    def valid_data(cls, v):
        assert isinstance(v, np.ndarray), "Data must be a NumpyArray"
        return v

    @validator('target')
    def valid_data(cls, v):
        assert isinstance(v, np.ndarray), "Data must be a NumpyArray"
        return v

    @validator('feature_names')
    def valid_feature_names(cls, v):
        assert isinstance(v, list), "Feature names must be in a list"
        fn = set(v)
        correct_names = set(
            ['MedInc', 'HouseAge', 'AveRooms', 'AveBedrms', 'Population', 'AveOccup', 'Latitude', 'Longitude'])
        if fn != correct_names:
            raise ValueError("Incorrect feature names")
        return v


class DataOutputCheck(BaseModel):
    output: float

    @validator('output')
    def valid_pred(cls, v):
        if v < 0:
            raise ValueError("The predicted value cannot be negative")
        return v
