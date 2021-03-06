import json
from datetime import datetime

from django.http  import JsonResponse
from django.views import View
from django.db    import transaction

from order.models   import Cart, Order
from user.models    import Address, OftenBuying, User
from product.models import Product
from user.utils     import signin_decorator


class CartView(View):
    @signin_decorator
    @transaction.atomic
    def post(self, request):
        try:
            data = json.loads(request.body)

            new_order, flag = Order.objects.get_or_create(
                user_id    = request.user.id,
                status_id  = 1,
                address_id = Address.objects.get(user_id=request.user.id, is_active=1).id,
                payment_method_id = 1,
            )
            if flag:
                new_order.order_number = f"{request.user.id}-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S-%f')}"
                new_order.save()

            new_order_id = new_order.id

            if Cart.objects.filter(order_id=new_order_id, product_id=data['product_id']).exists():
                product_in_cart           = Cart.objects.get(order_id=new_order_id, product_id=data['product_id'])
                product_in_cart.quantity += int(data['quantity'])
                product_in_cart.save()
                return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)

            Cart.objects.create(
                order_id    = new_order_id,
                product_id  = data['product_id'],
                quantity    = data['quantity'],
                is_selected = True,
            )
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)

        except KeyError as e:
            return JsonResponse({"MESSAGE": "KEY_ERROR => " + e.args[0]}, status=400)


    @signin_decorator
    def get(self, request):
        try:
            cart = Cart.objects.filter(order__user_id=request.user.id, order__status=1).prefetch_related("product__discount", "product__packing_type")

            items_in_cart = [{
                "id"                : item.id,
                "product_id"        : item.product.id,
                "name"              : item.product.name,
                "quantity"          : item.quantity,
                "price"             : item.product.price,
                "discount_rate"     : float(item.product.discount.percentage),
                "is_soldout"        : item.product.is_soldout,
                "cart_packing_type" : item.product.packing_type.cart_packing_type,
                "image_url"         : item.product.image_url,
                "selected"          : item.is_selected,
            }for item in cart]

            return JsonResponse({"MESSAGE": "SUCCESS", "items_in_cart": items_in_cart}, status=200)

        except Cart.DoesNotExist:
            return JsonResponse({"MESSAGE": "SUCCESS", "items_in_cart":[]}, status=200)


    @signin_decorator
    def delete(self, request):
        try:
            data = json.loads(request.body)
            item = Cart.objects.get(id=data['cart_item_id'])
            item.delete()

            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=204)

        except KeyError as e:
            return JsonResponse({"MESSAGE": "KEY_ERROR => " + e.args[0]}, status=400)
        except Cart.DoesNotExist:
            return JsonResponse({"MESSAGE": "ITEM_DOES_NOT_EXIST"}, status=400)


    @signin_decorator
    def patch(self, request):
        try:
            data      = json.loads(request.body)
            delta     = data.get('delta')
            select    = data.get('select')
            cart_item = Cart.objects.get(id=data['cart_item_id'])

            if delta == "minus":
                if cart_item.quantity == 1:
                    return JsonResponse({'MESSAGE': 'ITEM QUANTITY IS 1'}, status=400)
                cart_item.quantity -= 1
            elif delta == "plus":
                cart_item.quantity += 1
            elif select == "True":
                cart_item.is_selected = True
            elif select == "False":
                cart_item.is_selected = False
            else:
                return JsonResponse({"MESSAGE": "KEY_ERROR => IMPROPER delta OR select"}, status=400)
            cart_item.save()

            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)

        except KeyError as e:
            return JsonResponse({"MESSAGE": "KEY_ERROR => " + e.args[0]}, status=400)
        except Cart.DoesNotExist as e:
            return JsonResponse({"MESSAGE": "KEY_ERROR => " + e.args[0]}, status=400)


class OftenBuyingView(View):
    @signin_decorator
    def post(self, request):
        try:
            data    = json.loads(request.body)

            if not Product.objects.filter(id=data['product_id']).exists():
                return JsonResponse({'MESSAGE': 'PRODUCT_DOES_NOT_EXIST'}, status=400)

            if OftenBuying.objects.filter(user_id=request.user.id, product_id=data['product_id']).exists():
                return JsonResponse({'MESSAGE': 'PRODUCT_ALREADY_EXIST_IN_OFTEN_BUYING'}, status=400)

            OftenBuying.objects.create(
                user_id    = request.user.id,
                product_id = data['product_id'],
            )
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)

        except KeyError as e:
            return JsonResponse({"MESSAGE": "KEY_ERROR => " + str(e.args[0])}, status=400)

    @signin_decorator
    def get(self, request):
        try:
            user         = User.objects.get(id=request.user.id)
            often_buying = user.oftenbuying_set.all().select_related('product')

            items_in_often_buying = [{
                "id"               : item.id,
                "product_id"       : item.product.id,
                "name"             : item.product.name,
                "price"            : item.product.price,
                "image_url"        : item.product.image_url,
            }for item in often_buying]

            return JsonResponse({"MESSAGE": "SUCCESS", "items_in_often_buying": items_in_often_buying}, status=200)

        except OftenBuying.DoesNotExist:
            return JsonResponse({"MESSAGE": "SUCCESS", "items_in_cart":[]}, status=200)

    @signin_decorator
    def delete(self, request):
        try:
            data = json.loads(request.body)
            item = OftenBuying.objects.get(id=data['often_buying_item_id'])
            item.delete()

            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=204)

        except KeyError as e:
            return JsonResponse({"MESSAGE": "KEY_ERROR => " + e.args[0]}, status=400)
        except OftenBuying.DoesNotExist:
            return JsonResponse({"MESSAGE": "ITEM_DOES_NOT_EXIST"}, status=400)
