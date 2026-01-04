CREATE DATABASE  IF NOT EXISTS `rdc_realty_db` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `rdc_realty_db`;
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
  `id` bigint NOT NULL AUTO_INCREMENT,
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
) ENGINE=InnoDB AUTO_INCREMENT=97 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',3,'add_permission'),(6,'Can change permission',3,'change_permission'),(7,'Can delete permission',3,'delete_permission'),(8,'Can view permission',3,'view_permission'),(9,'Can add group',2,'add_group'),(10,'Can change group',2,'change_group'),(11,'Can delete group',2,'delete_group'),(12,'Can view group',2,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add customer',7,'add_customer'),(22,'Can change customer',7,'change_customer'),(23,'Can delete customer',7,'delete_customer'),(24,'Can view customer',7,'view_customer'),(25,'Can add payment',8,'add_payment'),(26,'Can change payment',8,'change_payment'),(27,'Can delete payment',8,'delete_payment'),(28,'Can view payment',8,'view_payment'),(29,'Can add user',6,'add_boardinghouseuser'),(30,'Can change user',6,'change_boardinghouseuser'),(31,'Can delete user',6,'delete_boardinghouseuser'),(32,'Can view user',6,'view_boardinghouseuser'),(33,'Can add room',9,'add_room'),(34,'Can change room',9,'change_room'),(35,'Can delete room',9,'delete_room'),(36,'Can view room',9,'view_room'),(37,'Can add user',10,'add_user'),(38,'Can change user',10,'change_user'),(39,'Can delete user',10,'delete_user'),(40,'Can view user',10,'view_user'),(41,'Can add Property',16,'add_property'),(42,'Can change Property',16,'change_property'),(43,'Can delete Property',16,'delete_property'),(44,'Can view Property',16,'view_property'),(45,'Can add local information',13,'add_localinformation'),(46,'Can change local information',13,'change_localinformation'),(47,'Can delete local information',13,'delete_localinformation'),(48,'Can view local information',13,'view_localinformation'),(49,'Can add owner information',15,'add_ownerinformation'),(50,'Can change owner information',15,'change_ownerinformation'),(51,'Can delete owner information',15,'delete_ownerinformation'),(52,'Can view owner information',15,'view_ownerinformation'),(53,'Can add financial information',12,'add_financialinformation'),(54,'Can change financial information',12,'change_financialinformation'),(55,'Can delete financial information',12,'delete_financialinformation'),(56,'Can view financial information',12,'view_financialinformation'),(57,'Can add additional information',11,'add_additionalinformation'),(58,'Can change additional information',11,'change_additionalinformation'),(59,'Can delete additional information',11,'delete_additionalinformation'),(60,'Can view additional information',11,'view_additionalinformation'),(61,'Can add supporting document',17,'add_supportingdocument'),(62,'Can change supporting document',17,'change_supportingdocument'),(63,'Can delete supporting document',17,'delete_supportingdocument'),(64,'Can view supporting document',17,'view_supportingdocument'),(65,'Can add user profile',18,'add_userprofile'),(66,'Can change user profile',18,'change_userprofile'),(67,'Can delete user profile',18,'delete_userprofile'),(68,'Can view user profile',18,'view_userprofile'),(69,'Can add notification',14,'add_notification'),(70,'Can change notification',14,'change_notification'),(71,'Can delete notification',14,'delete_notification'),(72,'Can view notification',14,'view_notification'),(73,'Can add property tax',19,'add_propertytax'),(74,'Can change property tax',19,'change_propertytax'),(75,'Can delete property tax',19,'delete_propertytax'),(76,'Can view property tax',19,'view_propertytax'),(77,'Can add Property',20,'add_airequestlog'),(78,'Can change Property',20,'change_airequestlog'),(79,'Can delete Property',20,'delete_airequestlog'),(80,'Can view Property',20,'view_airequestlog'),(81,'Can add title movement',21,'add_titlemovement'),(82,'Can change title movement',21,'change_titlemovement'),(83,'Can delete title movement',21,'delete_titlemovement'),(84,'Can view title movement',21,'view_titlemovement'),(85,'Can add title movement document',22,'add_titlemovementdocument'),(86,'Can change title movement document',22,'change_titlemovementdocument'),(87,'Can delete title movement document',22,'delete_titlemovementdocument'),(88,'Can view title movement document',22,'view_titlemovementdocument'),(89,'Can add Title Movement Request',23,'add_titlemovementrequest'),(90,'Can change Title Movement Request',23,'change_titlemovementrequest'),(91,'Can delete Title Movement Request',23,'delete_titlemovementrequest'),(92,'Can view Title Movement Request',23,'view_titlemovementrequest'),(93,'Can add property history',24,'add_propertyhistory'),(94,'Can change property history',24,'change_propertyhistory'),(95,'Can delete property history',24,'delete_propertyhistory'),(96,'Can view property history',24,'view_propertyhistory');
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
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$1200000$cjMvHJWhR4lxBywLRBC4gl$+k4GjFF+KQEbVdhctCPrYm9tvzJBRXoJRmEo4eAObYE=','2026-01-04 00:46:46.716917',1,'admin','','','',1,1,'2025-12-15 02:40:36.038768'),(2,'pbkdf2_sha256$1000000$P23xcuyFlBqyoZk3rCIP6i$xa6Huh8q7s93+DTiRVdn4gJ2ViMtrBi5hZchAq9GRQY=','2026-01-02 03:52:36.120965',0,'user','','','',0,1,'2025-12-15 03:16:15.129340'),(4,'pbkdf2_sha256$1200000$BfPpQGs2r2Zlq5Uttaunws$96rtMTzIA8zWEAe6Cbe47Gf8pGWnts5WUJyvJ19pvFU=','2026-01-02 08:53:09.568491',1,'Kaito','','','',1,1,'2025-12-15 06:24:39.087143'),(5,'pbkdf2_sha256$1200000$7YD6N8bcq1qaxb840YE6zS$C/rVGOvSqvg+zz6FZRI/sjZmLw7eSbflXFwk2X8cyJs=',NULL,0,'test_admin_notif','','','test@example.com',1,1,'2025-12-29 02:31:16.902191');
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
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk` FOREIGN KEY (`user_id`) REFERENCES `payment_scheduler_boardinghouseuser` (`id`),
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
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(2,'auth','group'),(3,'auth','permission'),(10,'auth','user'),(4,'contenttypes','contenttype'),(6,'Payment_Scheduler','boardinghouseuser'),(7,'Payment_Scheduler','customer'),(8,'Payment_Scheduler','payment'),(9,'Payment_Scheduler','room'),(11,'RDRealty_App','additionalinformation'),(20,'RDRealty_App','airequestlog'),(12,'RDRealty_App','financialinformation'),(13,'RDRealty_App','localinformation'),(14,'RDRealty_App','notification'),(15,'RDRealty_App','ownerinformation'),(16,'RDRealty_App','property'),(24,'RDRealty_App','propertyhistory'),(19,'RDRealty_App','propertytax'),(17,'RDRealty_App','supportingdocument'),(21,'RDRealty_App','titlemovement'),(22,'RDRealty_App','titlemovementdocument'),(23,'RDRealty_App','titlemovementrequest'),(18,'RDRealty_App','userprofile'),(5,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-12-17 00:05:54.697952'),(2,'contenttypes','0002_remove_content_type_name','2025-12-17 00:05:54.801451'),(3,'auth','0001_initial','2025-12-17 00:05:55.063728'),(4,'auth','0002_alter_permission_name_max_length','2025-12-17 00:05:55.120307'),(5,'auth','0003_alter_user_email_max_length','2025-12-17 00:05:55.127457'),(6,'auth','0004_alter_user_username_opts','2025-12-17 00:05:55.133637'),(7,'auth','0005_alter_user_last_login_null','2025-12-17 00:05:55.141776'),(8,'auth','0006_require_contenttypes_0002','2025-12-17 00:05:55.144256'),(9,'auth','0007_alter_validators_add_error_messages','2025-12-17 00:05:55.150922'),(10,'auth','0008_alter_user_username_max_length','2025-12-17 00:05:55.158366'),(11,'auth','0009_alter_user_last_name_max_length','2025-12-17 00:05:55.163713'),(12,'auth','0010_alter_group_name_max_length','2025-12-17 00:05:55.180295'),(13,'auth','0011_update_proxy_permissions','2025-12-17 00:05:55.188229'),(14,'auth','0012_alter_user_first_name_max_length','2025-12-17 00:05:55.194328'),(15,'Payment_Scheduler','0001_initial','2025-12-17 00:05:55.586414'),(16,'admin','0001_initial','2025-12-17 00:05:55.735124'),(17,'admin','0002_logentry_remove_auto_add','2025-12-17 00:05:55.742053'),(18,'admin','0003_logentry_add_action_flag_choices','2025-12-17 00:05:55.749276'),(19,'sessions','0001_initial','2025-12-17 00:05:55.785209'),(20,'Payment_Scheduler','0002_payment_amount_received_payment_change_amount_and_more','2025-12-17 00:48:19.712794'),(21,'Payment_Scheduler','0003_room_alter_customer_room_no_customer_room','2025-12-17 01:17:01.275132'),(22,'Payment_Scheduler','0004_customer_due_date','2025-12-17 04:14:38.254297'),(23,'Payment_Scheduler','0005_room_capacity_alter_room_room_type','2025-12-17 06:24:19.073319'),(24,'Payment_Scheduler','0006_room_date_left_alter_room_date_created','2025-12-17 07:36:22.775950'),(25,'Payment_Scheduler','0007_customer_date_left','2025-12-17 07:41:14.486706'),(26,'Payment_Scheduler','0008_remove_customer_room_no_alter_customer_customer_type_and_more','2025-12-17 08:18:31.798675'),(27,'Payment_Scheduler','0009_alter_boardinghouseuser_id_alter_payment_id_and_more','2025-12-17 23:31:45.769000'),(28,'Payment_Scheduler','0010_customer_date_entry_alter_boardinghouseuser_id_and_more','2025-12-18 00:47:28.868822'),(29,'Payment_Scheduler','0011_alter_customer_date_entry','2025-12-18 00:48:08.368580'),(30,'RDRealty_App','0001_initial','2025-12-25 23:23:44.939309'),(31,'RDRealty_App','0002_alter_property_id','2025-12-25 23:23:44.948695'),(32,'RDRealty_App','0003_titlemovement_propertytax','2025-12-25 23:23:44.950812'),(33,'RDRealty_App','0004_rename_property_propertytax_associated_property_and_more','2025-12-25 23:23:44.953290'),(34,'RDRealty_App','0005_remove_titlemovement_property_delete_propertytax_and_more','2025-12-25 23:23:44.955394'),(35,'RDRealty_App','0006_usermanagement','2025-12-25 23:23:44.957582'),(36,'RDRealty_App','0007_property_property_id_property_user_id_and_more','2025-12-25 23:23:44.959666'),(37,'RDRealty_App','0008_alter_property_title_classification_and_more','2025-12-25 23:23:44.961645'),(38,'RDRealty_App','0009_rename_ownerinformation_localinformation_and_more','2025-12-25 23:23:44.964565'),(39,'RDRealty_App','0010_ownerinformation','2025-12-25 23:23:44.966781'),(40,'RDRealty_App','0011_financialinformation','2025-12-25 23:23:44.968704'),(41,'RDRealty_App','0012_additionalinformation_supportingdocument','2025-12-25 23:23:44.971004'),(42,'RDRealty_App','0013_alter_supportingdocument_file_userprofile','2025-12-25 23:23:44.974604'),(43,'RDRealty_App','0014_notification','2025-12-25 23:23:44.976559'),(44,'RDRealty_App','0015_alter_localinformation_loc_barangay_and_more','2025-12-25 23:23:54.004437'),(45,'RDRealty_App','0016_propertytax','2025-12-29 00:49:29.944474'),(46,'RDRealty_App','0017_alter_property_options_alter_notification_category_and_more','2026-01-02 06:07:10.306752'),(47,'RDRealty_App','0018_alter_airequestlog_options_titlemovement','2026-01-03 00:16:21.000188'),(48,'RDRealty_App','0019_titlemovement_user_alter_titlemovement_movement_type','2026-01-03 00:21:25.775317'),(49,'RDRealty_App','0020_titlemovementrequest_titlemovementdocument','2026-01-03 00:59:18.733512'),(50,'RDRealty_App','0018_alter_airequestlog_options_titlemovementrequest','2026-01-03 08:47:30.160894'),(51,'RDRealty_App','0019_titlemovementdocument','2026-01-03 09:05:18.973745'),(52,'RDRealty_App','0020_titlemovementrequest_returned_at_and_more','2026-01-03 09:10:13.190375'),(53,'RDRealty_App','0021_notification_is_read_and_more','2026-01-03 09:52:34.200882'),(54,'RDRealty_App','0022_propertytax_created_at_propertytax_created_by','2026-01-03 14:25:52.949387'),(55,'RDRealty_App','0023_titlemovementrequest_tm_received_by_on_return_and_more','2026-01-03 14:35:17.349550'),(56,'RDRealty_App','0024_alter_titlemovementrequest_status','2026-01-03 14:40:51.944717'),(57,'RDRealty_App','0025_alter_titlemovementrequest_status','2026-01-03 14:46:28.328978'),(58,'RDRealty_App','0026_notification_user_alter_notification_category','2026-01-03 16:03:34.440288'),(59,'RDRealty_App','0027_notification_read_by','2026-01-03 16:03:57.239402'),(60,'RDRealty_App','0028_propertyhistory','2026-01-04 00:30:30.370378'),(61,'RDRealty_App','0029_alter_propertyhistory_change_type','2026-01-04 00:41:42.504316');
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
INSERT INTO `django_session` VALUES ('0newq0aou94c5cywtggvzr9q6qxx0mv2','.eJxVjEEOwiAQAP_C2RBgoVSP3vsGArusVA1NSnsy_l1JetDrzGReIsR9K2FveQ0ziYvQ4vTLUsRHrl3QPdbbInGp2zon2RN52CanhfLzerR_gxJb6VsD4ABxMMqp5HxidKMlk9giMQGCzZ6I-By1ouysMl-RvCbggUcS7w_q2Diy:1vbapS:nbVDrbvOHntDq8pxgC0KUG64qjMmns7HBo1QvvcytUM','2026-01-16 08:48:14.372102'),('0odmnq1uiw6oyzi15n7rlln4xztagf9z','.eJxVjEEOwiAQRe_C2hBA2gGX7nsGwjCDVA0kpV0Z765NutDtf-_9lwhxW0vYOi9hJnERRpx-N4zpwXUHdI_11mRqdV1mlLsiD9rl1Iif18P9Oyixl2-tHI6Ovcp0VpQdWm2Nd4NXQBa9YRXJkoGUNEYwNsPogcAhe80DGyveH9nwN7k:1vW2LD:NAWKQ0_i4SizDpvW__6ANZayuNcl2HBe30lam71iJSU','2026-01-01 00:58:03.155832'),('5s81bcrn3heqhwjlolugoss36y93i2jo','.eJxVjEEOwiAQRe_C2hAQOjou3fcMZIAZqRpISrsy3l2bdKHb_977LxVoXUpYO89hyuqirDr8bpHSg-sG8p3qrenU6jJPUW-K3mnXY8v8vO7u30GhXr61WCZCQ8k4RPFOXIro2Z8tpmOELB5gQIpAETOwGPKQhE8OxLAMot4fAyE5BA:1vXy1o:92JGBaTjDTFKVd-eAbxvvnjIqa8kkSaC4rLaYmunHeI','2026-01-06 08:46:00.235523'),('d2vyc3ntjrhq69jdmtu5s3ojfimt8m38','.eJxVjEEOwiAQAP_C2RBgoVSP3vsGArusVA1NSnsy_l1JetDrzGReIsR9K2FveQ0ziYvQ4vTLUsRHrl3QPdbbInGp2zon2RN52CanhfLzerR_gxJb6VsD4ABxMMqp5HxidKMlk9giMQGCzZ6I-By1ouysMl-RvCbggUcS7w_q2Diy:1vcCGc:AqK2mGwpTvz1_MKy4NqB30zj1sFTCvmGq9w3PSEy0xw','2026-01-18 00:46:46.721822'),('f51ccks8f78o6g44m4pv1yrwc1m64gwf','.eJxVjMsKwjAQAP9lzxLybuzRe78hbLobU5UEmvYk_rsUetDrzDBviLhvJe6d17gQjGDh8ssSzk-uh6AH1nsTc6vbuiRxJOK0XUyN-HU7279BwV5ghGA1WyMRFWYr2RvtrhoTJ3aeSTMapXwmNQzeWoWZjPNSeQ6OdCBK8PkC4ls38A:1vXjF7:DJ536494Pg7xJF5uPKuP2prst-WKrNNOANvVmaMwfZI','2026-01-05 16:58:45.341377'),('fj1hlena9uf5fensqwtxl2czk7r2hzze','.eJxVjMsOgjAUBf-la9PQSx_o0j3fQO6rFjWQUFgZ_11JWOj2zMx5mQG3tQxb1WUYxVyMM6ffjZAfOu1A7jjdZsvztC4j2V2xB622n0Wf18P9OyhYy7cm7KhlR8TC4SwJQwOtd8yQhaImBNAmZ-gEBXIUpJhYyCcFryE78_4AI485mQ:1vYQFs:zUmBwfMhP9EymExi9dLUDJ2BzZwQtbNtU7CVforEET8','2026-01-07 14:54:24.925917'),('j1nhc5z3k3kq3saldh6063vka249jvdz','.eJxVjEEOwiAQRe_C2hBpywAu3fcMZIYZpWogKe3KeHfbpAvd_vfef6uI65Lj2mSOE6uLMur0uxGmp5Qd8APLvepUyzJPpHdFH7TpsbK8rof7d5Cx5a22lCj4AMEa9r0PAt6S68PAxjhM0IEkcsHCGYUcA9kNgO_sTQaDLOrzBdEDN8I:1vYulW:fdX8CPS18k494HBBOYU1IOZTWSwp0B6-xnoOzZ18qtQ','2026-01-08 23:29:06.378581'),('naosg2lj3l0o9o3tehw5vttvu1w0bvvl','.eJxVjEEOwiAURO_C2hBKoBaX7j0DGf7_SNXQpLSrxrtrky50O--92VTEupS4NpnjyOqirDr9bgn0lLoDfqDeJ01TXeYx6V3RB236NrG8rof7d1DQyrc2bAeXbPYZhnsacJacSJjBFhnBeYD6YIS9hODgHdhz10nygQKJen8AKnc54Q:1vW1lw:oKW06MB7T8hywrm6jn7Q8j2PW2L90G0N21SKlcf-YJU','2026-01-01 00:21:36.510196'),('qovnweq6v8eg1rgjctk6ty10xu379czn','.eJxVjEEOwiAURO_C2hBKoBaX7j0DGf7_SNXQpLSrxrtrky50O--92VTEupS4NpnjyOqirDr9bgn0lLoDfqDeJ01TXeYx6V3RB236NrG8rof7d1DQyrc2bAeXbPYZhnsacJacSJjBFhnBeYD6YIS9hODgHdhz10nygQKJen8AKnc54Q:1vW10r:LzulMKFa45gbqPc6nMcUqAB7RPzI9IxkECaB3U-AsYA','2025-12-31 23:32:57.714559'),('rvwgshdx3qz8if0zstwuqygiwb7gmvtr','.eJxVjEEOwiAURO_C2hBKoBaX7j0DGf7_SNXQpLSrxrtrky50O--92VTEupS4NpnjyOqirDr9bgn0lLoDfqDeJ01TXeYx6V3RB236NrG8rof7d1DQyrc2bAeXbPYZhnsacJacSJjBFhnBeYD6YIS9hODgHdhz10nygQKJen8AKnc54Q:1vW141:cUnMaG8eC3cJNTYt1KuWD1aO2G_jqX5bdxqSBP5Os9Q','2025-12-31 23:36:13.906082'),('xq4hn8zoyynmb17l8l3xmtyf9i0spytz','.eJxVjEEOwiAQRe_C2hBmoDB16d4zEGBAqoYmpV0Z765NutDtf-_9l_BhW6vfel78xOIsQJx-txjSI7cd8D202yzT3NZlinJX5EG7vM6cn5fD_TuooddvbRAALWGkBFDQkXU2jNoWV5S2gKNSGnlANgmJAIh1ikUZPUBx6Fi8P5g7Nhs:1vZ7I0:yJf5siaiYmJOUY_bJPWDwDVNbAl0kdXnFECVtvsb2tM','2026-01-09 12:51:28.725792');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rdrealty_additional_information`
--

