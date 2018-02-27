from flask import Flask
from flask import render_template, jsonify
import psutil

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/pcInfo")
def PC_information():
    # logical cpu count numbers
    cpu_sum = psutil.cpu_count()
    # the percent of all cpu used, interval time of each get info is 0.5 second
    cpu_used = str(psutil.cpu_percent(interval=0.5)) + "%"

    # get the memory information of the PC
    # get total size of the memory
    mem_obj = psutil.virtual_memory()
    memory_total = mem_obj.total / 1024 / 1024
    memory_total = str(round(memory_total, 2)) + "MB"

    # get the used size and percent of the memory
    memory_used = mem_obj.used / 1024 / 1024
    memory_used = str(round(memory_used, 2)) + "MB"

    memory_used_per = str(mem_obj.percent) + "%"

    # get the total disk information of the PC
    disk_obj = psutil.disk_usage("/")
    disk_total = disk_obj.total / 1024 / 1024 / 1024
    disk_total = str(int(disk_total)) + "GB"

    disk_used = disk_obj.used / 1024 / 1024 / 1024
    disk_used = str(int(disk_used)) + "GB"

    disk_used_per = str(disk_obj.percent) + "%"

    # get the total network IO information if the PC
    net_io = psutil.net_io_counters()
    net_sent = net_io.bytes_sent / 1024 / 1024
    net_sent = str(round(net_sent, 2)) + "MB"

    net_recv = net_io.bytes_recv / 1024 / 1024
    net_recv = str(round(net_recv, 2)) + "MB"

    data_dict = dict(cpuSum=cpu_sum, cpuUsedPer=cpu_used,
                     memUsedPer=memory_used_per, memUsedNum=memory_used,memTotal=memory_total,
                     diskUsedPer=disk_used_per, diskUsedNum=disk_used, diskTotal=disk_total,
                     netWorkSent=net_sent, netWorkRcve=net_recv)
    return jsonify(errmsg="OK", data=data_dict)



if __name__ == '__main__':
    app.run()
