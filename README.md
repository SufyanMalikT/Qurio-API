# 🧠 Qurio API

Qurio API is a **Django REST Framework-based Question & Answer platform**, similar to Stack Overflow — where users can ask questions, post answers, tag topics, and vote on the best responses.


## 🚀 Features

- 🔐 **JWT Cookie Authentication** (Secure login using HttpOnly cookies)
- 👤 **Custom User Model** with password validation and hashing
- 🧵 **Nested Routes Support**
  - `/tags/{id}/questions/` → Questions under a specific tag  
  - `/questions/{id}/answers/` → Answers under a specific question  
- 📑 **Pagination, Filtering & Search**
  - Search questions or users by keywords  
  - Paginated responses for large datasets
- 🗳️ **Voting System**
  - Upvote or downvote answers  
  - Prevents duplicate votes with `update_or_create()`
- 🏷️ **Tag Management**
  - Create, attach, or list tags for questions
- ⚙️ **Rate Limiting & Throttling**
  - Custom burst and sustained throttles to prevent abuse
- 🌐 **CORS Support** for frontend integration (React or others)
- 🧩 **Environment-based Configuration**
  - `.env` file for sensitive settings (DB, Secret Keys, Debug mode)
- 🧱 **Custom Middleware**
  - Includes a timer middleware for tracking request duration



## 🧰 Tech Stack

- **Backend:** Django 5.2 + Django REST Framework  
- **Authentication:** JWT (via `rest_framework_simplejwt`)  
- **Database:** PostgreSQL (configurable via `.env`)  
- **Other Tools:**  
  - `django-cors-headers`  
  - `python-dotenv`



## ⚙️ Setup Instructions

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/SufyanMalikT/Qurio-API.git
cd Qurio-API 
```

### 2️⃣ Create and Activate a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate     # (Linux/Mac)
venv\Scripts\activate        # (Windows)
```

### 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Create a .env File

```bash
Example:

MY_SECRET_KEY=your_secret_key
MY_DEBUG=True
DB_ENGINE=django.db.backends.postgresql
DB_NAME=qurio_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
ALLOWED_HOSTS=127.0.0.1,localhost
```

### 5️⃣ Run Migrations

```bash
python manage.py migrate
```

### 6️⃣ Start the Server

```bash
python manage.py runserver
```




## 🧩 API Endpoints (Examples)

|Endpoint|Method|Description|
|--------|------|-----------|
|/api/token/|	POST |	Obtain JWT tokens (login)
|/api/token/refresh/|	POST|	Refresh JWT token|
|/users/|	GET, POST|	List or create users|
|/tags/|	GET, POST|	List or create tags|
|/tags/{id}/questions/|	GET|	Get all questions under a tag|
|/questions/|	GET, POST|	List or create questions|
|/questions/{id}/answers/|	GET, POST|	Manage answers for a question|
|/answers/{id}/upvote/|	POST	|Upvote an answer|
|/answers/{id}/downvote/	|POST	|Downvote an answer|





## 🔒 Authentication Flow

On login, JWT tokens (access_token & refresh_token) are stored in HTTP-only cookies.

Access tokens automatically refresh when expired using CookieTokenRefreshView.





## 📄 Example Models

CustomUser

Questions

Answers

Tags

Vote





## 💡 Future Improvements

✅ Swagger / ReDoc API documentation

✅ Unit & integration tests

✅ Add email verification for new users

✅ Add “accepted answer” feature for questions





## 👨‍💻 Author

Sufyan Malik
🔗 GitHub Profile




## 🪪 License

This project is licensed under the MIT License — feel free to use and modify it.



## 🧠 Summary

Qurio API demonstrates a complete, scalable RESTful backend built with Django and DRF — featuring secure authentication, nested relationships, and clear modular design. Perfect for integration with a React or mobile frontend.

