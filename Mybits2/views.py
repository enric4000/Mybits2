from django.shortcuts import redirect, render
from django.views import View

class HomeView(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/user/login')
        return render(request, self.template_name)
