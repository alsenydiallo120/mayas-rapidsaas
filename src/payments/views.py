import time

import stripe

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from generics.utils import get_domain, get_site_name
from payments.models import UserPayment, UserPaymentStatus
from payments.products import PRICE_CHECKOUT_MAPPING
from payments.utils import site_domain_to_stripe_redirect_format
from website.settings import LOGIN_REQUIRED_URL


@login_required(login_url=LOGIN_REQUIRED_URL)
def product_page(request, product_name: str):
    site_name = get_site_name(request)
    if site_name in UserPayment.get_premium_site_access_list(request.user.id):
        return redirect(f"{site_name}__index")
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_redirect_domain = site_domain_to_stripe_redirect_format(get_domain(request), request.META['SERVER_PORT'])
    checkout_session = stripe.checkout.Session.create(
        **PRICE_CHECKOUT_MAPPING[product_name],
        success_url=stripe_redirect_domain + '/payment_processing?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=stripe_redirect_domain + '/payment_cancelled',
    )
    return redirect(checkout_session.url, code=303)


@login_required(login_url=LOGIN_REQUIRED_URL)
def payment_processing(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe_checkout_id = request.GET.get('session_id', None)
    user_payment_status, _ = UserPaymentStatus.objects.get_or_create(
        user=request.user,
        site_name=get_site_name(request)
    )
    user_payment_status.status = UserPaymentStatus.PENDING
    user_payment_status.stripe_checkout_id = stripe_checkout_id
    user_payment_status.save()
    context = {
        'session_id': stripe_checkout_id,
    }
    return render(request, 'payments/payment_pending.html', context)


@login_required(login_url=LOGIN_REQUIRED_URL)
def payment_status_verif(request):
    stripe_checkout_id = request.GET.get('session_id', None)
    user_payment_status = UserPaymentStatus.objects.filter(
        user=request.user,
        site_name=get_site_name(request),
        stripe_checkout_id=stripe_checkout_id,
    ).first()

    if user_payment_status is None:
        return HttpResponse(status=202, headers={'HX-Redirect': '/'})

    if user_payment_status.status == UserPaymentStatus.PENDING:
        return HttpResponse(status=202)

    return HttpResponse(status=202, headers={'HX-Redirect': '/'})


@login_required(login_url=LOGIN_REQUIRED_URL)
def payment_cancelled(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session_id = request.GET.get('session_id', None)
    user_payment_status, _ = UserPaymentStatus.objects.get_or_create(
        user=request.user,
        site_name=get_site_name(request),
    )
    user_payment_status.status = UserPaymentStatus.CANCELED
    user_payment_status.stripe_checkout_id = checkout_session_id
    user_payment_status.save()
    return redirect(f'{get_site_name(request)}/')


@csrf_exempt
def stripe_webhook(request):
    time.sleep(10)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    payload = request.body
    signature_header = request.META['HTTP_STRIPE_SIGNATURE']
    try:
        event = stripe.Webhook.construct_event(
            payload, signature_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        return HttpResponse(status=400)
    if event['type'] == 'checkout.session.completed':
        session = event['data']['object']
        session_id = session.get('id', None)
        user_payment_status = None
        for _ in range(5):
            user_payment_status = UserPaymentStatus.objects.filter(stripe_checkout_id=session_id).first()
            if user_payment_status is not None:
                break
            time.sleep(10)

        if user_payment_status is None:
            return HttpResponse(status=404)

        user_payment, _ = UserPayment.objects.get_or_create(
            user=user_payment_status.user,
            site_name=user_payment_status.site_name,
        )
        user_payment.stripe_checkout_id = user_payment_status.stripe_checkout_id
        user_payment.payment_bool = True
        user_payment.customer_type = user_payment_status.customer_type
        user_payment_status.status = UserPaymentStatus.SUCCESS
        user_payment.customer_type = UserPayment.STANDARD
        user_payment.save()
        user_payment_status.save()  # Saving just to have log history
        user_payment_status.delete()
    if event['type'] == 'customer.subscription.deleted':
        session = event['data']['object']
        session_id = session.get('id', None)
        UserPayment.objects.filter(stripe_checkout_id=session_id).delete()
    return HttpResponse(status=200)
