-- Esquema MySQL equivalente a app/models.py.
-- La aplicación puede crear estas tablas automáticamente con scripts/init_db.py.

CREATE DATABASE IF NOT EXISTS gym_manager CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE gym_manager;

CREATE TABLE trainers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(120) NOT NULL,
    specialty VARCHAR(100) NOT NULL,
    phone VARCHAR(30) NOT NULL,
    email VARCHAR(160) NOT NULL,
    active BOOLEAN NOT NULL DEFAULT TRUE
) ENGINE=InnoDB;

CREATE TABLE clients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(160) NOT NULL UNIQUE,
    phone VARCHAR(30) NOT NULL,
    birth_date DATE NULL,
    goal VARCHAR(200) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Activo',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE disciplines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    category VARCHAR(80) NOT NULL,
    schedule VARCHAR(120) NOT NULL,
    capacity INT NOT NULL,
    monthly_fee DECIMAL(10,2) NOT NULL DEFAULT 0,
    description TEXT NOT NULL,
    trainer_id INT NOT NULL,
    CONSTRAINT ck_discipline_capacity_positive CHECK (capacity > 0),
    CONSTRAINT ck_discipline_fee_nonnegative CHECK (monthly_fee >= 0),
    CONSTRAINT fk_discipline_trainer FOREIGN KEY (trainer_id) REFERENCES trainers(id)
) ENGINE=InnoDB;

CREATE TABLE memberships (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    plan_name VARCHAR(80) NOT NULL,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Activa',
    monthly_fee DECIMAL(10,2) NOT NULL DEFAULT 0,
    CONSTRAINT ck_membership_dates CHECK (end_date >= start_date),
    CONSTRAINT fk_membership_client FOREIGN KEY (client_id) REFERENCES clients(id)
) ENGINE=InnoDB;

CREATE TABLE enrollments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    discipline_id INT NOT NULL,
    enrolled_on DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'Activa',
    notes TEXT NOT NULL,
    CONSTRAINT uq_client_discipline UNIQUE (client_id, discipline_id),
    CONSTRAINT fk_enrollment_client FOREIGN KEY (client_id) REFERENCES clients(id),
    CONSTRAINT fk_enrollment_discipline FOREIGN KEY (discipline_id) REFERENCES disciplines(id)
) ENGINE=InnoDB;

CREATE TABLE sales (
    id INT AUTO_INCREMENT PRIMARY KEY,
    client_id INT NOT NULL,
    membership_id INT NULL,
    concept VARCHAR(160) NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    sale_date DATE NOT NULL,
    payment_method VARCHAR(30) NOT NULL DEFAULT 'Efectivo',
    status VARCHAR(20) NOT NULL DEFAULT 'Pagada',
    CONSTRAINT ck_sale_amount_positive CHECK (amount > 0),
    CONSTRAINT fk_sale_client FOREIGN KEY (client_id) REFERENCES clients(id),
    CONSTRAINT fk_sale_membership FOREIGN KEY (membership_id) REFERENCES memberships(id)
) ENGINE=InnoDB;
