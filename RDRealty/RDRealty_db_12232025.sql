-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: rdc_realty_db
-- ------------------------------------------------------
-- Server version	8.0.44

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
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=53 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add Property',7,'add_property'),(26,'Can change Property',7,'change_property'),(27,'Can delete Property',7,'delete_property'),(28,'Can view Property',7,'view_property'),(29,'Can add Property Tax Record',8,'add_propertytax'),(30,'Can change Property Tax Record',8,'change_propertytax'),(31,'Can delete Property Tax Record',8,'delete_propertytax'),(32,'Can view Property Tax Record',8,'view_propertytax'),(33,'Can add Title Movement',9,'add_titlemovement'),(34,'Can change Title Movement',9,'change_titlemovement'),(35,'Can delete Title Movement',9,'delete_titlemovement'),(36,'Can view Title Movement',9,'view_titlemovement'),(37,'Can add User Management',10,'add_usermanagement'),(38,'Can change User Management',10,'change_usermanagement'),(39,'Can delete User Management',10,'delete_usermanagement'),(40,'Can view User Management',10,'view_usermanagement'),(41,'Can add local information',11,'add_localinformation'),(42,'Can change local information',11,'change_localinformation'),(43,'Can delete local information',11,'delete_localinformation'),(44,'Can view local information',11,'view_localinformation'),(45,'Can add owner information',12,'add_ownerinformation'),(46,'Can change owner information',12,'change_ownerinformation'),(47,'Can delete owner information',12,'delete_ownerinformation'),(48,'Can view owner information',12,'view_ownerinformation'),(49,'Can add financial information',13,'add_financialinformation'),(50,'Can change financial information',13,'change_financialinformation'),(51,'Can delete financial information',13,'delete_financialinformation'),(52,'Can view financial information',13,'view_financialinformation');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$1000000$vLdvX7RctVyM2OWTsLAEyy$4rdmtseJJnwvaSue4UtKfdqDZP3L7TXm+Dn6Nfsww8k=','2025-12-23 01:58:50.564500',1,'admin','','','',1,1,'2025-12-15 02:40:36.038768'),(2,'pbkdf2_sha256$1200000$TULAWgMEOHXtdIrWQDRHNc$v8vEuw19IWhfgm4DDZVvyuuMDGUmfCdPL16SXtt+gPI=','2025-12-19 08:29:26.193667',0,'user','','','',0,1,'2025-12-15 03:16:15.129340'),(4,'pbkdf2_sha256$1200000$npaIBeSuTTy9sk8zsiwYoX$ONbWzvROLOYCK9KsNyvfMrApWwOFLXuimujZ9RJV0tg=','2025-12-19 08:28:23.241935',1,'Kaito','','','',1,1,'2025-12-15 06:24:39.087143');
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_groups` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(13,'RDRealty_App','financialinformation'),(11,'RDRealty_App','localinformation'),(12,'RDRealty_App','ownerinformation'),(7,'RDRealty_App','property'),(8,'RDRealty_App','propertytax'),(9,'RDRealty_App','titlemovement'),(10,'RDRealty_App','usermanagement'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-12-04 07:55:45.116843'),(2,'auth','0001_initial','2025-12-04 07:55:45.666683'),(3,'admin','0001_initial','2025-12-04 07:55:45.790959'),(4,'admin','0002_logentry_remove_auto_add','2025-12-04 07:55:45.797345'),(5,'admin','0003_logentry_add_action_flag_choices','2025-12-04 07:55:45.806235'),(6,'contenttypes','0002_remove_content_type_name','2025-12-04 07:55:45.914373'),(7,'auth','0002_alter_permission_name_max_length','2025-12-04 07:55:45.988648'),(8,'auth','0003_alter_user_email_max_length','2025-12-04 07:55:46.013490'),(9,'auth','0004_alter_user_username_opts','2025-12-04 07:55:46.021153'),(10,'auth','0005_alter_user_last_login_null','2025-12-04 07:55:46.077444'),(11,'auth','0006_require_contenttypes_0002','2025-12-04 07:55:46.079732'),(12,'auth','0007_alter_validators_add_error_messages','2025-12-04 07:55:46.087415'),(13,'auth','0008_alter_user_username_max_length','2025-12-04 07:55:46.157399'),(14,'auth','0009_alter_user_last_name_max_length','2025-12-04 07:55:46.220763'),(15,'auth','0010_alter_group_name_max_length','2025-12-04 07:55:46.238914'),(16,'auth','0011_update_proxy_permissions','2025-12-04 07:55:46.247452'),(17,'auth','0012_alter_user_first_name_max_length','2025-12-04 07:55:46.308711'),(18,'sessions','0001_initial','2025-12-04 07:55:46.344179'),(19,'RDRealty_App','0001_initial','2025-12-04 08:01:20.611691'),(20,'RDRealty_App','0002_alter_property_id','2025-12-04 08:08:53.744219'),(21,'RDRealty_App','0003_titlemovement_propertytax','2025-12-09 04:01:30.230237'),(22,'RDRealty_App','0004_rename_property_propertytax_associated_property_and_more','2025-12-09 05:45:01.873185'),(23,'RDRealty_App','0005_remove_titlemovement_property_delete_propertytax_and_more','2025-12-09 05:52:44.476205'),(24,'RDRealty_App','0006_usermanagement','2025-12-15 02:29:15.496955'),(25,'RDRealty_App','0007_property_property_id_property_user_id_and_more','2025-12-19 06:29:29.653088'),(26,'RDRealty_App','0008_alter_property_title_classification_and_more','2025-12-20 02:10:17.412093'),(27,'RDRealty_App','0009_rename_ownerinformation_localinformation_and_more','2025-12-23 01:57:18.737817'),(28,'RDRealty_App','0010_ownerinformation','2025-12-23 02:40:08.575706'),(29,'RDRealty_App','0011_financialinformation','2025-12-23 03:17:26.949184');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('2h1smz8jv6btgxuwwrtgfqmivf7v1c3f','.eJxVjjsLwjAUhf9LZil5e-OmuLoUnMPNo1ZsQzHpIOJ_N5Yiup7Hd86TWJxLb-cc7_YayI4wsvnVHPpbTB-jPbYRh_Kw-2lqVjk35xo6YcJLHGMqhzX9h-gx97WvtVJCQzDggldURs-dAC9oYF4CMyiVExR46Bh64ajh0AFqujXCIHdYoQtu_K4th-XrDbLkQHI:1vV2Uu:6XuqicIncWMs0ka8JumeBvYnDUjGL2CWKb_tVfLZfGw','2025-12-29 06:55:56.588871'),('h6b78bkvutf6g5twtb2uxzai03mtsrv8','.eJxVjMsOwiAQRf-FtSEyvF267zeQgQGpGkhKuzL-uzbpQrf3nHNfLOC21rCNvISZ2IUJdvrdIqZHbjugO7Zb56m3dZkj3xV-0MGnTvl5Pdy_g4qjfmvrsikFLAI4QVqQL-oMUeQkTRROyVwIDFK0XhfvpS8uKZ-iVk4bIGLvD-NsN_M:1vWnZO:BQjK3qy2A3JDRNIxNk4qXc7NTHE-cmAkh_l7UrLemlc','2026-01-03 03:23:50.799890'),('jd8sn4t6idr5ae712fevrvn5xg86321v','.eJxVjMsOwiAQRf-FtSEyvF267zeQgQGpGkhKuzL-uzbpQrf3nHNfLOC21rCNvISZ2IUJdvrdIqZHbjugO7Zb56m3dZkj3xV-0MGnTvl5Pdy_g4qjfmvrsikFLAI4QVqQL-oMUeQkTRROyVwIDFK0XhfvpS8uKZ-iVk4bIGLvD-NsN_M:1vXrfm:WgCR8EbFgPP6JIamZ7d8NppSY1Ic5M7Z2fASvepMlNA','2026-01-06 01:58:50.568548'),('op5potkwbe8vejcv6bhx51xz2dg5ixo2','.eJxVjMsOwiAQRf-FtSEyvF267zeQgQGpGkhKuzL-uzbpQrf3nHNfLOC21rCNvISZ2IUJdvrdIqZHbjugO7Zb56m3dZkj3xV-0MGnTvl5Pdy_g4qjfmvrsikFLAI4QVqQL-oMUeQkTRROyVwIDFK0XhfvpS8uKZ-iVk4bIGLvD-NsN_M:1vWnTy:jHPoXAXjY-SQOzA1qbL0L7GC26plVbyy5SRDaHQrazM','2026-01-03 03:18:14.729053'),('v7wa0xncimo42pl8nxlsam9478tf8owa','.eJxVjLsKwkAQRf9lawmTzbIPO8XWJmC9zOxMjGhCcJNCxH83kSCkPefe81ZTlmfssMerdNKP8cZqX-5UxGls408uRBm1YYTpLv0i6lMt-Bhf8TAMxYpzcZlH53_0uK43iRZzO_-9JgPgyCVwKTBoSDaVaIJtErOrjCMbdEneEbMWEAnYEFRgAqOHSn2-VxRA9w:1vVJai:UB72zMvxBikm-MnJ6GDaLSlYnTWQk1ZdNLb9-1N9qhM','2025-12-30 01:11:04.512204');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rdrealty_app_property`
--

