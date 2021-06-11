from os import stat
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from schemas.job import ShowJob, JobCreate
from db.session import get_db
from models.jobs import Job

router = APIRouter(tags=["Jobs"], prefix="/jobs")


@router.get("/all", response_model=List[ShowJob])
def get_all_jobs(db: Session = Depends(get_db)):
    jobs = db.query(Job).filter(Job.is_active == True).all()

    if jobs is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")
    return jobs


@router.get("/{id}", response_model=ShowJob)
def get_job_by_id(id: int, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == id).first()

    if job is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    return job


@router.post("/", response_model=ShowJob)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    new_job = Job(**job.dict(), owner_id=6)
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job


@router.put("/{id}")
def update_job_by_id(id: int, job: JobCreate, db: Session = Depends(get_db)):
    existing_job = db.query(Job).filter(Job.id == id, Job.owner_id == 6)

    if existing_job.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    existing_job.update(job.__dict__)
    db.commit()
    return {"ok": "Successfully updated it!"}


@router.delete("/${id}")
def delete_job_by_id(id: int, db: Session = Depends(get_db)):
    existing_job = db.query(Job).filter(Job.id == id, Job.owner_id == 6)

    if existing_job.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Job not found")

    existing_job.delete(synchronize_session=False)
    db.commit()
    return {"ok": "Successfully job is deleted"}
