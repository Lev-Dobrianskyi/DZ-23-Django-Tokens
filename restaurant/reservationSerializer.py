from rest_framework import serializers
from restaurant.models import Table, Reservation


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ["id", "number", "seats", "available"]


class ReservationSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    table_number = serializers.IntegerField(source="table.number", read_only=True)
    table_seats = serializers.IntegerField(source="table.seats", read_only=True)

    class Meta:
        model = Reservation
        fields = [
            "id", "user", "table", "table_number", "table_seats",
            "date", "time", "guests", "status", "created_at",
        ]
        read_only_fields = ["id", "user", "status", "created_at"]

    def validate(self, data):
        table = data.get("table") or (self.instance.table if self.instance else None)
        guests = data.get("guests") or (self.instance.guests if self.instance else None)
        if table and guests and guests > table.seats:
            raise serializers.ValidationError(
                f"Table {table.number} only seats {table.seats} guests."
            )
        return data


class ReservationStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=[c[0] for c in Reservation.STATUS_CHOICES])