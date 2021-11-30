POST_TITLE_LEN = 100

USR_MIN_LEN = 2
USR_MAX_LEN = 20
EMAIL_MAX_LEN = 120
PASSWD_MIN_LEN = 8
PASSWD_MAX_LEN = 40
PASSWD_HASH_LEN = 60
FILENAME_LEN = 20

# Adults average words per minute (reading)
avg_wpm = 200

def est_read_time(content):
    return int(len(content.split())/avg_wpm)