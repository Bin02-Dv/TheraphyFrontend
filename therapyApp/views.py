from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests

# Create your views here.
BASE_URL = "https://theraphy.alphatech247solutions.com/api"

def signout(request):
    url = f"{BASE_URL}/user/signout"

    try:
        response = requests.post(url, cookies=request.COOKIES)
        response_data = response.json()

        if response.status_code == 200:
            response = redirect("/")  # Redirect to the login page
            response.delete_cookie('jwt')  # Clear the JWT cookie
            return response
        else:
            msg = response_data.get("detail", 'Failed!')
            return JsonResponse({'success': False, 'message': msg})

    except requests.exceptions.RequestException as e:
        return JsonResponse({'success': False, 'message': str(e)})
    
def signin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        
        url = f'{BASE_URL}/user/signin'
        
        data = {
            "email": email,
            "password": password
        }

        try:
            response = requests.post(url, json=data)
            response_data = response.json()
            
            if response.status_code == 200:
                token = response_data.get('jwt')
                msg = 'Login Successfully..'
                response = JsonResponse({'success': True, 'message': msg, 'data': response_data})
                response.set_cookie(key='jwt', value=token, httponly=True)
                return response
            else:
                msg = response_data.get('detail', 'An error occurred during registration..')
                return JsonResponse({'success': False, 'message': msg, 'errors': response_data})

        except requests.exceptions.RequestException as e:
            return JsonResponse({'success': False, 'message': str(e)})
        
    return render(request, 'signin.html')

def signup(request):
    if request.method == 'POST':
        fullname = request.POST.get("full_name")
        phone_number = request.POST.get("phone_number")
        role = request.POST.get("role")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if confirm_password != password:
            return JsonResponse({'success': False, 'message': 'Password and confirm password do not match.'})

        url = f'{BASE_URL}/user/signup'
        data = {
            "full_name": fullname,
            "email": email,
            "phone_number": phone_number,
            "role": role,
            "password": password
        }

        try:
            response = requests.post(url, json=data)
            response_data = response.json()

            if response.status_code == 200:
                redirect_url = f"http://127.0.0.1:8000/therapist-desc/{response_data.get('id')}" if role == 'therapist' else '/'
                return JsonResponse({
                    'success': True,
                    'message': 'Sign Up Completed Successfully.',
                    'data': response_data,
                    'therapist': role == 'therapist',
                    'redirect_url': redirect_url
                })
            else:
                msg = response_data.get('error', 'An error occurred during registration.')
                return JsonResponse({'success': False, 'message': msg, 'errors': response_data})

        except requests.exceptions.RequestException as e:
            return JsonResponse({'success': False, 'message': 'Server error: ' + str(e)})

    return render(request, 'signup.html')

def index(request):
    current_user = None
    try:
        # Fetch current user data
        current_url = f"{BASE_URL}/user/active"
        current_response = requests.get(current_url, cookies=request.COOKIES)
        if current_response.status_code == 200:
            current_user = current_response.json()
        else:
            # Handle unauthorized or other issues
            return redirect('/')  # Redirect to login if unauthorized
        
        # Fatch all users
        all_admin_url = f"{BASE_URL}/user/admin/all"
        all_admin_response = requests.get(all_admin_url, cookies=request.COOKIES)
        if all_admin_response.status_code == 200:
            all_admin = all_admin_response.json()
        else:
            return None
        
        if request.method == 'POST':
            fullname = request.POST.get("full_name")
            phone_number = request.POST.get("phone_number")
            email = request.POST.get("email")
            password = request.POST.get("password")
            confirm_password = request.POST.get("confirm_password")

            if confirm_password != password:
                return JsonResponse({'success': False, 'message': 'Password and confirm password do not match.'})

            url = f'{BASE_URL}/user/signup'
            data = {
                "full_name": fullname,
                "email": email,
                "phone_number": phone_number,
                "password": password,
                "role": "admin"
            }

            try:
                response = requests.post(url, json=data)
                response_data = response.json()

                if response.status_code == 200:
                    return JsonResponse({
                        'success': True,
                        'message': 'Admin Added Successfully.',
                        'data': response_data,
                    })
                else:
                    msg = response_data.get('error', 'An error occurred during registration.')
                    return JsonResponse({'success': False, 'message': msg, 'errors': response_data})

            except requests.exceptions.RequestException as e:
                return JsonResponse({'success': False, 'message': 'Server error: ' + str(e)})

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return JsonResponse({'error': 'Failed to fetch user data'}, status=500)

    context = {
        "current_user": current_user,
        "all_user": all_admin
    }
    return render(request, 'dash/index.html', context)

