-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 06, 2024 at 07:27 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_pegawai`
--

DELIMITER $$
--
-- Procedures
--
CREATE DEFINER=`root`@`localhost` PROCEDURE `edit_admin` (IN `p_id` INT, IN `p_username` VARCHAR(50), IN `p_password_hash` VARCHAR(255))   BEGIN
    UPDATE admin
    SET
        username = p_username,
        password_hash = p_password_hash,
        updated_at = CURRENT_TIMESTAMP
    WHERE id = p_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `edit_jabatan` (IN `p_id` INT, IN `p_nama_jabatan` VARCHAR(100), IN `p_deskripsi` TEXT, IN `p_gaji` DECIMAL(10,2))   BEGIN
    UPDATE jabatan
    SET
        nama_jabatan = p_nama_jabatan,
        deskripsi = p_deskripsi,
        gaji = p_gaji
    WHERE id = p_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `edit_pegawai` (IN `p_id` INT, IN `p_nama` VARCHAR(100), IN `p_alamat` VARCHAR(255), IN `p_tanggal_lahir` DATE, IN `p_jenis_kelamin` ENUM('Laki-laki','Perempuan'), IN `p_telepon` VARCHAR(15), IN `p_email` VARCHAR(100), IN `p_admin_id` INT)   BEGIN
    UPDATE pegawai
    SET
        nama = p_nama,
        alamat = p_alamat,
        tanggal_lahir = p_tanggal_lahir,
        jenis_kelamin = p_jenis_kelamin,
        telepon = p_telepon,
        email = p_email,
        admin_id = p_admin_id,
        updated_at = CURRENT_TIMESTAMP
    WHERE id = p_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `edit_pegawai_jabatan` (IN `p_id` INT, IN `p_pegawai_id` INT, IN `p_jabatan_id` INT)   BEGIN
    UPDATE pegawai_jabatan
    SET
        id_pegawai = p_pegawai_id,
        id_jabatan = p_jabatan_id,
        created_at = CURRENT_TIMESTAMP
    WHERE id = p_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `hapus_admin` (IN `p_id` INT)   BEGIN
    DELETE FROM admin WHERE id = p_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `hapus_jabatan` (IN `p_id` INT)   BEGIN
    DELETE FROM jabatan WHERE id = p_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `hapus_pegawai` (IN `p_id` INT)   BEGIN
    DELETE FROM pegawai WHERE id = p_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `hapus_pegawai_jabatan` (IN `p_id` INT)   BEGIN
    DELETE FROM pegawai_jabatan WHERE id = p_id;
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `tambah_admin` (IN `p_username` VARCHAR(50), IN `p_password_hash` VARCHAR(255))   BEGIN
    INSERT INTO admin (username, password_hash)
    VALUES (p_username, p_password_hash);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `tambah_jabatan` (IN `p_nama_jabatan` VARCHAR(100), IN `p_deskripsi` TEXT, IN `p_gaji` DECIMAL(10,2))   BEGIN
    INSERT INTO jabatan (nama_jabatan, deskripsi, gaji)
    VALUES (p_nama_jabatan, p_deskripsi, p_gaji);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `tambah_pegawai` (IN `p_nama` VARCHAR(100), IN `p_alamat` VARCHAR(255), IN `p_tanggal_lahir` DATE, IN `p_jenis_kelamin` ENUM('Laki-laki','Perempuan'), IN `p_telepon` VARCHAR(15), IN `p_email` VARCHAR(100), IN `p_admin_id` INT)   BEGIN
    INSERT INTO pegawai (nama, alamat, tanggal_lahir, jenis_kelamin, telepon, email, admin_id)
    VALUES (p_nama, p_alamat, p_tanggal_lahir, p_jenis_kelamin, p_telepon, p_email, p_admin_id);
END$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `tambah_pegawai_jabatan` (IN `p_pegawai_id` INT, IN `p_jabatan_id` INT)   BEGIN
    INSERT INTO pegawai_jabatan (id_pegawai, id_jabatan)
    VALUES (p_pegawai_id, p_jabatan_id);
END$$

DELIMITER ;

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `username`, `password_hash`, `created_at`, `updated_at`) VALUES
(1, 'admin@gmail.com', 'admin1234', '2024-02-06 08:12:49', '2024-02-06 09:57:22'),
(2, 'admin2', 'admin2', '2024-02-06 08:12:49', '2024-02-06 08:12:49');

-- --------------------------------------------------------

--
-- Table structure for table `jabatan`
--

CREATE TABLE `jabatan` (
  `id` int(11) NOT NULL,
  `nama_jabatan` varchar(100) NOT NULL,
  `deskripsi` text DEFAULT NULL,
  `gaji` decimal(10,2) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `jabatan`
--

INSERT INTO `jabatan` (`id`, `nama_jabatan`, `deskripsi`, `gaji`, `created_at`, `updated_at`) VALUES
(1, 'Manajer', 'Manajer Proyek', 8000.00, '2024-02-06 08:11:59', '2024-02-06 08:11:59'),
(2, 'Programmer', 'Programmer Senior', 6000.00, '2024-02-06 08:11:59', '2024-02-06 08:11:59'),
(5, 'Programmer', 'Programmer Junior', 4500.00, '2024-02-06 14:17:36', '2024-02-06 14:17:36');

-- --------------------------------------------------------

--
-- Table structure for table `pegawai`
--

CREATE TABLE `pegawai` (
  `id` int(11) NOT NULL,
  `nama` varchar(100) NOT NULL,
  `alamat` varchar(255) DEFAULT NULL,
  `tanggal_lahir` date DEFAULT NULL,
  `jenis_kelamin` enum('Laki-laki','Perempuan') DEFAULT NULL,
  `telepon` varchar(15) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `admin_id` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pegawai`
