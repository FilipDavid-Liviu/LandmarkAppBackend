# Landmark App Backend

The Landmark App Backend is a robust service designed to support the Landmark App, providing comprehensive RESTful API endpoints for managing landmarks, users, and associated data. Built with FastAPI, this backend ensures efficient and scalable operations, seamlessly integrating with the frontend to deliver a cohesive user experience.

## Features

-   **FastAPI Framework**: Utilizes FastAPI for building fast and efficient web APIs.
-   **Database Integration**: Uses SQLAlchemy for ORM and database interactions.
-   **Controlled CRUD Operations**: Supports read operations for landmarks without requiring authentication, while create, update, and delete operations are restricted to users with admin privileges.
-   **User Authentication with JWT**: Implements JSON Web Tokens (JWT) for secure user session management, ensuring user data privacy and integrity.
-   **Role-Based Access Control**: Enforces authentication and privilege checks to ensure that only authorized users can perform specific actions.
-   **Saved Landmarks Management**: Provides endpoints for users to save and manage their favorite landmarks, enhancing user personalization.
-   **Admin Monitoring and Management**: Admin endpoints allow for monitoring user activities, particularly to identify and manage users who may be spamming actions, ensuring the integrity and performance of the service.
-   **Static Files**: Capable of serving static files required by the application.
