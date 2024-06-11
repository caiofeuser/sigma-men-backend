from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.conf import settings
import stripe
import logging
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
# import actions
from rest_framework.decorators import action
from django.http import HttpResponse
import json
from . import serializers
from . import models
from rest_framework import viewsets
from django.db.models.signals import post_save
from django.dispatch import receiver
import datetime

# import custumo user model
from auth_api.models import CustomUserModel


class SurveyViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        if 'survey_name' not in self.kwargs:
            return models.Survey.objects.all()
        survey_name = self.kwargs['survey_name']
        queryset = models.Survey.objects.filter(name=survey_name)
        return queryset
    serializer_class = serializers.SurveySerializer


class QuestionViewSet(viewsets.ModelViewSet):

    def get_queryset(self):
        if 'survey_name' not in self.kwargs:
            return models.Question.objects.all()
        survey_name = self.kwargs['survey_name']
        queryset = models.Question.objects.filter(
            survey__name=survey_name).order_by('position')
        queryset = queryset.prefetch_related('options')

        return queryset

    @action(detail=True, methods=['get'])
    def options(self, request, pk=None, survey_name=None):
        survey_name = self.kwargs['survey_name']
        question = self.get_object()
        options = question.options.all()
        serializer = serializers.OptionSerializer(options, many=True)
        return Response(serializer.data)

    serializer_class = serializers.QuestionSerializer


class TrackViewSet(viewsets.ModelViewSet):
    queryset = models.Track.objects.all()
    serializer_class = serializers.TrackSerializer


class OptionsViewSet(viewsets.ModelViewSet):
    # queryset = models.Option.objects.all()
    def get_queryset(self):
        if 'question_id' not in self.kwargs:
            return models.Option.objects.all()
        question_id = self.kwargs['question_id']
        queryset = models.Option.objects.filter(question=question_id)
        return queryset
    serializer_class = serializers.OptionSerializer


class ResultViewSet(viewsets.ModelViewSet):
    def get_queryset(self):
        survey_name = self.kwargs['survey_name']
        track_id = self.kwargs['track_id']

        queryset = models.Result.objects.filter(
            survey__name=survey_name,
            track__id=track_id
        )
        return queryset

    def list(self, request, *args, **kwargs):
        survey_name = self.kwargs['survey_name']
        track_id = self.kwargs['track_id']
        queryset = self.get_queryset()
        serializer = serializers.ResultSerializer(queryset, many=True)
        # It should be only one result
        response = serializer.data[0]

        return Response(response)

    queryset = models.Result.objects.all()
    serializer_class = serializers.ResultSerializer


@api_view(['GET'])
def APIOverview(request):
    user = {'name': 'João', 'age': 22}
    return Response(user)


stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeCheckoutView(APIView):
    def post(self, req):
        try:
            user_email = str(req.user)
            custom_user_stripe_id = CustomUserModel.objects.filter(
                email=user_email).values('stripe_id')[0]['stripe_id']

            if not custom_user_stripe_id:
                custom_user = CustomUserModel.objects.get(email=user_email)
                custom_user.stripe_id = stripe.Customer.create(
                    email=user_email).id
                custom_user.save()

            line_items = []
            for item in req.data['formatedData']:
                line_item = {
                    'price': item['price_id'],
                    'quantity': item['quantity'],
                }
                line_items.append(line_item)

            checkout_session = stripe.checkout.Session.create(
                line_items=line_items,
                customer_email=user_email,
                payment_method_types=['card'],
                mode='payment',
                success_url=settings.DOMAIN +
                '/checkout/success/?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.DOMAIN + '/checkout/canceled',
                # cancel_url=settings.DOMAIN + 'canceled',
            )

            return Response({'url': checkout_session.url})
            # return Response({'message': 'Success'})

            # return redirect(checkout_session.url)
        except stripe.error.CardError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class StripeProductView(APIView):
    def get(self, req):
        try:
            products = stripe.Product.list()
            prices = stripe.Price.list()
            for price in prices:
                for product in products:
                    if price.product == product.id:
                        product['price_monetary'] = price.unit_amount/100

            formated_products = []
            for product in products:
                if product.active:
                    formated_products.append({
                        'stripeID': product.default_price,
                        'id': product.id,
                        'image': product.images,
                        'name': product.name,
                        'object': product.object,
                        'type': product.type,
                        'description': product.description,
                        'price_monetary': product['price_monetary'],
                        'label': product.unit_label
                    })

            return Response(formated_products)
        except stripe.error.CardError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class StripeOrdersView(APIView):
    def get(self, request):
        user_email = str(request.user)
        try:
            custom_user = CustomUserModel.objects.get(email=user_email)
        except CustomUserModel.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        custom_user_stripe_id = custom_user.stripe_id

        if not custom_user_stripe_id:
            stripe_customer = stripe.Customer.create(email=user_email)
            custom_user.stripe_id = stripe_customer.id
            custom_user.save()
            custom_user_stripe_id = stripe_customer.id

        custom_user_stripe_id = str(custom_user_stripe_id)
        users = stripe.Customer.list()
        try:
            orders = stripe.checkout.Session.list(
                customer_details={"email": str(user_email)},
                expand=['data.line_items']
            )

            formated_orders = []
            for order in orders:
                formated_orders.append({
                    'id': order.id,
                    'date': datetime.datetime.fromtimestamp(order.created).strftime('%Y-%m-%d %H:%M:%S'),
                    'status': order.payment_status,
                    'amount_total': order.amount_total,
                    'payment_status': order.payment_status,
                    'line_items': order.line_items
                })

        except stripe.error.StripeError as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(formated_orders)


def get_list_on_chekout(req):
    if req.method == 'GET':
        session_id = req.GET.get('session_id')
        product_list = stripe.checkout.Session.list_line_items(session_id).data
        formated_data = []
        products = stripe.Product.list()
        for product in product_list:
            # apend the image of the respective product
            for p in products:
                if p.id == product.price.product:
                    product.image = p.images[0]
                    break

            formated_data.append({
                'price': product.amount_subtotal/100,
                'name': product.description,
                'quantity': product.quantity,
                'price_id': product.price.id,
                'product_id': product.price.product,
                'image': product.image
            })

        serialized_info = json.dumps(formated_data)
        return HttpResponse(serialized_info)


def get_products_with_categories(req):
    track = req.GET.get('track')
    survey = req.GET.get('survey')
    query = f"metadata['track']:'{track}' AND metadata['survey']:'{survey}'"
    products = stripe.Product.search(
        query=query)
    prices = stripe.Price.list()
    for price in prices:
        for product in products:
            if price.product == product.id:
                product['price_monetary'] = price.unit_amount/100
    formated_products = []
    for product in products:
        if product.active:
            formated_products.append({
                'stripeID': product.default_price,
                'id': product.id,
                'image': product.images,
                'name': product.name,
                'object': product.object,
                'type': product.type,
                'description': product.description,
                'price_monetary': product['price_monetary'],
                'label': product.unit_label
            })

    serialized_info = json.dumps(formated_products)
    return HttpResponse(serialized_info)


def button_status_api(request):
    # Assuming you have only one instance
    button_status = models.Partnerships.objects.first()
    if button_status:
        return JsonResponse({"display_button": button_status.display_button})
    else:
        return JsonResponse({"display_button": False})


def get_info_contact(request):
    contact_info = models.ContactInformation.objects.first()
    if contact_info:
        return JsonResponse({
            "phone": contact_info.phone,
            "email": contact_info.email,
            "address": contact_info.address,
            "instragram": contact_info.instragram
        })
    else:
        return JsonResponse({
            "phone": "",
            "email": "",
            "address": "",
            "instragram": ""
        })


@receiver(post_save, sender=models.Partnerships)
def update_button_status(sender, instance, **kwargs):
    # Logic to determine if button should be displayed
    display_button = instance.display_button

    # You can send a signal to your Next.js app here
    # This example assumes you have an API endpoint to communicate with Next.js
    # You can send the updated button status via this endpoint
    # Example using JsonResponse:
    response_data = {"display_button": display_button}
    return JsonResponse(response_data)
