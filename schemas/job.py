from typing import Optional
from pydantic import BaseModel
from datetime import datetime, date


class JobBase(BaseModel):
    title: Optional[str] = None
    company: Optional[str] = None
    company_url: Optional[str] = None
    location: Optional[str] = "Remote"
    description: Optional[str] = None
    date_posted: Optional[str] = datetime.now().date()


class JobCreate(JobBase):
    title: str
    company: str
    location: str
    description: str


class ShowJob(JobBase):
    title: str
    company: str
    company_url: Optional[str] = None
    location: str
    description: str
    date_posted: date

    class Config:
        orm_mode = True
