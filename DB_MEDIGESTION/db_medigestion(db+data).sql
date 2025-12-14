-- MySQL dump 10.13  Distrib 8.0.43, for Win64 (x86_64)
--
-- Host: localhost    Database: db_medigestion
-- ------------------------------------------------------
-- Server version	8.0.43

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
-- Table structure for table `admintb`
--

DROP TABLE IF EXISTS `admintb`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admintb` (
  `id` int NOT NULL AUTO_INCREMENT,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email_UNIQUE` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admintb`
--

LOCK TABLES `admintb` WRITE;
/*!40000 ALTER TABLE `admintb` DISABLE KEYS */;
INSERT INTO `admintb` VALUES (1,'roberto@gmail.com','$2b$12$7mYzYSbvIJ8WLenBMPbzyugKmsK.zhhgngROrm2ov8r5bxZ0A3wR2','Roberto','Rodriguez'),(2,'jhonnesy@gmail.com','$2b$12$mWGfQnueTz5obgRZVnM6IOhddQHyhNc7Z.TJaM1.e9V1jijgH0d8u','Jhon','Alberto');
/*!40000 ALTER TABLE `admintb` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `citas`
--

DROP TABLE IF EXISTS `citas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `citas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `paciente_id` int NOT NULL,
  `medico_id` int NOT NULL,
  `consultorio` int NOT NULL,
  `motivo` text NOT NULL,
  `estado` enum('Programada','Completada','Cancelada') NOT NULL DEFAULT 'Programada',
  `fecha` date NOT NULL,
  `hora` text NOT NULL,
  PRIMARY KEY (`id`),
  KEY `paciente_id` (`paciente_id`),
  KEY `medico_id` (`medico_id`),
  KEY `consultorio` (`consultorio`),
  CONSTRAINT `citas_ibfk_1` FOREIGN KEY (`paciente_id`) REFERENCES `pacientes` (`id`),
  CONSTRAINT `citas_ibfk_2` FOREIGN KEY (`medico_id`) REFERENCES `medicos` (`id`),
  CONSTRAINT `citas_ibfk_3` FOREIGN KEY (`consultorio`) REFERENCES `consultorio` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `citas`
--

LOCK TABLES `citas` WRITE;
/*!40000 ALTER TABLE `citas` DISABLE KEYS */;
INSERT INTO `citas` VALUES (3,3,3,3,'loqsea','Completada','2025-12-23','18:38'),(5,1,1,2,'Me duele la pata derecha','Programada','2025-12-31','00:30'),(6,1,2,2,'Dolor abdominal','Programada','2025-12-31','16:30'),(7,1,3,1,'Otitis','Programada','2025-12-31','05:30'),(8,1,1,3,'Cita editada','Programada','2025-12-31','00:01');
/*!40000 ALTER TABLE `citas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `consultorio`
--

