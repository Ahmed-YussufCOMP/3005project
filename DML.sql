INSERT INTO users (username, password, memberstatus)
VALUES
    ('joe', 'hello', 1),
    ('martha', 'bye', 2),
    ('james', 'hey', 3);

  INSERT INTO trainer (Trainername, specialization, availability, membername, room_number, time)
VALUES ('billy', 'Running', FALSE, 'james', 101, '9');  


INSERT INTO ExerciseStats (ExerciseRoutine, FitnessAchievements, HealthStatistics) VALUES
('Running', 'Improved Endurance', 'Calories Burned: 300'),
('Weightlifting', 'Increased Strength', 'Calories Burned: 200'),
('Yoga', 'Enhanced Flexibility', 'Calories Burned: 150'),
('Swimming', 'Improved Cardiovascular Health', 'Calories Burned: 400'),
('Cycling', 'Stronger Legs', 'Calories Burned: 250');

INSERT INTO Fitness_Done (username, Fitness_Done, Health_Metric)
VALUES ('james', 'Yoga', 'Calories Burned: 150');

INSERT INTO Fitness_Goals (username, Fitness_todo, Health_Metric)
VALUES ('james', 'Running', 'Calories Burned: 300');

INSERT INTO Room_status (room_number, availability) VALUES
(101, TRUE),
(102, TRUE),
(103, TRUE),
(104, TRUE);

INSERT INTO equipment_maintenance_monitoring (Equipment, Availability)
VALUES
    ('Treadmill', TRUE),
    ('Elliptical Machine', FALSE),
    ('Stationary Bike', TRUE),
    ('Rowing Machine', FALSE),
    ('Weight Bench', TRUE),
    ('Dumbbells', TRUE),
    ('Barbell', FALSE),
    ('Leg Press Machine', TRUE),
    ('Cable Machine', FALSE),
    ('Exercise Ball', TRUE);

INSERT INTO payment (membername, payment, exercise)
VALUES ('james', 5.00, 'Yoga');