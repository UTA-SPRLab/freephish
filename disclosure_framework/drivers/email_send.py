def mail_send_module(url,domain,domain_email): #domain = domain to report to # domain_email = domain email address to report to
 

	import smtplib, ssl
	import imghdr
	from email.message import EmailMessage

	Sender_Email = "<Your-email-here>"
	Reciever_Email = domain_email
	Password = "<Password>"

	newMessage = EmailMessage()                         
	newMessage['Subject'] = "Phishing report for URL hosted using your Domain"
	newMessage['From'] = Sender_Email                   
	newMessage['To'] = Reciever_Email                   
	newMessage.set_content(f'Hello, we found a phishing website: {url} hosted on your domain. (Reported by FreePhish)') 

	context = ssl.create_default_context()

	with smtplib.SMTP('<your smtp server>', 587) as smtp:
	    smtp.starttls(context=context)
	    smtp.login(Sender_Email, Password)              
	    smtp.send_message(newMessage)    
	print("Email sent successfully")


