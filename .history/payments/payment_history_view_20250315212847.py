from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Payment

@login_required
def payment_history_view(request):
    """
    Fetch and display payment history for the logged-in user.
    Includes pagination to improve performance.
    """
    # Fetch payments for the logged-in user (optimized query)
    payments = Payment.objects.filter(user=request.user).order_by('-date').only('amount', 'status', 'date')

    # Paginate results (10 payments per page)
    paginator = Paginator(payments, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "payments/payment_history.html", {
        "page_obj": page_obj  # Pass paginated payments
    })
