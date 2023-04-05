from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView,CreateView,UpdateView
from todos.forms import TasksForm,RegistrationForm,LoginForm
from todos.models import Tasks
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.urls import reverse_lazy



class IndexView(TemplateView):
    template_name='index.html'


class TasksCreateView(CreateView):
    model=Tasks
    form_class=TasksForm
    template_name='task-add.html'
    success_url=reverse_lazy('task-list')

def task_list_view(request,*args,**kwargs):
    qs=Tasks.objects.all()
    return render(request,'task-list.html',{'tasks':qs}) 


def task_detail_view(request,*args,**kwargs):
    id=kwargs.get('pk')
    qs=Tasks.objects.get(id=id)
    return render(request,'task-detail.html',{'task':qs}) 



def task_delete_view(request,*args,**kwargs):
    id=kwargs.get('pk')
    Tasks.objects.get(id=id).delete() 
    messages.success(request,'Task has been deleted!')
    return redirect('task-list')       

class TaskEditView(UpdateView):
    model=Tasks
    form_class=TasksForm
    template_name='task-edit.html'
    success_url=reverse_lazy('task-list')
    

class RegistrationView(View):
    def get(self,request,*args,**kw):
        form=RegistrationForm()
        return render(request,'registration.html',{'form':form})
    def post(self,request,*args,**kwargs):
        form=RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            messages.success(request,'account is registered')
            return redirect('home')
        else:
            messages.error(request,'account is not added')
            return render(request,'registration.html',{'form':form})

class SignInView(View):
    def get(self,request,*args,**kwargs):
        form=LoginForm()
        return render(request,'login.html',{'form':form})
    def post(self,request,*args,**kwars):
        form=LoginForm(request.POST)
         
        if form.is_valid():
            uname=form.cleaned_data.get('username')
            pwd=form.cleaned_data.get('password')
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,usr)
                print(request.user)
                return redirect('home')
            else:
                return render(request,'login.html',{'form':form})


def signout_view(request,*args,**kw):
        logout(request)
        return redirect('signin')             
        
class TaskHome(TemplateView):
    template_name='taskhome.html'

