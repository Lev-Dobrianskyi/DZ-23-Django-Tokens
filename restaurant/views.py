from django.shortcuts import render, get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from restaurant.models import Dish, Category, Table, Reservation
from restaurant.dishSerializer import DishSerializer, CategorySerializer
from restaurant.userSerializer import RegisterUserSerializer
from restaurant.reservationSerializer import (
    TableSerializer,
    ReservationSerializer,
    ReservationStatusSerializer,
)


def index(request):
    return render(request, "restaurant/index.html")


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer
    permission_classes = [AllowAny]


class GetDishView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=DishSerializer)
    def get(self, request, dish_id):
        dish = get_object_or_404(Dish, pk=dish_id)
        return Response({
            "message": f"Dish view: {dish.name}",
            "dish_name": dish.name,
            "dish_description": dish.description,
            "dish_price": str(dish.price),
            "dish_available": dish.available,
        })


class GetDishesView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=DishSerializer(many=True))
    def get(self, request):
        dishes = Dish.objects.all()
        return Response({
            "message": "All dishes",
            "dishes": DishSerializer(dishes, many=True).data,
        })


class GetCategoriesView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=CategorySerializer(many=True))
    def get(self, request):
        categories = Category.objects.all()
        return Response({
            "message": "All categories",
            "categories": CategorySerializer(categories, many=True).data,
        })


class AddDishView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=DishSerializer, responses=DishSerializer)
    def post(self, request):
        serializer = DishSerializer(data=request.data)
        if serializer.is_valid():
            dish = serializer.save()
            return Response(DishSerializer(dish).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TableListView(generics.ListAPIView):
    queryset = Table.objects.all().order_by("number")
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticated]


class ReservationListCreateView(generics.ListCreateAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user).order_by("-date", "-time")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ReservationDetailView(generics.RetrieveAPIView):
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)


class ReservationStatusView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(request=ReservationStatusSerializer, responses=ReservationSerializer)
    def patch(self, request, pk):
        reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
        serializer = ReservationStatusSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reservation.status = serializer.validated_data["status"]
        reservation.save()
        return Response(ReservationSerializer(reservation).data)


class ReservationCancelView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=ReservationSerializer)
    def post(self, request, pk):
        reservation = get_object_or_404(Reservation, pk=pk, user=request.user)
        if reservation.status == "cancelled":
            return Response(
                {"error": "Reservation already cancelled."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        reservation.status = "cancelled"
        reservation.save()
        return Response(ReservationSerializer(reservation).data)