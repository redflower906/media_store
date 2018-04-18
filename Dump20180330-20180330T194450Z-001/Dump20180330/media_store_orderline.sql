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
-- Table structure for table `store_orderline`
--

DROP TABLE IF EXISTS `store_orderline`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `store_orderline` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `description` longtext NOT NULL,
  `qty` decimal(10,2) NOT NULL,
  `unit` varchar(30) DEFAULT NULL,
  `line_cost` decimal(10,2) NOT NULL,
  `inventory_id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `store_orderline_inventory_id_3cad57b5_fk_store_inventory_id` (`inventory_id`),
  KEY `store_orderline_order_id_5a82cf64_fk_store_order_id` (`order_id`),
  CONSTRAINT `store_orderline_inventory_id_3cad57b5_fk_store_inventory_id` FOREIGN KEY (`inventory_id`) REFERENCES `store_inventory` (`id`),
  CONSTRAINT `store_orderline_order_id_5a82cf64_fk_store_order_id` FOREIGN KEY (`order_id`) REFERENCES `store_order` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `store_orderline`
--

LOCK TABLES `store_orderline` WRITE;
/*!40000 ALTER TABLE `store_orderline` DISABLE KEYS */;
INSERT INTO `store_orderline` VALUES (1,'Charcoal: 60mm (sleeve)',1.00,'sleeve',14.50,610,1),(2,'4% agar: reused tray (plate)',1.00,'plate',3.30,609,1),(3,'Grape Juice plates: 35mm (sleeve)',2.00,'sleeve',28.00,613,2),(4,'4% agar: reused tray (plate)',2.00,'plate',6.60,609,3),(5,'Charcoal: 60mm (sleeve)',2.00,'sleeve',29.00,610,4),(6,'Grape Juice plates: 35mm (sleeve)',1.00,'sleeve',14.00,613,5),(7,'Starvation: vials (tray)',3.00,'tray',76.83,615,7),(8,'Charcoal: 60mm (sleeve)',1.00,'sleeve',14.50,610,8),(9,'4% agar: reused tray (plate)',1.00,'plate',3.30,609,9),(10,'Grape Juice plates: 35mm (sleeve)',2.00,'sleeve',28.00,613,10),(11,'4% agar: reused tray (plate)',2.00,'plate',6.60,609,11),(12,'Charcoal: 60mm (sleeve)',2.00,'sleeve',29.00,610,12),(13,'Grape Juice plates: 35mm (sleeve)',1.00,'sleeve',14.00,613,6),(14,'Starvation: vials (tray)',3.00,'tray',76.83,615,2);
/*!40000 ALTER TABLE `store_orderline` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2018-03-30 15:43:28