DROP TABLE IF EXISTS `rdrealty_app_property`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rdrealty_app_property` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `title_no` varchar(50) NOT NULL,
  `lot_no` varchar(100) NOT NULL,
  `lot_area` decimal(10,2) NOT NULL,
  `title_classification` varchar(3) NOT NULL,
  `title_status` varchar(4) NOT NULL,
  `title_description` longtext,
  `date_added` datetime(6) NOT NULL,
  `property_id` int unsigned DEFAULT NULL,
  `user_id` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `title_no` (`title_no`),
  UNIQUE KEY `property_id` (`property_id`),
  CONSTRAINT `rdrealty_app_property_chk_1` CHECK ((`property_id` >= 0)),
  CONSTRAINT `rdrealty_app_property_chk_2` CHECK ((`user_id` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rdrealty_app_property`
--

LOCK TABLES `rdrealty_app_property` WRITE;
/*!40000 ALTER TABLE `rdrealty_app_property` DISABLE KEYS */;
INSERT INTO `rdrealty_app_property` VALUES (1,'sample 1','lot 1 block 2',23626.00,'RES','PENT','sample sample sample','2025-12-09 05:45:01.743044',1,1),(2,'2387yfhk','Block 15, Lot 82',1200.00,'IND','UND','Sample 2','2025-12-09 05:45:01.743044',2,1),(3,'iweuw8','Block 15, Lot 17',450.00,'AGR','SOLD','Descirption Sample Here','2025-12-09 05:56:25.734669',3,1),(4,'12347Sage','Lot 34, Block 85, Unknown Street, PNG',400.00,'RES','ACT','Sample 4,','2025-12-15 05:18:06.165597',4,1),(5,'147-2024001199','Lot 4650',416.00,'COM','COL','','2025-12-20 02:04:40.928358',5,1);
/*!40000 ALTER TABLE `rdrealty_app_property` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rdrealty_financial_information`
--

DROP TABLE IF EXISTS `rdrealty_financial_information`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rdrealty_financial_information` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `fi_encumbrance` varchar(250) DEFAULT NULL,
  `fi_mortgage` varchar(150) DEFAULT NULL,
  `fi_borrower` varchar(80) DEFAULT NULL,
  `property_id` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `rdrealty_financial_i_property_id_535bd930_fk_RDRealty_` (`property_id`),
  CONSTRAINT `rdrealty_financial_i_property_id_535bd930_fk_RDRealty_` FOREIGN KEY (`property_id`) REFERENCES `rdrealty_app_property` (`property_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rdrealty_financial_information`
--

LOCK TABLES `rdrealty_financial_information` WRITE;
/*!40000 ALTER TABLE `rdrealty_financial_information` DISABLE KEYS */;
INSERT INTO `rdrealty_financial_information` VALUES (1,'Mortgages','SR:34398, PR#: 489579','Floyd',4);
/*!40000 ALTER TABLE `rdrealty_financial_information` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rdrealty_local_information`
--

DROP TABLE IF EXISTS `rdrealty_local_information`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rdrealty_local_information` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `loc_specific` longtext,
  `loc_province` varchar(255) DEFAULT NULL,
  `loc_city` varchar(255) DEFAULT NULL,
  `loc_barangay` varchar(255) DEFAULT NULL,
  `property_id` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `rdrealty_owner_infor_property_id_d238428c_fk_RDRealty_` (`property_id`),
  CONSTRAINT `rdrealty_owner_infor_property_id_d238428c_fk_RDRealty_` FOREIGN KEY (`property_id`) REFERENCES `rdrealty_app_property` (`property_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rdrealty_local_information`
--

LOCK TABLES `rdrealty_local_information` WRITE;
/*!40000 ALTER TABLE `rdrealty_local_information` DISABLE KEYS */;
INSERT INTO `rdrealty_local_information` VALUES (1,'Hose Banda','South Cotabato','City of General Santos','Calumpang',3),(2,'Dadiangas West, P. Acharon Blvd., General Santos City- Jo-Anns Bakeshop','South Cotabato','City of General Santos','Dadiangas West',5),(3,'','Bohol','Catigbian','Mahayag Sur',1),(4,'Bulacan Area','Bulacan','Plaridel','Rueda',2),(5,'Near Underpass.','South Cotabato','City of General Santos','Dadiangas North',4);
/*!40000 ALTER TABLE `rdrealty_local_information` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rdrealty_owner_information`
--

DROP TABLE IF EXISTS `rdrealty_owner_information`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rdrealty_owner_information` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `oi_fullname` varchar(80) DEFAULT NULL,
  `oi_bankname` varchar(50) DEFAULT NULL,
  `oi_custody_title` varchar(60) DEFAULT NULL,
  `property_id` int unsigned NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rdrealty_owner_information`
--

LOCK TABLES `rdrealty_owner_information` WRITE;
/*!40000 ALTER TABLE `rdrealty_owner_information` DISABLE KEYS */;
INSERT INTO `rdrealty_owner_information` VALUES (1,'Brother','PSBank','Manny Pacquiao',4);
/*!40000 ALTER TABLE `rdrealty_owner_information` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tbl_title_info`
--

DROP TABLE IF EXISTS `tbl_title_info`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tbl_title_info` (
  `title_info_id` int unsigned NOT NULL,
  `title_no` varchar(80) DEFAULT NULL,
  `lot_no` varchar(60) DEFAULT NULL,
  `lot_area` int DEFAULT NULL,
  `title_classfication` varchar(50) DEFAULT NULL,
  `title_status` varchar(20) DEFAULT NULL,
  `title_description` varchar(200) DEFAULT NULL,
  `tbl_title_infocol` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`title_info_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tbl_title_info`
--

LOCK TABLES `tbl_title_info` WRITE;
/*!40000 ALTER TABLE `tbl_title_info` DISABLE KEYS */;
/*!40000 ALTER TABLE `tbl_title_info` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-23 11:34:13
