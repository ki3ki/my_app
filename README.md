

-----------------------------------------------------------------------------------------------------------------------------------------
 A functioning web app with API
 
The project was implemented using Django with Django Rest Framework (DRF) for the backend and HTML, CSS, and JavaScript for the frontend. Below are the detailed steps taken and features implemented:

### **Admin Facing**:

- **Models**:
  - Created models for `App`, `AppCategory`, and `AppSubCategory` to manage the structure of the apps and their categories
  
- **Admin Views and Serializers**:
  - Implemented views and serializers for adding new apps and managing the points assigned to each app.
  - Provided functionality for the admin to manage categories and subcategories of apps.
  - Enabled the admin to review and either accept or reject tasks submitted by users.

- **Admin Authentication**:
  - Implemented JWT-based authentication for secure login and access to admin functionalities.

- **Dashboard and App Management**:
  - Created an admin dashboard to display key information and allow easy navigation to manage apps, categories, subcategories,user information, task details and points.
  - Admin can add, edit, view and delete categories and associated subcategories.
  - Admin can add new apps through a custom interface and view details about each app.
  - Admin can also manage the app's points and assign them to specific apps.
  - Admin can accept or reject user tasks.

### **User Facing**:

- **Models**:
  - Created models for `CustomUser`, `UserProfile`, and `Task` to manage users , userprofile and the tasks completed.

- **User Views and Serializers**:
  - Developed views and serializers for users to:
    - View available apps.
    - Access and manage their user profiles.
    - Track points earned and tasks completed.  
  - Enabled users to complete tasks by downloading apps and uploading screenshots for admin review.

- **User Registration and Authentication**:
  - Implemented user registration and login using JWT-based authentication, allowing users to securely log in and access their profiles.
  - Users can log out and refresh their tokens using dedicated API endpoints.

- **User Profile and Points**:
  - Users can view and update their profiles, including their name and other basic information.
  - Created an API to allow users to fetch their earned points.

- **Task Management**:
  - Developed the functionality for users to view and manage their tasks, such as downloading apps and uploading screenshots as proof of task completion.
  - Users can upload screenshots using a drag-and-drop interface to confirm task completion.
  - Tasks are marked as "pending" when a screenshot is uploaded and will be marked as "completed" upon approval by the admin.

- **Screenshot Upload**:
  - Implemented the ability for users to upload a screenshot to confirm completion of tasks. This feature utilizes AJAX for dynamic interaction and provides immediate feedback to the user.
  - Screenshot validation and task status updates are handled by the backend, with an admin approving the screenshots and updating task completion status.

### **API Integration**:
  - Created RESTful APIs using Django Rest Framework (DRF) for both user-facing and admin-facing functionalities.
  - JWT authentication was implemented for secure access to sensitive endpoints for both users and admins.
  - The API allows:
    - User registration, login, and logout.
    - Fetching and updating user profile information.
    - Viewing available apps and their associated points.
    - Managing tasks and uploading screenshots.
  - The admin can manage apps, app categories, app points, and approve task completions.

### **Frontend and Dynamic Interaction**:
  - Implemented a user-friendly interface for both the admin and user-facing parts of the application using HTML, CSS, and JavaScript.
  - Utilized AJAX for dynamic loading and interaction with the backend, allowing the user interface to be responsive without needing full-page reloads.
  - The frontend is built to allow the admin to add and manage apps and for users to interact with tasks, view their profiles, and track their points.

---

**Key Endpoints**:

- **User Authentication and Profile**:
    - `/api/auth/token/`: User login with JWT authentication.
    - `/api/auth/token/refresh/`: User token refresh.
    - `/api/register/`: User registration.
    - `/api/auth/token/logout/`: User logout.
    - `/api/tasks/completion`: View and manage tasks for the user.
    - `/api/profile/`: Fetch and update user profile.
    - `/api/points/`: Fetch user’s points.
    - `/api/apps/`: View available apps.
    - `/api/apps/<int:pk>/`: View details of a specific app.

- **Admin Authentication and Profile**:
    - `/admin-login/`: Admin login (with credentials or JWT).
    - `/api/admin/auth/token/`: Admin login with JWT authentication.
    - `/token-refresh/`: Admin token refresh.
    - `/api/apps/`: Admin can list, create, update and delete app.
    - `/api/apps/<int:pk>/`: Admin can view details of a specific app.
    - `/api/categories/`: Admin can list, create,update,delete app categories.
    - `/api/subcategories/`: Admin can list, create, update, delete app subcategories.
    - `/api/task/`: Admin can list tasks, update task status.

