-- MySQL dump 10.13  Distrib 5.7.20, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: media
-- ------------------------------------------------------
-- Server version	5.7.20-0ubuntu0.17.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `store_userprofile`
--

DROP TABLE IF EXISTS `store_userprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `store_userprofile` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hhmi_project_id` varchar(30) DEFAULT NULL,
  `employee_id` varchar(20) DEFAULT NULL,
  `email_address` varchar(255) DEFAULT NULL,
  `first_name` varchar(30) DEFAULT NULL,
  `last_name` varchar(30) DEFAULT NULL,
  `is_manager` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `is_janelia` tinyint(1) NOT NULL,
  `is_visitor` tinyint(1) NOT NULL,
  `department_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `is_privileged` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `store_userprofile_user_id_6db609dc_uniq` (`user_id`),
  KEY `store_userprofile_department_id_89cf167a_fk_store_department_id` (`department_id`),
  CONSTRAINT `store_userprofile_department_id_89cf167a_fk_store_department_id` FOREIGN KEY (`department_id`) REFERENCES `store_department` (`id`),
  CONSTRAINT `store_userprofile_user_id_6db609dc_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store_userprofile`
--

LOCK TABLES `store_userprofile` WRITE;
/*!40000 ALTER TABLE `store_userprofile` DISABLE KEYS */;
INSERT INTO `store_userprofile` VALUES (1,NULL,'12345','coffmans@janelia.hhmi.org','Brian','Rebhorn',0,1,1,0,5,3,1),(2,NULL,'51305','coffmans@janelia.hhmi.org','Scarlett','Harrison',0,1,1,0,1,2,1),(3,NULL,'67891','coffmans@janelia.hhmi.org','Guillermo','Gonzalez',0,1,1,0,1,4,0),(4,NULL,'10111','coffmans@janelia.hhmi.org','Greg','Harrison',1,1,1,0,2,5,1),(5,NULL,'21314','coffmans@janelia.hhmi.org','Eric','Pitts',0,1,0,1,NULL,6,0),(6,NULL,'15161','coffmans@janelia.hhmi.org','Kelie','Negron',0,0,1,0,3,7,0);
/*!40000 ALTER TABLE `store_userprofile` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-11-28 13:42:40
