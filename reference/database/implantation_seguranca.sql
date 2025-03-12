-- MySQL dump 10.13  Distrib 8.0.41, for Linux (x86_64)
--
-- Host: localhost    Database: seguranca
-- ------------------------------------------------------
-- Server version	8.0.41-0ubuntu0.22.04.1

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

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `seguranca` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `seguranca`;

--
-- Table structure for table `arquivo_texto`
--

DROP TABLE IF EXISTS `arquivo_texto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `arquivo_texto` (
  `id_arquivo` int NOT NULL AUTO_INCREMENT,
  `nome_arquivo` varchar(100) DEFAULT NULL,
  `conteudo` text,
  `usuario_associado` varchar(100) NOT NULL,
  `documento_usuario_associado` varchar(25) NOT NULL,
  PRIMARY KEY (`id_arquivo`),
  KEY `fk_arquivo_texto_usuarios` (`usuario_associado`,`documento_usuario_associado`),
  CONSTRAINT `fk_arquivo_texto_usuarios` FOREIGN KEY (`usuario_associado`, `documento_usuario_associado`) REFERENCES `usuarios` (`nome`, `documento_usuario`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `cartao_credito`
--

DROP TABLE IF EXISTS `cartao_credito`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cartao_credito` (
  `id_cartao` int NOT NULL AUTO_INCREMENT,
  `nome_cartao` varchar(100) NOT NULL,
  `numero_cartao` varchar(16) NOT NULL,
  `nome_titular` varchar(100) NOT NULL,
  `proprietario_cartao` varchar(100) NOT NULL,
  `documento_titular` varchar(25) NOT NULL,
  `data_validade` date NOT NULL,
  `codigo_seguranca` varchar(3) NOT NULL,
  `ativo` varchar(1) DEFAULT 'S',
  PRIMARY KEY (`id_cartao`),
  KEY `fk_cartao_credito_usuarios` (`proprietario_cartao`,`documento_titular`),
  CONSTRAINT `fk_cartao_credito_usuarios` FOREIGN KEY (`proprietario_cartao`, `documento_titular`) REFERENCES `usuarios` (`nome`, `documento_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `contas_bancarias`
--

DROP TABLE IF EXISTS `contas_bancarias`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contas_bancarias` (
  `id_conta` int NOT NULL AUTO_INCREMENT,
  `nome_conta` varchar(100) NOT NULL,
  `instituicao_financeira` varchar(100) NOT NULL,
  `codigo_instituicao_financeira` varchar(5) NOT NULL,
  `agencia` varchar(10) NOT NULL,
  `numero_conta` varchar(15) NOT NULL,
  `digito_conta` varchar(1) DEFAULT NULL,
  `senha_bancaria_conta` varchar(30) NOT NULL,
  `senha_digital_conta` varchar(30) DEFAULT NULL,
  `nome_proprietario_conta` varchar(100) NOT NULL,
  `documento_proprietario_conta` varchar(25) NOT NULL,
  PRIMARY KEY (`id_conta`),
  UNIQUE KEY `unq_contas_bancarias` (`documento_proprietario_conta`,`instituicao_financeira`,`agencia`,`numero_conta`),
  KEY `fk_contas_bancarias_usuarios` (`nome_proprietario_conta`,`documento_proprietario_conta`),
  CONSTRAINT `fk_contas_bancarias_usuarios` FOREIGN KEY (`nome_proprietario_conta`, `documento_proprietario_conta`) REFERENCES `usuarios` (`nome`, `documento_usuario`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `logs_atividades`
--

DROP TABLE IF EXISTS `logs_atividades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `logs_atividades` (
  `id_log` int NOT NULL AUTO_INCREMENT,
  `data_log` date NOT NULL DEFAULT (curdate()),
  `horario_log` time NOT NULL DEFAULT (curtime()),
  `usuario_log` varchar(25) NOT NULL,
  `tipo_log` varchar(100) NOT NULL,
  `conteudo_log` text NOT NULL,
  PRIMARY KEY (`id_log`),
  KEY `fk_logs_atividades_usuarios` (`usuario_log`),
  CONSTRAINT `fk_logs_atividades_usuarios` FOREIGN KEY (`usuario_log`) REFERENCES `usuarios` (`login`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `senhas`
--

DROP TABLE IF EXISTS `senhas`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `senhas` (
  `id_senha` int NOT NULL AUTO_INCREMENT,
  `nome_site` varchar(100) NOT NULL,
  `url_site` varchar(200) NOT NULL,
  `login` varchar(100) NOT NULL,
  `senha` varbinary(100) NOT NULL,
  `usuario_associado` varchar(100) NOT NULL,
  `documento_usuario_associado` varchar(25) NOT NULL,
  `ativa` varchar(1) NOT NULL DEFAULT 'S',
  PRIMARY KEY (`id_senha`),
  UNIQUE KEY `unq_senhas` (`nome_site`,`url_site`,`login`,`senha`),
  KEY `fk_senhas_usuarios` (`usuario_associado`,`documento_usuario_associado`),
  CONSTRAINT `fk_senhas_usuarios` FOREIGN KEY (`usuario_associado`, `documento_usuario_associado`) REFERENCES `usuarios` (`nome`, `documento_usuario`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `usuarios`
--

DROP TABLE IF EXISTS `usuarios`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios` (
  `id_usuario` int NOT NULL AUTO_INCREMENT,
  `login` varchar(25) NOT NULL,
  `senha` varbinary(100) NOT NULL,
  `nome` varchar(100) NOT NULL,
  `documento_usuario` varchar(25) NOT NULL,
  `sexo` varchar(1) NOT NULL,
  PRIMARY KEY (`id_usuario`),
  UNIQUE KEY `unq_usuarios_nome` (`nome`,`documento_usuario`),
  UNIQUE KEY `unq_usuarios` (`login`,`senha`,`nome`,`documento_usuario`),
  UNIQUE KEY `unq_usuarios_login` (`login`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Table structure for table `usuarios_logados`
--

DROP TABLE IF EXISTS `usuarios_logados`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `usuarios_logados` (
  `id` int NOT NULL AUTO_INCREMENT,
  `usuario_id` int NOT NULL,
  `nome_completo` varchar(255) NOT NULL,
  `documento` varchar(50) NOT NULL,
  `data_login` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `sessao_id` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `sessao_id` (`sessao_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-02-12  2:14:42
