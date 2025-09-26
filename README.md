# Quizly Backend Project


## Backend-Setup

1. **Clone the repository and navigate to this folder in your editor e.g Visual Studio Code**
```bash
git clone https://github.com/Fabian-85/quizly.git
cd quizly
```
 
2. **Create environment and activate virtual environment**
    -  **for Windows**

       ```bash
         python -m venv env
         "env\Scripts\activate" 
       ```
 

   -  **for Linux and MacOS**
 
      ```bash
         python -m venv env
         source venv/bin/activate 
      ```

3. **Create a env-file (.env) in the projects root and add your Gemini Api-Key**
```bash
GEMINI_API_KEY="your_api_key"
```


4. **Install requirements**
```bash
pip install -r requirements.txt
```

5. **Create migrations and apply migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

6. **Start the backend server**
```bash
python manage.py runserver
```
---


## API Endpoints

### Authentication

  <details>
  <summary><strong>POST</strong> <code>/api/register/</code></summary>
   
  **Request Body:**
  
  ```json
  {
    "username": "your_username",
    "password": "your_password",
    "confirmed_password": "your_confirmed_password",
    "email": "your_email@example.com"
  }
  ```
  </details>

  <details>
  <summary><strong>POST</strong> <code>/api/login/</code></summary>
   
  **Request Body:**
  
  ```json
  {
  "username": "your_username",
  "password": "your_password"
  }
  ```
  </details>

  <details>
  <summary><strong>POST</strong> <code>/api/logout/</code></summary>
   
  **Request Body:**
  
  ```json
  {

  }
  ```
  </details>

   <details>
  <summary><strong>POST</strong> <code>/api/token/refresh/</code></summary>
   
  **Request Body**
  
  ```json
  {

  }
  ```
  </details>
 
### Quiz Management

<details>
  <summary><strong>POST</strong> <code>/api/createQuiz/</code></summary>
   
  **Request Body:**
  
  ```json
  {
  "url": "https://www.youtube.com/watch?v=example"
  }
  ```
 </details>

<details>
  <summary><strong>GET</strong> <code>/api/quizzes/</code></summary>
 </details>

 <details>
  <summary><strong>GET</strong> <code>/api/quizzes/{id}/</code></summary>
 </details>

 <details>
  <summary><strong>PATCH</strong> <code>/api/quizzes/{id}z/</code></summary>
   
  **Request Body:**
  
  ```json
 {
  "title": "Updated Title",
  "description:"Updated Description"
}
  ```
 </details>

  <details>
  <summary><strong>DELETE</strong> <code>/api/quizzes/{id}/</code></summary>
 </details>

## Frontend-Setup

1. Open the frontend quizly project in a editor e.g. Visual Studio Code
2. Right-click on the file `index.html` at the top level and select Open with  **Open with Live Server** to start the project.
