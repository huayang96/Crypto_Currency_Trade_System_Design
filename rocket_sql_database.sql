-- MySQL dump 10.13  Distrib 8.0.18, for Win64 (x86_64)
--
-- Host: localhost    Database: relation_model
-- ------------------------------------------------------
-- Server version	8.0.18

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `action`
--

DROP TABLE IF EXISTS `action`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `action` (
  `action_id` int(11) NOT NULL,
  `action_type` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`action_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `action`
--

LOCK TABLES `action` WRITE;
/*!40000 ALTER TABLE `action` DISABLE KEYS */;
INSERT INTO `action` VALUES (1,'buy'),(2,'sell');
/*!40000 ALTER TABLE `action` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `blotter`
--

DROP TABLE IF EXISTS `blotter`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `blotter` (
  `product_id` int(11) NOT NULL,
  `action_id` int(11) NOT NULL,
  `quantity` double DEFAULT NULL,
  `transaction_id` int(11) NOT NULL AUTO_INCREMENT,
  `coin_price` char(34) DEFAULT NULL,
  `lastUpdated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`transaction_id`),
  KEY `trans_action_table_fk` (`action_id`),
  KEY `trans_product_table_fk` (`product_id`),
  CONSTRAINT `trans_action_table_fk` FOREIGN KEY (`action_id`) REFERENCES `action` (`action_id`),
  CONSTRAINT `trans_product_table_fk` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`)
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blotter`
--

LOCK TABLES `blotter` WRITE;
/*!40000 ALTER TABLE `blotter` DISABLE KEYS */;
INSERT INTO `blotter` VALUES (1,1,12,1,'7305.0','2019-12-03 21:59:52'),(1,1,12,2,'7305.0','2019-12-03 22:41:00'),(1,2,40,3,'7305.0','2019-12-03 22:41:29'),(1,1,1,4,'7305.0','2019-12-03 23:23:46'),(1,1,11,5,'7290.99','2019-12-04 00:03:56'),(1,1,12,6,'7267.58','2019-12-04 00:13:32'),(1,1,12,7,'7777','2019-12-11 01:08:03'),(1,1,12,8,'7777','2019-12-11 01:08:28'),(1,2,12,9,'7779','2019-12-11 01:08:28'),(1,1,11,10,'7155.95','2019-12-11 01:09:32'),(1,1,111,11,'7155.95','2019-12-11 18:50:32');
/*!40000 ALTER TABLE `blotter` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cash_balance`
--

DROP TABLE IF EXISTS `cash_balance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cash_balance` (
  `cash_balance_id` int(11) NOT NULL,
  `yh_cash_balance` double DEFAULT NULL,
  PRIMARY KEY (`cash_balance_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cash_balance`
--

LOCK TABLES `cash_balance` WRITE;
/*!40000 ALTER TABLE `cash_balance` DISABLE KEYS */;
INSERT INTO `cash_balance` VALUES (1,100000);
/*!40000 ALTER TABLE `cash_balance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `p_l`
--

DROP TABLE IF EXISTS `p_l`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `p_l` (
  `p_l_id` double NOT NULL,
  `product_id` int(11) DEFAULT NULL,
  `upl` double DEFAULT NULL,
  `rpl` double DEFAULT NULL,
  `qty` double DEFAULT NULL,
  `vwap` double DEFAULT NULL,
  PRIMARY KEY (`p_l_id`),
  KEY `product_id` (`product_id`),
  CONSTRAINT `p_l_ibfk_1` FOREIGN KEY (`product_id`) REFERENCES `product` (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `p_l`
--

LOCK TABLES `p_l` WRITE;
/*!40000 ALTER TABLE `p_l` DISABLE KEYS */;
INSERT INTO `p_l` VALUES (1,1,-4463.685999999947,376.195999999959,156,7184.563371794871),(2,2,-3.210000000000008,-1.6800000000001774,1,147.62),(3,3,0,0,0,0);
/*!40000 ALTER TABLE `p_l` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product` (
  `product_id` int(11) NOT NULL,
  `product_name` varchar(255) DEFAULT NULL,
  `price` char(34) DEFAULT NULL,
  PRIMARY KEY (`product_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (1,'BTC','7155.95'),(2,'ETH','144.41'),(3,'LTC','44.2');
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-12-11 15:47:47
