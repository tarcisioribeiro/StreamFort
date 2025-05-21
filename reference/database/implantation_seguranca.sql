-- MySQL dump 10.13  Distrib 8.0.42, for Linux (x86_64)
--
-- Host: localhost    Database: seguranca
-- ------------------------------------------------------
-- Server version	8.0.42

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
-- Current Database: `seguranca`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `seguranca` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `seguranca`;

--
-- Table structure for table `arquivo_texto`
--

DROP TABLE IF EXISTS `arquivo_texto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `arquivo_texto` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome_arquivo` varchar(100) DEFAULT NULL,
  `conteudo` text,
  `id_usuario` int NOT NULL,
  `doc_usuario` varchar(25) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_arquivo_texto_usuarios` (`id_usuario`,`doc_usuario`),
  CONSTRAINT `fk_arquivo_texto_usuarios` FOREIGN KEY (`id_usuario`, `doc_usuario`) REFERENCES `usuarios` (`id`, `documento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `arquivo_texto`
--

LOCK TABLES `arquivo_texto` WRITE;
/*!40000 ALTER TABLE `arquivo_texto` DISABLE KEYS */;
/*!40000 ALTER TABLE `arquivo_texto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `cartao_credito`
--

DROP TABLE IF EXISTS `cartao_credito`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cartao_credito` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome_cartao` varchar(100) NOT NULL,
  `numero_cartao` varchar(16) NOT NULL,
  `nome_titular` varchar(100) NOT NULL,
  `id_prop_cartao` int NOT NULL,
  `doc_titular_cartao` varchar(25) NOT NULL,
  `data_validade` date NOT NULL,
  `codigo_seguranca` varchar(3) NOT NULL,
  `ativo` varchar(1) DEFAULT 'S',
  PRIMARY KEY (`id`),
  KEY `fk_cartao_credito_usuarios` (`id_prop_cartao`,`doc_titular_cartao`),
  CONSTRAINT `fk_cartao_credito_usuarios` FOREIGN KEY (`id_prop_cartao`, `doc_titular_cartao`) REFERENCES `usuarios` (`id`, `documento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cartao_credito`
--

LOCK TABLES `cartao_credito` WRITE;
/*!40000 ALTER TABLE `cartao_credito` DISABLE KEYS */;
/*!40000 ALTER TABLE `cartao_credito` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contas_bancarias`
--

DROP TABLE IF EXISTS `contas_bancarias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contas_bancarias` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome_conta` varchar(100) NOT NULL,
  `instituicao` varchar(100) NOT NULL,
  `cod_instituicao` varchar(5) NOT NULL,
  `agencia` varchar(10) NOT NULL,
  `numero_conta` varchar(15) NOT NULL,
  `digito_conta` varchar(1) DEFAULT NULL,
  `senha_bancaria` varchar(30) NOT NULL,
  `senha_digital` varchar(30) DEFAULT NULL,
  `id_prop_conta` int NOT NULL,
  `doc_prop_conta` varchar(25) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unq_contas_bancarias` (`doc_prop_conta`,`instituicao`,`agencia`,`numero_conta`),
  KEY `fk_contas_bancarias_usuarios` (`id_prop_conta`,`doc_prop_conta`),
  CONSTRAINT `fk_contas_bancarias_usuarios` FOREIGN KEY (`id_prop_conta`, `doc_prop_conta`) REFERENCES `usuarios` (`id`, `documento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contas_bancarias`
--

LOCK TABLES `contas_bancarias` WRITE;
/*!40000 ALTER TABLE `contas_bancarias` DISABLE KEYS */;
/*!40000 ALTER TABLE `contas_bancarias` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `logs_atividades`
--

DROP TABLE IF EXISTS `logs_atividades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `logs_atividades` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int NOT NULL,
  `data_log` date NOT NULL DEFAULT (curdate()),
  `horario_log` time NOT NULL DEFAULT (curtime()),
  `tipo_log` varchar(100) NOT NULL,
  `conteudo_log` text NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_logs_atividades_usuarios` (`id_usuario`),
  CONSTRAINT `fk_logs_atividades_usuarios` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `logs_atividades`
--

LOCK TABLES `logs_atividades` WRITE;
/*!40000 ALTER TABLE `logs_atividades` DISABLE KEYS */;
/*!40000 ALTER TABLE `logs_atividades` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `senhas`
--

DROP TABLE IF EXISTS `senhas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `senhas` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nome` varchar(100) NOT NULL,
  `url` varchar(200) NOT NULL,
  `login` varchar(100) NOT NULL,
  `senha` varbinary(100) NOT NULL,
  `id_usuario` int NOT NULL,
  `doc_usuario` varchar(25) NOT NULL,
  `ativa` varchar(1) NOT NULL DEFAULT 'S',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unq_senhas` (`nome`,`url`,`login`,`senha`),
  KEY `fk_senhas_usuarios` (`id_usuario`,`doc_usuario`),
  CONSTRAINT `fk_senhas_usuarios` FOREIGN KEY (`id_usuario`, `doc_usuario`) REFERENCES `usuarios` (`id`, `documento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `senhas`
--

LOCK TABLES `senhas` WRITE;
/*!40000 ALTER TABLE `senhas` DISABLE KEYS */;
/*!40000 ALTER TABLE `senhas` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id` int NOT NULL AUTO_INCREMENT,
  `login` varchar(25) NOT NULL,
  `senha` varbinary(100) NOT NULL,
  `nome` varchar(100) NOT NULL,
  `documento` varchar(25) NOT NULL,
  `sexo` varchar(1) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unq_usuarios_nome` (`nome`,`documento`),
  UNIQUE KEY `unq_usuarios` (`login`,`senha`,`nome`,`documento`),
  UNIQUE KEY `unq_usuarios_login` (`login`),
  UNIQUE KEY `unq_usuarios_id` (`id`,`documento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios`
--

LOCK TABLES `usuarios` WRITE;
/*!40000 ALTER TABLE `usuarios` DISABLE KEYS */;
/*!40000 ALTER TABLE `usuarios` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `usuarios_logados`
--

DROP TABLE IF EXISTS `usuarios_logados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios_logados` (
  `id` int NOT NULL AUTO_INCREMENT,
  `id_usuario` int NOT NULL,
  `nome_completo` varchar(100) NOT NULL,
  `documento` varchar(50) NOT NULL,
  `data_login` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `sessao_id` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sessao_id` (`sessao_id`),
  KEY `fk_usuarios_logados_usuarios` (`id_usuario`,`documento`),
  CONSTRAINT `fk_usuarios_logados_usuarios` FOREIGN KEY (`id_usuario`, `documento`) REFERENCES `usuarios` (`id`, `documento`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `usuarios_logados`
--

LOCK TABLES `usuarios_logados` WRITE;
/*!40000 ALTER TABLE `usuarios_logados` DISABLE KEYS */;
/*!40000 ALTER TABLE `usuarios_logados` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-05-19  6:58:24