def dash(request):
    current_user = None
    try:
        # Fetch current user data
        current_url = f"{BASE_URL}/user/active"
        current_response = requests.get(current_url, cookies=request.COOKIES)
        if current_response.status_code == 200:
            current_user = current_response.json()
        else:
            # Handle unauthorized or other issues
            return redirect('/')  # Redirect to login if unauthorized
        
        all_users_url = f"{BASE_URL}/user/all"
        all_users_response = requests.get(all_users_url, cookies=request.COOKIES)
        if all_users_response.status_code == 200:
            all_users = all_users_response.json()
        else:
            return None

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return JsonResponse({'error': 'Failed to fetch user data'}, status=500)

    context = {
        "current_user": current_user,
        "all_users": all_users,
    }
    return render(request, "dash/dash.html", context)

def payments(request):
    current_user = None
    try:
        # Fetch current user data
        current_url = f"{BASE_URL}/user/active"
        current_response = requests.get(current_url, cookies=request.COOKIES)
        if current_response.status_code == 200:
            current_user = current_response.json()
        else:
            # Handle unauthorized or other issues
            return redirect('/')  # Redirect to login if unauthorized
        
        all_payment_url = f"{BASE_URL}/payment/session/all"
        all_payment_response = requests.get(all_payment_url, cookies=request.COOKIES)
        if all_payment_response.status_code == 200:
            all_payment = all_payment_response.json()
        else:
            return None
        
        all_session_url = f"{BASE_URL}/therapy/session/all"
        all_session_response = requests.get(all_session_url, cookies=request.COOKIES)
        if all_session_response.status_code == 200:
            all_session = all_session_response.json()
        else:
            return None
        
        if request.method == 'POST':
            session = request.POST.get("session")
            amount = request.POST.get("amount")

            url = f'{BASE_URL}/payment/session/create'
            data = {
                "session": session,
                "amount": amount
            }

            try:
                response = requests.post(url, json=data, cookies=request.COOKIES)
                response_data = response.json()

                if response.status_code == 200:
                    return JsonResponse({
                        'success': True,
                        'message': 'Payment Completed Successfully.',
                        'data': response_data,
                    })
                else:
                    msg = response_data.get('error', 'An error occurred during Making the payment.')
                    return JsonResponse({'success': False, 'message': msg, 'errors': response_data})

            except requests.exceptions.RequestException as e:
                return JsonResponse({'success': False, 'message': 'Server error: ' + str(e)})

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return JsonResponse({'error': 'Failed to fetch user data'}, status=500)

    context = {
        "current_user": current_user,
        "all_payment": all_payment,
        'all_session': all_session
    }
    return render(request, 'dash/payments.html', context)

def therapist(request):
    current_user = None
    try:
        # Fetch current user data
        current_url = f"{BASE_URL}/user/active"
        current_response = requests.get(current_url, cookies=request.COOKIES)
        if current_response.status_code == 200:
            current_user = current_response.json()
        else:
            # Handle unauthorized or other issues
            return redirect('/')  # Redirect to login if unauthorized
        
        # Fatch all users
        all_user_url = f"{BASE_URL}/user/therapist/all"
        all_user_response = requests.get(all_user_url, cookies=request.COOKIES)
        if all_user_response.status_code == 200:
            all_user = all_user_response.json()
        else:
            return None

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return JsonResponse({'error': 'Failed to fetch user data'}, status=500)

    context = {
        "current_user": current_user,
        "all_user": all_user
    }
    return render(request, 'dash/therapist.html', context)