DROP TABLE IF EXISTS `rdrealty_additional_information`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rdrealty_additional_information` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `ai_remarks` varchar(250) DEFAULT NULL,
  `property_id` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `rdrealty_additional__property_id_86549669_fk_RDRealty_` (`property_id`),
  CONSTRAINT `rdrealty_additional__property_id_86549669_fk_RDRealty_` FOREIGN KEY (`property_id`) REFERENCES `rdrealty_app_property` (`property_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rdrealty_additional_information`
--

LOCK TABLES `rdrealty_additional_information` WRITE;
/*!40000 ALTER TABLE `rdrealty_additional_information` DISABLE KEYS */;
INSERT INTO `rdrealty_additional_information` VALUES (9,'',1);
/*!40000 ALTER TABLE `rdrealty_additional_information` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rdrealty_app_airequestlog`
--

DROP TABLE IF EXISTS `rdrealty_app_airequestlog`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rdrealty_app_airequestlog` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `timestamp` datetime(6) NOT NULL,
  `request_type` varchar(50) NOT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `RDRealty_App_airequestlog_user_id_69ac4e01_fk_auth_user_id` (`user_id`),
  KEY `RDRealty_App_airequestlog_timestamp_c909d973` (`timestamp`),
  CONSTRAINT `RDRealty_App_airequestlog_user_id_69ac4e01_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=26 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rdrealty_app_airequestlog`
--

LOCK TABLES `rdrealty_app_airequestlog` WRITE;
/*!40000 ALTER TABLE `rdrealty_app_airequestlog` DISABLE KEYS */;
INSERT INTO `rdrealty_app_airequestlog` VALUES (1,'2026-01-02 06:20:10.601945','chat',1),(2,'2026-01-02 06:25:30.107806','chat',1),(3,'2026-01-02 06:31:07.422152','chat',1),(4,'2026-01-02 06:32:09.449342','chat',1),(5,'2026-01-02 06:33:50.916298','chat',1),(6,'2026-01-02 06:39:46.918606','chat',1),(7,'2026-01-02 06:57:16.445822','chat',1),(8,'2026-01-02 06:57:47.317511','chat',1),(9,'2026-01-02 07:17:59.694618','chat',1),(10,'2026-01-02 07:20:16.717557','chat',1),(11,'2026-01-02 07:22:09.083706','chat',1),(12,'2026-01-02 07:34:51.997627','chat',1),(13,'2026-01-02 07:45:40.155291','chat',1),(14,'2026-01-02 07:51:29.261801','chat',1),(15,'2026-01-02 08:04:19.959946','chat',1),(24,'2026-01-03 06:29:02.893955','chat',1);
/*!40000 ALTER TABLE `rdrealty_app_airequestlog` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rdrealty_app_notification`
--

