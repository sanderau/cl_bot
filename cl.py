from craigslist import CraigslistForSale
import sys #import command line arguments
import smtplib #import email libraries
import datetime
import time
import os


def sendUpdate(name, url, datePosted, email, pw):
	smtpObj = smtplib.SMTP('smtp.gmail.com', 587) #connect to the gmail server
	type(smtpObj)

	smtpObj.ehlo() #say hello to server and start communicating
	smtpObj.starttls() #start encyption boiiiiii
	smtpObj.login(email, pw)

	message = "Subject: %s\n\n%s\n%s" % (name, url, datePosted)

	smtpObj.sendmail(email, email, message) #send the message 
	print "Successfully sent!"
	smtpObj.quit() #ends connection
	return 0

def newPost(my_names, name):
	fp = open(my_names, 'r')
	line = fp.readline()
	while line:
		line = line.rstrip()
		if (line == name ):
			print "Already sent %s!\nWill not send again" % (line)
			fp.close()
			return False #if name already found return false so I dont send again
		line = fp.readline()
		
	fp.close()
	return True #if not in list then send true so I will send
	
#*******************************************************************#
######################BEGIN MAIN#####################################
#*******************************************************************#
if (len(sys.argv) < 3):
	print str(sys.argv[0]) + '[email] [password]'
	sys.exit()

my_names = 'names.txt'
fp = open(my_names, 'a')

while(True):
	cl = CraigslistForSale(site='sacramento', category='cto', filters={'max_price': 4000, 'min_price': 3000, 'max_miles': 200000, 'auto_title_status': u'clean', 'auto_transmission': u'manual', 'search_distance': 1000})
	print '**************************************** SEARCH *********************************************'

	results = cl.get_results(sort_by='newest', geotagged=True, limit=20)
	my_dates = []

	for result in results:
		nameLower = result['name'].lower() #name of the title
		out = 'outback'
		forester = 'forester' #key words to look for in title
		subaru = 'subaru'
		if out in nameLower or forester in nameLower or subaru in nameLower:
			if (newPost(my_names, nameLower)): #check to see if I have already sent it
				print "Sending %s to email...." % (result['name'])
				sendUpdate(result['name'], result['url'], result['datetime'], sys.argv[1], sys.argv[2])
				fp.write(nameLower)
				fp.write('\n')
	
	
	print '**************************************** SLEEP *********************************************'
	print 'Nothing else matches what you\'re looking for!\nSleeping for ten minutes!\nWill check again when I wake up'

	for i in range(0, 600) :
		sys.stdout.write('\rTime remaining in nap: %is' % (600-i))
		time.sleep(1)
		sys.stdout.flush()
	
	sys.stdout.write('\r \b')
