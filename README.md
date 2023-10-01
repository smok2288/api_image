# api_image
Getting Started
Clone the repository:

git clone <repository_url>
cd <repository_name>
Build the Docker image:

docker-compose build
Run the Docker containers:

docker-compose up -d
The -d flag is used to run the containers in the background.

Initialize the Django project and database:
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
Follow the prompts to create a superuser.

Access the Django development server:
Open your web browser and go to http://localhost:8000/

You can now access your Django application running within the Docker containers.

Stopping the Application
To stop the application and shut down the Docker containers, run:

docker-compose down
