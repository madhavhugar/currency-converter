from datetime import datetime

from django.http import Http404, JsonResponse

from currency_converter.exchange_rates import convert_amount


def convert(request):
    """
    Handles GET => /convert
    """
    try:
        if request.method == 'GET':
            amount = float(request.GET.get('amount', 0))
            src_currency = request.GET.get('src_currency', 'EUR')
            dest_currency = request.GET.get('dest_currency', 'EUR')
            reference_date = request.GET.get(
                'reference_date',
                datetime.now().date(),
                )

            converted = convert_amount(
                amount,
                reference_date,
                src_currency,
                dest_currency,
                )

            response = {
                'amount': converted,
                'currency': dest_currency,
            }
            return JsonResponse(response)
        else:
            raise Http404('Invalid request')
    except Exception:
        raise Http404('Invalid request - check input. \
                      Example:\
                        amount=20&\
                        src_currency=USD&\
                        dest_currency=GBP&\
                        reference_date=2020-05-22')