def session(request):
    try:
        # Fetch current user data
        current_url = f"{BASE_URL}/user/active"
        current_response = requests.get(current_url, cookies=request.COOKIES)
        if current_response.status_code == 200:
            current_user = current_response.json()
        else:
            # Handle unauthorized or other issues
            return redirect('/')  # Redirect to login if unauthorized
        
        all_session_url = f"{BASE_URL}/therapy/session/all"
        all_session_response = requests.get(all_session_url, cookies=request.COOKIES)
        if all_session_response.status_code == 200:
            all_session = all_session_response.json()
        else:
            return None
        
        # Fatch all therapist
        all_therapist_url = f"{BASE_URL}/user/therapist/all"
        all_therapist_response = requests.get(all_therapist_url, cookies=request.COOKIES)
        if all_therapist_response.status_code == 200:
            all_therapist = all_therapist_response.json()
        else:
            return None
        
        if request.method == 'POST':
            title = request.POST.get("title")
            description = request.POST.get("description")
            date = request.POST.get("date")
            therapist = request.POST.get("therapist")

            url = f'{BASE_URL}/therapy/session/create'
            data = {
                "title": title,
                "description": description,
                "date": date,
                "therapist": therapist,
            }

            try:
                response = requests.post(url, json=data, cookies=request.COOKIES)
                response_data = response.json()

                if response.status_code == 200:
                    return JsonResponse({
                        'success': True,
                        'message': 'Session Created Successfully.',
                        'data': response_data,
                    })
                else:
                    msg = response_data.get('error', 'An error occurred during registration.')
                    return JsonResponse({'success': False, 'message': msg, 'errors': response_data})

            except requests.exceptions.RequestException as e:
                return JsonResponse({'success': False, 'message': 'Server error: ' + str(e)})

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return JsonResponse({'error': 'Failed to fetch user data'}, status=500)

    context = {
        "current_user": current_user,
        "all_session": all_session,
        "all_therapist": all_therapist
    }
    return render(request, 'dash/session.html', context)

def therapist_desc(request, id):
    if request.method ==  'POST':
        bio = request.POST.get('bio')
        specialization = request.POST.get('specialization')
        years_of_experience = request.POST.get('years_of_experience')
        
        url = f"{BASE_URL}/user/therapist/profile/create/{id}"
        
        data = {
            "bio":bio,
            "specialty":specialization,
            "years_of_experience":years_of_experience
        }

        try:
            response = requests.post(url, json=data)
            response_data = response.json()

            if response.status_code == 200:
                return JsonResponse({
                    'success': True,
                    'message': 'Profile Completed Successfully..',
                    'data': response_data,
                })
            else:
                msg = response_data.get('error', 'An error occurred during creation.')
                return JsonResponse({'success': False, 'message': msg, 'errors': response_data})

        except requests.exceptions.RequestException as e:
            return JsonResponse({'success': False, 'message': 'Server error: ' + str(e)})
        
    return render(request, 'therapist-desc.html', {'id': id})

def client(request):
    current_user = None
    try:
        # Fetch current user data
        current_url = f"{BASE_URL}/user/active"
        current_response = requests.get(current_url, cookies=request.COOKIES)
        if current_response.status_code == 200:
            current_user = current_response.json()
        else:
            # Handle unauthorized or other issues
            return redirect('/')  # Redirect to login if unauthorized
        
        # Fatch all users
        all_user_url = f"{BASE_URL}/user/all"
        all_user_response = requests.get(all_user_url, cookies=request.COOKIES)
        if all_user_response.status_code == 200:
            all_user = all_user_response.json()
        else:
            return None

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return JsonResponse({'error': 'Failed to fetch user data'}, status=500)

    context = {
        "current_user": current_user,
        "all_user": all_user
    }
    return render(request, 'dash/client.html', context)

def update(request, id):
    current_user = None
    try:
        # Fetch current user data
        current_url = f"{BASE_URL}/user/active"
        current_response = requests.get(current_url, cookies=request.COOKIES)
        if current_response.status_code == 200:
            current_user = current_response.json()
        else:
            # Handle unauthorized or other issues
            return redirect('/')  # Redirect to login if unauthorized
        
        if request.method == 'POST':
            status = request.POST.get("status")

            url = f'{BASE_URL}/therapy/session/update/{id}'
            data = {
                "action": status
            }

            try:
                response = requests.put(url, json=data, cookies=request.COOKIES)
                response_data = response.json()

                if response.status_code == 200:
                    return JsonResponse({
                        'success': True,
                        'message': 'Session Updated Successfully.',
                        'data': response_data,
                    })
                else:
                    msg = response_data.get('error', 'An error occurred during Updating.')
                    return JsonResponse({'success': False, 'message': msg, 'errors': response_data})

            except requests.exceptions.RequestException as e:
                return JsonResponse({'success': False, 'message': 'Server error: ' + str(e)})

    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return JsonResponse({'error': 'Failed to fetch user data'}, status=500)

    context = {
        "current_user": current_user,
        "id": id
    }
    return render(request, 'dash/update.html', context)