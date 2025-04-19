from pydantic import BaseModel, Field, RootModel, validator, field_validator
from typing import Optional, Literal, Dict, Any


class Params(BaseModel):
  required: bool
  min: Optional[float] = None
  max: Optional[float] = None
  decimals: Optional[int] = None
  format: Optional[str] = None

  @validator("decimals")
  def check_decimals_positive(cls, v):
    if v is not None and v < 0:
      raise ValueError("decimals must be non-negative")
    return v


class Plot(BaseModel):
  format: Optional[str] = None
  axis_title: Optional[str] = None
  color: Optional[str] = None
  link_limits: Optional[str] = None
  min: Optional[float] = None
  max: Optional[float] = None
  title: Optional[str] = None
  unit: Optional[str] = None
  axis_location: Optional[Literal["left", "right", "none"]] = Field(default="right")


class FieldConfig(BaseModel):
  type: Literal["float", "date"]
  params: Params
  plot: Optional[Plot] = None

class ConfigMap(RootModel[Dict[str, FieldConfig]]):
  @field_validator('root')
  @classmethod
  def must_have_timestamp_first(cls, value: Dict[str, FieldConfig]):
    keys = list(value.keys())
    if not keys or keys[0] != 'timestamp':
      raise ValueError("'timestamp' must be present and be the first field in the config.")
    return value