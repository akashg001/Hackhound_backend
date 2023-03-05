DROP TABLE Userbase();
DROP TABLE Restaurant();
DROP TABLE Menu();
DROP TABLE Orders();
DROP TABLE Nutrition();

CREATE TABLE Userbase (
    id int PRIMARY KEY,
    name varchar,
    phone int
    );

CREATE TABLE Restaurant(
    id int PRIMARY KEY,
    name varchar,
    Address varchar,
    Phone = int
);

CREATE TABLE Menu(
    id int PRIMARY KEY,
    Rest FOREIGN KEY,
    name = varchar,
    Ingredients varchar,
    cost = int
);

CREATE TABLE Orders(
    id int PRIMARY KEY,
    users FOREIGN KEY,
    Total_cost int,
    Total_items int,
    status = varchar
);

CREATE TABLE Nutrition(
    id int PRIMARY KEY,
    food FOREIGN KEY,
    Protein int,
    Carbohydrates int,
    Fats int,
    Sugar int
);