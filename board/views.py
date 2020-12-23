import json

from django.http  import JsonResponse
from django.views import View

from .models import Review


class ReviewView(View):
    #@login_required
    def post(self, request):
        try:
            data = json.loads(request.body)
            user_id = "3"

            Review.objects.create(
                author_id  = user_id,
                product_id = data['product_id'],
                title      = data['title'],
                contents   = data['contents'],
                help_count = 0,
                hit_count  = 0,
                image_url  = data['image_url'],
            )
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)

        except KeyError as e:
            return JsonResponse({"MESSAGE": "KEY_ERROR => " + e.args[0]}, status=400)

    # @login_required
    def get(self, request, review_id):
        try:
            review = Review.objects.get(id=review_id)
            review.hit_count += 1
            review.save()
            review_post = [{
                'id'        : review.id,
                'title'     : review.title,
                'contents'  : review.contents,
                'help_count': review.help_count,
                'hit_count' : int(review.hit_count),
                'image_url' : review.image_url,
            }]

            return JsonResponse({"MESSAGE": "SUCCESS", "review_post": review_post}, status=201)

        except Review.DoesNotExist as e:
           return JsonResponse({"MESSAGE": "KEY_ERROR => " + e.args[0]}, status=400)


    # @login_required
    def patch(self, request, review_id):
        try:
            data = json.loads(request.body)
            user_id = "3"

            review = Review.objects.get(id=review_id, author_id=user_id)
            if data.get('title'):
                review.title = data.get('title')
            if data.get('contents'):
                review.contents = data.get('contents')
            if data.get('image_url'):
                review.image_url = data.get('image_url')
            if data.get('help') == "True":
                review.help_count += 1
            review.save()

            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=200)

        except KeyError as e:
            return JsonResponse({"MESSAGE": "KEY_ERROR => " + e.args[0]}, status=400)
        except Review.DoesNotExist:
            return JsonResponse({"MESSAGE": "REVIEW_DOES_NOT_EXIST"}, status=400)

    # @login_required
    def delete(self, request, review_id):
        try:
            user_id = "3"

            review = Review.objects.get(id=review_id, author_id=user_id)
            review.delete()

            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=204)

        except Review.DoesNotExist:
            return JsonResponse({"MESSAGE": "REVIEW_DOES_NOT_EXIST"}, status=400)


class ReviewListView(View):
    # @login_required
    def get(self, request, product_id):
        try:
            offset = int(request.GET.get('offset'), 0)
            limit  = int(request.GET.get('limit'), 10)
            limit += offset

            reviews = Review.objects.order_by('-id').filter(product_id=product_id)

            review_list = [{
                'id'        : review.id,
                'title'     : review.title,
                'contents'  : review.contents,
                'help_count': review.help_count,
                'hit_count' : review.hit_count,
                'image_url' : review.image_url,

            }for review in reviews[offset:limit]]

            return JsonResponse({'MESSAGE': 'SUCCESS', "review_list": review_list}, status=200)

        except Exception as e:
            return JsonResponse({'message' : 'ERROR => ' + e.args[0]}, status = 400)
