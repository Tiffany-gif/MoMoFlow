USE Momoflow;

CREATE TABLE IF NOT EXISTS Transactions (
    Transaction_id INT AUTO_INCREMENT PRIMARY KEY,
    transaction_ref VARCHAR(50) UNIQUE NOT NULL,
    amount DECIMAL(15,2) NOT NULL,
    currency VARCHAR(10) NOT NULL,
    transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending','completed','failed') NOT NULL,
    sender_id INT NOT NULL,
    receiver_id INT NOT NULL,
    category_id INT NOT NULL,
    FOREIGN KEY (sender_id) REFERENCES Users(UniqueID),
    FOREIGN KEY (receiver_id) REFERENCES Users(UniqueID),
    FOREIGN KEY (category_id) REFERENCES Transaction_Categories(Category_id)
);
