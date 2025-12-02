CREATE DATABASE LibraryDB;
USE LibraryDB;

CREATE TABLE Publishers (
PublishName VARCHAR(100) PRIMARY KEY,
ContactInfo VARCHAR(255)
);

CREATE TABLE Books (
ISBN CHAR(13) PRIMARY KEY,
Title VARCHAR(255) NOT NULL,
Categories VARCHAR(100),
PublishYear YEAR,
PublishName VARCHAR(100),
CONSTRAINT fk_books_publishers FOREIGN KEY (PublishName)
REFERENCES Publishers(PublishName)
ON UPDATE CASCADE
ON DELETE SET NULL
);

CREATE TABLE Authors (
AuthorName VARCHAR(100) PRIMARY KEY,
DOB DATE,
Nationality VARCHAR(100)
);

CREATE TABLE BookAuthors (
ISBN CHAR(13),
AuthorName VARCHAR(100),
PRIMARY KEY (ISBN, AuthorName),
CONSTRAINT fk_bookauthors_books FOREIGN KEY (ISBN)
REFERENCES Books(ISBN)
ON UPDATE CASCADE
ON DELETE CASCADE,
CONSTRAINT fk_bookauthors_authors FOREIGN KEY (AuthorName)
REFERENCES Authors(AuthorName)
ON UPDATE CASCADE
ON DELETE CASCADE
);

CREATE TABLE Copies (
CopyID INT PRIMARY KEY,
ISBN CHAR(13),
ShelfLocation VARCHAR(50),
ConditionDesc VARCHAR(50),
CONSTRAINT fk_copies_books FOREIGN KEY (ISBN)
REFERENCES Books(ISBN)
ON UPDATE CASCADE
ON DELETE CASCADE
);




CREATE TABLE Members (
    MemberID INT PRIMARY KEY,
    MemName VARCHAR(20),
    Email VARCHAR(30),
    Phone VARCHAR(15),
    Address VARCHAR(30)
);


CREATE TABLE Staff (
    StaffID INT PRIMARY KEY,
    StaffName VARCHAR(20),
    Position VARCHAR(20),
    WorkTime INT
);

CREATE TABLE Reservations (
    ReservationID INT PRIMARY KEY,
    DateFor DATE,
    MemberID INT,
    BookReserved CHAR(13),
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID),
    FOREIGN KEY (BookReserved) REFERENCES Books(ISBN)
);

CREATE TABLE Loans (
    LoanID INT PRIMARY KEY,
    ReturnDate DATE,
    ISBN CHAR(13),
    MemberID INT,
    StaffID INT,
    CopyID INT,
    FOREIGN KEY (ISBN) REFERENCES Books(ISBN),
    FOREIGN KEY (MemberID) REFERENCES Members(MemberID),
    FOREIGN KEY (StaffID) REFERENCES Staff(StaffID),
    FOREIGN KEY (CopyID) REFERENCES Copies(CopyID)
);

CREATE TABLE Fines (
    FineID INT PRIMARY KEY,
    AmountFined INT,
    DaysOverdue INT,
    LoanID INT UNIQUE,
    FOREIGN KEY (LoanID) REFERENCES Loans(LoanID)
);


INSERT INTO Publishers (PublishName, ContactInfo) VALUES 
('Penguin Random House', 'info@penguinrandomhouse.com'),
('HarperCollins', 'support@harpercollins.com'),
('Simon & Schuster', 'contact@simonandschuster.com'),
('Macmillan Publishers', 'help@macmillan.com'),
('Hachette Book Group', 'hello@hachette.com');


INSERT INTO Books (ISBN, Title, Categories, PublishYear, PublishName) VALUES
('9780143127741', 'The Martian', 'Science Fiction', 2014, 'Penguin Random House'),
('9780062315007', 'The Alchemist', 'Fiction', 1993, 'HarperCollins'),
('9781501128035', 'It Ends With Us', 'Romance', 2016, 'Simon & Schuster'),
('9781250278187', 'Project Hail Mary', 'Science Fiction', 2021, 'Macmillan Publishers'),
('9780316420259', 'The Silent Patient', 'Thriller', 2019, 'Hachette Book Group');

INSERT INTO Authors (AuthorName, DOB, Nationality) VALUES
('Andy Weir', '1972-06-16', 'American'),
('Paulo Coelho', '1947-08-24', 'Brazilian'),
('Colleen Hoover', '1979-12-11', 'American'),
('Alex Michaelides', '1977-09-04', 'Cypriot'),
('John Doe', '1980-05-14', 'British');

INSERT INTO BookAuthors (ISBN, AuthorName) VALUES
('9780143127741', 'Andy Weir'),
('9780062315007', 'Paulo Coelho'),
('9781501128035', 'Colleen Hoover'),
('9781250278187', 'Andy Weir'),
('9780316420259', 'Alex Michaelides');

