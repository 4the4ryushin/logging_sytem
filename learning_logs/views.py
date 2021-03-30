from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from .models import Topic , Entry
from .forms  import TopicForm , EntryForm
from django.http import Http404

# Create your views here.
def index(request):
	"""the home page for learning_log."""
	return render(request,'learning_logs/index.html')

@login_required
def topics(request ):
	topics=Topic.objects.filter(owner=request.user).order_by('date_added')
	context={'topics':topics}
	return render(request,'learning_logs/topics.html',context)

@login_required	
def topic(request , topic_id):
	topic=Topic.objects.get(id=topic_id)
	#Make sure that topic belonges to the current user.
	if topic.owner != request.user:
		raise Http404
	entries=topic.entry_set.order_by('-date_added')
	context={'topic':topic,'entries':entries}
	return render(request,'learning_logs/topic.html',context)

@login_required
def new_topic(request):
	"""add a new topic"""
	if request.method !='POST':
		#no data submitted;create a blank form.
		form=TopicForm()
	else:
		form=TopicForm(data=request.POST)
		if form.is_valid():
			new_topic=form.save(commit=False)#writes the data to database servers.
			new_topic.owner=request.user
			new_topic.save()
			return redirect('learning_logs:topics')
	# Display a blanck or invalid form.
	context={'form':form}
	return render(request,'learning_logs/new_topic.html',context)

@login_required
def new_entry(request,topic_id):
	"""add a new entry for a perticular topic."""
	topic=Topic.objects.get(id=topic_id)#quiery

	if request.method != 'POST':
		#no data is posted yet , create a blanck form. 
		form=EntryForm()
	else:
		#POST data submitted ,process data.
		form=EntryForm(data=request.POST)
		if form.is_valid():
			new_entry=form.save(commit=False)#creates new_entry(fuxn) obj.assigned to new_entry without saving the data to database
			new_entry.topic=topic
			new_entry.owner=request.user
			new_entry.save()
			return redirect('learning_logs:topic',topic_id=topic_id)

	#Display a blanck or invalid form:
	context={'topic':topic,'form':form}
	return render(request,'learning_logs/new_entry.html',context)

@login_required
def edit_entry(request,entry_id):
	"""edit an existing entry"""
	entry=Entry.objects.get(id=entry_id)
	topic=entry.topic
	if topic.owner != request.user:
		raiseHttp404

	if request.method != 'POST':
		#Initial request;pre-fill form with current entry.
		form=EntryForm(instance=entry)
	else:
		#POST data submitted;process data.
		form=EntryForm(instance=entry,data=request.POST)
		if form.is_valid():
			form.save()
			return redirect('learning_logs:topic',topic_id=topic.id)

	context={'entry':entry,'topic':topic,'form':form}
	return render(request,'learning_logs/edit_entry.html',context)
		



