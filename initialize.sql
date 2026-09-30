CREATE TABLE users(
    user_id INT PRIMARY KEY,
    name VARCHAR(100)
)

CREATE TABLE posts(
    post_id INT PRIMARY KEY,
    user_id INT,
    content VARCHAR(500),
    FOREIGN KEY (user_id) REFERENCES users(user_id)

)

INSERT INTO users VALUES (1,'Siri','sirinarne2025@gmail.com',19);
INSERT INTO users VALUES (2,'John','john@gmail.com',20);
INSERT INTO users VALUES (3,'Jane','jane@gmail.com',21);
INSERT INTO users VALUES (4,'Jim','jim@gmail.com',22);
INSERT INTO users VALUES (5,'Jill','jill@gmail.com',23);
INSERT INTO users VALUES (6,'Jack','jack@gmail.com',24);
INSERT INTO users VALUES (7,'Jill','jill@gmail.com',25);
INSERT INTO users VALUES (8,'Jill','jill@gmail.com',26);
INSERT INTO users VALUES (9,'Jill','jill@gmail.com',27);
INSERT INTO users VALUES (10,'Jill','jill@gmail.com',28);

INSERT INTO posts VALUES (1,'Hello, world!',1);
INSERT INTO posts VALUES (2,'Hello, world!',2);
INSERT INTO posts VALUES (3,'Hello, world!',3);
INSERT INTO posts VALUES (4,'Hello, world!',4);
INSERT INTO posts VALUES (5,'Hello, world!',5);
INSERT INTO posts VALUES (6,'Hello, world!',6);
INSERT INTO posts VALUES (7,'Hello, world!',7);
INSERT INTO posts VALUES (8,'Hello, world!',8);
INSERT INTO posts VALUES (9,'Hello, world!',9);
INSERT INTO posts VALUES (10,'Hello, world!',10);