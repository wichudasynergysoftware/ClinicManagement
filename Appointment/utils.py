from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import *

class Calendar(HTMLCalendar): # ใช้ html calendar ที่มีอยู่ในโมดูล calendar python
	def __init__(self, year=None, month=None): # กำหนด year, month จากพารามิเตอร์ี่รับเข้ามา
		self.year = year
		self.month = month
		super(Calendar, self).__init__() # เรียก constructor ของ super class

	def formatday(self, day, events): # day คือ จำนวนเต็มที่แทนวันของเดือน, event คือ ข้อมูลวันนัดหมาย สำหรับเดือนปัจจุบัน
		events_per_day = events.filter(date__day=day) # ตรงนี้ คือ กรอกข้อมูลนัดหมายว่าเป็นวันไหน
		d = ''
		for event in events_per_day:
			d += f'<li> {event.get_html_url} </li>' # มาจัดให้เป็น html unordered list และส่งคืน html string

		if day != 0:
			return f"<td><span class='date'>{day}</span><ul class='day-ul'> {d} </ul></td>"
		return '<td></td>' # ตรงนี้จ้า ที่ทำให้เห็น list นัดหมายในแต่ละวัน

	def formatweek(self, theweek, events): # รับพารามิเตอร์ the week -- รายการของตัวแปรทูเพิลที่มีวันของเดือน และชื่อวันในสัปดาห์
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events) # เมื่อวนลูปผ่านทุกวันในสัปดาห์ จะเรียกใช้ formatday() สำหรับแต่ละวัน และรวม html string และ return ออกไป
		return f'<tr> {week} </tr>' #

	def formatmonth(self, withyear=True): # สร้างแบบฟอร์มปฏิทินของเดือนและปีที่กำหนดโดยผู้ใช้
		events = EventAppointment.objects.filter(date__year=self.year, date__month=self.month) # filter ดึงข้อมูล EventAppointment จากฐานข้อมูลโดยกรองด้วยปีและเดือนของปฏิทินที่กำลังสร้าง

		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n' # HTML table ที่มีการกำหนด border, cellpadding, cellspacing และ class เพื่อให้เป็นตารางแบบปฏิทิน
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
  		# สร้างตารางแบบปฏิทิน ซึ่งจะมีข้อมูลของวันที่ และข้อมูลของเหตุการณ์ที่เกิดขึ้นในแต่ละวัน โดยข้อมูลเหตุการณ์ที่กำลังเก็บไว้ในตัวแปร events
		for week in self.monthdays2calendar(self.year, self.month): # วน loop ผ่านค่า week ที่ได้จาก monthdays2calendar() ซึ่งจะแบ่งแยกวันที่ในแต่ละสัปดาห์
			cal += f'{self.formatweek(week, events)}\n'
			# ใช้ method formatweek() เพื่อจัดการสร้าง HTML สำหรับแสดงวันในแต่ละสัปดาห์ โดยใช้ข้อมูล events ที่กรองไว้แล้ว
		return cal
		# ส่งค่า HTML string ที่สร้างขึ้นมาในตัวแปร cal ออกมา
