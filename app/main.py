from fastapi import FastAPI
from app.database import engine, SessionLocal
from app.models import Base, Project, Submittal

Base.metadata.create_all(bind=engine)
db = SessionLocal()

if db.query(Project).count() == 0:
    project = Project(
        id=1,
        name="Airport Construction"
    )

    db.add(project)

    submittal = Submittal(
        id=1,
        title="Steel Approval",
        status="Open",
        project_id=1
    )

    db.add(submittal)

    db.commit()

db.close()
app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Procore Integration Running"
    }


@app.get("/projects")
def get_projects():

    db = SessionLocal()

    projects = db.query(Project).all()

    result = []

    for project in projects:
        result.append({
            "id": project.id,
            "name": project.name
        })

    db.close()

    return result


@app.get("/projects/{project_id}/submittals")
def get_project_submittals(project_id: int):

    db = SessionLocal()

    submittals = db.query(Submittal).filter(
        Submittal.project_id == project_id
    ).all()

    result = []

    for submittal in submittals:
        result.append({
            "id": submittal.id,
            "title": submittal.title,
            "status": submittal.status,
            "project_id": submittal.project_id
        })

    db.close()

    return result


@app.get("/analytics/submittals/{project_id}")
def analytics(project_id: int):

    db = SessionLocal()

    submittals = db.query(Submittal).filter(
        Submittal.project_id == project_id
    ).all()

    total = len(submittals)

    approved = 0
    open_count = 0
    rejected = 0
    revisions = 0

    for s in submittals:

        if s.status and s.status.lower() == "approved":
            approved += 1

        elif s.status and s.status.lower() == "open":
            open_count += 1

        elif s.status and s.status.lower() == "rejected":
            rejected += 1

        if s.revision_count and s.revision_count > 0:
            revisions += 1

    revision_percentage = 0

    if total > 0:
        revision_percentage = (revisions / total) * 100

    db.close()

    return {
        "total_submittals": total,
        "approved": approved,
        "open": open_count,
        "rejected": rejected,
        "revision_percentage": revision_percentage
    }
@app.post("/webhooks/project-created")
def project_created(payload: dict):

    db = SessionLocal()

    project = Project(
        id=payload["id"],
        name=payload["name"]
    )

    db.add(project)
    db.commit()

    db.close()

    return {"message": "Project saved"}
@app.post("/webhooks/submittal-created")
def submittal_created(payload: dict):

    db = SessionLocal()

    submittal = Submittal(
        id=payload["id"],
        title=payload["title"],
        status=payload["status"],
        project_id=payload["project_id"],
        responsible_contractor=payload["responsible_contractor"],
        received_date=payload["received_date"],
        returned_date=payload["returned_date"],
        onsite_date=payload["onsite_date"],
        revision_count=payload["revision_count"]
    )

    db.add(submittal)
    db.commit()

    db.close()

    return {"message": "Submittal saved"}