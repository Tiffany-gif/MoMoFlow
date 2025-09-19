# MoMoFlow

## Team Name
Group 3

## Project Description
**MoMoFlow** is a tool designed for shop owners, freelancers, and small businesses that rely on MTN MoMo transactions. The system processes MoMo SMS data (in XML format), cleans and categorizes the data, and stores it in a relational database.  

On the frontend, a dashboard provides insights into:
- Cash-in (sales) vs Cash-out (expenses)  
- Daily, weekly, and monthly cashflow trends  
- Detection of high-value clients and frequent suppliers  
- Overall business performance overview  

This project demonstrates **ETL (Extract, Transform, Load) pipelines, relational database management, and frontend visualization** skills in a collaborative Agile workflow.

## System Architecture

The diagram below illustrates the overall flow of MoMoFlow, from data extraction to visualization
[View our Architecture Diagram here](https://app.diagrams.net/#G1eqeeRP8Qi9qhRQbUf0_CcVbUrzm4lOa5#%7B%22pageId%22%3A%22KhwDIHSNujK45m27qN_c%22%7D)


## Team Members
- Emma Tiffany Umwari – Tiffanygif 
- Keyla Bineza Nyacyesa – KeylaNyacyesa  
- Julius Kate Lorna Iriza – k10-j  

## Scrum Board 
We are using GitHub Projects to manage our Agile Workflow.
[View our Scrum Board here](https://github.com/users/Tiffany-gif/projects/1)

# Documentation
Database Design Documentation

The MoMoFlow database schema was designed for secure, scalable, and extensible processing of mobile money. At its core, the Users table manages customer identity and enforces unique phone numbers as the sole contact and authentication column. To provide system flexibility, user access levels are split into a User_role table, with a User_role_assignment many-to-many junction table enabling an M:N relationship. This design allows for a single user to have multiple roles (e.g., customer, admin) and supports role integrity.

The Accounts table is the users' financial wallet presentation, with account number uniqueness and direct reference to users through one-to-many (1:N) relationship. Transactions go through the Transactions table, which enforces necessary constraints such as unique transaction references, positive amounts, and non-null sender/receiver accounts. This ensures data correctness and prevents incorrect financial postings.

To support categorization and reporting, Transaction_Categories provide a structured classification of payments (e.g., bills, transfers, airtime). This improves usability, analysis, and regulatory compliance. Meanwhile, User_log logs system and transaction events with time stamps to maintain traceability, accountability, and audit-readiness.

The crow's foot notation facilitates easy expression of cardinalities and separating concerns in tables prevents redundancy and improves normalization. The junction table design was chosen as the best way to support complex user-role relationships without sacrificing database integrity.

Overall, this ERD is generally balanced between relational integrity, performance, and extensibility to support the needs of MoMoFlow as a secure financial service and as a user growth platform.
