-- MySQL dump 10.13  Distrib 8.0.44, for Win64 (x86_64)
--
-- Host: localhost    Database: paymentschedule_db
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
) ENGINE=InnoDB AUTO_INCREMENT=37 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',3,'add_permission'),(6,'Can change permission',3,'change_permission'),(7,'Can delete permission',3,'delete_permission'),(8,'Can view permission',3,'view_permission'),(9,'Can add group',2,'add_group'),(10,'Can change group',2,'change_group'),(11,'Can delete group',2,'delete_group'),(12,'Can view group',2,'view_group'),(13,'Can add content type',4,'add_contenttype'),(14,'Can change content type',4,'change_contenttype'),(15,'Can delete content type',4,'delete_contenttype'),(16,'Can view content type',4,'view_contenttype'),(17,'Can add session',5,'add_session'),(18,'Can change session',5,'change_session'),(19,'Can delete session',5,'delete_session'),(20,'Can view session',5,'view_session'),(21,'Can add customer',7,'add_customer'),(22,'Can change customer',7,'change_customer'),(23,'Can delete customer',7,'delete_customer'),(24,'Can view customer',7,'view_customer'),(25,'Can add payment',8,'add_payment'),(26,'Can change payment',8,'change_payment'),(27,'Can delete payment',8,'delete_payment'),(28,'Can view payment',8,'view_payment'),(29,'Can add user',6,'add_boardinghouseuser'),(30,'Can change user',6,'change_boardinghouseuser'),(31,'Can delete user',6,'delete_boardinghouseuser'),(32,'Can view user',6,'view_boardinghouseuser'),(33,'Can add room',9,'add_room'),(34,'Can change room',9,'change_room'),(35,'Can delete room',9,'delete_room'),(36,'Can view room',9,'view_room');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
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
  KEY `django_admin_log_user_id_c564eba6_fk_Payment_S` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_Payment_S` FOREIGN KEY (`user_id`) REFERENCES `payment_scheduler_boardinghouseuser` (`id`),
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
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(2,'auth','group'),(3,'auth','permission'),(4,'contenttypes','contenttype'),(6,'Payment_Scheduler','boardinghouseuser'),(7,'Payment_Scheduler','customer'),(8,'Payment_Scheduler','payment'),(9,'Payment_Scheduler','room'),(5,'sessions','session');
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
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2025-12-17 00:05:54.697952'),(2,'contenttypes','0002_remove_content_type_name','2025-12-17 00:05:54.801451'),(3,'auth','0001_initial','2025-12-17 00:05:55.063728'),(4,'auth','0002_alter_permission_name_max_length','2025-12-17 00:05:55.120307'),(5,'auth','0003_alter_user_email_max_length','2025-12-17 00:05:55.127457'),(6,'auth','0004_alter_user_username_opts','2025-12-17 00:05:55.133637'),(7,'auth','0005_alter_user_last_login_null','2025-12-17 00:05:55.141776'),(8,'auth','0006_require_contenttypes_0002','2025-12-17 00:05:55.144256'),(9,'auth','0007_alter_validators_add_error_messages','2025-12-17 00:05:55.150922'),(10,'auth','0008_alter_user_username_max_length','2025-12-17 00:05:55.158366'),(11,'auth','0009_alter_user_last_name_max_length','2025-12-17 00:05:55.163713'),(12,'auth','0010_alter_group_name_max_length','2025-12-17 00:05:55.180295'),(13,'auth','0011_update_proxy_permissions','2025-12-17 00:05:55.188229'),(14,'auth','0012_alter_user_first_name_max_length','2025-12-17 00:05:55.194328'),(15,'Payment_Scheduler','0001_initial','2025-12-17 00:05:55.586414'),(16,'admin','0001_initial','2025-12-17 00:05:55.735124'),(17,'admin','0002_logentry_remove_auto_add','2025-12-17 00:05:55.742053'),(18,'admin','0003_logentry_add_action_flag_choices','2025-12-17 00:05:55.749276'),(19,'sessions','0001_initial','2025-12-17 00:05:55.785209'),(20,'Payment_Scheduler','0002_payment_amount_received_payment_change_amount_and_more','2025-12-17 00:48:19.712794'),(21,'Payment_Scheduler','0003_room_alter_customer_room_no_customer_room','2025-12-17 01:17:01.275132'),(22,'Payment_Scheduler','0004_customer_due_date','2025-12-17 04:14:38.254297'),(23,'Payment_Scheduler','0005_room_capacity_alter_room_room_type','2025-12-17 06:24:19.073319'),(24,'Payment_Scheduler','0006_room_date_left_alter_room_date_created','2025-12-17 07:36:22.775950'),(25,'Payment_Scheduler','0007_customer_date_left','2025-12-17 07:41:14.486706'),(26,'Payment_Scheduler','0008_remove_customer_room_no_alter_customer_customer_type_and_more','2025-12-17 08:18:31.798675');
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
INSERT INTO `django_session` VALUES ('3otqmkcpu36b8zoj8vaa2lzuap89460d','.eJxVjEEOgjAQRe_StWla6FDGpXvPQKYzU4saSCisjHdXEha6_e-9_zIDbWsZtqrLMIo5m8acfrdE_NBpB3Kn6TZbnqd1GZPdFXvQaq-z6PNyuH8HhWr51sii3DWaJGfILZCLATBEBWBFZtaeFFyH4FVi9OhTyCgIbU-p9868PxJGOIM:1vVmIs:jAdKEoT85Rr613Brj267--Mt3Es6lVTUM74kvwoXUl8','2025-12-31 07:50:34.812669');
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
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_scheduler_boardinghouseuser`
--

