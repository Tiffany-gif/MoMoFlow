USE Momoflow;

CREATE TABLE IF NOT EXISTS User_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    log_type VARCHAR(50),
    message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    transaction_id INT,
    FOREIGN KEY (transaction_id) REFERENCES Transactions(transaction_id)
);
