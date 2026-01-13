# Social-Media-API-Project
Useful links:
- DockerHub: https://hub.docker.com/repositories/jadonay123
- Render Deployment: https://social-media-api-project-dglt.onrender.com
- Ubuntu web deployment: https://jadonsapi.me/docs


Section 1: Introduction
- Introduces the course project and overall goals.
- Explains what the course will cover and how the project fits into it.
- Provides a high‑level overview of the final application.
Section 2: Setup & Installation
- Shows how to install Python on both Mac and Windows.
- Walks through installing and configuring VS Code on both platforms.
- Explains Python virtual environments and how to create them on each OS.
Section 3: FastAPI
- Covers installing dependencies and starting a FastAPI server.
- Teaches path operations, ordering rules, and basic routing.
- Introduces Postman and demonstrates sending HTTP requests.
- Implements POST, GET, DELETE, and PUT operations.
- Adds schema validation with Pydantic.
- Builds CRUD logic and stores posts in memory.
- Shows how to use automatic API documentation.
Section 4: Databases
- Introduces relational databases and PostgreSQL installation on both OSes.
- Explains schemas, tables, and using PgAdmin.
- Teaches SQL basics: SELECT, WHERE, operators, LIKE, IN, ORDER BY, LIMIT, OFFSET.
- Demonstrates inserting, updating, and deleting data.
Section 5: Python + Raw SQL
- Sets up the application database connection.
- Connects Python directly to PostgreSQL.
- Implements raw SQL queries for retrieving, creating, updating, and deleting posts.
Section 6: ORMs
- Introduces ORMs and SQLAlchemy.
- Sets up SQLAlchemy models and adds timestamps.
- Replaces raw SQL with ORM queries for CRUD operations.
Section 7: Pydantic Models
- Explains differences between ORM models and Pydantic models.
- Builds Pydantic schemas and response models for cleaner API output.
Section 8: Authentication & Users
- Creates a users table and registration endpoint.
- Implements password hashing and refactors hashing logic.
- Adds user retrieval and organizes routes with routers, prefixes, and tags.
- Introduces JWT authentication and login flow.
- Generates tokens and validates logged‑in users.
- Protects routes and handles expired tokens.
- Uses Postman for advanced testing.
Section 9: Relationships
- Explains relational concepts and foreign keys.
- Adds user–post relationships in SQLAlchemy.
- Ensures posts are tied to owners and restricts updates/deletes to owners only.
- Retrieves posts belonging to the logged‑in user.
- Introduces SQLAlchemy relationships and query parameters.
- Cleans up the main application file and adds environment variables.
Section 10: Vote/Like System
- Introduces the voting/liking feature.
- Creates a votes table and SQLAlchemy model.
- Implements vote routes and logic.
- Teaches SQL joins and applies them in SQLAlchemy.
- Retrieves posts with aggregated join data.
Section 11: Database Migration with Alembic
- Explains what migration tools do and why they matter.
- Sets up Alembic and creates the first migration.
- Demonstrates rolling back and completing schema migrations.
- Disables SQLAlchemy’s automatic table creation in favor of Alembic.
Section 12: Pre‑Deployment Checklist
- Explains CORS and how to configure it.
- Covers Git prerequisites, installation, and GitHub setup for deployment.
Section 13: Render deployment
- Created a Render app
- Added Environment Variables to Render environment
- Created a postgres Database and migrated it onto Render using alembic
- pushed changes into production
