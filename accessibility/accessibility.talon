os: windows
-
# Useful accessibility commands for generic situations
# Actions include "click on","hover","highlight","label","go select","invoke"; see <user interface actions.talon-list>

# SEARCH FOR UI ELEMENT DYNAMICALLY
# Searches for a UI element with a name beginning with the spoken form

^{user.ui_action} {user.dynamic_element}$: user.act_on_named_element(dynamic_element,ui_action)

# NAVIGATE TO A TARGET USING KEYS
# Presses the designated navigation key until an element beginning with the target name is reached.
# user.nav_key includes things like tab, arrow keys, f6
# user.ax_target is just any spoken phrase. It will be translated 
#  into regex for continuation and catching homophones

^{user.nav_key} until [<user.ordinals>] <user.ax_target>$:
	key("{nav_key}")
	x = ordinals or 1
	user.key_to_elem_by_val(nav_key,"{ax_target}.*","name",ordinals or 1)
	
^{user.nav_key} {user.ui_action}$:
	user.clear_highlights()
	key("{nav_key}")
	user.act_on_element(user.focused_element(),ui_action)
	
# FOCUSED ELEMENT

^{user.ui_action} focused [element]$: user.act_on_element(user.focused_element(),ui_action) 

# MANAGING HIGHLIGHTS LIST

clear (highlights|labels): user.clear_highlights()

