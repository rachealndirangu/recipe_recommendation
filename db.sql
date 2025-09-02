CREATE DATABASE recipe_app;

USE recipe_app;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL
);

CREATE TABLE recipes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    ingredients TEXT,
    steps TEXT,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