INSERT INTO Copies (CopyID, ISBN, ShelfLocation, ConditionDesc) VALUES
(1, '9780143127741', 'A1-01', 'Excellent'),
(2, '9780143127741', 'A1-02', 'Poor'),
(3, '9780062315007', 'B2-01', 'Excellent'),
(4, '9781501128035', 'C3-05', 'Fair'),
(5, '9781250278187', 'D4-02', 'Excellent'),
(6, '9780316420259', 'E5-01', 'Good');

INSERT INTO Members (MemberID, MemName, Email, Phone, Address) VALUES
(1, 'Alice Johnson', 'alice@example.com', '5551234567', '123 Oak St'),
(2, 'Bob Smith', 'bob@example.com', '5559876543', '456 Pine Ave'),
(3, 'Carol Lee', 'carol@example.com', '5552468101', '789 Maple Dr');

INSERT INTO Staff (StaffID, StaffName, Position, WorkTime) VALUES
(1, 'David Green', 'Librarian', 40),
(2, 'Emma Brown', 'Assistant', 35),
(3, 'Frank White', 'Clerk', 30);

INSERT INTO Reservations (ReservationID, DateFor, MemberID, BookReserved) VALUES
(1, '2025-10-22', 1, '9780143127741'),
(2, '2025-10-23', 2, '9781501128035');

INSERT INTO Loans (LoanID, ReturnDate, ISBN, MemberID, StaffID, CopyID) VALUES
(1, '2025-10-10', '9780316420259', 1, 1, 6),
(2, '2025-10-20', '9781250278187', 3, 3, 5);

INSERT INTO Fines (FineID, AmountFined, DaysOverdue, LoanID) VALUES
(1, 10, 27, 1),
(2, 25, 60, 2);




# create view to see all the information of each book
CREATE VIEW BookDetails AS
SELECT b.Title, a.AuthorName, b.Categories, b.PublishYear, p.PublishName
FROM Books b
JOIN BookAuthors ba ON b.ISBN = ba.ISBN
JOIN Authors a ON ba.AuthorName = a.AuthorName
JOIN Publishers p ON b.PublishName = p.PublishName;
# Use the view:
SELECT * FROM BookDetails;


# Delete a book copy that was damaged beyond repair
SELECT * FROM Copies;
DELETE FROM Copies
WHERE CopyID = 2;


SELECT * FROM AUTHORS WHERE AuthorName = 'Alex Michaelides';
UPDATE Authors SET Nationality = 'Cypriot-British' WHERE AuthorName = 'Alex Michaelides';


# A statement that can represent filtering/sortingg
SELECT Title, Categories, PublishYear
FROM Books
WHERE Categories = 'Science Fiction'
ORDER BY PublishYear DESC;

# Nested Subquery to find which authors have books published by MacMillan Publishers.
SELECT AuthorName
FROM Authors
WHERE AuthorName IN ( 
	SELECT AuthorName
	FROM BookAuthors
		WHERE ISBN IN (
		SELECT ISBN
		FROM Books
		WHERE PublishName = 'Macmillan Publishers'
	)
);

# Outer Join example, show all books + authors even if a book doesn’t have an author
SELECT b.Title, a.AuthorName
FROM Books b
LEFT JOIN BookAuthors ba ON b.ISBN = ba.ISBN
LEFT JOIN Authors a ON ba.AuthorName = a.AuthorName;

#  INNER JOIN, List of all fines with member names and book titles
SELECT 
    Fines.FineID,
    Members.MemName,
    Books.Title AS BookTitle,
    Fines.AmountFined,
    Fines.DaysOverdue
FROM Fines
JOIN Loans ON Fines.LoanID = Loans.LoanID
JOIN Members ON Loans.MemberID = Members.MemberID
JOIN Books ON Loans.ISBN = Books.ISBN;

# LEFT JOIN, Show all members and any books they have on loan (or none)
SELECT 
    Members.MemberID,
    Loans.LoanID,
    Books.Title AS Borrowed_Book,
    Loans.ReturnDate
FROM Members
LEFT JOIN Loans ON Members.MemberID = Loans.MemberID
LEFT JOIN Books ON Loans.ISBN = Books.ISBN;

# index for faster search by Title
CREATE INDEX idx_title ON Books (Title);

# Alter and Constraint example, adding a constraint to books to make sure the publishing year makes sense.
ALTER TABLE Books
ADD CONSTRAINT chk_publish_year CHECK (PublishYear >= 1500 AND PublishYear <= 2025);
UPDATE Books SET PublishYear = 2013 WHERE ISBN = '9780143127741';


#### ALTER TABLE Books DROP CONSTRAINT chk_publish_year;