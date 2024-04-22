CREATE TABLE IF NOT EXISTS currencies_rub (
    name VARCHAR(5) NOT NULL,
    to_rub FLOAT NOT NULL,
    updated_at TIMESTAMP DEFAULT NOW(),
    PRIMARY KEY(name)
)