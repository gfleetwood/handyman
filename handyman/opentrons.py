def take_video(exp, file_name):

  # take_video <hh> <mm> <ss> <output_file_name>
  sys_call = "ffmpeg -y -video_size 640x480 -i /dev/video0 -t 00:00:05 /var/lib/jupyter/notebooks/vid.mp4"
  #sys_call = "!/bin/sh ffmpeg \
  #-y -video_size 640x480 \
  #-i /dev/video0 -t 00:00:05 /var/lib/jupyter/notebooks/vid$1.mp4"
  os.system(sys_call)

  return(True)

def take_pic():
    
  robot.set_lights(rails = 1)
    
  file_name = "/var/lib/jupyter/notebooks/data/file_" + str(dt.now().isoformat()) + ".jpg"
  sys_call = "ffmpeg -y -f video4linux2 -s 640x480 -i /dev/video0 -ss 0:0:1 -frames 1 {}".format(file_name)
  _ = os.system(sys_call)
    
  robot.set_lights(rails = 0)
  
  return(True)

def export_pic():
  
  time_interval = 10800*2/3 # run every 2 hours (value in seconds)
  threading.Timer(time_interval, export_pic).start()

  image_paths = glob("/var/lib/jupyter/notebooks/data/*.jpg")
  url = ''
    
  for img_path in image_paths:
    files = {'media': open(img_path, 'rb')}
    requests.post(url, files = files)  
    time.sleep(5)
