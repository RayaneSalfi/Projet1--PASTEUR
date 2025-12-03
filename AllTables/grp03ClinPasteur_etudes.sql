-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: 172.27.0.50    Database: grp03ClinPasteur
-- ------------------------------------------------------
-- Server version	5.5.5-10.11.11-MariaDB-0+deb12u1

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
-- Table structure for table `etudes`
--

DROP TABLE IF EXISTS `etudes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `etudes` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nomEtu` varchar(100) NOT NULL,
  `descEtude` text DEFAULT NULL,
  `idProtocole` int(11) DEFAULT NULL,
  `idQuestion` int(11) DEFAULT NULL,
  `idOrganisme` int(11) DEFAULT NULL,
  `dateDebEtu` date DEFAULT NULL,
  `dateFinEtu` date DEFAULT NULL,
  `idChirResp` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `idProtocole` (`idProtocole`),
  KEY `idQuestion` (`idQuestion`),
  KEY `idOrganisme` (`idOrganisme`),
  KEY `idChirResp` (`idChirResp`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `etudes`
--

LOCK TABLES `etudes` WRITE;
/*!40000 ALTER TABLE `etudes` DISABLE KEYS */;
INSERT INTO `etudes` VALUES (1,'Étude Cancer Poumon 2020','Suivi de patients atteints de cancer du poumon',2,NULL,1,'2020-01-01','2024-12-31',1),(2,'Étude Cirrhose Lyon','Ancien essai (non utilisé car hors cancer, conservé pour cohérence historique)',1,NULL,2,'2019-05-15','2023-12-31',2),(3,'Essai Chirurgie Cancer Rectum','Évaluation des résultats post-opératoires en chirurgie rectum',2,NULL,1,'2022-01-01','2026-12-31',4),(4,'Protocole RecaRe','Essai multicentrique sur la prise en charge du cancer rectum : chirurgie + radiochimiothérapie',2,NULL,2,'2023-01-01','2027-12-31',4),(5,'Étude Cancer Sein','Essai clinique sur traitements innovants cancer du sein',2,NULL,3,'2021-01-01','2025-12-31',5),(6,'E','E',11,11,11,'2025-11-24',NULL,NULL);
/*!40000 ALTER TABLE `etudes` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-03 14:18:45
