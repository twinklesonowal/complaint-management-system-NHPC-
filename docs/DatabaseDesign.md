# Database Design

## Table: Users

| Field | Type | Description |
|--------|------|-------------|
| id | Integer | Primary Key |
| full_name | Text | User's full name |
| username | Text | Login username |
| password | Text | Encrypted password |
| role | Text | Employee / IT Staff / IT Manager |
| department | Text | User department |
| email | Text | Official email |
| status | Text | Active / Inactive |
| created_at | DateTime | Account creation date |