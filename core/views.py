from django.shortcuts import render



def dashboard(request):
    return render(request, 'dashboard/dashboard.html')

def placements(request):
    return render(request, 'placements/placements.html')
