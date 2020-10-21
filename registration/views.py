from django.shortcuts import render
from django.views.generic.edit import FormView
from .forms import FormularioLogin, FormularioUsuario, UsuarioForm, TransporteForm
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from .models import Usuario, Transporte
from django.contrib.auth import login, logout
from django.views.generic import CreateView
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User


class Login(FormView):
    template_name = 'login.html'
    form_class = FormularioLogin
    success_url = reverse_lazy('index')

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return super(Login, self).form_valid(form)


class SignUpView(CreateView):
    form_class = FormularioUsuario
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse_lazy('login') + '?register'

    def get_form(self, form_class=None):
        form = super(SignUpView, self).get_form()
        # Modificar en tiempo real
        return form


def new_usuario(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            Usuario = form.save(commit=False)
            Usuario.password = make_password(request.POST['password'])
            Usuario.save()
    else:
        form = UsuarioForm()
    return render(request, 'registration/registro.html', {'form': form})

def new_transporte(request):
    if request.method == "POST":
        form = TransporteForm(request.POST)
        if form.is_valid():
            Transporte = form.save(commit=False)
            Transporte.id_cliente = request.user
            Transporte.save()
    else:
        form = TransporteForm()

    return render(request, 'registration/registroTransporte.html', {'form':form})

def lista_transportes(request):
    transportes = Transporte.objects.filter(id_cliente=request.user)
    return render(request, 'registration/listaTransportes.html', {'transportes':transportes})