import os

def node_temps_callback(s):
  os.system('pdsh -a "/opt/vc/bin/vcgencmd measure_temp"')

proto = {
  'init_menu_key' : 'main_menu',
  'main_menu' : {
    'head' : 'CM Main Menu',
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
