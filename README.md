# LYS_schoolapp
Account System for Al-Manar School

# Educational App

This is a Django-based educational app that allows you to manage educational stages, classrooms, academic years, and expenses.

## Models

### EducationalStage

- Represents an educational stage such as baby class, kindergarten, primary stage, prep stage, and secondary stage.
- Fields:
  - `name`: CharField with choices representing the educational stage.

### Classroom

- Represents a classroom in a specific educational stage.
- Fields:
  - `name`: CharField representing the name of the classroom.
  - `stage`: CharField with choices representing the stage of the classroom.
  - `educational_stage`: ForeignKey to the EducationalStage model, representing the associated educational stage.
  - `fee_per_student`: DecimalField representing the fee per student in the classroom.

### AcademicYear

- Represents an academic year.
- Fields:
  - `year`: CharField representing the year of the academic year.

### Expense

- Represents an expense associated with a classroom.
- Fields:
  - `classroom`: ForeignKey to the Classroom model, representing the associated classroom.
  - `expense_type`: CharField representing the type of expense.
  - `amount`: DecimalField representing the amount of the expense.
  - `date`: DateField representing the date of the expense.
  - `total_owed`: DecimalField representing the total amount owed for the expense.

## Usage

1. Install the required dependencies by running the command `pip install -r requirements.txt`.
2. Set up the Django project and configure the database settings in `settings.py`.
3. Run database migrations using the command `python manage.py migrate`.
4. Start the development server using the command `python manage.py runserver`.
5. Access the app through the provided URL.

Feel free to customize the app according to your specific requirements by modifying the models, views, and templates.

## License

This project is licensed under the [Eng. Mohamed Gamal License](LICENSE).
