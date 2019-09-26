import requests
import json 
import calendar
from bs4 import BeautifulSoup
import re
monthsYear = ["January", "February","March","April","May","June","July", "August","September", "October","November","December"]
monthtomm = len(monthsYear)
mm = 0
organiserlogo = "http://globalarbitrationreview.com/images/gar-live-logo.png"
r= requests.get('https://globalarbitrationreview.com/events')

soup = BeautifulSoup(r.text, 'lxml')

#Find all events on Page
hyperlink_array = []
events = soup.find_all('div', attrs={'class':'event-list'})
for hyperlinks in events:
	event_hyperlinks = hyperlinks.find('a', attrs={'href': re.compile("^http://")})
	#appending to hyperlink array
	hyperlink_array.append(event_hyperlinks.get('href'))
	#print(event_hyperlinks.get('href'))
eventArray_length = len(hyperlink_array)
#change i to 0 before upload.
i=0
while i < eventArray_length:
	if eventArray_length >= i:
		hyperLink_val = hyperlink_array[i]
		#print(hyperLink_val)
		#Set request for the event page
		p = requests.get(hyperLink_val)
		# If you want to test it, comment the above line and uncomment the one below.
		# p = requests.get('http://gar.live/vienna2019')
		event_soupy = BeautifulSoup(p.text, 'lxml')

		#Find Date, Event Title & Reg URL This works!
		event_title = event_soupy.find('div', attrs={'class':'description'}).h2.text
		event_date_unstripped = event_soupy.find('div', attrs={'class':'signup_button'}).p.text 
		
		#	Converted Day, Date, Month, Year to a List.This works!
		#	Deleted the first item in that list
		# 	Used monthYear array to simplify the code below.
		#	Compares the MONTH with the Month in the array
		# 	And replaces it with the iterated variable, if condition is true.
		event_date_unstripped = event_date_unstripped.split()
		del event_date_unstripped[0]

		while mm <= monthtomm:
			if monthtomm > mm:
				if event_date_unstripped[1] == monthsYear[mm]:
					event_date_unstripped[1] = mm
				else:
					mm += 1
			else:
				break
		# Joining the list together to form one entire date.This works!
		eventDate = str(event_date_unstripped[0]) + '/'+ str(event_date_unstripped[1]) + '/' + str(event_date_unstripped[2])
		#Event Registration URL This works!

		reg_url = hyperLink_val[i]

		#print(eventDate)
		#print(reg_url)
		# Getting the programme itinerary 
		itinerary = event_soupy.find('div', attrs={'id':'programme'})
		if itinerary == None:
			itinerary = 'Programme to be announced shortly.'
		#print(itinerary)
		#Getting the email ID: This works!
		#init_info = event_soupy.find_all('p', attrs={'id':'overview-contact'})
		mailTo = event_soupy.find('a', attrs={'href': re.compile("^mailto:")})
		email_id = mailTo.get('href')
		
		#print(email_id)
		#Getting the Phone No. This Works!
		tele_text = event_soupy.find('p', attrs={'id':'overview-contact'}).text
		telephone_no = re.sub("[^0-9]", "", tele_text)
		#print(telephone_no)

		#Getting the venue Address This Works!
		venueAddress = event_soupy.find('address').text
		venueAddress = venueAddress.strip()

		#Set the event data to a Json Dict. 
		eventData = {
					"Event Title": event_title,
					"Organiser Logo": organiserlogo,
					"Event Date": eventDate,
					"Event prog": itinerary,
					"Event_RegURL": reg_url, 
					"Contact Email": email_id, 
					"Contact Tele":telephone_no, 
					"LogisticalInfo":venueAddress}

		
		#Must call Python Wordpress Auth function here
		# Log into Wordpress, associate the JSON Dict to 
		# Python Array and publish post.



		#Export to Json File
		with open('event_info','w') as fp:
			json.dump(eventData, fp)
		#Must Call PHP function here. How do I do that?	

		print(eventData)
		print (i)
		i += 1
	else:
		break
