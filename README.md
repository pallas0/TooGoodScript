# Too Good To Go SMS Alerts - Backend

## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Database Design](#database-design)
- [Screenshots](#screenshots)

## Description

The Too Good To Go SMS Alerts backend is responsible for populating and managing a database of users and their favorite stores' updates from the Too Good To Go platform. It sends SMS alerts to users when new batches of items become available from their favorite stores.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/your-username/too-good-sms-alerts-backend.git

2. **Navigate to the Project Directory:**
   ```bash
   cd too-good-sms-alerts-backend
3. **Install Dependencies:**
   Use 'pip'  to install the required Python dependencies from the 'requirements.txt' file:
   ```bash
   pip install -r requirements.txt

## Usage
1. **Run the Application Locally:**
   You can run the backend locally using Flask. Make sure you are in the project directory.
   ```bash
   flask run
   ```
   The backend should now be accessible at 'http://localhost:5000'.
2. **API Endpoints:**
   
   * /submit_subscriber_info: POST request to submit user information and start receiving SMS alerts.

   * /sms: Webhook for processing incoming SMS messages, including opt-out requests.

   * Customize and expand the endpoints based on your application's requirements.
  
## Database Design

The Too Good To Go SMS Alerts backend utilizes a relational database to store user and store information. The database consists of three main tables:

1. **Subscriber Table:**

   - **Fields:**
     - `id` (Primary Key): A unique identifier for each subscriber.
     - `email`: The email address of the subscriber.
     - `phone_number`: The phone number of the subscriber.

   - **Relationships:**
     - Each subscriber can have one associated `Credentials` object.
     - Each subscriber can have multiple associated `Favorite` objects.

2. **Credentials Table:**

   - **Fields:**
     - `id` (Primary Key): A unique identifier for each set of credentials.
     - `access_token`: The access token for accessing the Too Good To Go API.
     - `refresh_token`: The refresh token for renewing access.
     - `user_id`: The user ID associated with these credentials.
     - `cookie`: A cookie used for authentication.

   - **Relationships:**
     - Each set of credentials belongs to one subscriber.

3. **Favorites Table:**

   - **Fields:**
     - `id` (Primary Key): A unique identifier for each favorite store.
     - `store_name`: The name of the favorite store.
     - `bags_available`: A boolean indicating whether bags are currently available at the store.

   - **Relationships:**
     - Each favorite store belongs to one subscriber.

This relational database design allows for efficient storage and retrieval of subscriber data, their associated credentials, and their favorite stores' availability status. The relationships between tables ensure data integrity and enable complex queries to provide SMS alerts based on user preferences.


## Screenshots

  
