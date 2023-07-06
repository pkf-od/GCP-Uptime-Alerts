from google.cloud import compute_v1
from date_library import get_current_time, get_start_time, get_total_uptime
from email_library import send_email
import os
import functions_framework
from flask import make_response

def uptime_alert(request):
  # Create a Compute Engine client: used to interact and manage a VM instance programatically
  compute_client = compute_v1.InstancesClient()

  # Provide your project ID and zone
  project_id = os.environ.get("PROJECT_ID")
  zone = os.environ.get("ZONE")
  instance_name = os.environ.get("INSTANCE_NAME")

  # Get the instance details
  instance_response = compute_client.get(project=project_id, zone=zone, instance=instance_name)
  print(f"Instance response: {instance_response.status}")

  # Check if the instance is currently running
  if instance_response.status == "RUNNING":
      # Extract the VM instance's start time
      start_time = instance_response.last_start_timestamp
      #print(f"start_time: {start_time}")

      # Convert the start time to the correct format
      start_time = get_start_time(start_time)

      # Get the current time in the correct format
      current_time = get_current_time()

      total_uptime = get_total_uptime(start_time, current_time)
      #print(f"Total Uptime in Hours: {total_uptime}")

      # If we exceed a total uptime of 2 hours, then we want to send an email alert
      if total_uptime > 2.0:
          # Set up the sender, sender password, and all receivers
          email_sender = os.environ.get("SENDER")
          email_password = os.environ.get("PASSWORD")
          email_recipients_string = os.environ.get("RECIPIENTS")
          email_recipients_list = email_recipients_string.split(",")
         
          # Create the email's subject and body message
          subject = "VM Uptime Threshold Exceeded"
          body = """The Kraken VM instance has exceeded a runtime of 2 hours, with a total uptime of {:0.2f} hours.

  If you are not currently using thekraken, please turn it off!""".format(total_uptime)

          # Send the email
          send_email(email_sender, email_password, email_recipients_list, subject, body)
      else:
          print("Did not exceed 5 minute threshold (no email sent)")
  else:
    print("Instance is not currently running.")

  response_body = "Code successfully executed!"
  status_code = 200
  headers = {"Content-Type": "text/plain"}

  return make_response(response_body, status_code, headers)