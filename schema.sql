-- ════════════════════════════════════════════════════════════
--  Rajasthan Internship Portal — MySQL Schema
--  Run: mysql -u root -p < schema.sql
-- ════════════════════════════════════════════════════════════

CREATE DATABASE IF NOT EXISTS rajasthan_portal;
USE rajasthan_portal;

-- ── Students ─────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS students (
    id          VARCHAR(10)  PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(120) UNIQUE,
    phone       VARCHAR(15),
    branch      VARCHAR(50)  NOT NULL,
    cgpa        DECIMAL(3,1) NOT NULL,
    skills      TEXT,
    status      ENUM('Searching','Placed','Completed') DEFAULT 'Searching',
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ── Employers ────────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS employers (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    name        VARCHAR(100) NOT NULL,
    email       VARCHAR(120) UNIQUE,
    city        VARCHAR(80),
    sector      VARCHAR(80),
    hired       INT DEFAULT 0,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ── Internships ──────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS internships (
    id          INT AUTO_INCREMENT PRIMARY KEY,
    company     VARCHAR(100) NOT NULL,
    role        VARCHAR(120) NOT NULL,
    stipend     INT          NOT NULL,
    duration    VARCHAR(30),
    skills      TEXT,
    status      ENUM('Open','Closing','Closed') DEFAULT 'Open',
    employer_id INT,
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (employer_id) REFERENCES employers(id) ON DELETE SET NULL
);

-- ── Applications ─────────────────────────────────────────────
CREATE TABLE IF NOT EXISTS applications (
    id            VARCHAR(10)  PRIMARY KEY,
    student_id    VARCHAR(10),
    internship_id INT,
    status        ENUM('Applied','Under Review','Shortlisted','Rejected','Completed') DEFAULT 'Applied',
    applied_date  DATE,
    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (student_id)    REFERENCES students(id)    ON DELETE CASCADE,
    FOREIGN KEY (internship_id) REFERENCES internships(id) ON DELETE CASCADE
);

-- ── Seed demo data ───────────────────────────────────────────
INSERT IGNORE INTO students VALUES
('STU001','Priya Sharma', 'priya@example.com', '9876500001','CSE',8.9,'Python, ML',         'Placed',   NOW()),
('STU002','Rahul Gupta',  'rahul@example.com', '9876500002','IT', 7.4,'Java, Spring',        'Searching',NOW()),
('STU003','Anjali Singh', 'anjali@example.com','9876500003','ECE',8.2,'VLSI, C++',           'Completed',NOW()),
('STU004','Vikram Rao',   'vikram@example.com','9876500004','CSE',6.8,'React, Node.js',      'Searching',NOW()),
('STU005','Meera Nair',   'meera@example.com', '9876500005','IT', 9.1,'Data Science, Python','Placed',   NOW());

INSERT IGNORE INTO employers(name,email,city,sector,hired) VALUES
('Tata Consultancy Services','hr@tcs.com',      'Mumbai',    'IT Services',12),
('Infosys Ltd',              'campus@infosys.com','Bengaluru','Technology',  8),
('Wipro Technologies',       'intern@wipro.com', 'Hyderabad', 'IT Services', 6),
('Accenture India',          'campus@accenture.com','Pune',   'Consulting',  9);

INSERT IGNORE INTO internships(company,role,stipend,duration,skills,status) VALUES
('TCS',      'ML Intern',          18000,'3 months','Python, ML',     'Open'),
('Infosys',  'Full Stack Dev Intern',20000,'6 months','React, Node.js','Open'),
('Wipro',    'Data Analyst Intern', 15000,'2 months','SQL, Tableau',   'Closing'),
('HCL',      'DevOps Intern',       16000,'3 months','Docker, CI/CD',  'Open'),
('Accenture','AI Research Intern',  22000,'6 months','PyTorch, NLP',   'Open');

INSERT IGNORE INTO applications VALUES
('A-101','STU001',1,'Completed',  '2026-03-20',NOW()),
('A-102','STU002',2,'Under Review','2026-03-22',NOW()),
('A-103','STU003',3,'Completed',  '2026-03-18',NOW()),
('A-104','STU004',4,'Rejected',   '2026-03-15',NOW()),
('A-105','STU005',5,'Shortlisted','2026-03-25',NOW());
