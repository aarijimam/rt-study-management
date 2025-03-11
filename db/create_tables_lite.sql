-- Create Staff Table (Doctors & Assistants)
CREATE TABLE Staff (
    StaffID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Role TEXT NOT NULL CHECK (Role IN ('Doctor', 'Assistant')),
    Specialization TEXT,
    ContactDetails TEXT
);

-- Create Hospital Table
CREATE TABLE Hospital (
    HospitalID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Address TEXT NOT NULL,
    ContactNumber TEXT
);

-- Create Study Table
CREATE TABLE Study (
    StudyID INTEGER PRIMARY KEY AUTOINCREMENT,
    Title TEXT NOT NULL,
    Description TEXT,
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL,
    HospitalID INTEGER NOT NULL,
    ManagerDoctorID INTEGER NOT NULL,
    FOREIGN KEY (HospitalID) REFERENCES Hospital(HospitalID) ON DELETE CASCADE,
    FOREIGN KEY (ManagerDoctorID) REFERENCES Staff(StaffID) ON DELETE CASCADE
);

-- Create trigger to ensure only Doctors can be Managers
CREATE TRIGGER enforce_doctor_role 
BEFORE INSERT ON Study 
FOR EACH ROW 
WHEN (SELECT Role FROM Staff WHERE StaffID = NEW.ManagerDoctorID) <> 'Doctor'
BEGIN
    SELECT RAISE(FAIL, 'Only a Doctor can manage a study');
END;

-- Create Researcher Table
CREATE TABLE Researcher (
    ResearcherID INTEGER PRIMARY KEY AUTOINCREMENT,
    StaffID INTEGER NOT NULL UNIQUE,
    FOREIGN KEY (StaffID) REFERENCES Staff(StaffID) ON DELETE CASCADE
);

-- Create Study_Researcher Join Table (Many-to-Many)
CREATE TABLE Study_Researcher (
    StudyID INTEGER NOT NULL,
    ResearcherID INTEGER NOT NULL,
    PRIMARY KEY (StudyID, ResearcherID),
    FOREIGN KEY (StudyID) REFERENCES Study(StudyID) ON DELETE CASCADE,
    FOREIGN KEY (ResearcherID) REFERENCES Researcher(ResearcherID) ON DELETE CASCADE
);

-- Create Patient Table
CREATE TABLE Patient (
    PatientID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    DateOfBirth DATE NOT NULL,
    ContactDetails TEXT
);

-- Create Study_Patient Join Table (Many-to-Many)
CREATE TABLE Study_Patient (
    StudyID INTEGER NOT NULL,
    PatientID INTEGER NOT NULL,
    PRIMARY KEY (StudyID, PatientID),
    FOREIGN KEY (StudyID) REFERENCES Study(StudyID) ON DELETE CASCADE,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID) ON DELETE CASCADE
);

-- Create Allergy Table
CREATE TABLE Allergy (
    AllergyID INTEGER PRIMARY KEY AUTOINCREMENT,
    AllergyName TEXT NOT NULL,
    Type TEXT NOT NULL,
    UNIQUE (AllergyName, Type) -- Ensure (AllergyName, Type) is unique
);

-- Create PatientAllergies Join Table (Many-to-Many)
CREATE TABLE PatientAllergies (
    PatientID INTEGER NOT NULL,
    AllergyID INTEGER NOT NULL,
    PRIMARY KEY (PatientID, AllergyID),
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID) ON DELETE CASCADE,
    FOREIGN KEY (AllergyID) REFERENCES Allergy(AllergyID) ON DELETE CASCADE
);
