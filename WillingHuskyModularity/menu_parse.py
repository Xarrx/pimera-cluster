"""
Prototype for simple menus in python.

  - Each menu is a dict containing:
    -> head 
      This is what will be printed at the top of the menu, should be a short
      description of what is being chosen in this menu.
    -> options
      This is a list of all of the possible options for this menu. When this
      is empty, the state is considered terminal and the callback will 
      be executed if it exists.
    -> (optional) callback
      Function to be executed when this menu is chosen. When this is
      called, it is passed a dict containing all of the previously selected
      options.
  - Each option is a dict containing:
    -> desc
      This is what will be printed next to each option, should be a short
      description of what each option is.
    -> flow
      ID number for tracking which options have been picked. Number to be
      entered to select the option.
    -> (optional) menu_key
      Key of the next menu for this option
    -> (optional) store
      dictionary of values to be saved to flowStorage.
  Notes:
    - Need some way to control and keep track of what is added to the protoStorage
    so it can be reverted if a back/quit option is received.
    - Solution: Store each variable as a stack so that the value can be popped 
    if the back option is received. Make the tracking element a stack and have each of 
    its elements contain a list of each variable which was changed during that step.
      -> push: .insert(0, <value>)
      -> pop: .pop(0)
      -> peek: <stack>[0]
"""

def construct_row(opt):
  # construct the menu row string
  return '{0}# {1}'.format(opt['flow'], opt['desc'])

def construct_menu_string(menu):
  # construct menu from dictionary
  ret = ''.join((menu['head'], '\n'))

  # loop over all of the options in the menu dict
  for opt in menu['options']:
    ret = ''.join((ret, construct_row(opt), '\n'))
  
  # add a back option to the menu
  ret = ''.join((ret, construct_row({
    'flow' : 'q',
    'desc' : 'Quit/Previous Menu'
  })))

  return ret

def build_acceptable_input(options):
  # builds a list of acceptable 
  ret = ['q'] # the option 'q' is the default back options that is available for all menus
  for opt in options:
    ret.append(str(opt['flow']))
  return ret

def build_option_flow_map(options):
  # builds a dictionary which maps options to menu_keys
  ret = {}
  for opt in options:
    ret[str(opt['flow'])] = opt['menu_key']
  return ret

def build_meta_data(options):
  # combines what build_acceptable_input and build_option_flow_map do into a single loop
  ret = {
    'acceptable_inputs' : ['q'],
    'opt_flow_map' : {'q' : ''}
  }
  for opt in options:
    ret['acceptable_inputs'].append(str(opt['flow']))
    if 'menu_key' in opt:
      ret['opt_flow_map'][str(opt['flow'])] = opt['menu_key']

  return ret
  
def get_option(options, flow):
  ret = False
  for opt in options:
    #print('iteration: {}'.format(opt))
    #print('comp: {} == {} ? {}'.format(opt['flow'], flow, (int(opt['flow']) == int(flow))))
    if int(opt['flow']) == int(flow):
      #print('option found')
      ret = opt
      break
  return ret

def traverse_menu(mdict):
  # variables to keep track of where we are in the menu
  #flowId = -1 # current flow position
  flow_storage = {
    'tracking' : [],
    'data' : {}
  }  # variables stored for use when the terminal state is reached
  flow_stack = ['main_menu'] # stack containing which menus have been visited

  while True:
    # handle terminal state here
    if len(mdict[flow_stack[0]]['options']) == 0:
      # state is terminal
      if 'callback' in mdict[flow_stack[0]]:
        mdict[flow_stack[0]]['callback'](flow_storage)

      break

    else:
      # state is not terminal
      # build metadata
      metadata = build_meta_data(mdict[flow_stack[0]]['options'])
      print(construct_menu_string(mdict[flow_stack[0]]))
      i = input('> ')
      print('\n')

      # validate input
      if i in metadata['acceptable_inputs']:
        if i == 'q': 
          if flow_stack[0] == 'main_menu':
            # break loop if quit on main menu
            break
          else:
            # pop the last menu key off of the stack
            flow_stack.pop(0)

            # revert changes made to flow_storage using the top of the flow_stack
            # get the changes from storage tracking
            to_revert = flow_storage['tracking'].pop(0)

            # pop from data lists using to_revert
            for r in to_revert:
              flow_storage['data'][r].pop(0)

        else:
          # check if there is storage for option selected
          # first, get the option:
          opt = get_option(mdict[flow_stack[0]]['options'], i)
          track = []
          if opt and 'store' in opt:
            for key in opt['store'].keys():
              # get the value
              v = opt['store'][key]

              # check if key is new
              if key not in flow_storage['data']:
                flow_storage['data'][key] = []

              # add the new value to the to of the stack
              flow_storage['data'][key].insert(0, v)

              # append the key to the tracking list
              track.append(key)

                
              
              

          flow_storage['tracking'].insert(0, track)
          flow_stack.insert(0, metadata['opt_flow_map'][i])
  #print('************************')
  #print('*Debug Info:')
  #print('*Ending flow_stack: {}'.format(flow_stack))
  #print('*Ending flow_storage: {}'.format(flow_storage))
  