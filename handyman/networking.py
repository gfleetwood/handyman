from subprocess import run
from re import search
from pandas import DataFrame

def read_ips_on_network():

  ip_call = run(["ip", "addr", "show"], capture_output = True)
  tp_output = ip_call.stdout.decode('utf-8').replace("\n", "")
  ip_wlp = search(r'wlp3s0: (.*?) inet [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/[0-9]{1,2}', tp_output).group()
  ip_wlp_inet = search(r'inet [0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/[0-9]{1,2}', ip_wlp).group()
  ip_wlp_inet_addr = search(r'[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/[0-9]{1,2}', ip_wlp_inet).group()
  ip_wo_bits = ip_wlp_inet_addr.split(".")[:-1] + ["1"]
  ip_w_bits = ".".join(ip_wo_bits) + "/{}".format(ip_wlp_inet_addr.split("/")[-1])

  nmap_scan = run(["nmap", "-sP", ip_w_bits], capture_output = True)

  nmap_scan_ips = [
    x.replace("Nmap scan report for ", "") 
    for i, x in enumerate(nmap_scan.stdout.decode('utf-8').split("\n")[1:-2])
    if i%2==0
  ]

  nmap_scan_ips_temp = [x.replace(")", "").split("(") for x in nmap_scan_ips]

  nmap_scan_ips_named = [
    ["Unknown", x[0]] 
    if len(x) == 1
    else x
    for x in nmap_scan_ips_temp
  ]

  nmap_scan_df = DataFrame(nmap_scan_ips_named, columns = ["device_name", "ip_address"])
  
  return(nmap_scan_df)
