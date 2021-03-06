from django.db.models import F, Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Auction
from .serializers import AuctionSerializer, BuyItNowSerializer
from .enums import AuctionStatusEnum, AuctionTypeEnum
from core.views import BaseDetailView
from core.views import Pagination
from offer.serializers import CreateOfferSerializer, OfferSerializer


class AuctionListView(APIView):
    def get(self, request, format=None):
        params = request.query_params
        filter_params = Q()

        if params.get('status'):
            status = params.get('status')
            if status and int(status) in [i.value for i in AuctionStatusEnum]:
                filter_params &= Q(auction_status=int(status))
                #
        if params.get('type'):
            type = params.get('type')
            if type and int(type) in [i.value for i in AuctionTypeEnum]:
                filter_params &= Q(type=int(type))

        auction_qs = Auction.objects.filter(filter_params).order_by(F('closing_date') - F('opening_date'), 'end_price')

        paginator = Pagination()
        page = paginator.paginate_queryset(auction_qs, request)
        serializer = AuctionSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class AuctionDetailView(BaseDetailView):
    model = Auction
    model_serializer = AuctionSerializer


class CreateAuctionView(APIView):
    def post(self, request, format=None):
        serializer = AuctionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class MakeOffer(APIView):
    def post(self, request, pk, format=None):
        print('OFFER USER:', request.user)
        context = {
            'user': request.user,
            'auction_pk': pk
        }
        offer_serializer = CreateOfferSerializer(data=request.data, context=context)
        if offer_serializer.is_valid():
            offer_serializer.save()       
            return Response(status=status.HTTP_201_CREATED)
        else:
            return Response({'detail': offer_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class AuctionRecentOffersView(APIView):
    def get(self, request, pk, format=None):
        """
            Return last 5 offers
        """
        offer_qs = Auction.objects.get(pk=pk).offer_set.order_by('-pk')[:5]
        serializer = OfferSerializer(offer_qs, many=True)
        return Response(serializer.data)


class BuyItNowView(APIView):
    def put(self, request, pk, format=None):
        try:
            auction = Auction.objects.get(pk=pk)
        except Auction.DoesNotExist:
            return Response({'detail': 'Invalid auction id'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = BuyItNowSerializer(auction, data={'id': pk})
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        return Response({'detail': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
