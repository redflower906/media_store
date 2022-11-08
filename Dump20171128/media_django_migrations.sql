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
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=42 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2017-06-14 19:46:55.782747'),(2,'auth','0001_initial','2017-06-14 19:46:56.417349'),(3,'admin','0001_initial','2017-06-14 19:46:56.578008'),(4,'admin','0002_logentry_remove_auto_add','2017-06-14 19:46:56.622855'),(5,'contenttypes','0002_remove_content_type_name','2017-06-14 19:46:56.726831'),(6,'auth','0002_alter_permission_name_max_length','2017-06-14 19:46:56.767241'),(7,'auth','0003_alter_user_email_max_length','2017-06-14 19:46:56.836148'),(8,'auth','0004_alter_user_username_opts','2017-06-14 19:46:56.886946'),(9,'auth','0005_alter_user_last_login_null','2017-06-14 19:46:56.940880'),(10,'auth','0006_require_contenttypes_0002','2017-06-14 19:46:56.945308'),(11,'auth','0007_alter_validators_add_error_messages','2017-06-14 19:46:56.958615'),(12,'auth','0008_alter_user_username_max_length','2017-06-14 19:46:57.007660'),(13,'sessions','0001_initial','2017-06-14 19:46:57.072011'),(14,'store','0001_initial','2017-06-14 19:46:57.124942'),(15,'store','0002_auto_20170608_1416','2017-06-14 19:46:57.305190'),(16,'store','0003_auto_20170608_1437','2017-06-14 19:46:57.357981'),(17,'store','0004_auto_20170612_1305','2017-06-14 19:46:57.721514'),(18,'store','0005_auto_20170613_1413','2017-06-14 19:46:57.991593'),(19,'store','0006_auto_20170613_1448','2017-06-14 19:46:58.108271'),(20,'store','0007_auto_20170614_1113','2017-06-14 19:46:58.218265'),(21,'store','0008_auto_20170615_1100','2017-06-16 17:48:05.018366'),(22,'store','0009_auto_20170616_1430','2017-06-16 18:41:17.787535'),(23,'store','0010_inventory_container','2017-06-28 17:49:11.363079'),(24,'store','0011_auto_20170707_1452','2017-07-07 18:52:36.603432'),(25,'store','0012_auto_20170710_1436','2017-07-10 18:36:36.537093'),(26,'store','0013_inventory_volume','2017-07-10 18:38:13.133395'),(27,'store','0014_auto_20170710_1439','2017-07-10 18:39:54.316801'),(28,'store','0015_auto_20170718_1110','2017-07-18 15:12:54.283520'),(29,'store','0016_auto_20170802_1100','2017-08-02 15:01:00.727586'),(30,'store','0017_auto_20170912_1021','2017-09-12 15:01:45.609501'),(31,'store','0018_auto_20170927_1351','2017-09-27 17:51:58.316132'),(32,'store','0019_auto_20170927_1417','2017-09-27 18:17:27.995791'),(33,'store','0020_auto_20171010_2300','2017-10-11 14:54:42.912164'),(34,'store','0021_auto_20171011_1536','2017-10-11 19:36:41.571084'),(35,'store','0022_auto_20171031_1138','2017-10-31 15:38:14.000923'),(36,'store','0022_auto_20171031_1142','2017-10-31 15:42:29.581591'),(37,'store','0023_auto_20171114_1132','2017-11-14 16:32:30.302442'),(38,'store','0024_auto_20171114_1432','2017-11-14 19:32:20.000294'),(39,'store','0025_userprofile_is_privileged','2017-11-14 19:50:29.577491'),(40,'store','0026_auto_20171114_1559','2017-11-14 20:59:53.533678'),(41,'store','0027_auto_20171114_1603','2017-11-14 21:03:44.679070');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
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
