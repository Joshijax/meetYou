from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic.edit import FormMixin

from django.views.generic import DetailView, ListView
from django.shortcuts import redirect, render
from .forms import ComposeForm
from .models import Thread, ChatMessage, Message
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth.decorators import login_required
@login_required(login_url='/')
def home(request, username,):
    form = ComposeForm()
    userThread = get_object_or_404(User, username=username,)
    obj, created   = Thread.objects.get_or_new(request.user, username)
    print(obj, 'threaddd')
    chat = ChatMessage.objects.filter(Q(user=request.user) and Q(thread=obj)).order_by('timestamp',)

    users = User.objects.all()
    
    print(chat)
    return render(request, 'chat/thread.html', {'form': form, 'chat': chat,'users': users,'Theuser': username,})

def sendMessage(request):
    chat = Message.objects.all().order_by('date',).reverse()
    message = request.POST['message']
    MessageSave = Message(text=message, user= request.user, to='1')
    MessageSave.save()

    
    
class InboxView(LoginRequiredMixin, ListView):
    template_name = 'chat/inbox.html'
    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)


class ThreadView(LoginRequiredMixin, FormMixin, DetailView):
    template_name = 'chat/thread.html'
    form_class = ComposeForm
    success_url = './'

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        other_username  = self.kwargs.get("username")
        obj, created    = Thread.objects.get_or_new(self.request.user, other_username)
        if obj == None:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        thread = self.get_object()
        user = self.request.user
        message = form.cleaned_data.get("message")
        ChatMessage.objects.create(user=user, thread=thread, message=message)
        return super().form_valid(form)




