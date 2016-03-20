from calendar import HTMLCalendar
from datetime import date
from itertools import groupby
from django.utils.html import conditional_escape as esc


# http://uggedal.com/journal/creating-a-flexible-monthly-calendar-in-django/
class MyCalendar(HTMLCalendar):
    color_today = "#0078D7"
    color_deadline = "#ffaddf"

    html = "<table onmouseover=\"bigImg({2})\" onmouseout=\"normalImg({2})\" border=\"0\" cellpadding=\"4\" cellspacing=\"0\">"
    html = html + "<tr><td bgcolor=\"{0}\">{1}</td>"
    html = html + "</tr></table>"

    def __init__(self, firstweekday, assignments):
        super(MyCalendar, self).__init__()
        self.assignments = assignments
        self.deadlines = []
        for a in assignments:
            self.deadlines.append(a.deadline.date())

    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
                body = self.html.format(self.color_today, day, 0)
                return self.day_cell(cssclass, body)
            if date(self.year, self.month, day) in self.deadlines:
                index = self.deadlines.index(date(self.year, self.month, day))
                body = self.html.format(self.color_deadline, day, self.assignments[index].id)
                return self.day_cell(cssclass, body)
            return self.day_cell(cssclass, day)
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month):
        self.year, self.month = year, month
        return super(MyCalendar, self).formatmonth(year, month)

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)
