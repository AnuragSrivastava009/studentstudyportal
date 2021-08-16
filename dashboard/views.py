from django.shortcuts import render,redirect
from . models import Notes 
from . forms import *
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from django.contrib.auth.decorators import login_required
# Create your views here.
def home(request):
    return render(request, 'dashboard/home.html')

@login_required
def notes(request):
    if request.method=="POST":
        form=NotesForm(request.POST)
        if form.is_valid():
            notes=Notes(User=request.user,title=request.POST['title'],description=request.POST['description'])
            notes.save()
            messages.success(request,f"suceesfully added from {request.user.username} Sucessfully")
    else:
        form=NotesForm()
    notes=Notes.objects.filter(User=request.user)
    context={'notes':notes, 'form':form}
    return render(request,'dashboard/notes.html',context)
#function for deletion of notes
@login_required  
def delete_notes(request,pk=None):
    Notes.objects.filter(id=pk).delete()

    return redirect('notes')
    # for generic views
class  NotesDetailView(generic.DetailView): 
    model=Notes



#HOMEWORK
@login_required
def homework(request):
    if request.method=="POST":
        form=HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished= request.POST['is_finished']
                if finished == 'on':
                    finished =True
                else:
                    finished= False
            except:
                   finished=False
            homeworks=Homework(
                User=request.user,
                title=request.POST['title'],
                description=request.POST['description'],
                subject=request.POST['subject'],
                due=request.POST['due'],
                is_finished=finished,
                )
            homeworks.save()
            messages.success(request,f"Homework successfully added from {request.user.username} Sucessfully")
    else:
        form=HomeworkForm()
    homework=Homework.objects.filter(User=request.user)
    if len(homework)==0:
        homework_done=True
    else:
        homework_done=False
    context={'homeworks':homework,
             'homework_done':homework_done,
             'form':form,

    }
    return render(request, 'dashboard/homework.html',context)
@login_required
def update_homework(request,pk=None):
     
    homework=Homework.objects.get(id=pk)
    if homework.is_finished == True:
        homework.is_finished =False
    else:
        homework.is_finished =True
         
    homework.save()     
    return redirect('homework')
@login_required
def delete_homework(request,pk=None):
    Homework.objects.filter(id=pk).delete()

    return redirect('homework')

#YOUTUBE APP 

def youtube(request):
    #CREATE OBJECT FOR FORM
    if request.method =='POST':
        form = DashboardFom(request.POST)
        text = request.POST.get('text')
        video=VideosSearch(text,limit=10)
        result_list=[]
        
        #for result in results:  
            #print(result.link)
        for i in video.result()['result']:
            result_dict =  {
                'input':text,
                'duration':i['duration'],
                'title':i['title'],
                'thumbnail':i['thumbnails'][0]['url'],
                'views':i['viewCount']['short'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'published':i['publishedTime'],

            }
            desc=''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc+=j['text']
            result_dict['description']=desc
            result_list.append(result_dict)
            context={
                'form':form,
                'results':result_list
            }
        return render(request,"dashboard/youtube.html",context)
    else:
        form= DashboardFom()
    context={ 'form':form}
    return render(request,"dashboard/youtube.html",context)
@login_required
def todo (request):
    if request.method=="POST":
        form=TodoForm(request.POST)
        try:
            finished= request.POST['is_finished']
            if finished == 'on':
                finished =True
            else:
                finished= False
        except:
            finished=False
            todos=TOdo(
                User=request.user,
                title=request.POST['title'],
                is_finished=finished,
                )
            todos.save()
            messages.success(request,f"Homework successfully added from {request.user.username} Sucessfully")
        


    else:    
        form=TodoForm() 
    todo=TOdo.objects.filter(User=request.user)
    if len(todo) == 0:
        todos_done = True
    else:
        todos_done = False       
    context={
        'form':form,
        'todos':todo,
        'todo_done':todos_done
     }
    return render(request,"dashboard/todo.html",context)
@login_required
def delete_todo(request,pk=None):
    TOdo.objects.filter(id=pk).delete()

    return redirect('todo')
@login_required
def update_todo(request,pk=None):
    todo = TOdo.objects.get(id=pk)
    if todo.is_finished == True:
        todo.is_finished = False
    else:
        todo.is_finished =True
    todo.save()
    return redirect('todo')

#book section start here
def books(request):
    #CREATE OBJECT FOR FORM
    if request.method =='POST':
        form = BookForm(request.POST)
        string = request.POST['strings']
        
        url="https://www.googleapis.com/books/v1/volumes?q="+string
       
        r =requests.get(url)
        answer =r.json()
        result_list=[]
      
        #for result in results:  
            #print(result.link)
        for i in range(10):
            result_dict =  {
             'title':answer['items'][i]['volumeInfo']['title'],
             
             'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
             'description':answer['items'][i]['volumeInfo'].get('description'),
             'count':answer['items'][i]['volumeInfo'].get('pageCount'),
             'categories':answer['items'][i]['volumeInfo'].get('Categories'),
             'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
             'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks'),
             'preview':answer['items'][i]['volumeInfo'].get('previewlink'),

            }
            
            result_list.append(result_dict)
            context={
                'form':form,
                'results':result_list
            }
        return render(request,"dashboard/books.html",context)
    else:
        form= BookForm()
    context={ 'form':form}
    return render(request,"dashboard/books.html",context)