--

INSERT INTO `pegawai` (`id`, `nama`, `alamat`, `tanggal_lahir`, `jenis_kelamin`, `telepon`, `email`, `created_at`, `updated_at`, `admin_id`) VALUES
(1, 'Muhammad Ilham Gymnastiar', 'Jl. Pahlawan No. 123', '1990-05-15', 'Laki-laki', '08123456789', 'IlhamG@email.com', '2024-02-06 08:11:45', '2024-02-06 11:18:23', 1),
(2, 'Tamara', 'Jl. Merdeka No. 456', '1988-08-22', 'Perempuan', '08765432100', 'tamsCans@email.com', '2024-02-06 08:11:45', '2024-02-06 11:18:38', 1),
(9, 'Acep', 'Jl. Caheum', '2024-02-06', 'Laki-laki', '0812125424', 'ac_cep@gmail.com', '2024-02-06 16:29:29', '2024-02-06 16:29:29', 1);

-- --------------------------------------------------------

--
-- Table structure for table `pegawai_jabatan`
--

CREATE TABLE `pegawai_jabatan` (
  `id` int(11) NOT NULL,
  `id_pegawai` int(11) DEFAULT NULL,
  `id_jabatan` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `pegawai_jabatan`
--

INSERT INTO `pegawai_jabatan` (`id`, `id_pegawai`, `id_jabatan`, `created_at`) VALUES
(1, 1, 1, '2024-02-06 08:13:01'),
(2, 1, 2, '2024-02-06 08:13:01'),
(3, 2, 2, '2024-02-06 08:13:01');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `jabatan`
--
ALTER TABLE `jabatan`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `pegawai`
--
ALTER TABLE `pegawai`
  ADD PRIMARY KEY (`id`),
  ADD KEY `admin_id` (`admin_id`);

--
-- Indexes for table `pegawai_jabatan`
--
ALTER TABLE `pegawai_jabatan`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_pegawai` (`id_pegawai`),
  ADD KEY `id_jabatan` (`id_jabatan`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `jabatan`
--
ALTER TABLE `jabatan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `pegawai`
--
ALTER TABLE `pegawai`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `pegawai_jabatan`
--
ALTER TABLE `pegawai_jabatan`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `pegawai`
--
ALTER TABLE `pegawai`
  ADD CONSTRAINT `pegawai_ibfk_1` FOREIGN KEY (`admin_id`) REFERENCES `admin` (`id`);

--
-- Constraints for table `pegawai_jabatan`
--
ALTER TABLE `pegawai_jabatan`
  ADD CONSTRAINT `pegawai_jabatan_ibfk_1` FOREIGN KEY (`id_pegawai`) REFERENCES `pegawai` (`id`),
  ADD CONSTRAINT `pegawai_jabatan_ibfk_2` FOREIGN KEY (`id_jabatan`) REFERENCES `jabatan` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
