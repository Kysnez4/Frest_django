import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(payment):
    """Создает продукт в Stripe"""
    product_name = None
    if payment.paid_course:
        product_name = payment.paid_course.name
    elif payment.paid_lesson:
        product_name = payment.paid_lesson.name

    product = stripe.Product.create(
        name=product_name,
        description=f"Payment for {product_name}",
    )
    return product


def create_stripe_price(payment, product_id):
    """Создает цену в Stripe"""
    price = stripe.Price.create(
        unit_amount=int(payment.amount * 100),  # Конвертируем в копейки
        currency="rub",
        product=product_id,
    )
    return price


def create_stripe_session(price_id, success_url, cancel_url):
    """Создает сессию оплаты в Stripe"""
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url=success_url,
        cancel_url=cancel_url,
    )
    return session


def get_payment_status(session_id):
    """Получает статус платежа"""
    session = stripe.checkout.Session.retrieve(session_id)
    return session.payment_status
