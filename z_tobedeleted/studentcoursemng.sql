-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 19, 2025 at 03:06 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `studentcoursemng`
--

-- --------------------------------------------------------

--
-- Table structure for table `course`
--

CREATE TABLE `course` (
  `course_code` int(11) NOT NULL,
  `course_title` varchar(100) NOT NULL,
  `department_code` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `course`
--

INSERT INTO `course` (`course_code`, `course_title`, `department_code`) VALUES
(1, 'Statistics for Business', 1),
(4, 'History of Art', 1),
(13, 'Introduction to Biology', 1),
(15, 'Statistics for Business', 1),
(20, 'Statistics for Business', 1),
(3, 'Computer Science Fundamentals', 2),
(6, 'Creative Writing Workshop', 2),
(8, 'Computer Science Fundamentals', 2),
(9, 'Introduction to Biology', 2),
(7, 'Creative Writing Workshop', 3),
(10, 'Creative Writing Workshop', 3),
(14, 'History of Art', 3),
(16, 'Creative Writing Workshop', 3),
(17, 'History of Art', 3),
(19, 'Creative Writing Workshop', 3),
(2, 'Statistics for Business', 4),
(5, 'Creative Writing Workshop', 4),
(11, 'Computer Science Fundamentals', 4),
(12, 'Statistics for Business', 4),
(18, 'Computer Science Fundamentals', 4);

-- --------------------------------------------------------

--
-- Table structure for table `department`
--

CREATE TABLE `department` (
  `department_code` int(11) NOT NULL,
  `department_name` varchar(70) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `department`
--

INSERT INTO `department` (`department_code`, `department_name`) VALUES
(1, 'Accounting'),
(2, 'Business Development'),
(3, 'Human Resources'),
(4, 'Legal2'),
(5, 'Marketing2'),
(9, 'Nine');

-- --------------------------------------------------------

--
-- Table structure for table `enrollment`
--

CREATE TABLE `enrollment` (
  `grade` float NOT NULL,
  `student_id` int(11) NOT NULL,
  `department_code` int(11) NOT NULL,
  `course_code` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `enrollment`
--

INSERT INTO `enrollment` (`grade`, `student_id`, `department_code`, `course_code`) VALUES
(36.4, 17, 1, 1);

-- --------------------------------------------------------

--
-- Table structure for table `student`
--

CREATE TABLE `student` (
  `student_id` int(11) NOT NULL,
  `first_name` varchar(40) NOT NULL,
  `last_name` varchar(40) NOT NULL,
  `gender` char(1) NOT NULL,
  `birthdate` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `student`
--

INSERT INTO `student` (`student_id`, `first_name`, `last_name`, `gender`, `birthdate`) VALUES
(1, 'Iorgo', 'Dunnett', 'M', '2025-04-10'),
(2, 'Mylo', 'Archibald', 'M', '2025-05-23'),
(3, 'Hanna', 'Nucciotti', 'F', '2025-10-10'),
(4, 'Dennie', 'Tomkiss', 'M', '2025-06-01'),
(5, 'Lori', 'McPeck', 'F', '2025-04-27'),
(6, 'Matthiew', 'Daens', 'M', '2025-09-03'),
(7, 'Saxon', 'O\'Hare', 'M', '2024-12-04'),
(8, 'Anna-diane', 'Dubble', 'F', '2025-07-31'),
(9, 'Julee', 'Cranna', 'F', '2025-09-28'),
(10, 'Devland', 'Basant', 'M', '2025-02-15'),
(11, 'Vivian', 'Postance', 'F', '2025-09-24'),
(12, 'Jasmin', 'Gregore', 'F', '2025-08-17'),
(13, 'Cassie', 'Sivior', 'M', '2025-09-26'),
(14, 'Hobart', 'Matczak', 'M', '2025-09-06'),
(15, 'Smitty', 'Jacquemy', 'M', '2025-06-27'),
(16, 'Tanya', 'Van de Castele', 'F', '2025-10-31'),
(17, 'Itch', 'Nicklin', 'M', '2024-11-15'),
(18, 'Ave', 'Teaze', 'M', '2025-01-24'),
(19, 'Nanon', 'Bremen', 'F', '2025-05-16'),
(20, 'Atlanta', 'Frances', 'F', '2025-10-02'),
(21, 'Chariot', 'Blackburn', 'M', '2025-02-22'),
(22, 'Orran', 'Owbridge', 'M', '2025-04-27'),
(23, 'Eran', 'Dorey', 'F', '2025-06-15'),
(24, 'Fritz', 'Instone', 'M', '2024-11-26'),
(25, 'Fredelia', 'Goodings', 'F', '2025-01-12'),
(26, 'Wilden', 'Groundwator', 'M', '2025-07-22');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `course`
--
ALTER TABLE `course`
  ADD PRIMARY KEY (`department_code`,`course_code`);

--
-- Indexes for table `department`
--
ALTER TABLE `department`
  ADD PRIMARY KEY (`department_code`),
  ADD UNIQUE KEY `department_code` (`department_code`),
  ADD UNIQUE KEY `department_name` (`department_name`);

--
-- Indexes for table `enrollment`
--
ALTER TABLE `enrollment`
  ADD KEY `student_id` (`student_id`),
  ADD KEY `department_code` (`department_code`,`course_code`);

--
-- Indexes for table `student`
--
ALTER TABLE `student`
  ADD PRIMARY KEY (`student_id`);

--
-- Constraints for dumped tables
--

--
-- Constraints for table `course`
--
ALTER TABLE `course`
  ADD CONSTRAINT `course_ibfk_1` FOREIGN KEY (`department_code`) REFERENCES `department` (`department_code`);

--
-- Constraints for table `enrollment`
--
ALTER TABLE `enrollment`
  ADD CONSTRAINT `enrollment_ibfk_1` FOREIGN KEY (`student_id`) REFERENCES `student` (`student_id`),
  ADD CONSTRAINT `enrollment_ibfk_2` FOREIGN KEY (`department_code`,`course_code`) REFERENCES `course` (`department_code`, `course_code`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