def dictionary(request):
    if request.method =='POST':
        form = DashboardFom(request.POST)
        text = request.POST['text']
       
        #url = "https://api.dictionaryapi.dev.api/v2/entries.en_US/"+text
        url ="https://api.dictionaryapi.dev/api/v2/entries/en/"+text
       
        r =requests.get(url)
        answer =r.json()
        try:
           phonetics =answer[0]['phonetics'][0]['text']
           audio = answer[0]['phonetics'][0]['audio']
           definition= answer[0]['meanings'][0]['definitions'][0]['definition']
           examples= answer[0]['meanings'][0]['definitions'][0]['example']
           synonyms= answer[0]['meanings'][0]['definitions'][0]['synonyms']
           context={
                'form':form,
                'input':text,
                'phonetics':phonetics,
                'audio':audio,
                'definition':definition,
                'example':examples,
                'synonyms':synonyms
            }
        except:
            context={ 
                 'form':form,
                 
                 'input':text,
                'phonetics':phonetics,
                'audio':audio,
                'definition':definition,
                'example':example,
                'synonyms':synonyms

                }
        return render(request,"dashboard/dictionary.html",context)
    else:
        form= DashboardFom()
        context={ 
           'form':form,
            'input':'',
        }
    return render(request,"dashboard/dictionary.html",context)
def wiki (request):
    if request.method =='POST':
        text=request.POST['text']
        form = DashboardFom(request.POST)
        search=wikipedia.page(text)
        context={ 
            'form':form,
            'title':search.title,
            'link':search.url,
            'details':search.summary
          }
        return render(request,"dashboard/wiki.html",context)
    else:
        form= DashboardFom()
    context={ 'form':form}
    return render(request,"dashboard/wiki.html",context)
def conversion (request):
    if request.method =='POST':
        form =ConverstionForm(request.POST)
        if request.POST['measurement'] == 'length':
            measurement_form =ConverstionLengthForm()
            context={ 
                'form':form,
                'm_form':measurement_form,
                'input':True

             }
            
            if 'input' in request.POST:
                first =request.POST['measure1']
                second =request.POST['measure2']
                input =request.POST['input']
               
                answer=''
                
                if input and int(input) >= 0:
                    if first == 'yard' and second =='foot':
                        answer =f'{input} yard ={int(input)*3} foot'
                    if first == 'foot' and second =="yard":
                        answer =f'{input} foot ={int(input)/3} yard'
                context={ 
                        'form':form,
                        'm_form':measurement_form,
                        'input':True,
                        'answer':answer

                 }
        if request.POST['measurement'] == 'mass':
            measurement_form =ConverstionMassForm()
            context={ 
                'form':form,
                'm_form':measurement_form,
                'input':True

            }
            if 'input' in request.POST:
                first =request.POST['measure1']
                second =request.POST['measure2']
                input =request.POST['input']
                answer=''
                if input and int(input)>=0:
                    if first == 'pound' and second =='kilogram':
                        answer =f'{input} pound ={int(input)*0.453592} kilogram'
                    if first == 'kilogram' and second =='pound':
                        answer =f'{input} kilogram ={int(input)*2.204622} pound'
                context={ 
                        'form':form,
                        'm_form':measurement_form,
                        'input':True,
                        'answer':answer

                }
    else:
        form=ConverstionForm()
        context={ 
            'form':form,
            'input':False
        }
    return render(request,"dashboard/conversion.html",context)

def register(request):
    if request.method =='POST':
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            messages.success(request,f"Account created for {username}!!")
            #redirect  to the log in page
            return  redirect('login')
    else:
        form=UserRegistrationForm()
    context={ 
            'form':form,
            
        }
    return render(request,"dashboard/register.html",context)

#log in

def login(request):
    context={ 
            'form':form,
        }
    return render(request,"dashboard/login.html",context)
#profile
@login_required
def profile(request):
    homeworks=Homework.objects.filter(is_finished=False,User=request.user)
    todos=TOdo.objects.filter(is_finished=False,User=request.user)
    if len(homeworks) == 0:
        homeworks_done == True
    else:
        homeworks_done == False
    if len(todos) == 0:
        todos_done == True
    else:
        todos_done == False
    context={ 
            'homeworks': homework,
            'todos':todo,
            'homework_done':homework_done,
            'todos_done':todos_done,
        }

    return render(request,"dashboard/profile.html",context)
    