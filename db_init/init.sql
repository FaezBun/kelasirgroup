CREATE DATABASE IF NOT EXISTS socket_db;
USE socket_db;

CREATE TABLE IF NOT EXISTS user_points (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user VARCHAR(50) NOT NULL UNIQUE,
    points INT DEFAULT 0
);

INSERT IGNORE INTO user_points (user, points) VALUES 
('c1_user', 0), ('c2_user', 0), ('c3_user', 0),
('py1_user', 0), ('py2_user', 0), ('py3_user', 0),
('c4_user', 0), ('c5_user', 0), ('c6_user', 0),
('py4_user', 0), ('py5_user', 0), ('py6_user', 0),
('c7_user', 0), ('c8_user', 0), ('c9_user', 0),
('py7_user', 0), ('py8_user', 0), ('py9_user', 0);
