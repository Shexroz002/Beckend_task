from django.db import models
from django.db.models import FloatField, F, Func, ExpressionWrapper
from django.db.models.functions import Sqrt, Power


class FootballFieldQuerySet(models.QuerySet):
    def annotate_distance(self, target_latitude, target_longitude):
        if target_latitude is None or target_longitude is None:
            return self.annotate(distance=None)

        # Calculate Euclidean distance
        distance_expression = Sqrt(
            Power(F('latitude') - target_latitude, 2) +
            Power(F('longitude') - target_longitude, 2)
        )

        return self.annotate(distance=ExpressionWrapper(distance_expression, output_field=FloatField()))



