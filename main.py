import demos
import institution_report
from precipy.main import render_fn

analytics_modules = [institution_report]

def render(request):
   return render_fn(request, analytics_mods=analytics_modules)


## for running locally... python main.py hello.json
if __name__ == '__main__':
    from precipy.mock import Request
    import sys
    uuid = render_fn(Request(sys.argv[1]), analytics_mods=analytics_modules)
    print(uuid)
