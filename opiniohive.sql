-- phpMyAdmin SQL Dump
-- version 5.1.1deb5ubuntu1
-- https://www.phpmyadmin.net/
--
-- Host: localhost:3306
-- Generation Time: Jan 18, 2024 at 04:25 AM
-- Server version: 8.0.35-0ubuntu0.22.04.1
-- PHP Version: 8.1.2-1ubuntu2.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `opiniohive`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  `password` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `email`, `phone_number`, `password`, `name`) VALUES
(1, 'admin1@example.com', '1234567890', 'hashed_password_1', 'Admin 1');

-- --------------------------------------------------------

--
-- Table structure for table `chat`
--

CREATE TABLE `chat` (
  `id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `admin_id` int DEFAULT NULL,
  `message` text,
  `timestamp` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `sender_type` varchar(10) NOT NULL DEFAULT 'user'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `chat`
--

INSERT INTO `chat` (`id`, `user_id`, `admin_id`, `message`, `timestamp`, `sender_type`) VALUES
(8, 10, 1, 'Hello User!', '2024-01-17 12:06:48', 'admin'),
(9, 10, 1, 'Hi Admin!', '2024-01-17 12:06:48', 'user'),
(10, 10, 1, 'How can I help you?', '2024-01-17 12:06:48', 'admin'),
(11, 10, 1, 'I have a question about my account.', '2024-01-17 12:06:48', 'user'),
(12, 10, 1, 'Sure, what would you like to know?', '2024-01-17 12:06:48', 'admin'),
(13, 10, 1, 'How can I reset my password?', '2024-01-17 12:06:48', 'user'),
(14, 10, 1, 'You can reset your password through the \"Forgot Password\" option on the login page.', '2024-01-17 12:06:48', 'admin'),
(15, 10, 1, 'Can you provide more details about the password reset process?', '2024-01-17 12:58:33', 'user'),
(16, 10, 1, 'Certainly! To reset your password, click on the \"Forgot Password\" link on the login page. You will receive an email with further instructions.', '2024-01-17 12:58:33', 'admin'),
(17, 10, 1, 'Thank you! I will try that now.', '2024-01-17 12:58:33', 'user'),
(18, 10, 1, 'You are welcome! Let me know if you encounter any issues.', '2024-01-17 12:58:33', 'admin'),
(19, 10, 1, 'Hello Admin, I need assistance with a recent purchase.', '2024-01-17 12:58:33', 'user'),
(20, 10, 1, 'Sure, I am here to help. Please provide more details about your purchase.', '2024-01-17 12:58:33', 'admin'),
(21, 10, 1, 'I ordered item X, but received item Y. How can I get a refund or exchange?', '2024-01-17 12:58:33', 'user'),
(22, 10, 1, 'I apologize for the inconvenience. We will process a refund for you. Please allow 3-5 business days for the transaction to reflect in your account.', '2024-01-17 12:58:33', 'admin'),
(23, 10, 1, 'test', '2024-01-17 13:31:31', 'user'),
(24, 10, 1, 'test', '2024-01-17 13:32:44', 'user'),
(25, 10, 1, 'How can I delete my account?', '2024-01-17 13:35:41', 'user'),
(26, 11, 1, 'Hey Admin', '2024-01-17 13:44:47', 'user'),
(27, 11, 1, 'Hey Admin', '2024-01-17 13:46:19', 'user'),
(28, 11, 1, 'Hey Admin', '2024-01-17 13:48:43', 'user'),
(29, 11, 1, 'hey', '2024-01-17 14:06:11', 'user'),
(30, 10, 1, 'hey', '2024-01-17 16:15:51', 'admin'),
(31, 9, 1, 'Hello', '2024-01-17 17:57:28', 'user'),
(32, 10, 1, 'Hello', '2024-01-17 21:05:27', 'admin'),
(33, 9, 1, 'Hello', '2024-01-18 00:49:36', 'admin'),
(34, 11, 1, 'Hey', '2024-01-18 00:55:12', 'user'),
(35, 11, 1, 'Hello', '2024-01-18 00:55:22', 'admin'),
(36, 10, 1, 'How can I delete my account?', '2024-01-18 01:01:28', 'admin'),
(37, 9, 1, 'How can I withdraw money', '2024-01-18 01:03:30', 'user');

-- --------------------------------------------------------

--
-- Table structure for table `payouts`
--

CREATE TABLE `payouts` (
  `id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `request_date` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `paid` varchar(3) DEFAULT 'NO'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `payouts`
--

INSERT INTO `payouts` (`id`, `user_id`, `request_date`, `paid`) VALUES
(3, 9, '2024-01-12 08:46:40', 'YES'),
(4, 10, '2024-01-12 09:06:32', 'YES');

-- --------------------------------------------------------

--
-- Table structure for table `surveys`
--

CREATE TABLE `surveys` (
  `id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `gender` varchar(20) DEFAULT NULL,
  `age` varchar(20) DEFAULT NULL,
  `shopping_frequency` varchar(20) DEFAULT NULL,
  `preferred_website` varchar(20) DEFAULT NULL,
  `satisfaction` int DEFAULT NULL,
  `influence_factors` varchar(255) DEFAULT NULL,
  `preferred_website_again` varchar(20) DEFAULT NULL,
  `improvements_features` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  `password` varchar(255) NOT NULL,
  `is_phone_verified` tinyint(1) DEFAULT '0',
  `is_email_verified` tinyint(1) DEFAULT '0',
  `request_verification` tinyint(1) DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `name`, `email`, `phone_number`, `password`, `is_phone_verified`, `is_email_verified`, `request_verification`) VALUES
(9, 'Kelvin Kahuho', 'kingkevo254@gmail.com', '254-741-5595', 'dea791eb830d33d25ae40c6fb04ee7d7209ea582ebebf2536d531ee0fc91514b', 1, 0, 0),
(10, 'Jeff  Kamau', 'jeffkamau@gmail.com', '074-155-9592', 'aa8ad65147669855501afaec14ab997b00f9ec95991d9380f3c9a44fae79655b', 1, 0, 1),
(11, 'John Mungai', 'johnmungai@gmail.com', '074-155-9592', 'dea791eb830d33d25ae40c6fb04ee7d7209ea582ebebf2536d531ee0fc91514b', 0, 0, 0);

-- --------------------------------------------------------

--
-- Table structure for table `wallet`
--

CREATE TABLE `wallet` (
  `wallet_id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `balance` decimal(10,2) DEFAULT '0.00'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- Dumping data for table `wallet`
--

INSERT INTO `wallet` (`wallet_id`, `user_id`, `balance`) VALUES
(6, 9, '0.00'),
(7, 10, '15.00'),
(8, 11, '0.00');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `phone_number` (`phone_number`);

--
-- Indexes for table `chat`
--
ALTER TABLE `chat`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `admin_id` (`admin_id`);

--
-- Indexes for table `payouts`
--
ALTER TABLE `payouts`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `surveys`
--
ALTER TABLE `surveys`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `wallet`
--
ALTER TABLE `wallet`
  ADD PRIMARY KEY (`wallet_id`),
  ADD KEY `user_id` (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `chat`
--
ALTER TABLE `chat`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

--
-- AUTO_INCREMENT for table `payouts`
--
ALTER TABLE `payouts`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `surveys`
--
ALTER TABLE `surveys`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `wallet`
--
ALTER TABLE `wallet`
  MODIFY `wallet_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `chat`
--
ALTER TABLE `chat`
  ADD CONSTRAINT `chat_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `chat_ibfk_2` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`);

--
-- Constraints for table `payouts`
--
ALTER TABLE `payouts`
  ADD CONSTRAINT `payouts_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `surveys`
--
ALTER TABLE `surveys`
  ADD CONSTRAINT `surveys_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `wallet`
--
ALTER TABLE `wallet`
  ADD CONSTRAINT `wallet_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
