from django.shortcuts import render, HttpResponse

topics = [
    {'id':1, 'title':'routing', 'body':'Routing is ..'},
    {'id':2, 'title':'view', 'body':'View is ..'},
    {'id':3, 'title':'Model', 'body':'Model is ..'},
]

def HTMLTemplate(article):
    global topics
    ol = ''
    for topic in topics:
        ol += f'<li> <a href="/read/{topic["id"]}"> {topic["title"]} </a> </li>'
    return f'''
        <html>
        <body>
            <h1><a href="/">Django</a></h1>
            <ol>
                {ol}
            </ol>

        {article}

        </body>
        </html>
    '''

# Create your views here.
def index(request):
    article = '''
        <h2>Welcome</h2>
        Hello, Django
    '''
    return HttpResponse(HTMLTemplate(article))

def create(request):
    return HttpResponse('Create!')

def read(request, id):
    global topics
    topic = [item for item in topics if item['id'] == int(id)][0]

    article = f'''
        <h2>{topic["title"]}</h2>
        {topic["body"]}
    '''
    return HttpResponse(HTMLTemplate(article))
