from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, Integer, String, Float

class Base(DeclarativeBase):
    pass


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    status = Column(String)
    created_at = Column(String)


class Submittal(Base):
    __tablename__ = "submittals"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer)
    title = Column(String)
    status = Column(String)
    responsible_contractor = Column(String)
    received_date = Column(String)
    returned_date = Column(String)
    onsite_date = Column(String)
    due_date = Column(String)
    revision_count = Column(Integer)
