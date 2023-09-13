# Too Good To Go SMS Alerts - Backend

## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
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
  
