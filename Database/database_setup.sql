-- Database Setup

CREATE DATABASE IF NOT EXISTS Momoflow;
USE Momoflow;

-- Users Table

CREATE TABLE IF NOT EXISTS Users (
    UniqueID INT AUTO_INCREMENT PRIMARY KEY COMMENT 'User ID',
    Full_name VARCHAR(100) NOT NULL COMMENT 'Full name of the user',
    Phone_number VARCHAR(15) UNIQUE NOT NULL COMMENT 'User phone number',
    CHECK (CHAR_LENGTH(Phone_number) BETWEEN 10 AND 15)
);

CREATE INDEX idx_phone_number ON Users (Phone_number);

-- Accounts Table

CREATE TABLE IF NOT EXISTS Accounts (
    Account_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Account ID',
    account_number VARCHAR(20) UNIQUE NOT NULL COMMENT 'MoMo account number',
    user_id INT NOT NULL COMMENT 'User ID of owner of this account',
    account_type ENUM('Personal','Business','Agent') DEFAULT 'Personal' COMMENT 'Type of account',
    FOREIGN KEY (user_id) REFERENCES Users(UniqueID)
);

CREATE INDEX idx_account_number ON Accounts (account_number);

-- User Roles Table

CREATE TABLE IF NOT EXISTS User_role (
    role_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Role ID',
    role_name VARCHAR(50) NOT NULL COMMENT 'Role name: Admin, Customer'
);

-- Transaction Categories Table

CREATE TABLE IF NOT EXISTS Transaction_Categories (
    Category_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Category ID',
    category_name VARCHAR(50) NOT NULL COMMENT 'Transaction category: Cash-in, Cash-out, Purchase'
);

-- Transactions Table

CREATE TABLE IF NOT EXISTS Transactions (
    Transaction_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Transaction ID',
    transaction_ref VARCHAR(50) UNIQUE NOT NULL COMMENT 'Transaction reference number',
    amount DECIMAL(15,2) NOT NULL COMMENT 'Transaction amount',
    currency VARCHAR(10) NOT NULL COMMENT 'Currency used',
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Date and time of transaction',
    status ENUM('Pending','Completed','Failed') NOT NULL COMMENT 'Current status of the transaction',
    sender_account INT NOT NULL COMMENT 'Account that sent money',
    receiver_account INT NOT NULL COMMENT 'Account that received money',
    Category_id INT NOT NULL COMMENT 'Transaction category reference',
    FOREIGN KEY (sender_account) REFERENCES Accounts(Account_id),
    FOREIGN KEY (receiver_account) REFERENCES Accounts(Account_id),
    FOREIGN KEY (Category_id) REFERENCES Transaction_Categories(Category_id),
    CHECK (amount > 0)
);

CREATE INDEX idx_transaction_ref ON Transactions (transaction_ref);
CREATE INDEX idx_transaction_date ON Transactions (transaction_date);

-- User Role Assignment Table

CREATE TABLE IF NOT EXISTS User_role_assignment (
    user_id INT NOT NULL COMMENT 'User ID being assigned role',
    role_id INT NOT NULL COMMENT 'Role assigned to the user',
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES Users(UniqueID),
    FOREIGN KEY (role_id) REFERENCES User_role(role_id)
);

-- User Log Table

CREATE TABLE IF NOT EXISTS User_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Log entry ID',
    log_type ENUM('INFO','ERROR','WARNING') NOT NULL COMMENT 'Type of log',
    message TEXT COMMENT 'Detailed log message',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Time of log creation',
    transaction_id INT COMMENT 'Related transaction ID if applicable',
    FOREIGN KEY (transaction_id) REFERENCES Transactions(Transaction_id)
);
