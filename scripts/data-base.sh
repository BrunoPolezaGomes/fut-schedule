CREATE USER 'garra'@'localhost' IDENTIFIED BY 'garra';
GRANT ALL PRIVILEGES ON * . * TO 'garra'@'localhost';

## MYSQL COMMANDS

sudo mysql -u garra -p

CREATE DATABASE garra_vermelha;

USE garra_vermelha;

CREATE TABLE users (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    confirmed BOOLEAN NOT NULL DEFAULT 0,
    confirmed_on DATETIME,
    photo VARCHAR(255),
    shirt_number INT(11),
    shoe_number INT(11),
    preferred_foot VARCHAR(20),
    preferred_position VARCHAR(20),
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    is_admin BOOLEAN NOT NULL DEFAULT 0
);

CREATE TABLE events (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    confirmed BOOLEAN NOT NULL DEFAULT 0,
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

CREATE TABLE user_event (
    user_id INT(11) NOT NULL,
    event_id INT(11) NOT NULL,
    confirmed BOOLEAN NOT NULL DEFAULT 0,
    PRIMARY KEY (user_id, event_id),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
);

CREATE TABLE payments (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id INT(11) NOT NULL,
    value DECIMAL(10, 2) NOT NULL,
    payment_date DATETIME NOT NULL,
    payment_proof VARCHAR(255) NOT NULL,
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

CREATE TABLE goals (
    id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id INT(11) NOT NULL,
    event_id INT(11) NOT NULL,
    goals_scored INT(11) NOT NULL DEFAULT 0,
    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (event_id) REFERENCES events(id) ON DELETE CASCADE
);

INSERT INTO usuarios (nome, email, senha, is_admin) 
VALUES ('admin', 'admin@garravermelha.com.br', 'test', 1);

INSERT INTO usuarios (nome, email, senha) 
VALUES ('user1', 'usuario1@garravermelha.com.br', 'test');

INSERT INTO usuarios (nome, email, senha) 
VALUES ('user2', 'usuario2@garravermelha.com.br', 'test');


CREATE DATABASE garra;
USE garra;

CREATE TABLE usuarios (
    id INT(11) NOT NULL AUTO_INCREMENT,
    nome VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL,
    senha VARCHAR(100) NOT NULL,
    PRIMARY KEY (id)
);