DROP TABLE IF EXISTS `rdrealty_app_notification`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rdrealty_app_notification` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `category` varchar(20) NOT NULL,
  `message` varchar(255) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `RDRealty_App_notification_user_id_bf031a2e_fk_auth_user_id` (`user_id`),
  CONSTRAINT `RDRealty_App_notification_user_id_bf031a2e_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=50 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rdrealty_app_notification`
--

LOCK TABLES `rdrealty_app_notification` WRITE;
/*!40000 ALTER TABLE `rdrealty_app_notification` DISABLE KEYS */;
INSERT INTO `rdrealty_app_notification` VALUES (1,'USER','User updated: Kaito','2025-12-23 06:37:24.597166',0,NULL),(2,'PROPERTY','Property updated with Title No.: 147-2024001199','2025-12-23 08:11:47.611014',0,NULL),(3,'PROPERTY','New Property added with Title No.: 146-2025002683','2025-12-23 08:15:02.185991',0,NULL),(4,'PROPERTY','Property updated with Title No.: 148-2022000663','2025-12-23 08:31:07.355660',0,NULL),(5,'PROPERTY','Property updated with Title No.: 147-2024007272','2025-12-23 08:37:44.326172',0,NULL),(6,'PROPERTY','Property updated with Title No.: 147-2024007271','2025-12-23 08:38:14.507320',0,NULL),(7,'PROPERTY','Property updated with Title No.: 147-2024001199','2025-12-23 08:43:13.419391',0,NULL),(8,'PROPERTY','Property updated with Title No.: 146-2025002683','2025-12-24 15:01:32.316745',0,NULL),(9,'PROPERTY','Property updated with Title No.: 146-2025002683','2025-12-24 22:45:32.291182',0,NULL),(10,'PROPERTY','New document uploaded for Property: sample 1','2025-12-25 23:46:32.373230',0,NULL),(11,'PROPERTY','Property updated with Title No.: sample 1','2025-12-25 23:47:12.967964',0,NULL),(12,'PROPERTY','Property updated with Title No.: sample1','2025-12-26 02:53:04.878496',0,NULL),(13,'USER','User updated: Kaito','2025-12-26 03:07:54.675350',0,NULL),(14,'TAX','Tax Record updated for Property: TEST-NOTIF-001','2025-12-29 02:31:17.967447',0,NULL),(15,'TAX','New Tax Record added for Property: 147-2024001199','2025-12-29 10:23:13.717581',0,NULL),(16,'PROPERTY','Property updated with Title No.: 147-2024001199','2025-12-29 10:28:53.828172',0,NULL),(17,'TAX','New Tax Record added for Property: iweuw8','2025-12-30 03:02:25.921347',0,NULL),(18,'PROPERTY','New document uploaded for Property: iweuw8','2025-12-30 03:10:36.484309',0,NULL),(19,'TAX','New Tax Record added for Property: 146-2025002683','2026-01-02 04:15:09.820034',0,NULL),(20,'PROPERTY','Title Movement Requested for 147-2024007271 (TM: TM-26-0001)','2026-01-03 01:21:24.972334',0,NULL),(21,'PROPERTY','Title Movement Requested for Property: 147-2024007271','2026-01-03 09:07:34.689498',0,NULL),(22,'PROPERTY','Title Movement Status Updated: TM-26-00001 -> Received','2026-01-03 10:40:56.280500',0,NULL),(23,'PROPERTY','Title Movement Status Updated: TM-26-00001 -> Returned','2026-01-03 10:41:16.111970',1,NULL),(24,'PROPERTY','Title Movement Status Updated: TM-26-00001 -> In Transit','2026-01-03 10:41:28.236735',1,NULL),(25,'PROPERTY','Title Movement Status Updated: TM-26-00001 -> Lost','2026-01-03 14:42:56.349879',1,NULL),(26,'PROPERTY','Title Movement Status Updated: TM-26-00001 -> Released','2026-01-03 14:43:41.284264',1,NULL),(27,'PROPERTY','Title Movement Status Updated: TM-26-00001 -> In Transit','2026-01-03 14:43:58.218641',1,NULL),(28,'PROPERTY','Title Movement Status Updated: TM-26-00001 -> Received','2026-01-03 14:44:39.878773',1,NULL),(29,'PROPERTY','Title Movement Status Updated: TM-26-00001 -> Pending Return','2026-01-03 14:48:11.327407',1,NULL),(30,'PROPERTY','Title Movement Status Updated: TM-26-00001 -> Released','2026-01-03 14:57:58.141239',1,NULL),(31,'MOVEMENT','Title Movement Status Updated: TM-26-00001 -> In Transit','2026-01-03 15:44:16.713260',1,NULL),(32,'PROPERTY','Property updated: TEST-NOTIF-001','2026-01-03 15:52:27.572256',1,NULL),(33,'PROPERTY','Property updated: TEST-NOTIF-001','2026-01-04 00:03:59.178543',0,1),(34,'PROPERTY','Property deleted: TEST-NOTIF-001','2026-01-04 00:23:30.423959',0,1),(35,'PROPERTY','Property deleted: 146-2025002683','2026-01-04 00:23:32.873372',0,1),(36,'PROPERTY','Property deleted: 147-2024001199','2026-01-04 00:23:34.935234',0,1),(37,'PROPERTY','Property deleted: 148-2022000663','2026-01-04 00:23:36.951618',0,1),(38,'PROPERTY','Property deleted: iweuw8','2026-01-04 00:23:39.062500',0,1),(39,'PROPERTY','Property deleted: sample1','2026-01-04 00:23:44.296972',0,1),(40,'MOVEMENT','Title Movement deleted: TM-26-00001','2026-01-04 00:24:00.180371',0,1),(41,'PROPERTY','Property deleted: 147-2024007271','2026-01-04 00:24:42.531537',0,1),(42,'PROPERTY','New property added: 147-2024001199','2026-01-04 00:35:28.618885',0,1),(43,'TAX','New tax record added for Property: 147-2024001199','2026-01-04 00:38:40.891946',0,1),(44,'MOVEMENT','Title Movement Requested for Property: 147-2024001199','2026-01-04 00:39:07.882407',0,1),(45,'PROPERTY','Property deleted: 147-2024001199','2026-01-04 00:47:00.284638',0,1),(46,'PROPERTY','New property added: 146-2025002683','2026-01-04 00:47:51.941006',0,1),(47,'TAX','New tax record added for Property: 146-2025002683','2026-01-04 00:48:50.476803',0,1),(48,'MOVEMENT','Title Movement Requested for Property: 146-2025002683','2026-01-04 00:49:08.018645',0,1),(49,'PROPERTY','Property updated: 146-2025002683','2026-01-04 00:49:39.095682',0,1);
/*!40000 ALTER TABLE `rdrealty_app_notification` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rdrealty_app_notification_read_by`
--

