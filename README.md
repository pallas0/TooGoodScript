# Too Good To Go SMS Alerts

TLDR: I enjoy the too good to go app, but it's annoying that I have to constantly check the app to see if my favorite restaurants have food available. Often, the hottest restaurants' bags run out in seconds. I therefore made a web app that anyone can sign up for that constantly hits the too good to go API and checks if there are bags available for any of a users favorite restaurants.  **Sign up and get your food [here](too-good-frontend.vercel.app/)**.

This specific repository contains the backend code. The frontend can be found [here](https://github.com/pallas0/TooGood_frontend). 

The Too Good To Go SMS Alerts backend is responsible for populating and managing a database of users and their favorite stores' updates from the Too Good To Go platform. It sends SMS alerts to users when new batches of items become available from their favorite stores.

## Demo / Screenshots
The demo vid is [here](https://www.loom.com/share/3556ac04a23b4d558a907021f58896c3?sid=9130706b-a8ca-46ce-b359-57f46fbdb13b).

<img width="846" alt="Screenshot 2023-09-07 at 3 10 34 PM" src="https://github.com/pallas0/TooGood_frontend/assets/52135849/29d27323-00ac-4a17-8e04-cdb21521dd9a">


<img width="1438" alt="Screenshot 2023-09-13 at 12 44 24 PM" src="https://github.com/pallas0/TooGoodScript/assets/52135849/209ca81c-02ee-43bb-8469-08e4939a6b89">

![IMG_7084](https://github.com/pallas0/TooGoodScript/assets/52135849/2cd832b6-bf76-47c7-a4c3-1535d0b98792)

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
   * /favorites: GET request to return all favorites in database
   * /subscribers: GET request to return all subscribers in database
   * /credentials: GET request to return all credentials in database
   * /sms: Webhook for processing incoming SMS messages, including opt-out requests.

   * Customize and expand the endpoints based on your application's requirements.
  
## Database Design

The Too Good To Go SMS Alerts backend utilizes a relational database to store user and store information. The database consists of three main tables:

<img width="1173" alt="Screenshot 2023-09-13 at 12 50 51 PM" src="https://github.com/pallas0/TooGoodScript/assets/52135849/6fc48467-96e0-42f6-bf02-59b67ae7cd99">

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



  
