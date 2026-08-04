-- MySQL dump 10.13  Distrib 8.0.46, for Win64 (x86_64)
--
-- Host: localhost    Database: vidplex
-- ------------------------------------------------------
-- Server version	8.0.46

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admin_usuarios`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admin_usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `correo` varchar(120) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `password_hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `usuario` (`usuario`),
  UNIQUE KEY `correo` (`correo`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admin_usuarios`
--

LOCK TABLES `admin_usuarios` WRITE;
/*!40000 ALTER TABLE `admin_usuarios` DISABLE KEYS */;
INSERT INTO `admin_usuarios` (`id`, `usuario`, `correo`, `password_hash`) VALUES (4,'admin','feriavidplex@gmail.com','$2b$12$oN2oMW/cSs0gi.vrYkXhPOozUQPGennhaP0LiLBoPvwKFb58tyymS');
/*!40000 ALTER TABLE `admin_usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `escaneos`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `escaneos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `producto_id` int NOT NULL,
  `fecha` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `producto_id` (`producto_id`),
  CONSTRAINT `escaneos_ibfk_1` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=444 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `escaneos`
--

LOCK TABLES `escaneos` WRITE;
/*!40000 ALTER TABLE `escaneos` DISABLE KEYS */;
INSERT INTO `escaneos` (`id`, `producto_id`, `fecha`) VALUES (289,17,'2026-08-01 09:06:44'),(291,19,'2026-08-01 09:42:35'),(292,16,'2026-08-01 09:42:36'),(293,18,'2026-08-01 09:42:38'),(299,16,'2026-08-01 09:42:49'),(302,17,'2026-08-01 09:42:54'),(303,18,'2026-08-01 09:42:56'),(304,16,'2026-08-01 09:43:00'),(305,16,'2026-08-01 09:43:03'),(306,18,'2026-08-01 09:43:05'),(307,16,'2026-08-01 09:44:52'),(308,1,'2026-08-01 09:44:55'),(309,17,'2026-08-01 09:44:57'),(310,20,'2026-08-01 09:44:59'),(311,18,'2026-08-01 09:45:01'),(312,16,'2026-08-01 09:45:02'),(313,19,'2026-08-01 09:45:03'),(314,1,'2026-08-01 09:45:08'),(315,12,'2026-08-01 09:45:11'),(318,15,'2026-08-01 09:48:52'),(319,16,'2026-08-01 09:48:54'),(320,12,'2026-08-01 09:48:55'),(321,14,'2026-08-01 09:48:56'),(322,1,'2026-08-01 09:48:58'),(323,13,'2026-08-01 09:48:59'),(324,19,'2026-08-01 09:49:04'),(325,18,'2026-08-01 09:49:06'),(326,20,'2026-08-01 09:49:07'),(327,17,'2026-08-01 09:49:09'),(330,15,'2026-08-01 09:55:07'),(331,16,'2026-08-01 09:55:08'),(332,12,'2026-08-01 09:55:09'),(333,14,'2026-08-01 09:55:10'),(334,1,'2026-08-01 09:55:12'),(335,13,'2026-08-01 09:55:14'),(336,19,'2026-08-01 09:55:17'),(337,18,'2026-08-01 09:55:18'),(338,25,'2026-08-01 09:55:19'),(339,20,'2026-08-01 09:55:21'),(340,26,'2026-08-01 09:55:22'),(341,17,'2026-08-01 09:55:24'),(343,29,'2026-08-01 09:55:30'),(344,28,'2026-08-01 09:55:31'),(345,32,'2026-08-01 09:55:32'),(346,30,'2026-08-01 09:55:34'),(347,27,'2026-08-01 09:55:35'),(350,38,'2026-08-01 09:55:42'),(351,37,'2026-08-01 09:55:43'),(352,35,'2026-08-01 09:55:45'),(353,36,'2026-08-01 09:55:46'),(355,42,'2026-08-01 09:55:50'),(356,41,'2026-08-01 09:55:51'),(357,40,'2026-08-01 09:55:52'),(358,39,'2026-08-01 09:55:54'),(359,44,'2026-08-01 09:55:55'),(360,41,'2026-08-01 09:55:59'),(361,42,'2026-08-01 09:56:00'),(363,46,'2026-08-01 09:56:04'),(364,47,'2026-08-01 09:56:05'),(365,45,'2026-08-01 09:56:06'),(366,48,'2026-08-01 09:56:07'),(367,49,'2026-08-01 09:56:09'),(368,50,'2026-08-01 09:56:10'),(370,42,'2026-08-01 09:57:45'),(371,39,'2026-08-01 09:57:49'),(372,44,'2026-08-01 09:57:51'),(373,42,'2026-08-01 09:57:52'),(374,41,'2026-08-01 09:57:53'),(375,40,'2026-08-01 09:57:55'),(377,15,'2026-08-01 10:03:24'),(378,16,'2026-08-01 10:03:27'),(379,12,'2026-08-01 10:03:28'),(380,14,'2026-08-01 10:03:29'),(381,13,'2026-08-01 10:03:32'),(382,1,'2026-08-01 10:03:33'),(383,19,'2026-08-01 10:03:37'),(384,18,'2026-08-01 10:03:38'),(385,25,'2026-08-01 10:03:39'),(386,20,'2026-08-01 10:03:40'),(387,17,'2026-08-01 10:03:42'),(388,26,'2026-08-01 10:03:43'),(389,29,'2026-08-01 10:03:46'),(390,28,'2026-08-01 10:03:47'),(391,32,'2026-08-01 10:03:48'),(392,27,'2026-08-01 10:03:50'),(393,31,'2026-08-01 10:03:53'),(394,30,'2026-08-01 10:03:54'),(395,38,'2026-08-01 10:03:58'),(396,37,'2026-08-01 10:03:59'),(397,36,'2026-08-01 10:04:00'),(398,35,'2026-08-01 10:04:01'),(399,33,'2026-08-01 10:04:03'),(400,34,'2026-08-01 10:04:04'),(401,42,'2026-08-01 10:04:07'),(402,41,'2026-08-01 10:04:08'),(403,40,'2026-08-01 10:04:09'),(404,44,'2026-08-01 10:04:10'),(405,43,'2026-08-01 10:04:12'),(406,39,'2026-08-01 10:04:13'),(407,42,'2026-08-01 10:04:16'),(408,41,'2026-08-01 10:04:20'),(409,40,'2026-08-01 10:04:21'),(410,44,'2026-08-01 10:04:22'),(411,43,'2026-08-01 10:04:24'),(412,39,'2026-08-01 10:04:25'),(413,48,'2026-08-01 10:04:28'),(414,46,'2026-08-01 10:04:29'),(415,47,'2026-08-01 10:04:31'),(416,45,'2026-08-01 10:04:32'),(417,49,'2026-08-01 10:04:34'),(418,50,'2026-08-01 10:04:36'),(419,38,'2026-08-01 10:08:15'),(420,15,'2026-08-01 10:08:29'),(421,1,'2026-08-01 10:08:42'),(422,39,'2026-08-01 10:08:47'),(423,15,'2026-08-01 10:12:24'),(424,15,'2026-08-01 10:12:30'),(425,20,'2026-08-01 10:34:33'),(426,16,'2026-08-03 08:32:28'),(427,34,'2026-08-03 09:52:33'),(428,34,'2026-08-03 09:52:41'),(429,33,'2026-08-03 09:52:44'),(430,33,'2026-08-03 09:52:50'),(431,33,'2026-08-03 09:53:09'),(432,33,'2026-08-03 09:53:31'),(433,33,'2026-08-03 09:53:33'),(434,33,'2026-08-03 09:53:37'),(435,33,'2026-08-03 09:53:43'),(436,30,'2026-08-03 09:53:57'),(437,30,'2026-08-03 09:54:07'),(438,19,'2026-08-03 09:55:46'),(439,33,'2026-08-03 10:05:53'),(440,33,'2026-08-03 10:10:41'),(441,15,'2026-08-03 10:41:42'),(442,15,'2026-08-03 10:43:10'),(443,15,'2026-08-03 10:50:29');
/*!40000 ALTER TABLE `escaneos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `lead_producto`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `lead_producto` (
  `id` int NOT NULL AUTO_INCREMENT,
  `lead_id` int NOT NULL,
  `producto_id` int NOT NULL,
  `fecha_interes` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unico_lead_producto` (`lead_id`,`producto_id`),
  KEY `producto_id` (`producto_id`),
  CONSTRAINT `lead_producto_ibfk_1` FOREIGN KEY (`lead_id`) REFERENCES `leads` (`id`) ON DELETE CASCADE,
  CONSTRAINT `lead_producto_ibfk_2` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `lead_producto`
--

LOCK TABLES `lead_producto` WRITE;
/*!40000 ALTER TABLE `lead_producto` DISABLE KEYS */;
/*!40000 ALTER TABLE `lead_producto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `leads`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `leads` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `telefono` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `correo` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tipo_proyecto` enum('residencial','comercial','constructora') COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `autorizo_datos` tinyint(1) NOT NULL DEFAULT '0',
  `fecha_autorizacion` datetime DEFAULT NULL,
  `fecha_creacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `ultima_actividad` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `correo` (`correo`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `leads`
--

LOCK TABLES `leads` WRITE;
/*!40000 ALTER TABLE `leads` DISABLE KEYS */;
/*!40000 ALTER TABLE `leads` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `producto_media`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `producto_media` (
  `id` int NOT NULL AUTO_INCREMENT,
  `producto_id` int NOT NULL,
  `tipo` enum('imagen','video') COLLATE utf8mb4_unicode_ci NOT NULL,
  `url` varchar(500) COLLATE utf8mb4_unicode_ci NOT NULL,
  `orden` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `producto_id` (`producto_id`),
  CONSTRAINT `producto_media_ibfk_1` FOREIGN KEY (`producto_id`) REFERENCES `productos` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `producto_media`
--

LOCK TABLES `producto_media` WRITE;
/*!40000 ALTER TABLE `producto_media` DISABLE KEYS */;
INSERT INTO `producto_media` (`id`, `producto_id`, `tipo`, `url`, `orden`) VALUES (1,1,'imagen','productos/vp-001-detalle-1.jpg',1),(2,1,'imagen','productos/vp-001-detalle-2.jpg',2),(3,1,'video','https://www.youtube.com/embed/REEMPLAZAR_CON_ID_DEL_VIDEO',3);
/*!40000 ALTER TABLE `producto_media` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `productos`
--

/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `productos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `ref_code` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nombre` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `tipo_vidrio` varchar(60) COLLATE utf8mb4_unicode_ci NOT NULL,
  `categoria` varchar(30) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `descripcion` text COLLATE utf8mb4_unicode_ci,
  `especificaciones` text COLLATE utf8mb4_unicode_ci,
  `imagen_principal` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `video_url` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `activo` tinyint(1) NOT NULL DEFAULT '1',
  `fecha_creacion` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ref_code` (`ref_code`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `productos`
--

LOCK TABLES `productos` WRITE;
/*!40000 ALTER TABLE `productos` DISABLE KEYS */;
INSERT INTO `productos` (`id`, `ref_code`, `nombre`, `tipo_vidrio`, `categoria`, `descripcion`, `especificaciones`, `imagen_principal`, `video_url`, `activo`, `fecha_creacion`) VALUES (1,'VP-001','Vidrio Templado 6mm','Templado','design','Vidrio templado de 6mm de espesor, ideal para divisiones de baño y puertas interiores. Alta resistencia al impacto y seguridad en caso de rotura.','Espesor: 6mm | Resistencia: 5 veces más que vidrio annealed | Acabado: Transparente | Uso: Interior','/static/img/vidrios/VP-001.jpg',NULL,1,'2026-07-18 08:15:54'),(12,'VP-002','Vidrio Laminado Acústico','Laminado','design','Vidrio laminado con intercalar acústico para reducción de ruido exterior. Perfecto para fachadas y ventanales en zonas urbanas.','Espesor total: 8.38mm (4+0.38+4) | Reducción acústica: 38dB | Seguridad: No se desprende al romper | Uso: Fachadas, ventanales','/static/img/vidrios/VP-002.jpg',NULL,1,'2026-07-21 13:05:41'),(13,'VP-003','Vidrio Reflectivo Solar','Reflectivo','design','Vidrio con capa reflectiva que reduce el calor solar en un 60%. Ideal para edificios con alta exposición al sol.','Espesor: 6mm | Factor solar: 0.40 | Reflexión exterior: 25% | Uso: Fachadas comerciales','/static/img/vidrios/VP-003.jpg',NULL,1,'2026-07-21 13:05:41'),(14,'VP-004','Vidrio Low-E 4mm','Low-E','design','Vidrio de baja emisividad que mejora la eficiencia energética del edificio. Mantiene el calor interior en invierno y lo repele en verano.','Espesor: 4mm | Emisividad: 0.03 | Transmisión luz: 80% | Uso: Ventanas residenciales','/static/img/vidrios/VP-004.jpg',NULL,1,'2026-07-21 13:05:41'),(15,'VP-005','Vidrio Espejado Bronce','Espejado','design','Vidrio espejado en tono bronce para fachadas con diseño arquitectónico distintivo. Privacidad total desde el exterior.','Espesor: 5mm | Color: Bronce | Reflexión: 55% | Uso: Fachadas, mobiliario','/static/img/vidrios/VP-005.jpg',NULL,1,'2026-07-21 13:05:41'),(16,'VP-006','Vidrio Grabado Ácido','Decorativo','design','Vidrio con acabado satinado por tratamiento ácido. Elegancia difusa que permite paso de luz con privacidad.','Espesor: 5mm | Acabado: Satinado unilateral | Transmisión luz: 85% | Uso: Divisiones, puertas','/static/img/vidrios/VP-006.jpg',NULL,1,'2026-07-21 13:05:41'),(17,'VP-007','Vidrio Templado Curvo','Templado Curvo','confort','Vidrio templado con curvatura personalizada para proyectos arquitectónicos únicos. Resistencia estructural mantenida.','Espesor: 8-12mm | Curvatura: según diseño | Radio mínimo: 500mm | Uso: Barandas, fachadas curvas','/static/img/vidrios/VP-007.jpg',NULL,1,'2026-07-21 13:05:41'),(18,'VP-008','Vidrio Laminado Blindado','Blindado','confort','Vidrio laminado de alta seguridad con capas de policarbonato. Resistencia a impactos balísticos nivel III-A.','Espesor total: 24mm | Nivel: III-A | Capas: 3 vidrios + 2 policarbonatos | Uso: Bancos, embajadas','/static/img/vidrios/VP-008.jpg',NULL,1,'2026-07-21 13:05:41'),(19,'VP-009','Vidrio Antihumedad para Baño','Antihumedad','confort','Vidrio con tratamiento hidrofóbico que repele el agua y evita manchas de cal. Ideal para mamparas de ducha.','Espesor: 6mm | Tratamiento: Nanocapa hidrofóbica | Garantía: 5 años | Uso: Mamparas, divisiones húmedas','/static/img/vidrios/VP-009.jpg',NULL,1,'2026-07-21 13:05:41'),(20,'VP-010','Vidrio Serigrafiado Decorativo','Serigrafiado','confort','Vidrio con diseños serigrafiados en cerámica cocida al fuego. Personalizable con logos o patrones arquitectónicos.','Espesor: 6-10mm | Diseño: Personalizable | Durabilidad: Permanente | Uso: Fachadas, divisiones corporativas','/static/img/vidrios/VP-010.jpg',NULL,1,'2026-07-21 13:05:41'),(25,'VP-011','Vidrio Laminado Decorativo Confort','Laminado','confort','Vidrio laminado pensado para espacios de confort residencial.',NULL,NULL,NULL,1,'2026-08-01 09:51:07'),(26,'VP-012','Vidrio Templado Térmico Confort','Templado','confort','Vidrio templado con aislamiento térmico para interiores.',NULL,NULL,NULL,1,'2026-08-01 09:51:07'),(27,'VP-013','Vidrio DVH Refrigeración Comercial','DVH','refrigeracion','Doble vidriado hermético para cámaras de refrigeración.',NULL,NULL,NULL,1,'2026-08-01 09:51:07'),(28,'VP-014','Vidrio Bajo Emisivo Refrigeración','Low-E','refrigeracion','Control térmico para vitrinas refrigeradas.',NULL,NULL,NULL,1,'2026-08-01 09:51:07'),(29,'VP-015','Vidrio Antiempañante Refrigeración','Antiempañante','refrigeracion','Evita condensación en cuartos fríos y neveras.',NULL,NULL,NULL,1,'2026-08-01 09:51:07'),(30,'VP-016','Vidrio Termopanel Refrigeración','Termopanel','refrigeracion','Aislamiento para exhibidores refrigerados.',NULL,NULL,NULL,1,'2026-08-01 09:51:07'),(31,'VP-017','Vidrio Triple Panel Refrigeración','Triple Panel','refrigeracion','Máximo aislamiento térmico para cuartos fríos.',NULL,NULL,NULL,1,'2026-08-01 09:51:07'),(32,'VP-018','Vidrio Curvo Refrigeración','Curvo','refrigeracion','Vidrio curvo para vitrinas de refrigeración.',NULL,NULL,NULL,1,'2026-08-01 09:51:07'),(33,'VP-019','Vidrio SolarCool Control Solar','Control Solar','control-solar','Reduce ganancia térmica en fachadas.',NULL,NULL,NULL,1,'2026-08-01 09:51:07'),(34,'VP-020','Vidrio Reflectivo Control Solar','Reflectivo','control-solar','Alta reflectividad para control de radiación solar.',NULL,NULL,NULL,1,'2026-08-01 09:51:07'),(35,'VP-021','Vidrio Low-E Control Solar','Low-E','control-solar','Baja emisividad para eficiencia energética.',NULL,NULL,NULL,1,'2026-08-01 09:51:07'),(36,'VP-022','Vidrio Gris Control Solar','Gris Solar','control-solar','Tono gris para reducción de luminosidad.',NULL,NULL,NULL,1,'2026-08-01 09:51:07'),(37,'VP-023','Vidrio Bronce Control Solar','Bronce Solar','control-solar','Tono bronce con control de calor.',NULL,NULL,NULL,1,'2026-08-01 09:51:07'),(38,'VP-024','Vidrio Azul Control Solar','Azul Solar','control-solar','Tono azul con filtro solar.',NULL,NULL,NULL,1,'2026-08-01 09:51:07'),(39,'VP-025','Vidrio Templado Seguridad HS','Templado HS','seguridad','Vidrio de seguridad termoendurecido.',NULL,NULL,NULL,1,'2026-08-01 09:51:07'),(40,'VP-026','Vidrio Laminado Seguridad','Laminado','seguridad','Laminado de seguridad anti-impacto.',NULL,NULL,NULL,1,'2026-08-01 09:51:07'),(41,'VP-027','Vidrio Blindado Seguridad','Blindado','seguridad','Protección balística para fachadas críticas.',NULL,NULL,NULL,1,'2026-08-01 09:51:07'),(42,'VP-028','Vidrio Antivandálico Seguridad','Antivandálico','seguridad','Resistente a impactos y vandalismo.',NULL,NULL,NULL,1,'2026-08-01 09:51:07'),(43,'VP-029','Vidrio Templado Seguridad Piso','Templado Piso','seguridad','Vidrio de seguridad para pisos.',NULL,NULL,NULL,1,'2026-08-01 09:51:07'),(44,'VP-030','Vidrio Laminado Seguridad Baranda','Laminado Baranda','seguridad','Para barandas y escaleras.',NULL,NULL,NULL,1,'2026-08-01 09:51:07'),(45,'VP-031','Vidrio Estructural Alto Desempeño','Estructural','alto-desempeno','Vidrio para fachadas estructurales de gran formato.',NULL,NULL,NULL,1,'2026-08-01 09:51:07'),(46,'VP-032','Vidrio Curvo Alto Desempeño','Curvo','alto-desempeno','Vidrio curvo para arquitectura de alto desempeño.',NULL,NULL,NULL,1,'2026-08-01 09:51:07'),(47,'VP-033','Vidrio DVH Alto Desempeño','DVH','alto-desempeno','Doble vidriado para fachadas de alto rendimiento.',NULL,NULL,NULL,1,'2026-08-01 09:51:07'),(48,'VP-034','Vidrio Acústico Alto Desempeño','Acústico','alto-desempeno','Control acústico para edificios corporativos.',NULL,NULL,NULL,1,'2026-08-01 09:51:07'),(49,'VP-035','Vidrio Estructural Fachada','Estructural','alto-desempeno','Sistema estructural de fachada continua.',NULL,NULL,NULL,1,'2026-08-01 09:51:07'),(50,'VP-036','Vidrio Panel Alto Desempeño','Panel','alto-desempeno','Panel de alto desempeño térmico-acústico.',NULL,NULL,NULL,1,'2026-08-01 09:51:07');
/*!40000 ALTER TABLE `productos` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-08-03 16:18:03
