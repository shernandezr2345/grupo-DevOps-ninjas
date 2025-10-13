-- =========================================
-- CREACIÓN DE TABLA: blacklist
-- =========================================
CREATE TABLE IF NOT EXISTS blacklist (
    id SERIAL PRIMARY KEY,
    email VARCHAR(120) UNIQUE NOT NULL,
    app_uuid CHAR(36) NOT NULL,
    blocked_reason VARCHAR(255),
    source_ip VARCHAR(45) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Índices recomendados para acelerar búsquedas frecuentes
CREATE INDEX IF NOT EXISTS idx_blacklist_email ON blacklist (email);
CREATE INDEX IF NOT EXISTS idx_blacklist_app_uuid ON blacklist (app_uuid);
CREATE INDEX IF NOT EXISTS idx_blacklist_source_ip ON blacklist (source_ip);

-- =========================================
-- CARGA DE DATOS DE EJEMPLO
-- =========================================
INSERT INTO blacklist (email, app_uuid, blocked_reason, source_ip, created_at) VALUES
('user1@example.com', 'a3e8d2c1-4f2b-4b6a-8d99-0f1a8bca1d11', 'Spam detected', '192.168.1.10', NOW()),
('user2@example.com', 'c7f2b8a3-1e9d-4c67-8f0a-9b2d7a3f2c99', 'Compromised account', '10.0.0.21', NOW()),
('user3@example.com', 'b2a5f4e1-7c1d-41af-bbb9-8accc7b2a7c1', 'Policy violation', '172.16.0.3', NOW()),
('user4@example.com', 'e8f9a1b2-3c5d-4a9f-9d3e-1c8a2b4e5f9c', 'User request', '192.168.1.44', NOW()),
('user5@example.com', 'f9a2b3c4-1d2e-4f3a-b4c5-6d7e8f9a0b1c', 'Suspicious activity', '10.0.0.55', NOW()),
('user6@example.com', 'a1b2c3d4-e5f6-47a8-b9c0-1d2e3f4a5b6c', 'Too many login attempts', '172.16.0.66', NOW()),
('user7@example.com', 'b9c8d7e6-f5a4-43b2-b1c0-d9e8f7a6b5c4', 'Reported by admin', '192.168.2.7', NOW()),
('user8@example.com', 'c3d4e5f6-a7b8-49c0-b1d2-e3f4a5b6c7d8', 'Phishing attempt', '10.0.1.8', NOW()),
('user9@example.com', 'd1e2f3a4-b5c6-48d7-b8e9-f0a1b2c3d4e5', 'Bot traffic', '172.16.1.9', NOW()),
('user10@example.com', 'e2f3a4b5-c6d7-49e8-b9f0-a1b2c3d4e5f6', 'Fake email address', '192.168.3.10', NOW()),
('user11@example.com', 'f3a4b5c6-d7e8-40f9-b0a1-b2c3d4e5f6a7', 'Spam detected', '10.0.2.11', NOW()),
('user12@example.com', 'a4b5c6d7-e8f9-41a0-b1b2-c3d4e5f6a8b9', 'Compromised account', '172.16.2.12', NOW()),
('user13@example.com', 'b5c6d7e8-f9a0-42b1-b2c3-d4e5f6a7b8c9', 'Policy violation', '192.168.4.13', NOW()),
('user14@example.com', 'c6d7e8f9-a0b1-43c2-b3d4-e5f6a8b9c0d1', 'User request', '10.0.3.14', NOW()),
('user15@example.com', 'd7e8f9a0-b1c2-44d3-b4e5-f6a7b8c9d0e1', 'Suspicious activity', '172.16.3.15', NOW()),
('user16@example.com', 'e8f9a0b1-c2d3-45e4-b5f6-a7b8c9d0e1f2', 'Too many login attempts', '192.168.5.16', NOW()),
('user17@example.com', 'f9a0b1c2-d3e4-46f5-b6a7-b8c9d0e1f2a3', 'Reported by admin', '10.0.4.17', NOW()),
('user18@example.com', 'a0b1c2d3-e4f5-47a6-b7b8-c9d0e1f2a3b4', 'Phishing attempt', '172.16.4.18', NOW()),
('user19@example.com', 'b1c2d3e4-f5a6-48b7-b8c9-d0e1f2a3b4c5', 'Bot traffic', '192.168.6.19', NOW()),
('user20@example.com', 'c2d3e4f5-a6b7-49c8-b9d0-e1f2a3b4c5d6', 'Fake email address', '10.0.5.20', NOW());