DROP TABLE IF EXISTS `rdrealty_app_notification_read_by`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rdrealty_app_notification_read_by` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `notification_id` bigint NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `RDRealty_App_notificatio_notification_id_user_id_ea245b4b_uniq` (`notification_id`,`user_id`),
  KEY `RDRealty_App_notific_user_id_a8cee9dc_fk_auth_user` (`user_id`),
  CONSTRAINT `RDRealty_App_notific_notification_id_99f542b4_fk_RDRealty_` FOREIGN KEY (`notification_id`) REFERENCES `rdrealty_app_notification` (`id`),
  CONSTRAINT `RDRealty_App_notific_user_id_a8cee9dc_fk_auth_user` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=70 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rdrealty_app_notification_read_by`
--

LOCK TABLES `rdrealty_app_notification_read_by` WRITE;
/*!40000 ALTER TABLE `rdrealty_app_notification_read_by` DISABLE KEYS */;
INSERT INTO `rdrealty_app_notification_read_by` VALUES (52,1,1),(51,2,1),(50,3,1),(49,4,1),(48,5,1),(47,6,1),(46,7,1),(45,8,1),(44,9,1),(43,10,1),(42,11,1),(41,12,1),(20,13,1),(19,14,1),(18,15,1),(17,16,1),(16,17,1),(15,18,1),(14,19,1),(13,20,1),(12,21,1),(11,22,1),(10,23,1),(9,24,1),(8,25,1),(7,26,1),(6,27,1),(5,28,1),(4,29,1),(3,30,1),(2,31,1),(1,32,1),(60,33,1),(59,34,1),(58,35,1),(57,36,1),(56,37,1),(55,38,1),(54,39,1),(53,40,1),(66,41,1),(65,42,1),(64,43,1),(63,44,1),(62,45,1),(61,46,1),(69,47,1),(68,48,1),(67,49,1);
/*!40000 ALTER TABLE `rdrealty_app_notification_read_by` ENABLE KEYS */;
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
  KEY `RDRealty_App_property_date_added_987f667a` (`date_added`),
  KEY `RDRealty_App_property_title_classification_7fa2c915` (`title_classification`),
  KEY `RDRealty_App_property_title_status_1b8decfa` (`title_status`),
  CONSTRAINT `rdrealty_app_property_chk_1` CHECK ((`property_id` >= 0)),
  CONSTRAINT `rdrealty_app_property_chk_2` CHECK ((`user_id` >= 0))
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rdrealty_app_property`
--

LOCK TABLES `rdrealty_app_property` WRITE;
/*!40000 ALTER TABLE `rdrealty_app_property` DISABLE KEYS */;
INSERT INTO `rdrealty_app_property` VALUES (9,'146-2025002683','Lot 34, Block 85, Unknown Street, PNG',3200.00,'AGR','UND','For Leasing','2026-01-04 00:47:51.884702',1,1);
/*!40000 ALTER TABLE `rdrealty_app_property` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rdrealty_app_userprofile`
--

