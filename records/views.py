from django.shortcuts import render, redirect
from .forms import TransactionForm
from django.db.models import Sum
from .models import Transaction
from django.shortcuts import render, get_object_or_404, redirect


def transaction_list(request):
    transactions = Transaction.objects.all()
    total_amount = transactions.aggregate(total=Sum('amount'))['total'] or 0
    return render(request, 'records/transactions.html', {
        'transactions': transactions,
        'total_amount': total_amount
    })

def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')  # Redirect to the transaction list view after saving
    else:
        form = TransactionForm()
    return render(request, 'records/add_transaction.html', {'form': form})

def edit_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction)
    
    return render(request, 'records/edit_transaction.html', {'form': form})

def delete_transaction(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        transaction.delete()
        return redirect('transaction_list')
    return render(request, 'records/delete_transaction.html', {'transaction': transaction})
