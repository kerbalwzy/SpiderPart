import psutil

# cpu_logical_numbers = psutil.cpu_count()
# cpu_used_percent = str(psutil.cpu_percent(interval=0.5))+"%"
#
# mem_obj = psutil.virtual_memory()
# memory_size = mem_obj.total/1024/1024
# memory_size = str(round(memory_size,2)) + "MB"
#
# memory_used_per = mem_obj.percent
# memory_used = mem_obj.used/1024/1024
# memory_used = str(round(memory_used,2)) + "MB"
#
#
# disk_obj = psutil.disk_usage("/")
# disk_total = disk_obj.total/1024/1024/1024
# disk_total = str(int(disk_total)) + "GB"
# disk_used = disk_obj.used/1024/1024/1024
# disk_used = str(int(disk_used)) + "GB"
# disk_used_per = str(disk_obj.percent)



net_io = psutil.net_io_counters()
net_sent = net_io.bytes_sent/1024/1024
net_sent = str(round(net_sent,2)) + "MB"

net_recv = net_io.bytes_recv/1024/1024
net_recv = str(round(net_recv,2)) + "MB"


print(net_io)
print(net_sent)
print(net_recv)