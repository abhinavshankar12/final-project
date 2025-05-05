# This is the main file to run Django commands
import os
import sys

if __name__ == '__main__':

    # set settings module
    
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_catalog.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError:
        print("Django isn't installed yet!")
        sys.exit(1)
    execute_from_command_line(sys.argv)