DROP TABLE IF EXISTS `rdrealty_app_userprofile`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rdrealty_app_userprofile` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `full_name` varchar(255) NOT NULL,
  `date_created` datetime(6) NOT NULL,
  `date_updated` datetime(6) NOT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`),
  CONSTRAINT `RDRealty_App_userprofile_user_id_bbb71362_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rdrealty_app_userprofile`
--

LOCK TABLES `rdrealty_app_userprofile` WRITE;
/*!40000 ALTER TABLE `rdrealty_app_userprofile` DISABLE KEYS */;
INSERT INTO `rdrealty_app_userprofile` VALUES (1,'System Administrator','2025-12-23 06:10:51.772079','2025-12-23 06:11:03.117155',1),(2,'Mr. Xavier','2025-12-23 06:11:05.890622','2025-12-26 03:07:54.670838',4),(3,'Default User','2025-12-23 06:11:12.780541','2025-12-23 06:11:18.152321',2);
/*!40000 ALTER TABLE `rdrealty_app_userprofile` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rdrealty_financial_information`
--

LOCK TABLES `rdrealty_financial_information` WRITE;
/*!40000 ALTER TABLE `rdrealty_financial_information` DISABLE KEYS */;
INSERT INTO `rdrealty_financial_information` VALUES (9,'','','',1);
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
  KEY `rdrealty_local_information_loc_barangay_c7469db7` (`loc_barangay`),
  KEY `rdrealty_local_information_loc_city_9a225bd3` (`loc_city`),
  KEY `rdrealty_local_information_loc_province_9f3ff2a5` (`loc_province`),
  KEY `rdrealty_lo_loc_pro_7a2575_idx` (`loc_province`,`loc_city`,`loc_barangay`),
  CONSTRAINT `rdrealty_owner_infor_property_id_d238428c_fk_RDRealty_` FOREIGN KEY (`property_id`) REFERENCES `rdrealty_app_property` (`property_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rdrealty_local_information`
--

LOCK TABLES `rdrealty_local_information` WRITE;
/*!40000 ALTER TABLE `rdrealty_local_information` DISABLE KEYS */;
INSERT INTO `rdrealty_local_information` VALUES (9,'','Biliran','Culaba','Patag',1);
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
  PRIMARY KEY (`id`),
  KEY `rdrealty_owner_information_oi_fullname_01bc64dc` (`oi_fullname`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rdrealty_owner_information`
--

LOCK TABLES `rdrealty_owner_information` WRITE;
/*!40000 ALTER TABLE `rdrealty_owner_information` DISABLE KEYS */;
INSERT INTO `rdrealty_owner_information` VALUES (9,'Gensan Shipyard and Machine Works, Inc.','PSBank','James',1);
/*!40000 ALTER TABLE `rdrealty_owner_information` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rdrealty_property_history`
--

DROP TABLE IF EXISTS `rdrealty_property_history`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rdrealty_property_history` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `field_name` varchar(100) NOT NULL,
  `old_value` longtext,
  `new_value` longtext,
  `change_type` varchar(20) NOT NULL,
  `reason` longtext,
  `changed_at` datetime(6) NOT NULL,
  `changed_by_id` int DEFAULT NULL,
  `property_id` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `rdrealty_property_history_changed_by_id_3a7fdf05_fk_auth_user_id` (`changed_by_id`),
  KEY `rdrealty_property_hi_property_id_75da5361_fk_RDRealty_` (`property_id`),
  CONSTRAINT `rdrealty_property_hi_property_id_75da5361_fk_RDRealty_` FOREIGN KEY (`property_id`) REFERENCES `rdrealty_app_property` (`property_id`),
  CONSTRAINT `rdrealty_property_history_changed_by_id_3a7fdf05_fk_auth_user_id` FOREIGN KEY (`changed_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rdrealty_property_history`
--

LOCK TABLES `rdrealty_property_history` WRITE;
/*!40000 ALTER TABLE `rdrealty_property_history` DISABLE KEYS */;
INSERT INTO `rdrealty_property_history` VALUES (7,'Title No','','146-2025002683','ADD','Initial creation','2026-01-04 00:47:51.895904',1,1),(8,'Lot No','','Lot 34, Block 85, Unknown Street, PNG','ADD','Initial creation','2026-01-04 00:47:51.899159',1,1),(9,'Lot Area','','3200','ADD','Initial creation','2026-01-04 00:47:51.901638',1,1),(10,'Title Classification','','AGRICULTURAL','ADD','Initial creation','2026-01-04 00:47:51.904029',1,1),(11,'Title Status','','UNDER DEVELOPMENT','ADD','Initial creation','2026-01-04 00:47:51.905746',1,1),(12,'Province','','Biliran','ADD','Initial creation','2026-01-04 00:47:51.909712',1,1),(13,'City','','Culaba','ADD','Initial creation','2026-01-04 00:47:51.911321',1,1),(14,'Barangay','','Patag','ADD','Initial creation','2026-01-04 00:47:51.913126',1,1),(15,'Owner Full Name','','Gensan Shipyard and Machine Works, Inc.','ADD','Initial creation','2026-01-04 00:47:51.921972',1,1),(16,'Bank Name','','PSBank','ADD','Initial creation','2026-01-04 00:47:51.923664',1,1),(17,'Custody Of Title','','James','ADD','Initial creation','2026-01-04 00:47:51.925242',1,1),(18,'Tax Record','','Year: 2026, Quarter: Annual, Amount: 120000','ADD','Added tax record for 2026 Annual','2026-01-04 00:48:50.474380',1,1),(19,'Title Movement','','Purpose: Property Lease, Transmittal No: TM-26-00001, Received By: Bryant Christopher','ADD','Requested title movement','2026-01-04 00:49:08.016613',1,1),(20,'Title Description','','For Leasing','UPDATE',NULL,'2026-01-04 00:49:39.086968',1,1);
/*!40000 ALTER TABLE `rdrealty_property_history` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rdrealty_supporting_documents`
--

DROP TABLE IF EXISTS `rdrealty_supporting_documents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rdrealty_supporting_documents` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `file` varchar(100) NOT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `property_id` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `rdrealty_supporting__property_id_b3ca4b04_fk_RDRealty_` (`property_id`),
  CONSTRAINT `rdrealty_supporting__property_id_b3ca4b04_fk_RDRealty_` FOREIGN KEY (`property_id`) REFERENCES `rdrealty_app_property` (`property_id`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rdrealty_supporting_documents`
--

LOCK TABLES `rdrealty_supporting_documents` WRITE;
/*!40000 ALTER TABLE `rdrealty_supporting_documents` DISABLE KEYS */;
/*!40000 ALTER TABLE `rdrealty_supporting_documents` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rdrealty_tax_record`
--

DROP TABLE IF EXISTS `rdrealty_tax_record`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rdrealty_tax_record` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tax_year` int NOT NULL,
  `tax_quarter` varchar(20) NOT NULL,
  `tax_amount` decimal(12,2) NOT NULL,
  `tax_due_date` date NOT NULL,
  `tax_from` date NOT NULL,
  `tax_to` date NOT NULL,
  `tax_status` varchar(20) NOT NULL,
  `tax_remarks` varchar(200) DEFAULT NULL,
  `property_id` int unsigned NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `created_by_id` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `rdrealty_tax_record_property_id_2625776c_fk_RDRealty_` (`property_id`),
  KEY `rdrealty_tax_record_created_by_id_ca49c8ff_fk_auth_user_id` (`created_by_id`),
  CONSTRAINT `rdrealty_tax_record_created_by_id_ca49c8ff_fk_auth_user_id` FOREIGN KEY (`created_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `rdrealty_tax_record_property_id_2625776c_fk_RDRealty_` FOREIGN KEY (`property_id`) REFERENCES `rdrealty_app_property` (`property_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rdrealty_tax_record`
--

LOCK TABLES `rdrealty_tax_record` WRITE;
/*!40000 ALTER TABLE `rdrealty_tax_record` DISABLE KEYS */;
INSERT INTO `rdrealty_tax_record` VALUES (9,2026,'Annual',120000.00,'2026-01-04','2026-01-04','2027-01-04','Pending','',1,'2026-01-04 00:48:50.470386',1);
/*!40000 ALTER TABLE `rdrealty_tax_record` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rdrealty_title_mov_docs`
--

DROP TABLE IF EXISTS `rdrealty_title_mov_docs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rdrealty_title_mov_docs` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `file` varchar(100) NOT NULL,
  `uploaded_at` datetime(6) NOT NULL,
  `movement_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `rdrealty_title_mov_d_movement_id_f36f4b1b_fk_rdrealty_` (`movement_id`),
  CONSTRAINT `rdrealty_title_mov_d_movement_id_f36f4b1b_fk_rdrealty_` FOREIGN KEY (`movement_id`) REFERENCES `rdrealty_title_mov_request` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rdrealty_title_mov_docs`
--

LOCK TABLES `rdrealty_title_mov_docs` WRITE;
/*!40000 ALTER TABLE `rdrealty_title_mov_docs` DISABLE KEYS */;
/*!40000 ALTER TABLE `rdrealty_title_mov_docs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `rdrealty_title_mov_request`
--

DROP TABLE IF EXISTS `rdrealty_title_mov_request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `rdrealty_title_mov_request` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `tm_purpose` varchar(200) NOT NULL,
  `tm_transmittal_no` varchar(20) NOT NULL,
  `tm_received_by` varchar(60) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `property_id` int unsigned NOT NULL,
  `tm_approved_by_id` int DEFAULT NULL,
  `tm_released_by_id` int DEFAULT NULL,
  `returned_at` datetime(6) DEFAULT NULL,
  `status` varchar(20) NOT NULL,
  `tm_turned_over_by` varchar(60) DEFAULT NULL,
  `tm_received_by_on_return` varchar(60) DEFAULT NULL,
  `tm_returned_by` varchar(60) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `rdrealty_title_mov_r_property_id_6556bfbf_fk_RDRealty_` (`property_id`),
  KEY `rdrealty_title_mov_r_tm_approved_by_id_7d6708c2_fk_auth_user` (`tm_approved_by_id`),
  KEY `rdrealty_title_mov_r_tm_released_by_id_42a67744_fk_auth_user` (`tm_released_by_id`),
  CONSTRAINT `rdrealty_title_mov_r_property_id_6556bfbf_fk_RDRealty_` FOREIGN KEY (`property_id`) REFERENCES `rdrealty_app_property` (`property_id`),
  CONSTRAINT `rdrealty_title_mov_r_tm_approved_by_id_7d6708c2_fk_auth_user` FOREIGN KEY (`tm_approved_by_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `rdrealty_title_mov_r_tm_released_by_id_42a67744_fk_auth_user` FOREIGN KEY (`tm_released_by_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rdrealty_title_mov_request`
--

LOCK TABLES `rdrealty_title_mov_request` WRITE;
/*!40000 ALTER TABLE `rdrealty_title_mov_request` DISABLE KEYS */;
INSERT INTO `rdrealty_title_mov_request` VALUES (3,'Property Lease','TM-26-00001','Bryant Christopher','2026-01-04 00:49:08.013168',1,1,1,NULL,'Released',NULL,NULL,NULL);
/*!40000 ALTER TABLE `rdrealty_title_mov_request` ENABLE KEYS */;
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

-- Dump completed on 2026-01-04  8:52:02
