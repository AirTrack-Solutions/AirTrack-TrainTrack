-- TrainTrack 1.0.0
-- Copyright (c) 2025 Trevor ("Subhuti"). All rights reserved.
-- SPDX-License-Identifier: LicenseRef-TrainTrack-Proprietary-NC

-- schema.sql
-- Full TrainTrack database schema.
-- Run once on a fresh MariaDB instance.

SET NAMES utf8mb4;
SET foreign_key_checks = 0;

-- ---------------------------------------------------------------------------
-- countries
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS countries (
    code        CHAR(2)      NOT NULL,
    name        VARCHAR(100) NOT NULL,
    PRIMARY KEY (code)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------------------------
-- types  (Steam / Diesel / Electric / DMU / EMU / Tram / HST / Other)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS types (
    id          INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name        VARCHAR(50)  NOT NULL UNIQUE,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT IGNORE INTO types (name) VALUES
    ('Steam'),
    ('Diesel'),
    ('Electric'),
    ('DMU'),
    ('EMU'),
    ('Tram'),
    ('HST'),
    ('Other');

-- ---------------------------------------------------------------------------
-- operators
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS operators (
    id          INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name        VARCHAR(150) NOT NULL,
    code        VARCHAR(20)  DEFAULT NULL,
    country_code CHAR(2)     DEFAULT NULL,
    type        ENUM('passenger','freight','heritage','other') DEFAULT 'passenger',
    logo        VARCHAR(255) DEFAULT NULL,
    notes       TEXT         DEFAULT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (country_code) REFERENCES countries(code) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------------------------
-- depots
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS depots (
    id          INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name        VARCHAR(150) NOT NULL,
    code        VARCHAR(20)  DEFAULT NULL,
    operator_id INT UNSIGNED DEFAULT NULL,
    country_code CHAR(2)     DEFAULT NULL,
    notes       TEXT         DEFAULT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (operator_id) REFERENCES operators(id) ON DELETE SET NULL,
    FOREIGN KEY (country_code) REFERENCES countries(code) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------------------------
-- classes
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS classes (
    id              INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name            VARCHAR(100) NOT NULL,
    type_id         INT UNSIGNED DEFAULT NULL,
    manufacturer    VARCHAR(100) DEFAULT NULL,
    introduced_year YEAR         DEFAULT NULL,
    country_code    CHAR(2)      DEFAULT NULL,
    description     TEXT         DEFAULT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (type_id) REFERENCES types(id) ON DELETE SET NULL,
    FOREIGN KEY (country_code) REFERENCES countries(code) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------------------------
-- locomotives
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS locomotives (
    id              INT UNSIGNED NOT NULL AUTO_INCREMENT,
    number          VARCHAR(50)  NOT NULL,
    name            VARCHAR(150) DEFAULT NULL,   -- named locos e.g. "Flying Scotsman"
    class_id        INT UNSIGNED DEFAULT NULL,
    type_id         INT UNSIGNED DEFAULT NULL,
    operator_id     INT UNSIGNED DEFAULT NULL,
    depot_id        INT UNSIGNED DEFAULT NULL,
    livery          VARCHAR(100) DEFAULT NULL,
    built_year      YEAR         DEFAULT NULL,
    status          ENUM('active','withdrawn','preserved','stored','scrapped','maintenance','transferred') DEFAULT 'active',
    country_code    CHAR(2)      DEFAULT NULL,
    notes           TEXT         DEFAULT NULL,
    image           VARCHAR(255) DEFAULT NULL,
    date_added      DATETIME     DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_loco_number (number),
    FOREIGN KEY (class_id)     REFERENCES classes(id)    ON DELETE SET NULL,
    FOREIGN KEY (type_id)      REFERENCES types(id)      ON DELETE SET NULL,
    FOREIGN KEY (operator_id)  REFERENCES operators(id)  ON DELETE SET NULL,
    FOREIGN KEY (depot_id)     REFERENCES depots(id)     ON DELETE SET NULL,
    FOREIGN KEY (country_code) REFERENCES countries(code) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------------------------
-- formations  (multiple unit sets — e.g. Class 158 3-car set)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS formations (
    id          INT UNSIGNED NOT NULL AUTO_INCREMENT,
    set_number  VARCHAR(50)  NOT NULL,
    class_id    INT UNSIGNED DEFAULT NULL,
    operator_id INT UNSIGNED DEFAULT NULL,
    status      ENUM('active','withdrawn','preserved','stored','scrapped','maintenance','transferred') DEFAULT 'active',
    notes       TEXT         DEFAULT NULL,
    date_added  DATETIME     DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY uq_set_number (set_number),
    FOREIGN KEY (class_id)    REFERENCES classes(id)   ON DELETE SET NULL,
    FOREIGN KEY (operator_id) REFERENCES operators(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------------------------
-- formation_vehicles  (individual cars within a formation)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS formation_vehicles (
    id              INT UNSIGNED NOT NULL AUTO_INCREMENT,
    formation_id    INT UNSIGNED NOT NULL,
    vehicle_number  VARCHAR(50)  NOT NULL,
    position        TINYINT UNSIGNED DEFAULT NULL,  -- car 1, 2, 3...
    vehicle_type    VARCHAR(50)  DEFAULT NULL,      -- DMC, MS, DTSO etc
    notes           TEXT         DEFAULT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (formation_id) REFERENCES formations(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------------------------
-- locations
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS locations (
    id          INT UNSIGNED NOT NULL AUTO_INCREMENT,
    name        VARCHAR(150) NOT NULL,
    station_code VARCHAR(10) DEFAULT NULL,    -- CRS/IATA/UIC codes
    line        VARCHAR(150) DEFAULT NULL,
    country_code CHAR(2)     DEFAULT NULL,
    lat         DECIMAL(9,6) DEFAULT NULL,
    lng         DECIMAL(9,6) DEFAULT NULL,
    notes       TEXT         DEFAULT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (country_code) REFERENCES countries(code) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------------------------
-- sightings
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS sightings (
    id              INT UNSIGNED NOT NULL AUTO_INCREMENT,
    -- Link to either a locomotive OR a formation (not both)
    locomotive_id   INT UNSIGNED DEFAULT NULL,
    formation_id    INT UNSIGNED DEFAULT NULL,
    -- When and where
    sighting_date   DATE         NOT NULL,
    sighting_time   TIME         DEFAULT NULL,
    location_id     INT UNSIGNED DEFAULT NULL,
    -- Service details
    working         VARCHAR(50)  DEFAULT NULL,   -- headcode / service number
    direction       VARCHAR(50)  DEFAULT NULL,   -- Up / Down / Northbound etc
    -- Cops & dubs
    is_cop          TINYINT(1)   NOT NULL DEFAULT 1,  -- 1=cop (first sighting), 0=dub
    cop_date        DATE         DEFAULT NULL,         -- date of first ever sighting
    -- Haulage
    hauled_by       INT UNSIGNED DEFAULT NULL,    -- locomotive_id of traction if formation hauled
    -- Extra
    notes           TEXT         DEFAULT NULL,
    image           VARCHAR(255) DEFAULT NULL,
    date_added      DATETIME     DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    -- Ensure sighting links to exactly one subject
    CONSTRAINT chk_subject CHECK (
        (locomotive_id IS NOT NULL AND formation_id IS NULL) OR
        (locomotive_id IS NULL AND formation_id IS NOT NULL)
    ),
    FOREIGN KEY (locomotive_id) REFERENCES locomotives(id) ON DELETE CASCADE,
    FOREIGN KEY (formation_id)  REFERENCES formations(id)  ON DELETE CASCADE,
    FOREIGN KEY (location_id)   REFERENCES locations(id)   ON DELETE SET NULL,
    FOREIGN KEY (hauled_by)     REFERENCES locomotives(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------------------------
-- haulage  (detailed haulage log — child of a sighting)
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS haulage (
    id              INT UNSIGNED NOT NULL AUTO_INCREMENT,
    sighting_id     INT UNSIGNED NOT NULL,
    service_number  VARCHAR(50)  DEFAULT NULL,
    origin          VARCHAR(150) DEFAULT NULL,
    destination     VARCHAR(150) DEFAULT NULL,
    stock_desc      TEXT         DEFAULT NULL,  -- free text description of coaches
    notes           TEXT         DEFAULT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (sighting_id) REFERENCES sightings(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ---------------------------------------------------------------------------
-- app_settings
-- ---------------------------------------------------------------------------
CREATE TABLE IF NOT EXISTS app_settings (
    SettingKey      VARCHAR(100) NOT NULL,
    SettingValue    TEXT         DEFAULT NULL,
    PRIMARY KEY (SettingKey)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT IGNORE INTO app_settings (SettingKey, SettingValue) VALUES
    ('FirstName',   ''),
    ('LastName',    ''),
    ('Callsign',    ''),
    ('timezone',    'UTC'),
    ('Theme',       'default');

SET foreign_key_checks = 1;
