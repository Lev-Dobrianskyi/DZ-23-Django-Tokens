from django.urls import path
from restaurant.views import ( index, RegisterView, AddDishView, GetDishesView, GetDishView, GetCategoriesView, TableListView, ReservationListCreateView, ReservationDetailView, ReservationStatusView, ReservationCancelView)

urlpatterns = [
    path("", index, name="index"),
    path("register/", RegisterView.as_view(), name="register"),
    path("dishes/add/", AddDishView.as_view(), name="add_dish"),
    path("dishes/<int:dish_id>/", GetDishView.as_view(), name="get_dish"),
    path("dishes/", GetDishesView.as_view(), name="get_dishes"),
    path("categories/", GetCategoriesView.as_view(), name="get_categories"),
    path("tables/", TableListView.as_view(), name="table_list"),
    path("reservations/", ReservationListCreateView.as_view(), name="reservation_list_create"),
    path("reservations/<int:pk>/", ReservationDetailView.as_view(), name="reservation_detail"),
    path("reservations/<int:pk>/status/", ReservationStatusView.as_view(), name="reservation_status"),
    path("reservations/<int:pk>/cancel/", ReservationCancelView.as_view(), name="reservation_cancel"),
]