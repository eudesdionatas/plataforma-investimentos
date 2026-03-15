from django.shortcuts import render, redirect
from .forms import OperacaoForm

def cadastro_operacao(request):
    if request.method == 'POST':
        form = OperacaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('cadastro_operacao')  # Redirect to the same page or a success page
    else:
        form = OperacaoForm()
    return render(request, 'portfolio/cadastro_operacao.html', {'form': form})
