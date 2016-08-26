import json
import datetime
import time
import jenkinsapi
from jenkinsapi.jenkins import Jenkins
from jenkinsapi.views import Views
from jenkinsapi.view import View
from slackoff.models.model import Message
from slackoff.messagequeue import subscribe_to
from slackoff.messagebuilder.attachments import Attachment, Attachments

jenkinsUrl = "http://localhost:8080/"
j = None

try:
    j = Jenkins(jenkinsUrl)
except:
    raise Exception("Unable to connect to Jenkins")

@subscribe_to(Message)
def list_jobs_for_view(message):
    """
    respond to "jobs" with a list of jobs for the given View
    """

    # Dont reply to another bot
    if 'bot_id' in message.data:
        return

    if not message.text.startswith("jobs"):
        return

    client = message.get_client()
    view = message.text.replace("jobs", "").strip()
    jobsAttachment = get_jobs_for_view_attachments(view)
    if jobsAttachment is None:
        text = "Unknown View: " + view
        client.send_message(message.channel, text=text)
    else:                       
        client.send_message(message.channel, attachments=jobsAttachment)

@subscribe_to(Message)
def list_views(message):
    """
    respond to "views" with of the current views in jenkins
    """

    # Dont reply to another bot
    if 'bot_id' in message.data:
        return

    if not message.text == "views":
        return
    
    client = message.get_client()
    views = get_views_attachments()
    client.send_message(channel=message.channel, attachments=views)

def get_views_list():
    """
    get a list of all of the view names in Jenkins
    """
    views = Views(j)
    return list(views.iterkeys())

def get_views_attachments():
    """
    get attachments json of all of the views in Jenkins with links to each one
    """
    viewList = get_views_list()
    attachments = Attachments()

    for view in viewList:
        viewAttachment = Attachment()
        viewAttachment.title = view
        viewAttachment.title_link = jenkinsUrl + "view/" + view
        viewAttachment.use_random_color()

        attachments.add_attachment(viewAttachment)

    return attachments.get_json()

def get_jobs_for_view_attachments(name):
    """
    get attachments json of all of the jobs for a given view name in jenkins
    """
    if name not in get_views_list():
        return 

    view = View(jenkinsUrl + "view/" + name, name, j)
    jobs = view.get_job_dict()

    attachments = Attachments()
    for jobName, url in jobs.items():
        job = view.__getitem__(jobName)
        build = job.get_last_build_or_none()
        jobAttachment = Attachment()
        jobAttachment.title = jobName.replace(name+"-", "")
        jobAttachment.title_link = url
        jobAttachment.color = get_color_for_job(job, build)

        if build is not None:
            jobAttachment.ts = time.mktime(build.get_timestamp().timetuple())

        attachments.add_attachment(jobAttachment)

    return attachments.get_json()

def get_color_for_job(job, build):
    """Get the color to use for a specific job

    Keyword arguments:
    job -- {Job} The job to return a color for
    build -- {Build} The build to return a color for
    """
    if build is None:
        return '#D3D3D3' # Grey

    if job.is_queued_or_running():
        return "#33A8FF" # Blue

    if build.get_status() == "SUCCESS":
        return "#33FF5B" # Green
    
    return "#FC1A1A" # Red
