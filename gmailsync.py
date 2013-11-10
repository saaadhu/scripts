# Script to download raw email messages using IMAP from gmail and dump it
# to disk. Parameters are username, password and a directory to dump.
# Is smart enough to query before downloading all message ids.

# Pass in username, password, backup_dir as environment variables

import imaplib
import os
import time

# Connect
m = imaplib.IMAP4_SSL('imap.gmail.com', 993)

# Login
type, data = m.login(os.environ['username'], os.environ['password'])
if type != 'OK':
    raise 'Authentication failed'

# Select INBOX
type, data = m.select()
if type != 'OK':
    raise 'INBOX selection failed'

# Get the most recent message's UID
last_message = data[0]

type, data = m.fetch(last_message, 'UID')
if type != 'OK':
    raise 'Could not get UID of last message'
last_uid = data[0].split()[2][:-1].decode('UTF8')

# Match against our backup
last_fetched_uid = ''

f = open(os.environ['backup_dir'] + '/last_fetched_uid', 'r+')
lines = f.readlines()
if len(lines) >= 1:
    last_fetched_uid = lines[0].strip()

if last_fetched_uid != last_uid:
    type, data = m.uid('search', None, 'ALL')
    if type != 'OK':
        raise 'Search failed'
    
    # Save missing UIDs to our backup folder
    for uid in data[0].split():
        uid = uid.decode('UTF8')
        msg_file = os.environ['backup_dir'] + '/' + str(uid)
        if os.path.exists(msg_file) == False:
            print ('Downloading ' + str(uid))
            type, data = m.uid('fetch', uid, 'RFC822')    

            if type != 'OK':
                raise 'Fetch failed for uid: ' + uid

            id, content = data[0]
            msg_f = open(msg_file, 'w')
            msg_f.write(str(content))
            msg_f.close()

            # Take a breather for a second
            time.sleep(1)

    f.write(last_uid)

f.close()

m.close()
m.logout()

