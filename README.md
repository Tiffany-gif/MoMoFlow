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

When building the MoMoFlow database, our goal was to make it both reliable and flexible, since it needs to handle sensitive mobile money transactions while also being easy to scale as the system grows.

We started with the Users table, which stores customer information. Every user must have a unique phone number, since that’s the main way people identify themselves in mobile money systems. From there, each user can have multiple Accounts (for example, a personal wallet and a business wallet). This one-to-many setup makes sense because one person can manage different accounts, but every account always belongs to one specific user.

To manage system access, we created a User_role table and linked it to users through a User_role_assignment table. This design allows a single user to take on more than one role (like being both a customer and an admin) while keeping the database clean and organized.

The heart of the system is the Transactions table. It keeps track of every payment or transfer and makes sure key details like reference numbers, sender/receiver accounts, and amounts are valid. We also added Transaction_Categories to organize transactions into groups (like bills, transfers, airtime). This makes reporting and analysis much easier.

Finally, the User_log table records what happens with each transaction, creating an audit trail for transparency and accountability.

Altogether, this design avoids redundancy, enforces strong rules for data integrity, and leaves room for MoMoFlow to expand as the platform grows.
