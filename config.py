# config.py
'''
    To use the auto description option enable the autodesc flag by setting its value to True.
    Some additional librarys are required see requirements.txt
'''

host_name = "localhost"
host_port = 5000
filepaths = dict(
    dbfile = "gallery.db",
    SQLFILE = "gallery.sql",
    demo = './static/demo/',
    gallery = './static/gallery/' 
)
options = dict(
    clusters = 3,
    enable_autodesc = False,
    job_time = 3,
    job_limit = 3,
    max_instances = 1
)
