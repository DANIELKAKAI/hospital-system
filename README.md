# Blog Api

## Local Installation and Setup

1. Make sure you have Python3 and Postgresql installed on your machine.

   https://www.python.org/

   https://www.postgresql.org/download/

2. Install Virtualenv and create a virtual environment

   ` pip install virtualenv`

   ` virtualenv -p python3 env`

   ` source env/bin/activate`

3. Clone the repo and install requirements

   `git clone https://github.com/DANIELKAKAI/MiniBloggingApp-test`

   `cd MiniBloggingApp-test`

   `pip install -r requirements.txt`

4. Create a .env file for environment variables

   ```text
   DJANGO_ENVIRONMENT=DEVELOPMENT or PRODUCTION
   DJANGO_SECRET_KEY=
   DB_NAME=
   DB_USER=
   DB_PASSWORD=
   DB_HOST=
   DB_PORT=
   ```

5. Start development server

   `python manage.py migrate`

   `python manage.py runserver`

6. Run tests

   `python manage.py tests`

## Docker Installation and Setup

1. Make sure you have Docker installed on your machine.

   https://www.docker.com/get-started/

2. Start the docker containers

   `docker compose up`

## Example Api Usage

### Sign Up Doctor

#### Request

```shell
curl --location 'http://127.0.0.1:8000/users/doctor' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email":"doc6@gmail.com",
    "full_name":"fname lname",
    "password":"password",
    "role":"doctor"
}'
```

#### Response

```json
{
    "id": "eda9f6ac-65e9-4ca6-b01b-7aabae3492de",
    "full_name": "fname lname",
    "email": "doc6@gmail.com",
    "role": "doctor"
}
```

### Sign Up Patient

#### Request

```shell
curl --location 'http://127.0.0.1:8000/users/patient' \
--header 'Authorization: Bearer <access_token>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email":"patient2@gmail.com",
    "full_name":"fname lname",
    "password":"password",
    "role":"patient"
}'
```

#### Response

```json
{
    "id": "00aa72bf-304e-4d59-8e8c-3979553e0bbd",
    "full_name": "fname lname",
    "email": "patient2@gmail.com",
    "role": "patient"
}
```

### Login User

#### Request

```shell
curl --location 'http://127.0.0.1:8000/login' \
--header 'Content-Type: application/json' \
--data-raw '{
    "email":"doc4@gmail.com",
    "password":"password"
}'
```

#### Response

```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

### Create Booking

#### Request

```shell
curl --location 'http://127.0.0.1:8000/booking/' \
--header 'Authorization: Bearer <access_token>' \
--header 'Content-Type: application/json' \
--data '{
    "doctor_id":"d07ce5a5-c4de-40d1-b75c-8cb33b7ef986",
    "start_time":"2023-10-27T19:31:00Z",
    "end_time":"2023-10-27T20:30:00Z"
}'
```

#### Response

```json
{
    "id": "7f11ad2f-4a4f-43e5-9913-efa675387f2b",
    "doctor": {
        "id": "d07ce5a5-c4de-40d1-b75c-8cb33b7ef986",
        "email": "doc4@gmail.com",
        "full_name": "fname lname",
        "role": "doctor"
    },
    "patient": {
        "id": "ebe23f04-00f8-4dbf-8a78-76ae2c413091",
        "email": "patient1@gmail.com",
        "full_name": "fname lname",
        "role": "patient"
    },
    "start_time": "2023-10-27T19:31:00Z",
    "end_time": "2023-10-27T20:30:00Z"
}
```

### List Bookings

#### Request

```shell
curl --location 'http://127.0.0.1:8000/booking/' \
--header 'Authorization: Bearer <access_token>'
```

#### Response

```json
[
    {
        "id": "790cdc57-6511-42b4-9b2d-373fbd849a9f",
        "doctor": {
            "id": "d07ce5a5-c4de-40d1-b75c-8cb33b7ef986",
            "email": "doc4@gmail.com",
            "full_name": "",
            "role": "doctor"
        },
        "patient": {
            "id": "ebe23f04-00f8-4dbf-8a78-76ae2c413091",
            "email": "patient1@gmail.com",
            "full_name": "",
            "role": "patient"
        },
        "start_time": "2023-10-27T15:30:00Z",
        "end_time": "2023-10-27T17:30:00Z"
    },
   ...
]
```