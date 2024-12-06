from .models import Cart


def get_cart(request):
    session_id = request.session.get("cart_session_id")
    if not session_id:
        cart = Cart.objects.create()
        request.session["cart_session_id"] = str(cart.session_id)
    else:
        cart, _ = Cart.objects.get_or_create(session_id=session_id)
    return cart
