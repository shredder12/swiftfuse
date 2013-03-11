import errno  
import fuse  
import stat  
import time
import swiftclient
from os import environ
  
fuse.fuse_python_api = (0, 2)  
  
class swiftfuse(fuse.Fuse):
    
    swift_conn = None

    def __init__(self, *args, **kw):  
        fuse.Fuse.__init__(self, *args, **kw)
        self.swift_conn = swiftclient.client.Connection(
            authurl=environ['OS_AUTH_URL'],
            user=environ['OS_USERNAME'], 
            key=environ['OS_PASSWORD'], 
            tenant_name=environ['OS_TENANT_NAME'],
            auth_version=2
            )
  
    def getattr(self, path):  
        st = fuse.Stat()  
        st.st_mode = stat.S_IFDIR | 0755  
        st.st_nlink = 2  
        st.st_atime = int(time.time())  
        st.st_mtime = st.st_atime  
        st.st_ctime = st.st_atime    
        return st

    def readdir(self, path, offset):
        for bucket in self.swift_conn.get_account()[1]:
            yield fuse.Direntry(bucket['name'])

  
if __name__ == '__main__':  
    fs = swiftfuse()  
    fs.parse(errex=1)  
    fs.main()  