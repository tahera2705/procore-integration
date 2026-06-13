CREATE TABLE projects (
    id INTEGER PRIMARY KEY,
    name VARCHAR(255)
);

CREATE TABLE submittals (
    id INTEGER PRIMARY KEY,
    title VARCHAR(255),
    status VARCHAR(255),
    project_id INTEGER,
    responsible_contractor VARCHAR(255),
    received_date VARCHAR(50),
    returned_date VARCHAR(50),
    onsite_date VARCHAR(50),
    revision_count INTEGER
);