import os
import sys

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ms3_project.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    # Run server on port 5053
    execute_from_command_line([sys.argv[0], 'runserver', '0.0.0.0:5053', '--noreload'])

if __name__ == '__main__':
    main()