---

**Technologies Used**:
- Django , Django Rest Framework, Bootstrap, JavaScript, HTML, CSS, AJAX, JWT, PostgreSQL, Git, Render


## Deployment on Render

Steps to deploy Django application on Render:

### Prerequisites
- A Render account.
- The Django project is version-controlled and pushed to a repository (GitLab).
- `requirements.txt` file includes all necessary dependencies.
- Database migrations have been prepared.

### Deployment Steps

#### 1. Create a New Web Service on Render:
- Log in to Render account.
- Navigate to the **Dashboard** and click on **New > Web Service**.
- Connect repository and choose the branch to deploy.

#### 2. Set Environment Variables:
- Add the following environment variables under the "Environment" section:
  - `SECRET_KEY`: Django secret key.
  - `DATABASE_URL`: Connection URL for Render-managed PostgreSQL.
  - `HOST`: Set it to Render app URL.
  - `DEBUG`: Set to `False` for production.

#### 3. Install Dependencies:
- Ensure `requirements.txt` contains all the necessary packages, including:
  ```plaintext
  Django
  gunicorn
  whitenoise
  psycopg2-binary
  ```
- Render will automatically install the dependencies with:
  ```bash
  pip install -r requirements.txt
  ```

#### 4. Set Up the Build Command:
- In the "Build Command" section, Render will use:
  ```bash
  pip install -r requirements.txt
  ```

#### 5. Set Up the Start Command:
- Add the following as the "Start Command":
  ```bash
  web: gunicorn taskmanager.wsgi:application
  ```

#### 6. Configure Static Files:
- Make sure Whitenoise is set up :
  - Add `whitenoise.middleware.WhiteNoiseMiddleware` to  `MIDDLEWARE` settings.
  - Set the following in `settings.py`:
    ```python
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    ```
- Collect static files before deployment:
  ```bash
  python manage.py collectstatic --noinput
  ```

#### 7. Enable Auto-Deploy:
- In the "Deployment" settings Render service, enable **Auto-Deploy**.
- This ensures that every new commit pushed to the selected branch triggers a new deployment automatically.

#### 8. Database Setup:
- Render will automatically set up a managed PostgreSQL database if you choose this option during service creation.
- After deployment, run migrations to initialize the database:
  ```bash
  python manage.py migrate
  ```

#### 9. Deployment Process:
- Click **Create Web Service**. Render will build and deploy the project.
- Once deployed, you can access application via the URL provided by Render.

#### 10. Test the Application:
- Visit the deployed app URL to ensure it is functioning correctly.
- Verify that static files load properly, and database operations work as expected.

#### 11. Manage Service:
- Use Render's dashboard to monitor logs, redeploy changes, and manage resources.

---


**Future Improvements**

- User Features:

  - Pagination: Implement pagination for the app listing to improve performance for users viewing a large number of apps.
  - Search Functionality: Add search and filtering for apps, allowing users to find apps by name, category, or points.
  - Social Login: Allow users to sign up and log in via social platforms (Google, Facebook, etc.).
  - Password change and validation

- Admin Features:

  - Analytics Dashboard:
      - Display insights like the number of tasks completed, total points awarded, and app performance.
      - Include charts and tables for better visualization.
  - Admin Logout: Add a secure logout option for admins.
  - Admin Page Access Restriction.
       -Restrict access to the admin-side pages so that only authenticated admin users can view them. Currently, while endpoints are  secure, any registerd user can access the admin pages' UI.

- Task Management Enhancements:
  - Bulk Approval: Allow admins to approve/reject multiple tasks at once.


- UI/UX Enhancements:
  - Improve frontend design for both user and admin users.

- API Documentation:
  - Use tools like Swagger or DRF's built-in schema generator for interactive API documentation.


**Screencast Submission**

A video demonstration of the project, showcasing all key features and functionalities, has been included as part of this submission. You can access the video at the following link:

<https://drive.google.com/file/d/1OK35y8wfjWwQ729m5NTi9JXBQV74pxJG/view?usp=sharing>

**Deployed Project**
You can access the live project here: #https://task-manager-6xg2.onrender.com
## admin credentials:
  - username : January
  - password : 12345

## Admin Access Instructions
  To access the admin side of the project,  will need to create a superuser. 
  Navigate to the project directory.
         python manage.py createsuperuser
Follow the prompts to set a username, email, and password for the admin account.
Once the superuser is created, you can log in to the admin dashboard using these credentials.



