from django.shortcuts import render, redirect


def landingPage(request):
    user = request.user
    if user.is_authenticated:
        return redirect('user-homepage', user.id)
    context = {}
    return render(request, 'landing.html', context)
