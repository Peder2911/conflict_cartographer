
from django.contrib.auth.models import User

from rest_framework.viewsets import ModelViewSet
#from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import ModelSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.routers import DefaultRouter
from rest_framework.pagination import PageNumberPagination

from django_filters import rest_framework as filters

from api.models import Shape,Feedback,Country


# ========================================================

class AdminModelViewSet(ModelViewSet):
    permission_classes=[IsAdminUser]


class SmallAdminPagination(PageNumberPagination):
    page_size = 25 
    page_size_query_param = 'page_size'
    max_page_size = 25 

class LargeAdminPagination(PageNumberPagination):
    page_size = 100 
    page_size_query_param = 'page_size'
    max_page_size = 1000

# ========================================================

class UserSerializer(ModelSerializer):
    class Meta:
        model = User 
        fields = ["username"]

class UserViewSet(AdminModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer 
    pagination_class = LargeAdminPagination

# ========================================================

class ShapeFilter(filters.FilterSet):
    after = filters.DateFilter(field_name="date",lookup_expr="gte")
    before = filters.DateFilter(field_name="date",lookup_expr="lte")
    author = filters.ModelChoiceFilter(field_name="author",queryset=User.objects.all())
    gwno = filters.ModelChoiceFilter(field_name="country",queryset=Country.objects.all())

class ShapeSerializer(ModelSerializer):
    class Meta:
        model = Shape
        fields = ["country","shape","date","author","values"]

class ShapeViewSet(AdminModelViewSet):
    queryset = Shape.objects.all()
    serializer_class = ShapeSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ShapeFilter
    pagination_class = LargeAdminPagination

# ========================================================

class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = ["gwno","name","active"]

class CountryViewset(AdminModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer 
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_fields = ["active"] 
    pagination_class = LargeAdminPagination

# ========================================================

class FeedbackSerializer(ModelSerializer):
    class Meta:
        model = Feedback 
        fields = ["message","author","stars"]

class FeedbackViewset(AdminModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer 
    filter_backends = (filters.DjangoFilterBackend,)
    pagination_class = SmallAdminPagination 

# ========================================================

router = DefaultRouter()
router.register(r"shapes",ShapeViewSet,basename="admin_shape")
router.register(r"users",UserViewSet,basename="admin_user")
router.register(r"countries",CountryViewset,basename="admin_country")
router.register(r"feedback",FeedbackViewset,basename="admin_feedback")
