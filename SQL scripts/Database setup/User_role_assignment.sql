USE Momoflow;

CREATE TABLE IF NOT EXISTS User_role_assignment (
    user_id INT NOT NULL,
    role_id INT NOT NULL,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES Users(UniqueID),
    FOREIGN KEY (role_id) REFERENCES User_role(role_id)
);
