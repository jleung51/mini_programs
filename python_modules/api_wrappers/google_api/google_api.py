# This Python 3 module provides classes to access the Google API.

import argparse
import os

from httplib2 import Http

# Google API
from apiclient.discovery import build
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.service_account import ServiceAccountCredentials

# Gmail
import base64
from email.mime.text import MIMEText

# Google Drive
import json
from apiclient.http import MediaFileUpload

# Custom modules
from logger import Logger

class _GoogleApi:
    """Template for a wrapper class for the Google API.

    To use, extend this class in the same file.
    """

    _scope = ""
    _service = None

    def _get_credentials(self):
        """Refreshes Google access credentials, authorizing if necessary.

        self._scope must have been set in the subclass.

        Requires a client_secret.json file in the same directory. See README
        for instructions to create it.
        The credentials will be saved to generated_credentials.json.

        Arguments:
        scope -- String. Google Authentication scope which allows for a specific
            area of access.
            https://developers.google.com/identity/protocols/googlescopes
        Returns: OAuth credentials.
        """
        credential_path = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                "generated_credentials.json"
        )
        store = Storage(credential_path)

        credentials = store.get()
        if not credentials or credentials.invalid:
            flow = client.flow_from_clientsecrets(
                "client_secret.json", self._scope
            )
            flow.user_agent = self.application_name

            flags = argparse \
                    .ArgumentParser(parents=[tools.argparser]) \
                    .parse_args()
            flags.noauth_local_webserver = True
            credentials = tools.run_flow(flow, store, flags)

            Logger.debug(
                    "Google Drive credentials saved to [" +
                    credential_path + "]"
            )

        return credentials

class GmailApi(_GoogleApi):
    """Wrapper for the Gmail API."""

    _scope = "https://www.googleapis.com/auth/gmail.send"

    def _create_message(self, sender, recipient, subject, message_text):
        message = MIMEText(message_text)
        message["from"] = sender
        message["to"] = recipient
        message["subject"] = subject
        return {"raw":
                base64.urlsafe_b64encode(
                        message.as_string().encode()
                ).decode("utf-8")
        }

    def __init__(self, source_email, application_name=None):
        """Instantiates a GmailApi object and refreshes its credentials.

        Parameters:
        source_email -- String. Gmail account from which your emails
            will be sent. This should include the "@gmail.com".
            E.g. "gmail_source@email.com"
        application_name -- String. Application name from which the
            email is sent. Internal to the Google API.
        """
        if application_name is None:
            application_name = "Mail Sender"

        self.source_email = source_email
        self.application_name = application_name

        http_auth = self._get_credentials().authorize(Http())
        self._service = build("gmail", "v1", http=http_auth)

    def send_email(self, target_email, subject, message):
        """Sends an email to the specific email address.

        Parameters:
        target_email -- String. Destination email account to which your email
            will be sent. This should include the "@____.com".
            E.g. "john_smith@email.com"
        subject -- String. Text describing the subject of the email.
        message -- String. Message body of the email. Use newlines ("\n")
            for line breaks.
        """
        Logger.debug("Mail source:  " + self.source_email)
        Logger.debug("Mail target:  " + target_email)
        Logger.debug("Mail subject: " + subject)
        Logger.debug("Mail message: " + message.replace("\n", "[newline]"))

        mail = self._create_message(
                self.source_email, target_email,
                subject, message
        )
        response = self._service.users().messages() \
                .send(userId=self.source_email, body=mail).execute()

        Logger.debug("Mail sent.")

