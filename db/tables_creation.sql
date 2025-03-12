-- Create Staff Table (Doctors & Assistants)
CREATE TABLE Staff (
    StaffID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Role VARCHAR(20) CHECK (Role IN ('Doctor', 'Assistant')) NOT NULL,
    Specialization VARCHAR(255),
    ContactDetails VARCHAR(255)
);Q

-- Create Hospital Table
CREATE TABLE Hospital (
    HospitalID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Address TEXT NOT NULL,
    ContactNumber VARCHAR(20)
);

-- Create Study Table
CREATE TABLE Study (
    StudyID SERIAL PRIMARY KEY,
    Title VARCHAR(255) NOT NULL,
    Description TEXT,
    StartDate DATE NOT NULL,
    EndDate DATE NOT NULL,
    HospitalID INT NOT NULL,
    ManagerDoctorID INT NOT NULL,
    FOREIGN KEY (HospitalID) REFERENCES Hospital(HospitalID) ON DELETE CASCADE,
    FOREIGN KEY (ManagerDoctorID) REFERENCES Staff(StaffID) ON DELETE CASCADE
);

-- Create a trigger to ensure only Doctors can be Managers
CREATE OR REPLACE FUNCTION enforce_doctor_role()
RETURNS TRIGGER AS $$
BEGIN
    IF (SELECT Role FROM Staff WHERE StaffID = NEW.ManagerDoctorID) != 'Doctor' THEN
        RAISE EXCEPTION 'Only a Doctor can manage a study';
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER check_manager_role
BEFORE INSERT OR UPDATE ON Study
FOR EACH ROW EXECUTE FUNCTION enforce_doctor_role();

-- Create Researcher Table (To Differentiate Researchers from Other Staff)
CREATE TABLE Researcher (
    ResearcherID SERIAL PRIMARY KEY,
    StaffID INT NOT NULL UNIQUE,
    FOREIGN KEY (StaffID) REFERENCES Staff(StaffID) ON DELETE CASCADE
);

-- Create Study_Researcher Join Table (Many-to-Many)
CREATE TABLE Study_Researcher (
    StudyID INT NOT NULL,
    ResearcherID INT NOT NULL,
    PRIMARY KEY (StudyID, ResearcherID),
    FOREIGN KEY (StudyID) REFERENCES Study(StudyID) ON DELETE CASCADE,
    FOREIGN KEY (ResearcherID) REFERENCES Researcher(ResearcherID) ON DELETE CASCADE
);

-- Create Patient Table
CREATE TABLE Patient (
    PatientID SERIAL PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    DateOfBirth DATE NOT NULL,
    ContactDetails VARCHAR(255)
);

-- Create Study_Patient Join Table (Many-to-Many)
CREATE TABLE Study_Patient (
    StudyID INT NOT NULL,
    PatientID INT NOT NULL,
    PRIMARY KEY (StudyID, PatientID),
    FOREIGN KEY (StudyID) REFERENCES Study(StudyID) ON DELETE CASCADE,
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID) ON DELETE CASCADE
);

-- Create Allergy Table
CREATE TABLE Allergy (
    AllergyID SERIAL PRIMARY KEY,
    AllergyName VARCHAR(255) NOT NULL,
    Type VARCHAR(255) NOT NULL,
    CONSTRAINT unique_allergy UNIQUE (AllergyName, Type) -- Ensure (AllergyName, Type) is unique
);

-- Create PatientAllergies Join Table (Many-to-Many)
CREATE TABLE PatientAllergies (
    PatientID INT NOT NULL,
    AllergyID INT NOT NULL,
    PRIMARY KEY (PatientID, AllergyID),
    FOREIGN KEY (PatientID) REFERENCES Patient(PatientID) ON DELETE CASCADE,
    FOREIGN KEY (AllergyID) REFERENCES Allergy(AllergyID) ON DELETE CASCADE
);
