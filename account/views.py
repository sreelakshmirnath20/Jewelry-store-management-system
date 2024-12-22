from django.forms import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views import View
from django.views.generic import TemplateView,FormView,CreateView
from .forms import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.urls import reverse_lazy


# Create your views here.

class LandingView(TemplateView):
    template_name="landing.html"



class LoginView(FormView):
    template_name="login.html"
    form_class=LoginForm
    def post(sel,request):
        form=LoginForm(data=request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pswd=form.cleaned_data.get('password')
            user=authenticate(request,username=uname,password=pswd)
            if user:
                login(request,user)
                return redirect("home")
            else:
                messages.error(request,"Login Failed!!")
                return redirect('log')
        return render(request,"login.html",{"form":form})
    

class RegView(CreateView):
    template_name="reg.html"
    form_class=RegForm
    success_url=reverse_lazy('log')


    def form_valid(self, form):
        messages.success(self.request,"User registration compleated")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.success(self.request,"User registration Failed!!")
        return super().form_invalid(form)

class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('landing')




