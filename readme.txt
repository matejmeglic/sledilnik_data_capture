## Sledilnik Data Capture

# Functionality:
- define each user into a group with appropriate permissions
- Create hospitals and set them to active if they have COVID patients
- Create Email lists for a report (use the same slug as Hospital.short_name)
- In Email list, define Parital reporting time (currently not working but still required)
- On FE, push some data inside
- After all active hospitals report for a selected day, email is generated in /management/commands and sent through SendGrid
- One can check what was sent by going to the database and re-generate HTML template in a new page

- Currently, HOS report is working as a MVP
- Emails are sent on form_submit

Todo:
- Active hospitals filter doesn't work on BE
- There is a problem with login form, if you hit Enter key for U and P submit instead of clicking the button
- password reset over email doesn't work (SendGrid not connected)
- connect SendGrid to domain (currently in weak test mode)
- extend the reports to EPI and Municipalities
- migrate to better-suited environment
- set up cron job for sending out mail (run script each minute)
- re-do css on base_generic.html (currently hardcoded to another server as Heroku doesn't support static pages)
- define, if Partial reporting (send email at a certain point in time even if not all hospitals had reported yet) is needed
- define scheduling (probably cron script should look at db to determine and not re-send the report, what to do with full reports if partial report was sent already etc.)
- will we optimize report function or set up multiple functions one-per-report
- optimize page for smaller screens and mobile

https://sledilnik-data-capture.herokuapp.com/
