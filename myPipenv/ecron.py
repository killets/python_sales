import webapp2
import time
import datetime
import string
import logging
from google.appengine.ext import ndb
from webapp2_extras.auth import InvalidAuthIdError
from webapp2_extras.auth import InvalidPasswordError

from dbconn import *
from functions import *

from google.appengine.api import urlfetch


class EmailAbsent(Handler):

    # a cron job that will automatically update the grade of every student in our database to the next year up on July 1st.
    @cron_method
    def get(self):
        database = conn_to_db()
        # self.response.write('class id, week, number of students<br>')
        db = database.cursor()
        # TODO SQL timezone is UTC, so +5 ahead of East Time
        # if change cron time to before 7pm, should change date here
        rows = db.execute(
            '''
            select s.student_id, student_first_name, student_last_name, class_id, primary_email, student.household_id
            from   (select student_id, class_id from enrollment 
            where date = subdate(current_date, 1)
            and attended_class_id is NULL
            and attended_date is NULL
            and withdraw = 0
            and reported_absence = 0 ) as s
            
            join student
            on s.student_id = student.student_id
            join household
            on student.household_id = household.household_id
            order by class_id
            '''
        )
        absent_students_info = db.fetchall()
        db.close()
        class_name = class_name_by_id()
        emails = []
        info = "student_id  -  firstname  -  lastname  -  class_id  -  email - class_name\r\n"
        for el in absent_students_info:
            info += ", ".join(v.encode('utf-8') for v in el[0:4])
            if el[4]:
                info += ", " + el[4]
                emails.append(el[4])
            else:
                db = database.cursor()
                db.execute(
                    'SELECT DISTINCT email FROM email WHERE household_id = %s', [el[5]]
                )
                email = db.fetchone()
                if email:
                    info += ", " + email[0]
                    emails.append(email[0])
                else:
                    info += ", None"
            info += ", " + class_name[int(el[3])]
            info += "\r\n"
        database.close()
        '''
        # use below to send student info list to SAC

        # select s.student_id, student_first_name, student_last_name, class_id, primary_email

        absent_students_info = db.fetchall()
        db.close()
        database.close()

        emails = []
        info = "student_id  -  firstname  -  lastname  -  class_id  -  email\r\n"
        for el in absent_students_info:
            info += "    ".join(str(v) for v in el)
            info += "\r\n"
            emails.append(el[4])

        class_name = class_name_by_id()[class_id]
        to = ['management@sharronartcenter.com', 'register@sharronartcenter.com', 'ioteye.dev@gmail.com'] #,


        # to = map(lambda x: x[0], emails)
        '''
        to = emails
        # to.append('ioteye.dev@gmail.com')
        subject = "Missed Class Alert [Sharron Art]"
        body = u"Dear Parent,\r\n\r\nWe missed your child at their registered class today, and their absence was not reported.\r\n\r\nThis is an automatically generated email. If you need help, please contact register@sharronartcenter.com\r\n\r\nYou can review our makeup polices by <a href = 'https://drive.google.com/file/d/1ul6H0LUwr_Ubvy7hQSqD2H81ad8_E5P3/view' >clicking the link here.</a>\r\n\r\n"
        logging.info('at emailAbsent try_send')
        logging.info(to)
        if to:
            try_send(to, subject, body)
        if rows > 0:
            to = [
                'management@sharronartcenter.com',
                'register@sharronartcenter.com',
                'Ireneg@sharronartcenter.com',
                'Natashaw@sharronartcenter.com',
                'Angelal@sharronartcenter.com',
                'ioteye.dev@gmail.com',
            ]
            # to = ['ioteye.dev@gmail.com']
            body = u"Today's list of missed class alert ({rows} total):\r\n\r\n {info}".format(
                rows=rows, info=info
            )
            try_send(to, "Missed Class Alert Report [Sharron Art]", body)
            logging.info("at emial absent report")
            logging.info(info)
