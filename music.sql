-- phpMyAdmin SQL Dump
-- version 4.5.1
-- http://www.phpmyadmin.net
--
-- Host: 127.0.0.1
-- Generation Time: Apr 20, 2017 at 08:54 AM
-- Server version: 10.1.19-MariaDB
-- PHP Version: 5.6.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `music`
--

DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_addsong` (IN `p_title` VARCHAR(45), IN `p_user_id` BIGINT)  BEGIN
    insert into tbl_song(
        song_title,
        song_user_id,
        song_date
    )
    values
    (
        p_title,
        p_user_id,
        NOW()
    );
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_createUser` (IN `p_name` VARCHAR(20), IN `p_username` VARCHAR(20), IN `p_password` VARCHAR(255))  BEGIN
    if ( select exists (select 1 from tbl_user where user_username = p_username) ) THEN
     
        select 'Username Exists !!';
     
    ELSE
     
        insert into tbl_user
        (
            user_name,
            user_username,
            user_password
        )
        values
        (
            p_name,
            p_username,
            p_password
        );
     
    END IF;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_GetSongByUser` (IN `p_user_id` BIGINT)  BEGIN
    select * from tbl_song where song_user_id = p_user_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `sp_validateLogin` (IN `p_username` VARCHAR(20))  BEGIN
    select * from tbl_user where user_username = p_username;
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `tbl_song`
--

CREATE TABLE `tbl_song` (
  `song_id` int(11) NOT NULL,
  `song_title` varchar(255) DEFAULT NULL,
  `song_user_id` int(11) DEFAULT NULL,
  `song_date` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tbl_song`
--

INSERT INTO `tbl_song` (`song_id`, `song_title`, `song_user_id`, `song_date`) VALUES
(5, '3_Doors_Down_-_Here_Without_You.mp3', 4, '2017-04-19 11:14:30'),
(6, 'Avicii_-_Wake_Me_Up.mp3', 4, '2017-04-19 13:00:38'),
(7, 'Avril_-_Innocence.mp3', 6, '2017-04-19 13:02:18'),
(8, 'Breanne_Duren_-_Daydreams_demo.mp3', 6, '2017-04-19 13:02:42'),
(9, 'Avril_Lavigne_-_Complicated.mp3', 7, '2017-04-19 13:19:41'),
(10, 'Maroon_5_-_One_More_Night.mp3', 4, '2017-04-19 23:35:00'),
(11, '01._Signal.mp3', 4, '2017-04-19 23:40:10');

-- --------------------------------------------------------

--
-- Table structure for table `tbl_user`
--

CREATE TABLE `tbl_user` (
  `user_id` bigint(20) NOT NULL,
  `user_name` varchar(45) DEFAULT NULL,
  `user_username` varchar(45) DEFAULT NULL,
  `user_password` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `tbl_user`
--

INSERT INTO `tbl_user` (`user_id`, `user_name`, `user_username`, `user_password`) VALUES
(4, 'test', 'test@test.com', 'pbkdf2:sha1:1000$SgxAgJMS$2d849bda95a7a2a3197feadd05f03e0f6163d990'),
(5, 'Aditya', 'aditya@gmail.com', 'pbkdf2:sha1:1000$HdqVCJXV$cd8b6f1e44e683d4c7417ee95d9f4d87717844e9'),
(6, 'Saurabh', 'saurabh@gmail.com', 'pbkdf2:sha1:1000$eJHZDAso$6e40a4dd79797489db020aae1e25f5807e1f6c51'),
(7, 'Snehil', 'snehil@gmail.com', 'pbkdf2:sha1:1000$bVqklCfE$68446538cdb8de75669f16707441003f5c75331b');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tbl_song`
--
ALTER TABLE `tbl_song`
  ADD PRIMARY KEY (`song_id`);

--
-- Indexes for table `tbl_user`
--
ALTER TABLE `tbl_user`
  ADD PRIMARY KEY (`user_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tbl_song`
--
ALTER TABLE `tbl_song`
  MODIFY `song_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;
--
-- AUTO_INCREMENT for table `tbl_user`
--
ALTER TABLE `tbl_user`
  MODIFY `user_id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
