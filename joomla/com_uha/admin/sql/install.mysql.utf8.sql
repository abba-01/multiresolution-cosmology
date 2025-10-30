-- UHA Component Database Schema
-- User-Token mapping table

CREATE TABLE IF NOT EXISTS `#__uha_user_tokens` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `user_id` INT(11) NOT NULL COMMENT 'Joomla user ID',
  `token` VARCHAR(255) NOT NULL COMMENT 'API token from Django',
  `access_tier` VARCHAR(20) NOT NULL DEFAULT 'academic' COMMENT 'academic|commercial|enterprise',
  `daily_limit` INT(11) DEFAULT 1000 COMMENT 'Daily API call limit',
  `status` VARCHAR(20) DEFAULT 'pending' COMMENT 'pending|approved|denied|revoked',
  `request_date` DATETIME NOT NULL COMMENT 'When token was requested',
  `approved_date` DATETIME NULL COMMENT 'When token was approved',
  `approved_by` INT(11) NULL COMMENT 'Admin user ID who approved',
  `use_case` TEXT NULL COMMENT 'Research use case description',
  `institution` VARCHAR(255) NULL COMMENT 'Institution name',
  `notes` TEXT NULL COMMENT 'Admin notes',
  `params` TEXT NULL COMMENT 'JSON params',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_token` (`token`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_status` (`status`),
  KEY `idx_access_tier` (`access_tier`),
  CONSTRAINT `fk_uha_tokens_user` FOREIGN KEY (`user_id`)
    REFERENCES `#__users`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 DEFAULT COLLATE=utf8mb4_unicode_ci;

-- Usage statistics cache table (cache data from Django)
CREATE TABLE IF NOT EXISTS `#__uha_usage_cache` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `token_id` INT(11) NOT NULL,
  `date` DATE NOT NULL COMMENT 'Usage date',
  `requests_count` INT(11) DEFAULT 0 COMMENT 'Number of requests',
  `last_updated` DATETIME NOT NULL COMMENT 'When cache was updated',
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_token_date` (`token_id`, `date`),
  KEY `idx_date` (`date`),
  CONSTRAINT `fk_uha_usage_token` FOREIGN KEY (`token_id`)
    REFERENCES `#__uha_user_tokens`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 DEFAULT COLLATE=utf8mb4_unicode_ci;

-- Documentation pages
CREATE TABLE IF NOT EXISTS `#__uha_docs` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NOT NULL,
  `slug` VARCHAR(255) NOT NULL COMMENT 'URL-friendly identifier',
  `content` LONGTEXT NOT NULL COMMENT 'Markdown/HTML content',
  `category` VARCHAR(50) NULL COMMENT 'getting-started|api-reference|examples',
  `ordering` INT(11) DEFAULT 0,
  `published` TINYINT(1) DEFAULT 1,
  `created` DATETIME NOT NULL,
  `modified` DATETIME NULL,
  `created_by` INT(11) NULL,
  `modified_by` INT(11) NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_slug` (`slug`),
  KEY `idx_category` (`category`),
  KEY `idx_published` (`published`),
  KEY `idx_ordering` (`ordering`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 DEFAULT COLLATE=utf8mb4_unicode_ci;

-- Proof execution logs
CREATE TABLE IF NOT EXISTS `#__uha_proof_logs` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `user_id` INT(11) NOT NULL,
  `token_id` INT(11) NULL,
  `execution_date` DATETIME NOT NULL,
  `resolution_schedule` VARCHAR(100) NULL COMMENT 'e.g., [8,16,24,32]',
  `status` VARCHAR(20) DEFAULT 'pending' COMMENT 'pending|running|completed|failed',
  `results_hash` VARCHAR(128) NULL COMMENT 'SHA3-512 hash of results',
  `results_json` LONGTEXT NULL COMMENT 'Full results JSON',
  `error_message` TEXT NULL,
  `execution_time_ms` INT(11) NULL,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_token_id` (`token_id`),
  KEY `idx_status` (`status`),
  KEY `idx_execution_date` (`execution_date`),
  CONSTRAINT `fk_uha_proof_user` FOREIGN KEY (`user_id`)
    REFERENCES `#__users`(`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_uha_proof_token` FOREIGN KEY (`token_id`)
    REFERENCES `#__uha_user_tokens`(`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 DEFAULT COLLATE=utf8mb4_unicode_ci;

-- Component configuration (key-value store)
CREATE TABLE IF NOT EXISTS `#__uha_config` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `config_key` VARCHAR(100) NOT NULL,
  `config_value` TEXT NULL,
  `description` VARCHAR(255) NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_key` (`config_key`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 DEFAULT COLLATE=utf8mb4_unicode_ci;

-- Insert default configuration
INSERT INTO `#__uha_config` (`config_key`, `config_value`, `description`) VALUES
('django_api_endpoint', 'https://got.gitgap.org/api', 'Django API base URL'),
('api_timeout', '30', 'API request timeout in seconds'),
('cache_duration', '3600', 'Cache duration in seconds'),
('auto_approve_academic', '1', 'Auto-approve academic tier (.edu emails)'),
('email_notifications', '0', 'Enable email notifications for token approval');
