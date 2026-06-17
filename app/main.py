from fastapi import FastAPI
from app.database import engine, SessionLocal
from app.models import Base, Project, Submittal
from datetime import datetime, date

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Procore Integration Running"}


@app.get("/projects")
def get_projects():
    db = SessionLocal()
    projects = db.query(Project).all()
    result = []
    for project in projects:
        result.append({
            "id": project.id,
            "name": project.name,
            "status": project.status,
            "created_at": project.created_at
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
    for s in submittals:
        result.append({
            "id": s.id,
            "title": s.title,
            "status": s.status,
            "project_id": s.project_id,
            "responsible_contractor": s.responsible_contractor,
            "received_date": s.received_date,
            "returned_date": s.returned_date,
            "onsite_date": s.onsite_date,
            "due_date": s.due_date,
            "revision_count": s.revision_count
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
    today = date.today()

    approved = 0
    open_count = 0
    rejected = 0
    revise_resubmit = 0
    revisions = 0
    overdue_not_approved = 0
    near_onsite_not_approved = 0
    total_days = 0
    days_count = 0
    contractor_groups = {}

    for s in submittals:
        status = (s.status or "").lower()

        if status == "approved":
            approved += 1
        elif status == "open":
            open_count += 1
        elif status == "rejected":
            rejected += 1
        elif status == "revise & resubmit":
            revise_resubmit += 1

        if s.revision_count and s.revision_count > 0:
            revisions += 1

        if status != "approved":
            if s.due_date:
                try:
                    due = datetime.strptime(s.due_date, "%Y-%m-%d").date()
                    if due < today:
                        overdue_not_approved += 1
                except ValueError:
                    pass

            if s.onsite_date:
                try:
                    onsite = datetime.strptime(s.onsite_date, "%Y-%m-%d").date()
                    days_until_onsite = (onsite - today).days
                    if 0 <= days_until_onsite <= 14:
                        near_onsite_not_approved += 1
                except ValueError:
                    pass

        if s.received_date and s.returned_date:
            try:
                received = datetime.strptime(s.received_date, "%Y-%m-%d").date()
                returned = datetime.strptime(s.returned_date, "%Y-%m-%d").date()
                total_days += (returned - received).days
                days_count += 1
            except ValueError:
                pass

        if status == "open" and s.responsible_contractor:
            contractor = s.responsible_contractor
            contractor_groups[contractor] = contractor_groups.get(contractor, 0) + 1

    avg_days = round(total_days / days_count, 1) if days_count > 0 else 0
    revision_percentage = round((revisions / total) * 100, 1) if total > 0 else 0

    db.close()

    return {
        "total_submittals": total,
        "approved": approved,
        "open": open_count,
        "rejected": rejected,
        "revise_and_resubmit": revise_resubmit,
        "overdue_not_approved": overdue_not_approved,
        "average_days_received_to_returned": avg_days,
        "open_by_contractor": contractor_groups,
        "not_approved_onsite_within_14_days": near_onsite_not_approved,
        "revision_percentage": revision_percentage
    }


@app.post("/webhooks/project-created")
def project_created(payload: dict):
    db = SessionLocal()
    existing = db.query(Project).filter(Project.id == payload["id"]).first()
    if not existing:
        project = Project(
            id=payload["id"],
            name=payload["name"],
            status=payload.get("status"),
            created_at=payload.get("created_at")
        )
        db.add(project)
        db.commit()
    db.close()
    return {"message": "Project saved"}


@app.post("/webhooks/submittal-created")
def submittal_created(payload: dict):
    db = SessionLocal()
    existing = db.query(Submittal).filter(Submittal.id == payload["id"]).first()
    if not existing:
        submittal = Submittal(
            id=payload["id"],
            title=payload["title"],
            status=payload["status"],
            project_id=payload["project_id"],
            responsible_contractor=payload.get("responsible_contractor"),
            received_date=payload.get("received_date"),
            returned_date=payload.get("returned_date"),
            onsite_date=payload.get("onsite_date"),
            due_date=payload.get("due_date"),
            revision_count=payload.get("revision_count", 0)
        )
        db.add(submittal)
        db.commit()
    db.close()
    return {"message": "Submittal saved"}
