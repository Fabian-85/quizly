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

## Frontend-Setup

1. Open the frontend quizly project in a editor e.g. Visual Studio Code
2. Right-click on the file `index.html` at the top level and select Open with  **Open with Live Server** to start the project.
