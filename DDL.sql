CREATE TABLE users (
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(50) NOT NULL,
    memberstatus INTEGER 
);

CREATE TABLE trainer (
    Trainername VARCHAR(100),    
    specialization VARCHAR(100),
    availability BOOLEAN DEFAULT TRUE,
    membername VARCHAR(100),
    room_number INTEGER,
    time VARCHAR(10)
);

CREATE TABLE ExerciseStats (
    ExerciseRoutine VARCHAR(100),
    FitnessAchievements VARCHAR(100),
    HealthStatistics VARCHAR(100)
);


CREATE TABLE Fitness_Done (        
    username VARCHAR(255),           
    Fitness_Done VARCHAR(255),
    Health_Metric   VARCHAR(255)           
);  

CREATE TABLE Fitness_Goals (      
    username VARCHAR(255),
    Fitness_todo VARCHAR(255),
    Health_Metric  VARCHAR(255)   
);      

CREATE TABLE Room_status (
    room_number INT PRIMARY KEY,
    availability BOOLEAN DEFAULT TRUE,
    admin_name VARCHAR(100)
);

CREATE TABLE equipment_maintenance_monitoring (
    Equipment VARCHAR(100),
    Availability BOOLEAN
);

CREATE TABLE payment (
    membername VARCHAR(50),
    payment DECIMAL(10, 2),
    exercise VARCHAR(100)
);   