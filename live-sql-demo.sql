-- Dimension: Student
CREATE TABLE Student (
    Student_ID NUMBER PRIMARY KEY,
    Student_Major VARCHAR2(50)
);

-- Dimension: Professor
CREATE TABLE Professor (
    Professor_ID NUMBER PRIMARY KEY,
    Professor_Name VARCHAR2(100),
    Title VARCHAR2(50),
    Department_ID NUMBER,
    Department_Name VARCHAR2(100)
);

-- Dimension: Course_Section
CREATE TABLE Course_Section (
    Course_ID NUMBER,
    Section_ID NUMBER,
    Course_Name VARCHAR2(100),
    Units NUMBER,
    Room_ID VARCHAR2(10),
    Room_Capacity NUMBER,
    PRIMARY KEY (Course_ID, Section_ID)
);

-- Dimension: Period
CREATE TABLE Period (
    Semester_ID VARCHAR2(10),
    Year NUMBER,
    PRIMARY KEY (Semester_ID, Year)
);

-- Fact Table: Grades
CREATE TABLE Grades (
    Student_ID NUMBER,
    Course_ID NUMBER,
    Section_ID NUMBER,
    Professor_ID NUMBER,
    Semester_ID VARCHAR2(10),
    Year NUMBER,
    Grade NUMBER(3,1),
    FOREIGN KEY (Student_ID) REFERENCES Student(Student_ID),
    FOREIGN KEY (Professor_ID) REFERENCES Professor(Professor_ID),
    FOREIGN KEY (Course_ID, Section_ID) REFERENCES Course_Section(Course_ID, Section_ID),
    FOREIGN KEY (Semester_ID, Year) REFERENCES Period(Semester_ID, Year)
);

-- Students
INSERT INTO Student VALUES (1, 'Computer');
INSERT INTO Student VALUES (2, 'IT');
INSERT INTO Student VALUES (3, 'Computer');

-- Professors
INSERT INTO Professor VALUES (101, 'Dr. Sharma', 'Professor', 10, 'Computer Science');
INSERT INTO Professor VALUES (102, 'Dr. Iyer', 'Associate Professor', 11, 'Information Technology');

-- Course Sections
INSERT INTO Course_Section VALUES (201, 1, 'Data Structures', 4, 'A101', 60);
INSERT INTO Course_Section VALUES (202, 1, 'Networking', 3, 'B202', 45);

-- Periods
INSERT INTO Period VALUES ('Fall', 2023);
INSERT INTO Period VALUES ('Spring', 2024);

-- Grades
INSERT INTO Grades VALUES (1, 201, 1, 101, 'Fall', 2023, 8.5);
INSERT INTO Grades VALUES (2, 201, 1, 101, 'Fall', 2023, 7.0);
INSERT INTO Grades VALUES (3, 202, 1, 102, 'Fall', 2023, 6.5);
INSERT INTO Grades VALUES (1, 202, 1, 102, 'Spring', 2024, 9.0);

COMMIT;

--rollup
SELECT 
    Year, 
    AVG(Grade) AS Avg_Grade
FROM Grades
GROUP BY Year
ORDER BY Year;

--drilldown
SELECT 
    G.Year, 
    G.Semester_ID, 
    CS.Course_Name, 
    AVG(G.Grade) AS Avg_Grade
FROM Grades G
JOIN Course_Section CS ON G.Course_ID = CS.Course_ID AND G.Section_ID = CS.Section_ID
GROUP BY G.Year, G.Semester_ID, CS.Course_Name
ORDER BY G.Year, G.Semester_ID, CS.Course_Name;

--slice
SELECT 
    S.Student_ID, 
    S.Student_Major, 
    CS.Course_Name, 
    G.Grade
FROM Grades G
JOIN Student S ON G.Student_ID = S.Student_ID
JOIN Course_Section CS ON G.Course_ID = CS.Course_ID AND G.Section_ID = CS.Section_ID
WHERE G.Year = 2023 AND G.Semester_ID = 'Fall';

--dice
SELECT 
    P.Department_Name, 
    CS.Course_Name, 
    G.Grade
FROM Grades G
JOIN Professor P ON G.Professor_ID = P.Professor_ID
JOIN Course_Section CS ON G.Course_ID = CS.Course_ID AND G.Section_ID = CS.Section_ID
WHERE P.Department_Name = 'Computer Science'
  AND G.Year = 2023
  AND G.Semester_ID = 'Fall'
  AND CS.Room_Capacity > 50;

  --pivote
  SELECT 
    CS.Course_Name,
    AVG(CASE WHEN S.Student_Major = 'Computer' THEN G.Grade END) AS Avg_Computer,
    AVG(CASE WHEN S.Student_Major = 'IT' THEN G.Grade END) AS Avg_IT
FROM Grades G
JOIN Student S ON G.Student_ID = S.Student_ID
JOIN Course_Section CS ON G.Course_ID = CS.Course_ID AND G.Section_ID = CS.Section_ID
GROUP BY CS.Course_Name
ORDER BY CS.Course_Name;