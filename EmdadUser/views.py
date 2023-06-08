from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser, Technecian
from django.contrib.auth.hashers import check_password
from .serializers import UserSerializer
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions
import json

@csrf_exempt
def validate_credentials(request):
    if request.method == 'POST':
        try:
            body = request.body.decode('utf-8')
            data = json.loads(body)
            phone = data.get('phone')
            password = data.get('password')
            user = Technecian.objects.get(user_id__phone=phone)
            
            if check_password(password,user.user_id.password):
                return JsonResponse({'success': True, 'message':'ok'})
            else:
                return JsonResponse({'success': False, 'message': 'Invalid phone number or password.'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'message': 'Invalid JSON format.'}, status=400)
        except CustomUser.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invalid phone number or password.'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, status=400)
    else:
        return JsonResponse({'success': False, 'message': 'Invalid request method.'}, status=400)
    



class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, permissions.BasePermission]

    def get_object(self):
        user =  self.request.user
        obj = get_object_or_404(CustomUser, phone=user.phone)
        self.check_object_permissions(self.request, obj)
        return obj    