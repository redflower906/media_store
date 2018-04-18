-- MySQL dump 10.13  Distrib 5.7.21, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: media
-- ------------------------------------------------------
-- Server version	5.7.21-log

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
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add inventory',1,'add_inventory'),(2,'Can change inventory',1,'change_inventory'),(3,'Can delete inventory',1,'delete_inventory'),(4,'Can add vendor',2,'add_vendor'),(5,'Can change vendor',2,'change_vendor'),(6,'Can delete vendor',2,'delete_vendor'),(7,'Can add order',3,'add_order'),(8,'Can change order',3,'change_order'),(9,'Can delete order',3,'delete_order'),(10,'Can add department',4,'add_department'),(11,'Can change department',4,'change_department'),(12,'Can delete department',4,'delete_department'),(13,'Can add log entry',5,'add_logentry'),(14,'Can change log entry',5,'change_logentry'),(15,'Can delete log entry',5,'delete_logentry'),(16,'Can add user',6,'add_user'),(17,'Can change user',6,'change_user'),(18,'Can delete user',6,'delete_user'),(19,'Can add group',7,'add_group'),(20,'Can change group',7,'change_group'),(21,'Can delete group',7,'delete_group'),(22,'Can add permission',8,'add_permission'),(23,'Can change permission',8,'change_permission'),(24,'Can delete permission',8,'delete_permission'),(25,'Can add content type',9,'add_contenttype'),(26,'Can change content type',9,'change_contenttype'),(27,'Can delete content type',9,'delete_contenttype'),(28,'Can add session',10,'add_session'),(29,'Can change session',10,'change_session'),(30,'Can delete session',10,'delete_session'),(31,'Can add announcements',11,'add_announcements'),(32,'Can change announcements',11,'change_announcements'),(33,'Can delete announcements',11,'delete_announcements'),(34,'Can add Order Status',12,'add_orderstatus'),(35,'Can change Order Status',12,'change_orderstatus'),(36,'Can delete Order Status',12,'delete_orderstatus'),(37,'Can add order line',13,'add_orderline'),(38,'Can change order line',13,'change_orderline'),(39,'Can delete order line',13,'delete_orderline'),(40,'Can add user profile',14,'add_userprofile'),(41,'Can change user profile',14,'change_userprofile'),(42,'Can delete user profile',14,'delete_userprofile'),(43,'Can add user full name',6,'add_userfullname'),(44,'Can change user full name',6,'change_userfullname'),(45,'Can delete user full name',6,'delete_userfullname');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-03-30 15:43:16
