from django.shortcuts import render
import requests
from django.urls import reverse_lazy
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator

from django.views.generic import (
    TemplateView,
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    FormView
)

from .models import Prestamo

from .forms import NuevoPrestamoForm


class InicioView(TemplateView):
    template_name = 'prestamo/home.html'


@method_decorator(staff_member_required, name='dispatch')
class PrestamosListView(ListView):
    template_name="prestamo/listaPrestamos.html"
    model = Prestamo
    paginate_by = 10
    context_object_name = "prestamos"


class PrestamosCreateView(FormView):
    template_name = "prestamo/agregarPrestamo.html"
    form_class = NuevoPrestamoForm
    success_url = reverse_lazy('prestamo_app:agregarPrestamos')

    #declaro varibles
    dni = ""
    nombre=""
    apellido=""
    genero = ""
    email = ""
    monto_solicitado = None
    aprobado = ""
    error = ""
   
    def form_valid(self, form):

        self.dni = form.cleaned_data['dni']
        self.nombre = form.cleaned_data['nombre']
        self.apellido = form.cleaned_data['apellido']
        self.genero = form.cleaned_data['genero']
        self.email = form.cleaned_data['email']
        self.monto_solicitado = form.cleaned_data['monto_solicitado']

        #consulto api moni_online
        try:
            url = "https://api.moni.com.ar/api/v4/scoring/pre-score/"+str(self.dni)
            headers = {'credential': 'ZGpzOTAzaWZuc2Zpb25kZnNubm5u'}
            r = requests.get(url=url, headers=headers)
            response = r.json()
            print("response",response)
            
            # response = {'status': 'refuce', 'has_error': False}

            if response['status'] == 'approve':
                self.aprobado = 'aprobado'
            else:
                self.aprobado = 'rechazado'

        except:
            response = {}
            response['has_error'] = True


        if response['has_error'] != True:
            Prestamo.objects.create(
                dni=self.dni,
                nombre=self.nombre,
                apellido=self.apellido,
                genero=self.genero,
                email=self.email,
                monto_solicitado=self.monto_solicitado,
                aprobado = self.aprobado
            )

            super(PrestamosCreateView, self).form_valid(form)
            return render(self.request, self.template_name,
                        self.get_context_data(form=form))


        else:
            self.error = True

            super(PrestamosCreateView, self).form_valid(form)
            return render(self.request, self.template_name,
                        self.get_context_data(form=form))

        
    
    def get_context_data(self, **kwargs):
        response = super(PrestamosCreateView, self).get_context_data(**kwargs)
        response['dni'] = self.dni
        response['nombre'] = self.nombre
        response['apellido'] = self.apellido
        response['genero'] = self.genero
        response['email'] = self.email
        response['monto_solicitado'] = self.monto_solicitado
        response['aprobado'] = self.aprobado
        response['error']=self.error
        return response

 
    

@method_decorator(staff_member_required, name='dispatch')
class PrestamosDetailView(DetailView):
    template_name="prestamo/detallePrestamo.html"
    model = Prestamo
    
 

@method_decorator(staff_member_required, name='dispatch')
class PrestamosUpdateView(UpdateView):
    template_name = "prestamo/editarPrestamo.html"
    model = Prestamo
    form_class = NuevoPrestamoForm
    success_url = reverse_lazy('prestamo_app:listaPrestamos')



@method_decorator(staff_member_required, name='dispatch')
class PrestamosDeleteView(DeleteView):
    model = Prestamo
    success_url = reverse_lazy('prestamo_app:listaPrestamos')

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

 