LOCK TABLES `payment_scheduler_boardinghouseuser` WRITE;
/*!40000 ALTER TABLE `payment_scheduler_boardinghouseuser` DISABLE KEYS */;
INSERT INTO `payment_scheduler_boardinghouseuser` VALUES (1,'pbkdf2_sha256$1200000$izqArOTVeRv8FOdgW3fc3g$/CSIeIYUV+PeZM7Jsf7NRKLvKicSb/wl+Cg3SMyDHhE=','2025-12-17 00:39:18.984832',1,'admin','','','admin@example.com',1,1,'2025-12-17 00:06:52.604604','Admin','Active','2025-12-17 00:06:53.586391'),(2,'pbkdf2_sha256$1200000$d2Vlvk2ZIldQcGHtebaNyu$gB/tnuzpBn7GlNIuLEMNv+k+O+4fwFUwiW4vnDcv7LA=','2025-12-17 07:50:34.806655',0,'kaito','','','sample@gmail.com',0,1,'2025-12-17 00:40:15.999111','Admin','Active','2025-12-17 00:40:17.021553');
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
  CONSTRAINT `Payment_Scheduler_bo_boardinghouseuser_id_7058dc52_fk_Payment_S` FOREIGN KEY (`boardinghouseuser_id`) REFERENCES `payment_scheduler_boardinghouseuser` (`id`),
  CONSTRAINT `Payment_Scheduler_bo_group_id_6780cbc3_fk_auth_grou` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
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
  CONSTRAINT `Payment_Scheduler_bo_boardinghouseuser_id_084e4523_fk_Payment_S` FOREIGN KEY (`boardinghouseuser_id`) REFERENCES `payment_scheduler_boardinghouseuser` (`id`),
  CONSTRAINT `Payment_Scheduler_bo_permission_id_6e4e74dc_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
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
  PRIMARY KEY (`customer_id`),
  KEY `Payment_Scheduler_cu_room_id_02ed51c0_fk_Payment_S` (`room_id`),
  CONSTRAINT `Payment_Scheduler_cu_room_id_02ed51c0_fk_Payment_S` FOREIGN KEY (`room_id`) REFERENCES `payment_scheduler_room` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_scheduler_customer`
--

LOCK TABLES `payment_scheduler_customer` WRITE;
/*!40000 ALTER TABLE `payment_scheduler_customer` DISABLE KEYS */;
INSERT INTO `payment_scheduler_customer` VALUES (17,'Bryant','asdasd',21,'Male','Active','Student',9,'2025-12-17','2025-12-17'),(18,'Kaito','fghfhg',12,'Female','Active','Student',8,'2026-01-10',NULL),(19,'Christopher','sdfsdf',21,'Male','Active','Student',9,'2025-12-24',NULL);
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
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
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
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payment_scheduler_room`
--

LOCK TABLES `payment_scheduler_room` WRITE;
/*!40000 ALTER TABLE `payment_scheduler_room` DISABLE KEYS */;
INSERT INTO `payment_scheduler_room` VALUES (8,'1','2025-12-17','Occupied','Single',2100.00,1,NULL),(9,'2','2025-12-17','Occupied','Bed Spacer',1100.00,2,NULL);
/*!40000 ALTER TABLE `payment_scheduler_room` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-17 16:30:52
