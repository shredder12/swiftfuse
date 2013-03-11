import errno  
import llfuse  
import stat  
import time
import swiftclient
import logging
from os import environ
import sys

log = logging.getLogger()
  
class swiftfuse(llfuse.Operations):
    
    swift_conn = None

    def __init__(self):  
        super(swiftfuse, self).__init__()
        self.swift_conn = swiftclient.client.Connection(
            authurl=environ['OS_AUTH_URL'],
            user=environ['OS_USERNAME'], 
            key=environ['OS_PASSWORD'], 
            tenant_name=environ['OS_TENANT_NAME'],
            auth_version=2
            )
  
    def getattr(self, inode):  
        st = llfuse.EntryAttributes()
        st.st_ino = inode
        st.generation = 0
        st.entry_timeout = 300
        st.attr_timeout = 300
        st.st_mode = stat.S_IFDIR | 0755  
        st.st_nlink = 2  
        st.st_atime = int(time.time())  
        st.st_mtime = st.st_atime  
        st.st_ctime = st.st_atime
        st.st_uid = 1000
        st.st_gid = 1000
        st.st_rdev = 0
        st.st_size = 0
        st.st_blksize = 512
        st.st_blocks = 1    
        return st

    def readdir(self, path, offset=0):
        if path == ".":
            bucket = self.swift_conn.get_account()[1][offset]
            yield (bucket['name'], self.getattr(bucket['name']), int(offset + 1))

def init_logging():
    formatter = logging.Formatter('%(message)s') 
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    log.setLevel(logging.INFO)    
    log.addHandler(handler)    

if __name__ == '__main__':  
    init_logging()
    sf = swiftfuse()
    mountpoint = sys.argv[1]

    llfuse.init(sf, mountpoint, [])
    llfuse.main(single=True)

    llfuse.close()