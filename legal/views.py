from django.shortcuts import render

def privacyPolicy(request):
    return render(request, 'legal/privacyPolicy.html')

def about(request):
    return render(request, 'legal/about.html')