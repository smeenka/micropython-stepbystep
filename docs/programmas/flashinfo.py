import os

"""
f_bsize – file system block size

f_frsize – fragment size

f_blocks – size of fs in f_frsize units

f_bfree – number of free blocks

f_bavail – number of free blocks for unprivileged users

f_files – number of inodes

f_ffree – number of free inodes

f_favail – number of free inodes for unprivileged users

f_flag – mount flags

f_namemax – maximum filename length
"""
print (os.statvfs("/"))

f_bsize, f_frsize, f_blocks, f_bfree, f_bavail, f_files, f_ffree, f_favail, f_flag, _ = os.statvfs("/")

print ("block size: %s" % f_bsize)

print ("fragment size:%s" % f_bsize)

disk_size = f_blocks * f_frsize / 1000

print ("Disk size %.1f Kbyte" % disk_size)

free_size = f_bfree * f_frsize / 1000

print ("Free disk size %.1f Kbyte" % free_size)



