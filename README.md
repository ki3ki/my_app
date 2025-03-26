"# Django Evaluation" 
## Problem Set 1 - Regex

Write a regex to extract all the numbers with orange color background from the below text in italics (Output should be a list).


{"orders":[{"id":1},{"id":2},{"id":3},{"id":4},{"id":5},{"id":6},{"id":7},{"id":8},{"id":9},{"id":10},{"id":11},{"id":648},{"id":649},{"id":650},{"id":651},{"id":652},{"id":653}],"errors":[{"code":3,"message":"[PHP Warning #2] count(): Parameter must be an array or an object that implements Countable (153)"}]}

Solution:

The solution for extracting numbers with an orange background from the above text can be achieved using the following regular expression:

import re

text = '{"orders":[{"id":1},{"id":2},{"id":3},{"id":4},{"id":5},{"id":6},{"id":7},{"id":8},{"id":9},{"id":10},{"id":11},{"id":648},{"id":649},{"id":650},{"id":651},{"id":652},{"id":653}],"errors":[{"code":3,"message":"[PHP Warning #2] count(): Parameter must be an array or an object that implements Countable (153)"}]}'

pattern = r'(?<=id":)(\d+)'
numbers = re.findall(pattern , text)
print(numbers)

Output : This will output a list of all the numbers in the text.
['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '648', '649', '650', '651', '652', '653']
 
-----------------------------------------------------------------------------------------------------------------------------------------

## Problem Set 3 

A. Write and share a small note about your choice of system to schedule periodic tasks (such as downloading a list of ISINs every 24 hours). Why did you choose it? Is it reliable enough; Or will it scale? If not, what are the problems with it? And, what else would you recommend to fix this problem at scale in production?

B. In what circumstances would you use Flask instead of Django and vice versa? 

Solution:

For scheduling periodic tasks, I would choose **Celery** with **Redis** as the message broker. Celery is a powerful, asynchronous task queue/job queue based on distributed message passing. It is designed to handle tasks such as sending emails, processing files, and making API calls asynchronously. Redis as the message broker because of its speed and reliability.

**Why choose Celery ?**  
- Celery allows tasks to be scheduled and executed in the background asynchronously, which is a good choice for tasks like downloading lists or batch processing.
- Redis is a fast, lightweight, and highly reliable message broker, making it ideal for production environments.

**Reliability and Scalability**:
- Celery with Redis is highly reliable and scalable. It can handle a high volume of tasks, and tasks can be distributed across multiple worker nodes to improve throughput.
- It is horizontally scalable, that is  we can add more workers as the load increases.
  
**Potential Problems**:
- If the tasks are very resource-intensive or involve long-running processes, Redis or Celery might need to be tuned to handle such operations efficiently.
- Redis can run into memory limitations, especially with very large datasets, which could be mitigated by using persistent storage or a more powerful message broker like RabbitMQ.
  
**Recommendation for Production**:
- In a production environment, it’s important to monitor the health of Celery workers, Redis, and the queue. Monitoring tools like **Flower** for Celery can be used to track task statuses and failures.
- For large-scale production environments, advanced distributed task queue with stronger message broker support, like RabbitMQ, can be used to handle large workloads.

Alternatives to Celery include APScheduler, a lightweight library for simple task scheduling in small to medium applications, and RQ (Redis Queue), a simpler task queue for smaller projects using Redis. For very basic periodic tasks without advanced features, cron jobs are a straightforward choice. While Celery is ideal for scalable, complex background tasks due to its reliability and rich features, simpler alternatives like APScheduler or cron jobs are better suited for less demanding applications.

-----------------------------------------------------------------------------------------------------------------------------------------

**Flask** is a microframework that is lightweight and flexible. It is suitable for applications that require more control over the architecture and design. Some of the circumstances where Flask would be a better choice are:
- Small, lightweight applications: If you are building a small application and don't need many features out of the box, Flask is a good choice.
- Microservices architecture: Flask allows to quickly build isolated services, and its simplicity is ideal for microservices.
- More control over the application structure : It gives freedom in deciding how to organize your application, Flask gives you complete control.

**Django** is a full-fledged web framework designed for larger, complex applications. Some circumstances where Django would be more appropriate include:
- Full-stack applications: If the application need a lot of built-in features like an admin panel, authentication, database migrations, etc., Django is a better choice.
- Scalable applications: Django provides built-in support for scaling, including its ORM and middleware.
- Time-to-market:To get a product up and running quickly with a lot of built-in functionality, Django is a good choice
- Security: Django includes several built-in security features like protection against CSRF, XSS, and SQL injection attacks. It also     includes a secure authentication system and user management, making it a good choice for projects that require robust security.
- Large Community and Ecosystem: Django has a large community and extensive documentation. It's a mature framework with a wide range of reusable plugins, which can accelerate development
**when to use Django and Flask**
Flask: Choose Flask for small to medium-sized projects, microservices, APIs, or prototypes that require flexibility and quick iteration.
Django: Choose Django for large-scale, feature-rich applications, particularly when rapid development, security, and scalability are important factors.

-----------------------------------------------------------------------------------------------------------------------------------------

## Problem Set 2 - A functioning web app with API

I. Please create a website - which should have two components:

- Expose all the endpoints using Rest API, with proper permissions, authentication, and documentation. Please refer to the image link: ![Image](https://i.imgur.com/T0ZCO9A.png)

- **Admin Facing** - Where the admin user can add an Android app as well as the number of points earned by users for downloading the app.
- **User Facing** - Where the user can see the apps added by the admin and the points. The user should be able to see the following fields:
  - Signup and Login (Feel free to use any package for the same).
  - Their Name and Profile.
  - Points Earned.
  - Tasks completed.
  - Option to upload a screenshot (which must include drag and drop) for that particular task (e.g., if a user downloads a particular app, they can send a screenshot of the open app to confirm that they have downloaded the app).

## Solution

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



