from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse

from .models import FalseInformation, RFRModel, FeedbackModel

from users.models import Interests
from users.forms import InterestsForm
from gossips.models import GossipsModel
from cheaters.models import CheatersModel


def index(request):
    if request.user.is_authenticated:
        return redirect('gossips:gossips_index')
    else:
        return redirect('/accounts/login')


@login_required()
def welcome(request):
    interests = Interests.objects.all()
    if request.method == 'POST':
        form = InterestsForm(request.POST or None, instance=request.user.profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Interests saved successfully")
            return redirect('gossips:gossips_index')

    context = {'interests': interests}
    return render(request, 'welcome.html', context)


@login_required()
def rfr(request):
    if request.method == 'POST':
        section = request.POST.get('section', False)
        post_id = request.POST.get('post_id', False)
        reason = request.POST.get('reason', False)

        if section == 'gossip':
            post = get_object_or_404(GossipsModel, id=post_id)
        elif section == 'cheater':
            post = get_object_or_404(CheatersModel, id=post_id)

        post_url = request.build_absolute_uri(post.get_absolute_url())
        subject = f"Request For Removal for {section} - {post.title}"
        message = f"Request came from user: {request.user.username} \n \nPost Id: {post.id} \n \nPost Title: {post.title} \n \nPost link: {post_url} \n \nReason: {reason}"
        send_mail(subject, message, 'gossipsbook.in@gmail.com', ['gossipsbook.in@gmail.com', 'emperorgold360@gmail.com'])

        RFRModel.objects.create(
            user = request.user,
            post_id = post_id,
            post_title = post.title,
            section = section,
            reason = reason
            )

        messages.success(request, 'Your request has been submitted and will be reviewed')
    return redirect('gossips:gossips_index')


def feedback(request):
    feedback_message = request.GET.get('feedback_message', False)
    if feedback_message:
        if request.user.is_authenticated:
            username = request.user.username
            email = request.user.email
        else:
            username = "AnonymousUser"
            email = "AnonymousUser"

        user = username
        email = email
        subject = 'Gossipsbook - New Feedback Message'
        message = f"Feedback from '{username}'. \nEmail: {email} \n \nMessage: {feedback_message}"
        send_mail(subject, message, 'gossipsbook.in@gmail.com', ['gossipsbook.in@gmail.com', 'emperorgold360@gmail.com'])

        FeedbackModel.objects.create(
            user = username,
            email = email,
            message = feedback_message,
            )
        
        messages.success(request, 'Feedback received. Thank you!')
    return redirect('gossips:gossips_index')


def false_information(request):
    return render(request, 'false_information.html', {'posts': FalseInformation.objects.all().order_by('-date_published')})


def privacy_policy(request):
    return render(request, 'privacy_policy.html')

