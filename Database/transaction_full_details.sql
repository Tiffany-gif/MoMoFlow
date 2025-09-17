-- View showing full details of each transaction in one go

CREATE VIEW transaction_full_details AS
SELECT
  
  --Transaction info
  
    t.Transaction_id,
    t.transaction_ref,
    t.amount,
    t.currency,
    t.transaction_date,
    t.status,
    
    -- Sender account info
  
    s_acc.account_number AS sender_account_number,
    s_user.Full_name AS sender_name,
    s_user.Phone_number AS sender_phone,
    
    -- Receiver account info
  
    r_acc.account_number AS receiver_account_number,
    r_user.Full_name AS receiver_name,
    r_user.Phone_number AS receiver_phone,
    
    -- Transaction category
    c.category_name AS transaction_category,
    
    -- Related logs
  
    GROUP_CONCAT(CONCAT(ul.log_type, ': ', ul.message, ' (', ul.created_at, ')') SEPARATOR ' | ') AS related_logs

FROM Transactions t

-- Joining sender account and its user
  
LEFT JOIN Accounts s_acc ON t.sender_account = s_acc.Account_id
LEFT JOIN Users s_user ON s_acc.user_id = s_user.UniqueID

-- Joining receiver account and its user
  
LEFT JOIN Accounts r_acc ON t.receiver_account = r_acc.Account_id
LEFT JOIN Users r_user ON r_acc.user_id = r_user.UniqueID

-- Transaction category
  
LEFT JOIN Transaction_Categories c ON t.Category_id = c.Category_id

-- Joining logs
  
LEFT JOIN User_log ul ON t.Transaction_id = ul.transaction_id

GROUP BY t.Transaction_id;
