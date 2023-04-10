from django.shortcuts import render, HttpResponse, redirect
from django.views.decorators.csrf import csrf_exempt

next_id = 4
topics = [
    {'id':1, 'title':'routing', 'body':'Routing is ..'},
    {'id':2, 'title':'view', 'body':'View is ..'},
    {'id':3, 'title':'Model', 'body':'Model is ..'},
]

def HTMLTemplate(article, id=None):
    global topics

    buttons = ''
    if not id:
        buttons = f'''
            <li><a href="/create/">create</a></li>
        '''
    else:
        buttons = f'''
            <li>
                <form action = "/delete/" method="POST">
                    <input type="hidden" name="id" value={id}>
                    <input type="submit" value="delete">
                </form>
            </li>
            <li><a href="/update/{id}">update</a></li>
        '''

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

        <ul>
            {buttons}
        </ul>

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

@csrf_exempt
def create(request):
    global next_id
    if request.method == "GET":
        article = f'''
            <form action="/create/" method="post">
                <p> <input type="text" name="title" placeholder="title"> </p>
                <p> <textarea name="body" placeholder="body"></textarea></p>
                <p> <input type="submit"></p>
            </form>
        '''

        return HttpResponse(HTMLTemplate(article))
    
    elif request.method == "POST":
        new_topic = dict()
        new_topic['id'] = next_id
        next_id += 1

        new_topic['title'] = request.POST['title']
        new_topic['body'] = request.POST['body']

        topics.append(new_topic)


        return redirect('/read/' + str(next_id - 1), str(next_id - 1))

def read(request, id):
    global topics
    topic = [item for item in topics if item['id'] == int(id)][0]

    article = f'''
        <h2>{topic["title"]}</h2>
        {topic["body"]}
    '''
    return HttpResponse(HTMLTemplate(article, id))

@csrf_exempt
def delete(request):
    global topics
    if request.method == 'POST':
        id = request.POST['id']
        topics = [topic for topic in topics if topic['id'] != int(id)]
    
    return redirect('/')

@csrf_exempt
def update(request, id):
    global topics
    topic = [item for item in topics if item['id'] == int(id)][0]

    if request.method == "GET":
        article = f'''
            <form action="/update/{id}/" method="post">
                <p> <input type="text" name="title" placeholder="title" value={topic["title"]}></input> </p>
                <p> <textarea name="body" placeholder="body">{topic["body"]}</textarea></p>
                <p> <input type="submit"></p>
            </form>
        '''
        return HttpResponse(HTMLTemplate(article, id))
    
    
    elif request.method == "POST":
        for topic in topics:
            if topic['id'] == int(id):
                topic['title'] = request.POST['title']
                topic['body'] = request.POST['body']

        


        return redirect('/read/' + str(id), str(id))