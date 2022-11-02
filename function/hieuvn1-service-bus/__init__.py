import azure.functions as func
import logging
import os
from datetime import datetime
import psycopg2
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def main(msg: func.ServiceBusMessage):

    notificationId = int(msg.get_body().decode('utf-8'))
    logging.info('Python ServiceBus queue trigger processed message: %s', notificationId)
 
    # Done: Get connection to database
    connection = psycopg2.connect(host="hieuvn1-postgre-server.postgres.database.azure.com",user="hieuvn1@hieuvn1-postgre-server",dbname="techconfdb", password="L1ndsaylohan")
    cursor = connection.cursor()
    try:
        # TODO: Get notification message and subject from database using the notification_id
        notification_message_subject = cursor.execute("SELECT message, subject FROM notification where id = {};".format(notificationId))

        # TODO: Get attendees email and name
        cursor.execute("SELECT first_name, last_name, email FROM attendee;")
        # TODO: Loop through each attendee and send an email with a personalized subject
        attendees = cursor.fetchall()
        for att in attendees:
            Mail('{}, {}, {}'.format('ngochieuvnu@gmail.com', {att[2]}, {notification_message_subject}))

        # TODO: Update the notification table by setting the completed date and updating the status with the total number of attendees notified
        notificationDateTime = datetime.utcnow()
        notificationStatus = 'Notified to {} attendees'.format(len(attendees))
        cursor.execute("UPDATE notification SET status = '{}', completed_date = '{}' WHERE id = {};".format(notificationStatus, notificationDateTime, notificationId))        

        connection.commit()

    except (Exception, psycopg2.DatabaseError) as error:
        logging.error(error)
        connection.rollback()
    finally:
        cursor.close()
        connection.close()
        # Done: Close connection