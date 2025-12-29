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
) ENGINE=InnoDB AUTO_INCREMENT=77 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',3,'add_permission'),(6,'Can change permission',3,'change_permission'),(7,'Can delete permission',3,'delete_permission'),(8,'Can view permission',3,'view_permission'),(9,'Can add group',2,'add_group'),(10,'Can change group',2,'change_group'),(11,'Can delete group',2,'delete_group'),(12,'Can view group',2,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add customer',7,'add_customer'),(22,'Can change customer',7,'change_customer'),(23,'Can delete customer',7,'delete_customer'),(24,'Can view customer',7,'view_customer'),(25,'Can add payment',8,'add_payment'),(26,'Can change payment',8,'change_payment'),(27,'Can delete payment',8,'delete_payment'),(28,'Can view payment',8,'view_payment'),(29,'Can add user',6,'add_boardinghouseuser'),(30,'Can change user',6,'change_boardinghouseuser'),(31,'Can delete user',6,'delete_boardinghouseuser'),(32,'Can view user',6,'view_boardinghouseuser'),(33,'Can add room',9,'add_room'),(34,'Can change room',9,'change_room'),(35,'Can delete room',9,'delete_room'),(36,'Can view room',9,'view_room'),(37,'Can add user',10,'add_user'),(38,'Can change user',10,'change_user'),(39,'Can delete user',10,'delete_user'),(40,'Can view user',10,'view_user'),(41,'Can add Property',16,'add_property'),(42,'Can change Property',16,'change_property'),(43,'Can delete Property',16,'delete_property'),(44,'Can view Property',16,'view_property'),(45,'Can add local information',13,'add_localinformation'),(46,'Can change local information',13,'change_localinformation'),(47,'Can delete local information',13,'delete_localinformation'),(48,'Can view local information',13,'view_localinformation'),(49,'Can add owner information',15,'add_ownerinformation'),(50,'Can change owner information',15,'change_ownerinformation'),(51,'Can delete owner information',15,'delete_ownerinformation'),(52,'Can view owner information',15,'view_ownerinformation'),(53,'Can add financial information',12,'add_financialinformation'),(54,'Can change financial information',12,'change_financialinformation'),(55,'Can delete financial information',12,'delete_financialinformation'),(56,'Can view financial information',12,'view_financialinformation'),(57,'Can add additional information',11,'add_additionalinformation'),(58,'Can change additional information',11,'change_additionalinformation'),(59,'Can delete additional information',11,'delete_additionalinformation'),(60,'Can view additional information',11,'view_additionalinformation'),(61,'Can add supporting document',17,'add_supportingdocument'),(62,'Can change supporting document',17,'change_supportingdocument'),(63,'Can delete supporting document',17,'delete_supportingdocument'),(64,'Can view supporting document',17,'view_supportingdocument'),(65,'Can add user profile',18,'add_userprofile'),(66,'Can change user profile',18,'change_userprofile'),(67,'Can delete user profile',18,'delete_userprofile'),(68,'Can view user profile',18,'view_userprofile'),(69,'Can add notification',14,'add_notification'),(70,'Can change notification',14,'change_notification'),(71,'Can delete notification',14,'delete_notification'),(72,'Can view notification',14,'view_notification'),(73,'Can add property tax',19,'add_propertytax'),(74,'Can change property tax',19,'change_propertytax'),(75,'Can delete property tax',19,'delete_propertytax'),(76,'Can view property tax',19,'view_propertytax');
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
INSERT INTO `auth_user` VALUES (1,'pbkdf2_sha256$1200000$jOTmT44UbOgabcOMqjI8mx$KDPOR3xEdQW9G80PyE1aA1ZI/ev05uQsuG9ivAb7v2M=','2025-12-29 02:59:50.525971',1,'admin','','','',1,1,'2025-12-15 02:40:36.038768'),(2,'pbkdf2_sha256$1000000$P23xcuyFlBqyoZk3rCIP6i$xa6Huh8q7s93+DTiRVdn4gJ2ViMtrBi5hZchAq9GRQY=','2025-12-26 03:07:23.359005',0,'user','','','',0,1,'2025-12-15 03:16:15.129340'),(4,'pbkdf2_sha256$1000000$of87PW5z8axX1VjbOqbYde$6RX1YEfkyNNSjNZBw6CHmpYzIAGUPYkVu3a4fOxM03s=','2025-12-26 03:21:48.369063',1,'Kaito','','','',1,1,'2025-12-15 06:24:39.087143'),(5,'pbkdf2_sha256$1200000$7YD6N8bcq1qaxb840YE6zS$C/rVGOvSqvg+zz6FZRI/sjZmLw7eSbflXFwk2X8cyJs=',NULL,0,'test_admin_notif','','','test@example.com',1,1,'2025-12-29 02:31:16.902191');
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
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(2,'auth','group'),(3,'auth','permission'),(10,'auth','user'),(4,'contenttypes','contenttype'),(6,'Payment_Scheduler','boardinghouseuser'),(7,'Payment_Scheduler','customer'),(8,'Payment_Scheduler','payment'),(9,'Payment_Scheduler','room'),(11,'RDRealty_App','additionalinformation'),(12,'RDRealty_App','financialinformation'),(13,'RDRealty_App','localinformation'),(14,'RDRealty_App','notification'),(15,'RDRealty_App','ownerinformation'),(16,'RDRealty_App','property'),(19,'RDRealty_App','propertytax'),(17,'RDRealty_App','supportingdocument'),(18,'RDRealty_App','userprofile'),(5,'sessions','session');
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
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-12-17 00:05:54.697952'),(2,'contenttypes','0002_remove_content_type_name','2025-12-17 00:05:54.801451'),(3,'auth','0001_initial','2025-12-17 00:05:55.063728'),(4,'auth','0002_alter_permission_name_max_length','2025-12-17 00:05:55.120307'),(5,'auth','0003_alter_user_email_max_length','2025-12-17 00:05:55.127457'),(6,'auth','0004_alter_user_username_opts','2025-12-17 00:05:55.133637'),(7,'auth','0005_alter_user_last_login_null','2025-12-17 00:05:55.141776'),(8,'auth','0006_require_contenttypes_0002','2025-12-17 00:05:55.144256'),(9,'auth','0007_alter_validators_add_error_messages','2025-12-17 00:05:55.150922'),(10,'auth','0008_alter_user_username_max_length','2025-12-17 00:05:55.158366'),(11,'auth','0009_alter_user_last_name_max_length','2025-12-17 00:05:55.163713'),(12,'auth','0010_alter_group_name_max_length','2025-12-17 00:05:55.180295'),(13,'auth','0011_update_proxy_permissions','2025-12-17 00:05:55.188229'),(14,'auth','0012_alter_user_first_name_max_length','2025-12-17 00:05:55.194328'),(15,'Payment_Scheduler','0001_initial','2025-12-17 00:05:55.586414'),(16,'admin','0001_initial','2025-12-17 00:05:55.735124'),(17,'admin','0002_logentry_remove_auto_add','2025-12-17 00:05:55.742053'),(18,'admin','0003_logentry_add_action_flag_choices','2025-12-17 00:05:55.749276'),(19,'sessions','0001_initial','2025-12-17 00:05:55.785209'),(20,'Payment_Scheduler','0002_payment_amount_received_payment_change_amount_and_more','2025-12-17 00:48:19.712794'),(21,'Payment_Scheduler','0003_room_alter_customer_room_no_customer_room','2025-12-17 01:17:01.275132'),(22,'Payment_Scheduler','0004_customer_due_date','2025-12-17 04:14:38.254297'),(23,'Payment_Scheduler','0005_room_capacity_alter_room_room_type','2025-12-17 06:24:19.073319'),(24,'Payment_Scheduler','0006_room_date_left_alter_room_date_created','2025-12-17 07:36:22.775950'),(25,'Payment_Scheduler','0007_customer_date_left','2025-12-17 07:41:14.486706'),(26,'Payment_Scheduler','0008_remove_customer_room_no_alter_customer_customer_type_and_more','2025-12-17 08:18:31.798675'),(27,'Payment_Scheduler','0009_alter_boardinghouseuser_id_alter_payment_id_and_more','2025-12-17 23:31:45.769000'),(28,'Payment_Scheduler','0010_customer_date_entry_alter_boardinghouseuser_id_and_more','2025-12-18 00:47:28.868822'),(29,'Payment_Scheduler','0011_alter_customer_date_entry','2025-12-18 00:48:08.368580'),(30,'RDRealty_App','0001_initial','2025-12-25 23:23:44.939309'),(31,'RDRealty_App','0002_alter_property_id','2025-12-25 23:23:44.948695'),(32,'RDRealty_App','0003_titlemovement_propertytax','2025-12-25 23:23:44.950812'),(33,'RDRealty_App','0004_rename_property_propertytax_associated_property_and_more','2025-12-25 23:23:44.953290'),(34,'RDRealty_App','0005_remove_titlemovement_property_delete_propertytax_and_more','2025-12-25 23:23:44.955394'),(35,'RDRealty_App','0006_usermanagement','2025-12-25 23:23:44.957582'),(36,'RDRealty_App','0007_property_property_id_property_user_id_and_more','2025-12-25 23:23:44.959666'),(37,'RDRealty_App','0008_alter_property_title_classification_and_more','2025-12-25 23:23:44.961645'),(38,'RDRealty_App','0009_rename_ownerinformation_localinformation_and_more','2025-12-25 23:23:44.964565'),(39,'RDRealty_App','0010_ownerinformation','2025-12-25 23:23:44.966781'),(40,'RDRealty_App','0011_financialinformation','2025-12-25 23:23:44.968704'),(41,'RDRealty_App','0012_additionalinformation_supportingdocument','2025-12-25 23:23:44.971004'),(42,'RDRealty_App','0013_alter_supportingdocument_file_userprofile','2025-12-25 23:23:44.974604'),(43,'RDRealty_App','0014_notification','2025-12-25 23:23:44.976559'),(44,'RDRealty_App','0015_alter_localinformation_loc_barangay_and_more','2025-12-25 23:23:54.004437'),(45,'RDRealty_App','0016_propertytax','2025-12-29 00:49:29.944474');
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
INSERT INTO `django_session` VALUES ('0odmnq1uiw6oyzi15n7rlln4xztagf9z','.eJxVjEEOwiAQRe_C2hBA2gGX7nsGwjCDVA0kpV0Z765NutDtf-_9lwhxW0vYOi9hJnERRpx-N4zpwXUHdI_11mRqdV1mlLsiD9rl1Iif18P9Oyixl2-tHI6Ovcp0VpQdWm2Nd4NXQBa9YRXJkoGUNEYwNsPogcAhe80DGyveH9nwN7k:1vW2LD:NAWKQ0_i4SizDpvW__6ANZayuNcl2HBe30lam71iJSU','2026-01-01 00:58:03.155832'),('5s81bcrn3heqhwjlolugoss36y93i2jo','.eJxVjEEOwiAQRe_C2hAQOjou3fcMZIAZqRpISrsy3l2bdKHb_977LxVoXUpYO89hyuqirDr8bpHSg-sG8p3qrenU6jJPUW-K3mnXY8v8vO7u30GhXr61WCZCQ8k4RPFOXIro2Z8tpmOELB5gQIpAETOwGPKQhE8OxLAMot4fAyE5BA:1vXy1o:92JGBaTjDTFKVd-eAbxvvnjIqa8kkSaC4rLaYmunHeI','2026-01-06 08:46:00.235523'),('775a3c0zu3krzmrz2plf53nnnhvcctj9','.eJxVjEEOwiAQRe_C2hCgMBCX7j0DGZhBqgaS0q6Md9cmXej2v_f-S0Tc1hq3wUucSZyFFqffLWF-cNsB3bHdusy9rcuc5K7Igw557cTPy-H-HVQc9VtbM1EoRgWVA2nNBMkUEzgn67W1WBgLaQAE8JZNCa44b9E7o6YE2on3B-ScN6A:1va3U6:ggtkSctSgWNKlMUHF-USUZkZVZj7ugBrojzNKQRatMo','2026-01-12 02:59:50.528733'),('f51ccks8f78o6g44m4pv1yrwc1m64gwf','.eJxVjMsKwjAQAP9lzxLybuzRe78hbLobU5UEmvYk_rsUetDrzDBviLhvJe6d17gQjGDh8ssSzk-uh6AH1nsTc6vbuiRxJOK0XUyN-HU7279BwV5ghGA1WyMRFWYr2RvtrhoTJ3aeSTMapXwmNQzeWoWZjPNSeQ6OdCBK8PkC4ls38A:1vXjF7:DJ536494Pg7xJF5uPKuP2prst-WKrNNOANvVmaMwfZI','2026-01-05 16:58:45.341377'),('fj1hlena9uf5fensqwtxl2czk7r2hzze','.eJxVjMsOgjAUBf-la9PQSx_o0j3fQO6rFjWQUFgZ_11JWOj2zMx5mQG3tQxb1WUYxVyMM6ffjZAfOu1A7jjdZsvztC4j2V2xB622n0Wf18P9OyhYy7cm7KhlR8TC4SwJQwOtd8yQhaImBNAmZ-gEBXIUpJhYyCcFryE78_4AI485mQ:1vYQFs:zUmBwfMhP9EymExi9dLUDJ2BzZwQtbNtU7CVforEET8','2026-01-07 14:54:24.925917'),('j1nhc5z3k3kq3saldh6063vka249jvdz','.eJxVjEEOwiAQRe_C2hBpywAu3fcMZIYZpWogKe3KeHfbpAvd_vfef6uI65Lj2mSOE6uLMur0uxGmp5Qd8APLvepUyzJPpHdFH7TpsbK8rof7d5Cx5a22lCj4AMEa9r0PAt6S68PAxjhM0IEkcsHCGYUcA9kNgO_sTQaDLOrzBdEDN8I:1vYulW:fdX8CPS18k494HBBOYU1IOZTWSwp0B6-xnoOzZ18qtQ','2026-01-08 23:29:06.378581'),('naosg2lj3l0o9o3tehw5vttvu1w0bvvl','.eJxVjEEOwiAURO_C2hBKoBaX7j0DGf7_SNXQpLSrxrtrky50O--92VTEupS4NpnjyOqirDr9bgn0lLoDfqDeJ01TXeYx6V3RB236NrG8rof7d1DQyrc2bAeXbPYZhnsacJacSJjBFhnBeYD6YIS9hODgHdhz10nygQKJen8AKnc54Q:1vW1lw:oKW06MB7T8hywrm6jn7Q8j2PW2L90G0N21SKlcf-YJU','2026-01-01 00:21:36.510196'),('qovnweq6v8eg1rgjctk6ty10xu379czn','.eJxVjEEOwiAURO_C2hBKoBaX7j0DGf7_SNXQpLSrxrtrky50O--92VTEupS4NpnjyOqirDr9bgn0lLoDfqDeJ01TXeYx6V3RB236NrG8rof7d1DQyrc2bAeXbPYZhnsacJacSJjBFhnBeYD6YIS9hODgHdhz10nygQKJen8AKnc54Q:1vW10r:LzulMKFa45gbqPc6nMcUqAB7RPzI9IxkECaB3U-AsYA','2025-12-31 23:32:57.714559'),('rvwgshdx3qz8if0zstwuqygiwb7gmvtr','.eJxVjEEOwiAURO_C2hBKoBaX7j0DGf7_SNXQpLSrxrtrky50O--92VTEupS4NpnjyOqirDr9bgn0lLoDfqDeJ01TXeYx6V3RB236NrG8rof7d1DQyrc2bAeXbPYZhnsacJacSJjBFhnBeYD6YIS9hODgHdhz10nygQKJen8AKnc54Q:1vW141:cUnMaG8eC3cJNTYt1KuWD1aO2G_jqX5bdxqSBP5Os9Q','2025-12-31 23:36:13.906082'),('xq4hn8zoyynmb17l8l3xmtyf9i0spytz','.eJxVjEEOwiAQRe_C2hBmoDB16d4zEGBAqoYmpV0Z765NutDtf-_9l_BhW6vfel78xOIsQJx-txjSI7cd8D202yzT3NZlinJX5EG7vM6cn5fD_TuooddvbRAALWGkBFDQkXU2jNoWV5S2gKNSGnlANgmJAIh1ikUZPUBx6Fi8P5g7Nhs:1vZ7I0:yJf5siaiYmJOUY_bJPWDwDVNbAl0kdXnFECVtvsb2tM','2026-01-09 12:51:28.725792');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment_scheduler_boardinghouseuser`
--

DROP TABLE IF EXISTS `payment_scheduler_boardinghouseuser`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment_scheduler_boardinghouseuser` (
  `id` bigint NOT NULL AUTO_INCREMENT,
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
  `role` varchar(10) NOT NULL,
  `status` varchar(10) NOT NULL,
  `date_created` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_scheduler_boardinghouseuser`
--

LOCK TABLES `payment_scheduler_boardinghouseuser` WRITE;
/*!40000 ALTER TABLE `payment_scheduler_boardinghouseuser` DISABLE KEYS */;
INSERT INTO `payment_scheduler_boardinghouseuser` VALUES (3,'pbkdf2_sha256$1200000$KHqNQNBQJvTK70EzLBkszr$KYvJpwckSNAZxrxfSMQtqVqizm2bxZjh5JK5b8sqeKA=','2025-12-22 16:32:27.090291',0,'admin','','','admin@gmail.com',0,1,'2025-12-18 01:39:35.463686','Admin','Active','2025-12-18 01:39:36.461782'),(4,'pbkdf2_sha256$1200000$WW2ZzBdYWYfmwQW2GaGyKd$8SyDuqV9SgLhKI9L41fr2HBoqVTPr9TUkMI7mlyXbBc=','2025-12-22 16:58:45.331324',0,'user','','','user@gmail.com',0,1,'2025-12-18 01:41:15.408241','User','Active','2025-12-18 01:41:16.403763');
/*!40000 ALTER TABLE `payment_scheduler_boardinghouseuser` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment_scheduler_boardinghouseuser_groups`
--

DROP TABLE IF EXISTS `payment_scheduler_boardinghouseuser_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment_scheduler_boardinghouseuser_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `boardinghouseuser_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Payment_Scheduler_boardi_boardinghouseuser_id_gro_d066a6c5_uniq` (`boardinghouseuser_id`,`group_id`),
  KEY `Payment_Scheduler_bo_group_id_6780cbc3_fk_auth_grou` (`group_id`),
  CONSTRAINT `Payment_Scheduler_bo_group_id_6780cbc3_fk_auth_grou` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `Payment_Scheduler_boardin_boardinghouseuser_id_7058dc52_fk` FOREIGN KEY (`boardinghouseuser_id`) REFERENCES `payment_scheduler_boardinghouseuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_scheduler_boardinghouseuser_groups`
--

LOCK TABLES `payment_scheduler_boardinghouseuser_groups` WRITE;
/*!40000 ALTER TABLE `payment_scheduler_boardinghouseuser_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `payment_scheduler_boardinghouseuser_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment_scheduler_boardinghouseuser_user_permissions`
--

DROP TABLE IF EXISTS `payment_scheduler_boardinghouseuser_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment_scheduler_boardinghouseuser_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `boardinghouseuser_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `Payment_Scheduler_boardi_boardinghouseuser_id_per_0e462e6d_uniq` (`boardinghouseuser_id`,`permission_id`),
  KEY `Payment_Scheduler_bo_permission_id_6e4e74dc_fk_auth_perm` (`permission_id`),
  CONSTRAINT `Payment_Scheduler_bo_permission_id_6e4e74dc_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `Payment_Scheduler_boardin_boardinghouseuser_id_084e4523_fk` FOREIGN KEY (`boardinghouseuser_id`) REFERENCES `payment_scheduler_boardinghouseuser` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_scheduler_boardinghouseuser_user_permissions`
--

LOCK TABLES `payment_scheduler_boardinghouseuser_user_permissions` WRITE;
/*!40000 ALTER TABLE `payment_scheduler_boardinghouseuser_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `payment_scheduler_boardinghouseuser_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment_scheduler_customer`
--

DROP TABLE IF EXISTS `payment_scheduler_customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment_scheduler_customer` (
  `customer_id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `address` longtext NOT NULL,
  `age` int NOT NULL,
  `gender` varchar(10) NOT NULL,
  `status` varchar(10) NOT NULL,
  `customer_type` varchar(20) NOT NULL,
  `room_id` bigint DEFAULT NULL,
  `due_date` date DEFAULT NULL,
  `date_left` date DEFAULT NULL,
  `date_entry` date DEFAULT NULL,
  PRIMARY KEY (`customer_id`),
  KEY `Payment_Scheduler_customer_room_id_02ed51c0_fk` (`room_id`),
  CONSTRAINT `Payment_Scheduler_customer_room_id_02ed51c0_fk` FOREIGN KEY (`room_id`) REFERENCES `payment_scheduler_room` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_scheduler_customer`
--

LOCK TABLES `payment_scheduler_customer` WRITE;
/*!40000 ALTER TABLE `payment_scheduler_customer` DISABLE KEYS */;
INSERT INTO `payment_scheduler_customer` VALUES (34,'JUDY ANN CARIAGA','.',20,'Female','Active','Student',NULL,'2026-01-11',NULL,'2025-03-11'),(35,'ALAYSSA A. SUBONG','.',20,'Female','Active','Student',NULL,'2026-01-13',NULL,'2025-07-13'),(36,'Jilliane Khyee C. Losala','.',20,'Female','Active','Student',NULL,'2025-12-21',NULL,'2025-07-21'),(37,'Leah Jane C. Espinosa','.',20,'Female','Active','Student',NULL,'2025-12-16',NULL,'2025-07-16'),(38,'Mira Chelsy A. Abueva','.',20,'Female','Active','Student',NULL,'2025-12-16',NULL,'2025-07-16'),(39,'Gwyneth Ann C. Brumo','.',20,'Female','Active','Student',NULL,'2025-12-20',NULL,'2025-07-20'),(40,'Ashly Caramat','Geralyn Tun-ogan\r\n09676057677',20,'Female','Active','Student',NULL,'2025-12-16',NULL,'2025-07-16'),(41,'Chrysline Mae Dargantes','------\r\n09358533472',20,'Female','Active','Student',NULL,'2025-01-17',NULL,'2025-08-16'),(42,'GENEVIEVE M. BLEL','-------\r\n09751459468',20,'Female','Active','Student',NULL,'2025-12-20',NULL,'2025-07-20'),(43,'Norhaya M. Fernandez','Kipa Fernandez\r\n09356789731',20,'Female','Active','Student',NULL,'2025-01-21',NULL,'2025-12-22'),(44,'Jaylo Joy D. Vitug','Roda Dawang\r\n09814165191',20,'Female','Active','Student',NULL,'2025-12-16',NULL,'2025-07-16'),(45,'EDRIANE DAVE E. ENOFERIO','--------\r\n09073489064',20,'Male','Active','Student',NULL,'2025-12-17',NULL,'2025-07-17'),(46,'Naila M. Gulam','Naima M. Gulam - 09484005282',20,'Female','Active','Student',NULL,'2025-12-16',NULL,'2022-08-16'),(47,'IVAN ACE T. SALINTO','JOVELYN T SALINTO \r\n09169947184',20,'Male','Active','Student',NULL,'2025-12-17',NULL,'2025-07-17'),(48,'Jaleela Esparas','Facebook acc only- Jhafz Abdin',20,'Female','Active','Student',NULL,'2026-01-16',NULL,'2025-07-16'),(49,'ARLEX E. VALDEZ','09502969637',20,'Male','Active','Student',NULL,'2025-12-17',NULL,'2025-07-17'),(50,'Alexis Zaragoza','Alexander Zaragoza - 09532052392',20,'Male','Active','Student',NULL,'2026-01-20',NULL,'2025-11-20');
/*!40000 ALTER TABLE `payment_scheduler_customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment_scheduler_payment`
--

DROP TABLE IF EXISTS `payment_scheduler_payment`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment_scheduler_payment` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `due_date` date NOT NULL,
  `previous_date` date DEFAULT NULL,
  `amount` decimal(10,2) NOT NULL,
  `remarks` varchar(255) DEFAULT NULL,
  `is_paid` tinyint(1) NOT NULL,
  `customer_id` int NOT NULL,
  `amount_received` decimal(10,2) DEFAULT NULL,
  `change_amount` decimal(10,2) DEFAULT NULL,
  `date_paid` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `Payment_Scheduler_pa_customer_id_17c23d54_fk_Payment_S` (`customer_id`),
  CONSTRAINT `Payment_Scheduler_pa_customer_id_17c23d54_fk_Payment_S` FOREIGN KEY (`customer_id`) REFERENCES `payment_scheduler_customer` (`customer_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_scheduler_payment`
--

LOCK TABLES `payment_scheduler_payment` WRITE;
/*!40000 ALTER TABLE `payment_scheduler_payment` DISABLE KEYS */;
/*!40000 ALTER TABLE `payment_scheduler_payment` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payment_scheduler_room`
--

DROP TABLE IF EXISTS `payment_scheduler_room`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payment_scheduler_room` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `room_number` varchar(50) NOT NULL,
  `date_created` date NOT NULL,
  `status` varchar(20) NOT NULL,
  `room_type` varchar(50) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `capacity` int NOT NULL,
  `date_left` date DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `room_number` (`room_number`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_scheduler_room`
--

LOCK TABLES `payment_scheduler_room` WRITE;
/*!40000 ALTER TABLE `payment_scheduler_room` DISABLE KEYS */;
/*!40000 ALTER TABLE `payment_scheduler_room` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rdrealty_additional_information`
--

LOCK TABLES `rdrealty_additional_information` WRITE;
/*!40000 ALTER TABLE `rdrealty_additional_information` DISABLE KEYS */;
INSERT INTO `rdrealty_additional_information` VALUES (1,'Sample additional Information',4),(2,'',5),(3,'',2),(4,'',3),(5,'',1),(6,'',6);
/*!40000 ALTER TABLE `rdrealty_additional_information` ENABLE KEYS */;
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
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rdrealty_app_notification`
--

LOCK TABLES `rdrealty_app_notification` WRITE;
/*!40000 ALTER TABLE `rdrealty_app_notification` DISABLE KEYS */;
INSERT INTO `rdrealty_app_notification` VALUES (1,'USER','User updated: Kaito','2025-12-23 06:37:24.597166'),(2,'PROPERTY','Property updated with Title No.: 147-2024001199','2025-12-23 08:11:47.611014'),(3,'PROPERTY','New Property added with Title No.: 146-2025002683','2025-12-23 08:15:02.185991'),(4,'PROPERTY','Property updated with Title No.: 148-2022000663','2025-12-23 08:31:07.355660'),(5,'PROPERTY','Property updated with Title No.: 147-2024007272','2025-12-23 08:37:44.326172'),(6,'PROPERTY','Property updated with Title No.: 147-2024007271','2025-12-23 08:38:14.507320'),(7,'PROPERTY','Property updated with Title No.: 147-2024001199','2025-12-23 08:43:13.419391'),(8,'PROPERTY','Property updated with Title No.: 146-2025002683','2025-12-24 15:01:32.316745'),(9,'PROPERTY','Property updated with Title No.: 146-2025002683','2025-12-24 22:45:32.291182'),(10,'PROPERTY','New document uploaded for Property: sample 1','2025-12-25 23:46:32.373230'),(11,'PROPERTY','Property updated with Title No.: sample 1','2025-12-25 23:47:12.967964'),(12,'PROPERTY','Property updated with Title No.: sample1','2025-12-26 02:53:04.878496'),(13,'USER','User updated: Kaito','2025-12-26 03:07:54.675350'),(14,'TAX','Tax Record updated for Property: TEST-NOTIF-001','2025-12-29 02:31:17.967447');
/*!40000 ALTER TABLE `rdrealty_app_notification` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rdrealty_app_property`
--

LOCK TABLES `rdrealty_app_property` WRITE;
/*!40000 ALTER TABLE `rdrealty_app_property` DISABLE KEYS */;
INSERT INTO `rdrealty_app_property` VALUES (1,'sample1','lot 1 block 2',23626.00,'RES','PENT','sample sample sample','2025-12-09 05:45:01.743044',1,1),(2,'147-2024007271','Block 15, Lot 82',1200.00,'IND','UND','Sample 2','2025-12-09 05:45:01.743044',2,1),(3,'iweuw8','Block 15, Lot 17',450.00,'AGR','SOLD','Descirption Sample Here','2025-12-09 05:56:25.734669',3,1),(4,'148-2022000663','Lot 3-B-2-B',57033.00,'IND','COL','','2025-12-15 05:18:06.165597',4,1),(5,'147-2024001199','Lot 4650',416.00,'COM','COL','','2025-12-20 02:04:40.928358',5,1),(6,'146-2025002683','Lot 35-C',342.00,'COM','COL','','2025-12-23 08:15:02.163161',6,1),(7,'TEST-NOTIF-001','LOT-001',0.00,'RES','ACT',NULL,'2025-12-29 02:31:17.953958',99999,1);
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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rdrealty_financial_information`
--

LOCK TABLES `rdrealty_financial_information` WRITE;
/*!40000 ALTER TABLE `rdrealty_financial_information` DISABLE KEYS */;
INSERT INTO `rdrealty_financial_information` VALUES (1,'','','Union Bank',4),(2,'','','',5),(3,'','','',2),(4,'','','',3),(5,'','','',1),(6,'','','Union Bank',6);
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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rdrealty_local_information`
--

LOCK TABLES `rdrealty_local_information` WRITE;
/*!40000 ALTER TABLE `rdrealty_local_information` DISABLE KEYS */;
INSERT INTO `rdrealty_local_information` VALUES (1,'Hose Banda','South Cotabato','City of General Santos','Calumpang',3),(2,'Dadiangas West, P. Acharon Blvd., General Santos City- Jo-Anns Bakeshop','South Cotabato','City of General Santos','Dadiangas West',5),(3,'','Bohol','Catigbian','Mahayag Sur',1),(4,'Bulacan Area','Bulacan','Plaridel','Rueda',2),(5,'Maasim, Sarangani Province','Sarangani','Maasim','Colon',4),(6,'Davao City','Davao Del Sur','City of Davao','Acacia',6);
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
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rdrealty_owner_information`
--

LOCK TABLES `rdrealty_owner_information` WRITE;
/*!40000 ALTER TABLE `rdrealty_owner_information` DISABLE KEYS */;
INSERT INTO `rdrealty_owner_information` VALUES (1,'Gensan Shipyard and Machine Works, Inc.','PSBank','Hashime Rodrigo',4),(2,'RD Realty Development Corporation','Metrobank','James',5),(3,'LBC','','',2),(4,'Sannovex','','',3),(5,'PhilTrust','','',1),(6,'RD Realty Development Corporation','','Hashime Rodrigo',6);
/*!40000 ALTER TABLE `rdrealty_owner_information` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rdrealty_supporting_documents`
--

LOCK TABLES `rdrealty_supporting_documents` WRITE;
/*!40000 ALTER TABLE `rdrealty_supporting_documents` DISABLE KEYS */;
INSERT INTO `rdrealty_supporting_documents` VALUES (13,'supporting_docs/1_6_20251224.jpg','2025-12-24 15:01:32.303254',6),(14,'supporting_docs/rd_fishing_logo_6_20251224.jpg','2025-12-24 15:01:32.311102',6);
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
  PRIMARY KEY (`id`),
  KEY `rdrealty_tax_record_property_id_2625776c_fk_RDRealty_` (`property_id`),
  CONSTRAINT `rdrealty_tax_record_property_id_2625776c_fk_RDRealty_` FOREIGN KEY (`property_id`) REFERENCES `rdrealty_app_property` (`property_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `rdrealty_tax_record`
--

LOCK TABLES `rdrealty_tax_record` WRITE;
/*!40000 ALTER TABLE `rdrealty_tax_record` DISABLE KEYS */;
INSERT INTO `rdrealty_tax_record` VALUES (1,2025,'Annual',25000.00,'2025-12-29','2025-12-29','2025-12-29','Pending','',1),(2,2024,'Q4',13000.00,'2025-12-31','2024-10-01','2024-10-31','Overdue','',1),(3,2025,'Q1',5000.00,'2025-12-29','2025-12-29','2025-12-29','Pending','',99999);
/*!40000 ALTER TABLE `rdrealty_tax_record` ENABLE KEYS */;
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

-- Dump completed on 2025-12-29 11:03:21
