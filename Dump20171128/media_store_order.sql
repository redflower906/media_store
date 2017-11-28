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
-- Table structure for table `store_order`
--

DROP TABLE IF EXISTS `store_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `store_order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `special_instructions` longtext NOT NULL,
  `date_created` date NOT NULL,
  `date_modified` date DEFAULT NULL,
  `date_submitted` date DEFAULT NULL,
  `date_complete` date DEFAULT NULL,
  `department_id` int(11) DEFAULT NULL,
  `date_billed` date DEFAULT NULL,
  `date_recurring_start` date DEFAULT NULL,
  `date_recurring_stop` date DEFAULT NULL,
  `is_recurring` tinyint(1) NOT NULL,
  `status` varchar(30) NOT NULL,
  `location` varchar(30) NOT NULL,
  `requester_id` int(11) DEFAULT NULL,
  `submitter_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `store_order_department_id_bddd5136_fk_store_department_id` (`department_id`),
  KEY `store_order_requester_id_8bab98c7` (`requester_id`),
  KEY `store_order_submitter_id_f98f486a` (`submitter_id`),
  CONSTRAINT `store_order_department_id_bddd5136_fk_store_department_id` FOREIGN KEY (`department_id`) REFERENCES `store_department` (`id`),
  CONSTRAINT `store_order_requester_id_8bab98c7_fk_auth_user_id` FOREIGN KEY (`requester_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `store_order_submitter_id_f98f486a_fk_auth_user_id` FOREIGN KEY (`submitter_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store_order`
--

LOCK TABLES `store_order` WRITE;
/*!40000 ALTER TABLE `store_order` DISABLE KEYS */;
INSERT INTO `store_order` VALUES (1,'complete, not recurring','2017-08-06','2017-08-06','2017-08-09','2017-08-10',1,'2017-08-20',NULL,NULL,0,'Complete','One',2,2),(2,'complete, recurring','2017-08-06','2017-08-06','2017-08-08','2017-08-08',2,NULL,NULL,NULL,0,'Complete','Two',3,3),(3,'complete, not recurring','2017-08-06','2017-08-06','2017-08-07','2017-08-09',3,'2017-09-20','2017-08-10','2017-09-10',1,'Complete','One',4,4),(4,'submitted, recurring','2017-08-06','2017-08-06','2017-08-06',NULL,4,NULL,'2017-08-11','2017-09-11',1,'Submitted','Two',5,5),(5,'In-Progress, recurring','2017-08-06','2017-08-06','2017-08-05',NULL,1,NULL,'2017-08-12','2017-09-12',1,'In Progress','One',6,6),(6,'complete, recurring','2017-08-06','2017-08-06','2017-08-04','2017-08-09',3,NULL,'2017-08-13','2017-09-13',1,'Complete','Two',7,7),(7,'complete, not recurring','2017-08-06','2017-08-06','2017-08-10','2017-08-10',1,'2017-08-20',NULL,NULL,0,'Complete','One',6,7),(8,'submitted not recurring','2017-08-06','2017-08-06','2017-08-08',NULL,2,NULL,NULL,NULL,0,'Submitted','Two',4,5),(9,'complete, not recurring','2017-08-06','2017-08-06','2017-08-11','2017-08-09',3,'2017-09-20','2017-08-10','2017-09-10',1,'Complete','One',2,3),(10,'submitted, recurring','2017-08-06','2017-08-06','2017-08-06',NULL,3,NULL,'2017-08-11','2017-09-11',1,'Submitted','Two',2,2),(11,'In-Progress, recurring','2017-08-06','2017-08-06','2017-08-05',NULL,2,NULL,'2017-08-12','2017-09-12',1,'In Progress','One',3,3),(12,'complete, not recurring','2017-08-06','2017-08-06','2017-08-04','2017-08-10',3,NULL,'2017-08-13','2017-09-13',0,'Complete','Two',4,4);
/*!40000 ALTER TABLE `store_order` ENABLE KEYS */;
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
