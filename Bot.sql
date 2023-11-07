-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Nov 08, 2023 at 12:01 AM
-- Server version: 8.0.34-0ubuntu0.22.04.1
-- PHP Version: 8.1.2-1ubuntu2.14

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `Bot`
--

-- --------------------------------------------------------

--
-- Table structure for table `Main`
--

CREATE TABLE `Main` (
  `ChannelID` bigint NOT NULL,
  `UserID` bigint NOT NULL,
  `UserNickname` text CHARACTER SET utf16 COLLATE utf16_unicode_ci NOT NULL,
  `LastPingTime` text
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Settings`
--

CREATE TABLE `Settings` (
  `UserID` text NOT NULL,
  `State` tinyint(1) NOT NULL,
  `TimeWhenPing` text NOT NULL,
  `ReloadTime` smallint NOT NULL,
  `DNDM` tinyint NOT NULL,
  `DNDM_Time` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Table structure for table `Test`
--

CREATE TABLE `Test` (
  `ChannelID` text NOT NULL,
  `UserID` bigint NOT NULL,
  `UserNickname` text CHARACTER SET utf16 COLLATE utf16_unicode_ci NOT NULL,
  `State` tinyint(1) NOT NULL,
  `TimeWhenPing` text NOT NULL,
  `ReloadTime` int NOT NULL,
  `DNDM` tinyint(1) NOT NULL,
  `DNDM_Time` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
