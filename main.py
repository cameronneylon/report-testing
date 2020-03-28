import sys
import institution_report
from precipy.main import render_file
from precipy.storage import GoogleCloudStorage

storage = GoogleCloudStorage()

analytics_modules = [institution_report]

if __name__ == '__main__':
    render_file(sys.argv[1], analytics_modules, storages=[storage])
