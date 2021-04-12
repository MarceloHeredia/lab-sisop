import time
import os
from datetime import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import cpustat
import platform
from subprocess import Popen, PIPE


HOST_NAME = '192.168.1.10' # !!!REMEMBER TO CHANGE THIS!!!
PORT_NUMBER = 8000

encoding = "utf-8"
cpuloads = cpustat.GetCpuLoad()


class MyHandler(BaseHTTPRequestHandler):
    def do_HEAD(s):
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
    def do_GET(s):
        """Respond to a GET request."""
        cpuinfo = get_cpu_info()
        meminfo = memstat()
        s.send_response(200)
        s.send_header("Content-type", "text/html")
        s.end_headers()
        s.wfile.write(bytes("<html><head><title>T1 - Lab Sisop. Marcelo Heredia.</title></head>", encoding))
        s.wfile.write(bytes("<body><p>Hello!</p>", encoding))
        s.wfile.write(bytes("<p>Date and Time of access: %s</p>" % datetime.now().strftime('%c'), encoding))
        s.wfile.write(bytes("<p>System Uptime: %s seconds</p>" % get_uptime(), encoding))
        s.wfile.write(bytes("<p>Processor Model: %s </p>" % cpuinfo[0], encoding))
        s.wfile.write(bytes("<p>CPU Clock MHZ:  %s </p>" % cpuinfo[1], encoding))
        s.wfile.write(bytes("<p>Current Processor Workload:  %s </p>" % cpuloads.getcpuload(), encoding))
        s.wfile.write(bytes("<p>Total RAM Memory: %s MB</p>" % meminfo[0], encoding))
        s.wfile.write(bytes("<p>Used Memory:  %s MB</p>" % meminfo[1], encoding))
        s.wfile.write(bytes("<p>System platform and version:  %s </p>" % platform.platform(), encoding))
        s.wfile.write(bytes("<p>Proceseses open:  </p>", encoding))
        processes = get_processes()
        for i in range(len(processes)):
            s.wfile.write(bytes("<p> %s | %s </p>" % (processes[i][0], processes[i][1]), encoding))

        s.wfile.write(bytes("<p>You accessed path: %s</p>" % s.path, encoding))
        s.wfile.write(bytes("</body></html>", encoding))


def get_uptime():
    with open('/proc/uptime', 'r') as f:
        up_seconds = float(f.readline().split()[0])
    return up_seconds

def get_cpu_info():
    info = []
    with open('/proc/cpuinfo', 'r') as f:    
        for line in f:
            if line.strip():
                if line.rstrip('\n').startswith('model name'):
                    model_name = line.rstrip('\n').split(':')[1]
                    model=model_name
                    model=model.strip()
                    break
        info.append(model)
        for line in f:
            if line.strip():
                if line.rstrip('\n').startswith('cpu MHz'):
                    clock = line.rstrip('\n').split(':')[1]
                    clock=clock.strip()
                    break
        info.append(clock)
    return info

def memstat():
    tot_m, used_m = map(int, os.popen('free -m').readlines()[-2].split()[1:3])
    return tot_m, used_m


def get_processes():
    procs = []
    
    for proc in os.popen('ps axo pid,comm'):
        line = proc.strip().split(' ')
        pid, cmm = line[0], line[-1]
        procs.append([pid, cmm])
    return procs


if __name__ == '__main__':
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    print (time.asctime(), "Server Starts - %s:%s" % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), "Server Stops - %s:%s" % (HOST_NAME, PORT_NUMBER))

