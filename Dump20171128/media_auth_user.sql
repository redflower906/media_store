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
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$36000$tzmKmAyLycQg$P9vH20dffOiD/pFP0EbnDSRGy55tWmToKc5VAJHj5kc=','2017-11-15 16:17:00.311380',1,'admin','','','coffmansr906@gmail.com',1,1,'2017-06-16 17:36:27.674439'),(2,'pbkdf2_sha256$36000$RhhZJI12DcuP$brAFxBmHGiRR4Ar5KSKng9PwnoYq0IIFYTAGvjtnW+s=','2017-11-15 16:17:11.605712',1,'scar','Scarlett','Harrison','coffmansr906@gmail.com',1,1,'2017-08-02 19:51:58.840257'),(3,'pbkdf2_sha256$36000$QJQfb5BponsU$TiZFwPReNaU6TSKsT3L5eHcYrDayY1Q+5NP/pV+dtcA=','2017-11-15 18:17:07.654966',0,'stafftest','Brian','Rebhorn','coffmans@janelia.hhmi.org',0,1,'2017-11-14 15:10:56.000000'),(4,'pbkdf2_sha256$36000$nlnGmpkykISi$x1Qt3OvqwC3NSXFsUt77rnHFTkCa41D3nnB2+b5Nl7Q=','2017-11-28 15:33:40.382798',0,'usertest','guillermo','gonzalez','coffmans@janelia.hhmi.org',0,1,'2017-11-14 15:11:09.000000'),(5,'pbkdf2_sha256$36000$LSwWPGcx0v96$yQ3GzDEztBO8XUcRjzWOkT4kmFhnBEXTce4ADVP/hOE=','2017-11-28 15:38:16.491170',0,'managertest','Greg','Harrison','coffmans@janelia.hhmi.org',1,1,'2017-11-14 19:06:48.000000'),(6,'pbkdf2_sha256$36000$C7S7YXIQ6wTJ$/SAP7LEGegnlc5JjtwgNQaeXUs5WceSEO4opnXXDRsc=','2017-11-28 15:37:44.814550',0,'visitortest','Eric','Pitts','coffmans@janelia.hhmi.org',0,1,'2017-11-14 19:08:06.000000'),(7,'pbkdf2_sha256$36000$s65KPM4bpdH6$yUTovqZsP7RTvP6QG38KPc0J6dTbvjcge/f+yrB/NCI=',NULL,0,'inactivetest','Kelie','Negon','coffmans@janelia.hhmi.org',0,0,'2017-11-14 19:12:52.000000');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
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
