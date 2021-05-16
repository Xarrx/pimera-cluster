#!/usr/bin/python3.7
from src.mparse.mparse import traverse_menu
def node_temps_callback(s):
  #import os
  #os.system('pdsh -a "/opt/vc/bin/vcgencmd measure_temp" | dshbak -c')
  import subprocess
  #cmd = 'pdsh -a /opt/vc/bin/vcgencmd measure_temp | dshbak -c'
  cmd = 'pdsh -a cat /sys/class/thermal/thermal_zone0/temp | sort'
  process = subprocess.Popen(cmd, shell=True, executable='/bin/bash', stdout=subprocess.PIPE)
  out, err = process.communicate()
  print(out.decode('utf-8'))

menu = {
  'init_menu_key' : 'main_menu',
  'main_menu' : {
    'head' : 'Cluster Manager Menu',
    'options' : [
      {
        'desc' : 'Measure Node Temps',
        'flow' : 1,
        'menu_key' : 'node_temps'
      },
    ]
  },
  'node_temps' : {
    'head' : 'node_temps_term',
    'options' : [],
    'callback' : node_temps_callback
  }
}

traverse_menu(menu)

exit()