DROP TABLE IF EXISTS `consultorio`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `consultorio` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(10) NOT NULL,
  `ubicacion` varchar(100) NOT NULL,
  `horario` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `nombre` (`nombre`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `consultorio`
--

LOCK TABLES `consultorio` WRITE;
/*!40000 ALTER TABLE `consultorio` DISABLE KEYS */;
INSERT INTO `consultorio` VALUES (1,'C1','Piso 1 - Ala Norte','2025-10-29 07:00:00'),(2,'C2','Piso 1 - Ala Sur','2025-10-29 08:00:00'),(3,'C3','Piso 2 - Ala Este','2025-10-29 09:00:00');
/*!40000 ALTER TABLE `consultorio` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `efectuar_pago`
--

DROP TABLE IF EXISTS `efectuar_pago`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `efectuar_pago` (
  `id` int NOT NULL AUTO_INCREMENT,
  `cita_pagada` int NOT NULL,
  `paciente` int NOT NULL,
  `email` varchar(100) NOT NULL,
  `metodo_pago` enum('Tarjeta Crédito','Tarjeta Débito','PSE') NOT NULL,
  PRIMARY KEY (`id`),
  KEY `cita_pagada_idx` (`cita_pagada`),
  KEY `paciente_pago_idx` (`paciente`),
  CONSTRAINT `cita_pagada` FOREIGN KEY (`cita_pagada`) REFERENCES `citas` (`id`),
  CONSTRAINT `paciente_pago` FOREIGN KEY (`paciente`) REFERENCES `pacientes` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `efectuar_pago`
--

LOCK TABLES `efectuar_pago` WRITE;
/*!40000 ALTER TABLE `efectuar_pago` DISABLE KEYS */;
/*!40000 ALTER TABLE `efectuar_pago` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `especialidades`
--

DROP TABLE IF EXISTS `especialidades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `especialidades` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `descripcion` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `especialidades`
--

LOCK TABLES `especialidades` WRITE;
/*!40000 ALTER TABLE `especialidades` DISABLE KEYS */;
INSERT INTO `especialidades` VALUES (1,'Medicina General','Atención primaria y diagnóstico general'),(2,'Pediatría','Atención médica de niños y adolescentes'),(3,'Dermatología','Tratamiento de afecciones de la piel'),(4,'Cardiología','Diagnóstico y tratamiento de enfermedades del corazón');
/*!40000 ALTER TABLE `especialidades` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `historial_medico`
--

DROP TABLE IF EXISTS `historial_medico`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `historial_medico` (
  `id` int NOT NULL AUTO_INCREMENT,
  `paciente_id` int NOT NULL,
  `medico_id` int NOT NULL,
  `fecha` date NOT NULL,
  `diagnostico` text,
  `tratamiento` text,
  `notas` text,
  PRIMARY KEY (`id`),
  KEY `paciente_id` (`paciente_id`),
  KEY `medico_id` (`medico_id`),
  CONSTRAINT `historial_medico_ibfk_1` FOREIGN KEY (`paciente_id`) REFERENCES `pacientes` (`id`),
  CONSTRAINT `historial_medico_ibfk_2` FOREIGN KEY (`medico_id`) REFERENCES `medicos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `historial_medico`
--

LOCK TABLES `historial_medico` WRITE;
/*!40000 ALTER TABLE `historial_medico` DISABLE KEYS */;
INSERT INTO `historial_medico` VALUES (1,1,1,'2025-10-29','Migraña leve','Analgésicos y descanso','Controlar estrés'),(2,3,3,'2025-10-25','Dermatitis alérgica','Crema tópica y antihistamínico','Evitar exposición solar');
/*!40000 ALTER TABLE `historial_medico` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `horario_dias`
--

DROP TABLE IF EXISTS `horario_dias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `horario_dias` (
  `id` int NOT NULL AUTO_INCREMENT,
  `medico_id` int NOT NULL,
  `dia_semana` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `medico_id_idx` (`medico_id`),
  CONSTRAINT `medico_id_dias` FOREIGN KEY (`medico_id`) REFERENCES `medicos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `horario_dias`
--

LOCK TABLES `horario_dias` WRITE;
/*!40000 ALTER TABLE `horario_dias` DISABLE KEYS */;
INSERT INTO `horario_dias` VALUES (1,1,0),(2,1,1),(3,1,2),(4,1,3),(5,1,4),(6,2,0),(7,2,1),(8,2,2),(9,2,3),(10,2,4),(11,3,2),(12,3,3),(13,3,4),(14,3,5),(15,3,6);
/*!40000 ALTER TABLE `horario_dias` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `horario_medicos`
--

DROP TABLE IF EXISTS `horario_medicos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `horario_medicos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `hora_ingreso` int NOT NULL,
  `hora_ingreso_tp` enum('AM','PM') NOT NULL,
  `hora_salida` int NOT NULL,
  `hora_salida_tp` enum('AM','PM') NOT NULL,
  `horario` enum('Lun-Vier','Mier-Dom') NOT NULL,
  `medico_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `medico_id_idx` (`medico_id`),
  CONSTRAINT `medico_id` FOREIGN KEY (`medico_id`) REFERENCES `medicos` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `horario_medicos`
--

LOCK TABLES `horario_medicos` WRITE;
/*!40000 ALTER TABLE `horario_medicos` DISABLE KEYS */;
INSERT INTO `horario_medicos` VALUES (1,8,'AM',4,'PM','Lun-Vier',1),(2,4,'PM',12,'AM','Lun-Vier',2),(3,8,'AM',4,'PM','Mier-Dom',3);
/*!40000 ALTER TABLE `horario_medicos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medicos`
--

DROP TABLE IF EXISTS `medicos`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medicos` (
  `id` int NOT NULL AUTO_INCREMENT,
  `especialidad_id` int NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `telefono` varchar(10) NOT NULL,
  `email` varchar(100) NOT NULL,
  `password` varchar(255) NOT NULL,
  `documento` varchar(20) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `telefono` (`telefono`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `documento_UNIQUE` (`documento`),
  KEY `especialidad_id` (`especialidad_id`),
  CONSTRAINT `medicos_ibfk_1` FOREIGN KEY (`especialidad_id`) REFERENCES `especialidades` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medicos`
--

LOCK TABLES `medicos` WRITE;
/*!40000 ALTER TABLE `medicos` DISABLE KEYS */;
INSERT INTO `medicos` VALUES (1,1,'Ana','Martínez','3105559988','ana.martinez@hospital.com','$2b$12$hn3zwt2zUWMndPOowtQwuOiZxBwiRfKjCmZ8WfdoEFRw0HaqlH5Tm','12342567'),(2,3,'Luis','García','3109876543','luis.garcia@hospital.com','$2b$12$qw6CNAAzuJ1EZts3cCkQwexvSKivdXHKA8V5ELkyh38fTTBBOaPpq','987654321'),(3,3,'Sofía','Ruiz','3125554488','sofia.ruiz@hospital.com','$2b$12$aVg7HE7pVm5nYyW9kwU6cOD9D/M4PubPWRv/S/ugd.Db4wYLrw3x2','123585589');
/*!40000 ALTER TABLE `medicos` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pacientes`
--

DROP TABLE IF EXISTS `pacientes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pacientes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `tipo_documento` enum('Cédula de ciudadanía','Cédula de extranjería','Tarjeta de identidad') NOT NULL,
  `documento` varchar(20) NOT NULL,
  `fecha_nacimiento` date NOT NULL,
  `genero` enum('Masculino','Femenino','Otro') NOT NULL,
  `telefono` varchar(10) NOT NULL,
  `email` varchar(100) NOT NULL,
  `rh` enum('A+','A-','B+','B-','AB+','AB-','O+','O-') NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `documento` (`documento`),
  UNIQUE KEY `telefono` (`telefono`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pacientes`
--

LOCK TABLES `pacientes` WRITE;
/*!40000 ALTER TABLE `pacientes` DISABLE KEYS */;
INSERT INTO `pacientes` VALUES (1,'Laura','Gómez','Cédula de ciudadanía','1059876543','1995-03-12','Femenino','3216549870','laura@gmail.com','O+','$2b$12$VfhR6iQ2qYluFGYwWLsl5.tNCS8BNqcGMteFMU30UGa.fXY3b66ze'),(2,'Carlos','Ramírez','Cédula de ciudadanía','1023456789','1988-07-25','Masculino','3004567891','carlosr@gmail.com','A+','$2b$12$Cm3kt5RXc6Hn3uSSriFf.e2X6c.2LLJylJMOb8jNXhtqG5Fzv9QWm'),(3,'María','Torres','Tarjeta de identidad','890123456','2000-11-09','Otro','3109876543','maria.torres@hotmail.com','O-','$2b$12$cteVfgcFj7nVoOd64cK4XOz4d1kKZ1PrrGvwmfQpHbDaRi7TkTsZ2');
/*!40000 ALTER TABLE `pacientes` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-12-02 16:12:23