class GoogleDriveApi(_GoogleApi):
    """Wrapper for the Google Drive API (v3)."""

    _scope = "https://www.googleapis.com/auth/drive"

    def __init__(self, application_name=None):
        """Instantiates a GoogleDriveApi object and refreshes its credentials.

        Parameters:
        source_email -- String. Gmail account from which your emails
            will be sent. This should include the "@gmail.com".
            E.g. "gmail_source@email.com"
        application_name -- String. Application name from which the
            email is sent. Internal to the Google API.
        """
        if application_name is None:
            application_name = "Google Drive Accesser"

        self.application_name = application_name

        http_auth = self._get_credentials().authorize(Http())
        self._service = build("drive", "v3", http=http_auth)

    def get_file_list(self):
        """Retrieves the data of all files  and dirs in the Google Drive.

        Reference: https://developers.google.com/drive/v3/reference/files/list
        """
        file_list = []

        pageToken = ""
        while(pageToken is not None):
            file_obj = self._service.files()\
                    .list(pageToken=pageToken).execute()
            file_list.extend(file_obj.get("files"))
            pageToken = file_obj.get("nextPageToken")

        Logger.debug("File and directory details:")
        for file in file_list:
            Logger.debug("  " + json.dumps(file))

        return file_list

    def upload_file(self, file_path_local,
            file_name_gdrive, parent_dir_id=None):
        """Uploads a file to a Google Drive account.

        Parameters:
        file_path_local -- String. Absolute path to the file to be uploaded.
        file_name_gdrive -- String. Filename for the uploaded file in
            Google Drive.
        parent_dir_id -- String (optional). File ID for the parent directory
            of the uploaded file. See README.md for instructions.
        """
        body = {"name": file_name_gdrive}
        if parent_dir_id is not None:
            body["parents"] = [parent_dir_id]

        self._service.files().create(
                body=body,
                media_body=MediaFileUpload(file_path_local),
        ).execute()

        Logger.debug("File [" + file_path_local + "] uploaded to Google Drive.")

class GoogleCalendarApi(_GoogleApi):
    """Wrapper for the Google Calendar API."""

    _scope = "https://www.googleapis.com/auth/calendar"

    def __init__(self, application_name=None):
        """Instantiates a GoogleCalendarApi object and refreshes credentials.

        Parameters:
        application_name -- String. Application name for the application which
        uses Google Calendar.
        """
        if application_name is None:
            application_name = "Google Calendar API Wrapper"

        self.application_name = application_name

        http = self._get_credentials().authorize(Http())
        self._service = build("calendar", "v3", http=http)

    def list_calendars(self):
        """Returns a list of all calendars listed on the Google account.

        Reference: https://developers.google.com/google-apps/calendar/v3/reference/calendarList/list

        Returns:
        Dictionary with the following structure:
        [
            {
                "summary": "Name of the event in Google Calendar",
                "id": "Event UUID in Google Calendar"
            },
            ...
        ]
        """
        cal_list = []
        page_token = ""

        while(page_token is not None):
            response = self._service.calendarList()\
                    .list(pageToken=page_token).execute()

            for calendar in response.get("items"):
                simple_calendar = {}
                simple_calendar["summary"] = calendar["summary"]
                simple_calendar["id"] = calendar["id"]
                cal_list.append(simple_calendar)

            page_token = response.get("nextPageToken")

        return cal_list

    @staticmethod
    def _simplify_event(event):
        """Simplifies a complex event in-place, only keeping basic elements."""
        e = {}

        e["summary"] = event["summary"]
        e["start"] = event["start"]
        e["end"] = event["end"]

        try:
            e["description"] = event["description"]
        except KeyError:
            pass

        try:
            e["location"] = event["location"]
        except KeyError:
            pass

        event.clear()
        event.update(e)

    def list_events(self, calendar_id=None, timestamp_min=None,
            timestamp_max=None, time_zone=None):
        """Lists all events from the selected calendar.

        Reference: https://developers.google.com/google-apps/calendar/v3/reference/events/list

        Arguments:
        calendar_id -- String. If not provided, "primary" is used (the
                default calendar).
        timeMin -- String. RFC 3339 time.
            Tools to find the correctly formatted time:
            https://www.unixtimestamp.com/index.php
            https://www.infobyip.com/epochtimeconverter.php)
        timeZone -- String.
            List of timezones: http://www.timezoneconverter.com/cgi-bin/zonehelp.tzc

        Returns:
        Dictionary with the following structure:
        [
            {
                "summary": string (Name of the event in Google Calendar)
                "start": {
                    "date": date,
                    "dateTime": datetime,
                    "timeZone": string
                },
                "end": {
                    "date": date,
                    "dateTime": datetime,
                    "timeZone": string
                },
                "description": string (Optional - Event description
                        in Google Calendar),
                "location": string (Optional - Event location
                        in Google Calendar)
            },
            ...
        ]
        """
        if calendar_id is None:
            calendar_id = "primary"

        events_list = []

        page_token = ""
        while(page_token is not None):
            response = self._service.events() \
                    .list(calendarId=calendar_id,
                            timeMin=timestamp_min, timeMax=timestamp_max,
                            timeZone=time_zone,
                            showDeleted=False, orderBy="startTime",
                            singleEvents=True, pageToken=page_token) \
                    .execute()

            for event in response.get("items"):
                self._simplify_event(event)
                events_list.append(event)

            page_token = response.get("nextPageToken")

        return events_list
