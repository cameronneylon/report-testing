import demos
from precipy.main import render_fn

analytics_modules = [demos]

def render(request):
   return render_fn(request, analytics_mods=analytics_modules)



## for local testing... python main.py hello.json
if __name__ == '__main__':
    from precipy.mock import Request
    import sys
    render_fn(Request(sys.argv[1]), analytics_mods=analytics_modules)
