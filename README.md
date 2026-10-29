# Flask SQLAlchemy Serialization Lab

A full-stack backend application built with **Flask**, **Flask-SQLAlchemy**, **Flask-Migrate**, and **Marshmallow** featuring many-to-many relationships, association proxies, and robust object serialization.

## Features
* **Many-to-Many Relationships**: Manages customers, items, and reviews.
* **Association Proxies**: Simplifies accessing related data across models.
* **Serialization**: Uses Marshmallow and `marshmallow-sqlalchemy` to serialize models cleanly without circular reference issues.
* **Test-Driven Development**: Verified with a comprehensive `pytest` suite.

## Project Setup

1. **Clone the repository:**
   ```bash
   git clone <YOUR_FORKED_REPO_URL>
   cd flask-sqlalchemy-serialization-lab