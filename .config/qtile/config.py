import os
import re
import socket
import subprocess
import json
from libqtile import qtile
from libqtile.config import Drag, Key, Screen, Group, Drag, Click, Rule, KeyChord, Match, DropDown, ScratchPad
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.widget import Spacer

# logfile: ~/.local/share/qtile
# reqs: psutil, rofi, alacritty, thunar

mod = "mod4" #  mod4 or mod = super key
mod1 = "alt"
mod2 = "control"

# PATHS
home = os.path.expanduser('~')
myTerm = "alacritty"
rofi_file_find = 'rofi  -show find -modi find:~/.config/rofi/scripts/file-finder -width 1600'
rofi_power_menu = 'rofi  -show menu -modi "menu:~/.config/rofi/scripts/power-menu --choices=logout/suspend/shutdown/reboot" -config "~/.config/rofi/themes/Pmenu.rasi" --no-symbols'
notes_app = '~/Applications/Joplin-2.7.13.AppImage'

@lazy.function
def window_to_prev_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i - 1].name)

@lazy.function
def window_to_next_group(qtile):
    if qtile.currentWindow is not None:
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentWindow.togroup(qtile.groups[i + 1].name)

# KEYBINDINGS
keys = [
	# SUPER + KEYS
    Key([mod], "q", lazy.window.kill()),
    Key([mod], "w", lazy.window.toggle_floating()),
    Key([mod], "e", lazy.spawn(rofi_file_find)), 
    Key([mod], "r", lazy.layout.flip()), # flip layout for monadrall/monadwide
    Key([mod], "a", lazy.spawn(myTerm + ' -e ranger')), 
    Key([mod], "s", lazy.spawn()),
    Key([mod], "d", lazy.spawn('rofi -show drun')),
    Key([mod], "f", lazy.window.toggle_fullscreen()),
	Key([mod], "period", lazy.next_screen()), 
    Key([mod], "space", lazy.next_screen()),
    Key([mod], "Escape", lazy.spawn('xkill')),
    Key([mod], "Return", lazy.spawn(myTerm)),
    # SUPER + KEYPAD
    Key([mod], "KP_Insert", lazy.restart()), # KP 0
    Key([mod], "KP_Subtract", lazy.spawn(rofi_power_menu)), # KP -
    Key([mod], "KP_Add", lazy.spawn('pavucontrol')), # KP +
	# SUPER + SHIFT + KEYS
    Key([mod, "shift"], "q", lazy.spawn('qalculate-gtk')),
    Key([mod, "shift"], "w", lazy.spawn('geany')),
    Key([mod, "shift"], "e", lazy.spawn('pycharm')),
    Key([mod, "shift"], "a", lazy.spawn('firefox')),
    Key([mod, "shift"], "s", lazy.spawn('./.local/bin/internet-search')), # No es un rofi modi es un script que usa rofi
    Key([mod, "shift"], "d", lazy.spawn('chromium -no-default-browser-check')),
	Key([mod, "shift"], "z", lazy.spawn(myTerm)),	
    Key([mod, "shift"], "x", lazy.spawn(myTerm)),
    Key([mod, "shift"], "c", lazy.spawn(myTerm)), 
    Key([mod, "shift"], "Return", lazy.spawn('Thunar')),
	# SUPER + CTRL KEYS (File association programs)
    #Key([mod, "control"], "s", lazy.spawn('libreoffice')),
    #Key([mod, "shift"], "x", lazy.shutdown()),
	# CONTROL KEYS
	#Key([mod], "z", lazy.next_screen()),
	# CONTROL + ALT KEYS
    #Key(["mod1", "control"], "Next", lazy.spawn('conky-rotate -n')), #
    #Key(["mod1", "control"], "Prior", lazy.spawn('conky-rotate -p')), #
    #Key(["mod1", "control"], "c", lazy.spawn('catfish')),
    Key(["mod1", "control"], "o", lazy.spawn(home + '/.config/qtile/scripts/picom-toggle.sh')),
    #Key(["mod1", "control"], "w", lazy.spawn('')),
	# ALT + Fx KEYS
    #Key(["mod1"], "F2", lazy.spawn('gmrun')),
    #Key(["mod1"], "F3", lazy.spawn('xfce4-appfinder')),
	# CONTROL + SHIFT KEYS
    #Key([mod2, "shift"], "Escape", lazy.spawn('xfce4-taskmanager')),
    Key([], "Print", lazy.spawn('xfce4-screenshooter')),
	# MULTIMEDIA KEYS
    # INCREASE/DECREASE BRIGHTNESS
    Key([], "XF86MonBrightnessUp", lazy.spawn("xbacklight -inc 5")),
    Key([], "XF86MonBrightnessDown", lazy.spawn("xbacklight -dec 5")),
    # INCREASE/DECREASE/MUTE VOLUME
    Key([], "XF86AudioMute", lazy.spawn("amixer -q set Master toggle")),
    Key([], "XF86AudioLowerVolume", lazy.spawn("amixer -q set Master 5%-")),
    Key([], "XF86AudioRaiseVolume", lazy.spawn("amixer -q set Master 5%+")),
    Key([], "XF86AudioPlay", lazy.spawn("playerctl play-pause")),
    Key([], "XF86AudioNext", lazy.spawn("playerctl next")),
    Key([], "XF86AudioPrev", lazy.spawn("playerctl previous")),
    Key([], "XF86AudioStop", lazy.spawn("playerctl stop")),
	#Key([], "XF86AudioPlay", lazy.spawn("mpc toggle")),
	#Key([], "XF86AudioNext", lazy.spawn("mpc next")),
	#Key([], "XF86AudioPrev", lazy.spawn("mpc prev")),
	#Key([], "XF86AudioStop", lazy.spawn("mpc stop")),
	# CHANGE FOCUS
    Key([mod], "Up", lazy.layout.up()),
    Key([mod], "Down", lazy.layout.down()),
    Key([mod], "Left", lazy.layout.left()),
    Key([mod], "Right", lazy.layout.right()),
    Key([mod], "k", lazy.layout.up()),
    Key([mod], "j", lazy.layout.down()),
    Key([mod], "h", lazy.layout.left()),
    Key([mod], "l", lazy.layout.right()),
	# RESIZE UP, DOWN, LEFT, RIGHT
	# Commented lazy.layouts generate errors on qtiles logfile
    Key([mod, "control"], "l",
        #lazy.layout.grow_right(),
        lazy.layout.grow(),
        #lazy.layout.increase_ratio(),
        #lazy.layout.delete(),
        ),
    Key([mod, "control"], "Right",
        #lazy.layout.grow_right(),
        lazy.layout.grow(),
        #lazy.layout.increase_ratio(),
        #lazy.layout.delete(),
        ),
    Key([mod, "control"], "h",
        #lazy.layout.grow_left(),
        lazy.layout.shrink(),
        #lazy.layout.decrease_ratio(),
        #lazy.layout.add(),
        ),
    Key([mod, "control"], "Left",
        #lazy.layout.grow_left(),
        lazy.layout.shrink(),
        #lazy.layout.decrease_ratio(),
        #lazy.layout.add(),
        ),
    Key([mod, "control"], "k",
        #lazy.layout.grow_up(),
        lazy.layout.grow(),
        #lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "Up",
        #lazy.layout.grow_up(),
        lazy.layout.grow(),
        #lazy.layout.decrease_nmaster(),
        ),
    Key([mod, "control"], "j",
        #lazy.layout.grow_down(),
        lazy.layout.shrink(),
        #lazy.layout.increase_nmaster(),
        ),
    Key([mod, "control"], "Down",
        #lazy.layout.grow_down(),
        lazy.layout.shrink(),
        #lazy.layout.increase_nmaster(),
        ),
	# MOVE WINDOWS UP OR DOWN MONADTALL/MONADWIDE LAYOUT
    Key([mod, "shift"], "Up", lazy.layout.shuffle_up()),
    Key([mod, "shift"], "Down", lazy.layout.shuffle_down()),
    Key([mod, "shift"], "Left", lazy.layout.swap_left()),
    Key([mod, "shift"], "Right", lazy.layout.swap_right()),
	# FUNCTION KEYS
    Key([], "F12", lazy.spawn('xfce4-terminal --drop-down')),
	# FLIP LAYOUT FOR BSP
	#Key([mod, "mod1"], "k", lazy.layout.flip_up()),
	#Key([mod, "mod1"], "j", lazy.layout.flip_down()),
	#Key([mod, "mod1"], "l", lazy.layout.flip_right()),
	#Key([mod, "mod1"], "h", lazy.layout.flip_left()),
	# MOVE WINDOWS UP OR DOWN BSP LAYOUT
	#Key([mod, "shift"], "k", lazy.layout.shuffle_up()),
	#Key([mod, "shift"], "j", lazy.layout.shuffle_down()),
	#Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
	#Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
    ]

# GROUPS
groups = []
group_names = ["1", "2", "3", "4", "5", "6",]
group_labels = ["1 ", "2 ", "3 ", "4 ", "5 ", "6 ",]
group_layouts = ["ratiotile", "ratiotile", "ratiotile", "ratiotile", "ratiotile", "ratiotile",]

for i in range(len(group_names)):
    groups.append(
        Group(
            name=group_names[i],
            layout=group_layouts[i].lower(),
            label=group_labels[i],
        ))


for i in groups:
    keys.extend([

# CHANGE GROUPS
        Key([mod], i.name, lazy.group[i.name].toscreen()),
        Key([mod], "Tab", lazy.next_layout()),
        Key(["mod1"], "Tab", lazy.spawn("rofi -show window")),
        #Key(["mod1", "shift"], "Tab", lazy.screen.prev_group()),

# MOVE WINDOW TO SELECTED WORKSPACE AND STAY ON WORKSPACE
        Key([mod, "shift"], i.name, lazy.window.togroup(i.name)),

# MOVE WINDOW TO SELECTED WORKSPACE AND FOLLOW MOVED WINDOW TO WORKSPACE
        #Key([mod, "shift"], i.name, lazy.window.togroup(i.name) , lazy.group[i.name].toscreen()),
    ])

# SCRATCHPADS
#groups.append(ScratchPad("0",[DropDown("notes", 'alacritty -o "window.opacity=1" -e "joplin"', x=0.05, y=0.02, width=0.9, height=0.95, on_focus_lost_hide=True)]))
groups.append(ScratchPad("0",[DropDown("notes", 'xfce4-terminal -e "joplin"', x=0.05, y=0.02, width=0.9, height=0.95, on_focus_lost_hide=True)]))
keys.append(Key([mod], 's', lazy.group['0'].dropdown_toggle('notes')))

# COLOR PALETTE
def init_theme():
	theme_name = 'theme03'
	config_file = home + '/.config/qtile/themes/' + theme_name + '.json'
	if os.path.isfile(config_file):
		with open(config_file) as f:
			dict_theme = json.load(f)
		return [key for key in dict_theme.values()]
	else:
		# fallback to /themes/default.json
		with open(home + '/.config/qtile/themes/default.json') as f:
			dict_theme = json.load(f)
		return [key for key in dict_theme.values()]
	

current_theme = init_theme()

def init_layout_theme():
    return {
		"margin":8,
		"border_width":3,
		#"border_focus": "#5294e2", #"#acb9ca",
		"border_focus": current_theme[6], #"#5294e2", #"#acb9ca",
		"border_normal": current_theme[9] # "#4c566a"
		}

layout_theme = init_layout_theme()

# LAYOUTS
layouts = [
    layout.RatioTile(**layout_theme),
    layout.MonadTall(**layout_theme),
    # layout.MonadWide(**layout_theme),
    # layout.Matrix(**layout_theme),
    # layout.Bsp(**layout_theme),   
    # layout.Max(**layout_theme),
    # layout.TreeTab(sections=['Tabs:'], panel_width=85, bg_color="#2F343F", fontsize=10, place_right=True),
    # layout.Floating(margin=3, border_width=1, border_focus="#fba922", border_normal="#fba922"),
    # layout.Stack(num_stacks=2)
]

# WIDGETS
def init_widgets_defaults():
    return dict(
		font = "Noto Sans Bold", #"JetBrains Mono",
		fontsize = 12,
		padding = 2,
		background = current_theme[0]
		)
widget_defaults = init_widgets_defaults()

# BUILT-IN WIDGETS
wdg_menu = widget.TextBox(
	fontsize = 20,
	foreground = current_theme[5],
	text = "",
	padding = 0,
	mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('rofi -show drun')}
	)
wdg_updates = widget.GenPollText(
	padding = 2,
	fontsize = 14,
	foreground = current_theme[5],
	background = current_theme[2],
	update_interval= 900,
	func=lambda: subprocess.check_output(os.path.expanduser("~/.config/qtile/scripts/packages.sh")).decode().strip(),
	mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' --hold -e checkupdates')}
	)
wdg_clock = widget.Clock(
	fontsize = 14,
	foreground = current_theme[5],
	background = current_theme[2],
	padding = 6,
	format = "%d %b, %a [%H:%M:%S]",
	mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' --hold -e cal -3m')}
	)
wdg_miniclock = widget.Clock(
	fontsize = 14,
	foreground = current_theme[5],
	background = current_theme[2],
	padding = 6,
	format = "%Y/%m/%d [%H:%M]",
	mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' --hold -e cal -3m')}
	)
wdg_cpuload = widget.CPU(
	format = 'CPU: {load_percent}%',
	foreground = current_theme[5],
	background = current_theme[2],
	padding = 3,
	update_interval = 3,
	mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' -e htop')}
	)
wdg_cputemp = widget.ThermalSensor(
	foreground = current_theme[5],
	foreground_alert = current_theme[7],
	background = current_theme[2],
	metric = True,
	padding = 3,
	threshold = 80,
	update_interval = 3
	)
wdg_ram = widget.Memory(
	format = 'RAM:{MemUsed: .0f}{mm}',
	update_interval = 3,
	padding = 3,
	fontsize = 12,
	foreground = current_theme[5],
	background = current_theme[2],
	mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' --hold -e top -o +%MEM')} # top -o +%MEM // free -h
	)		    
wdg_gpu = widget.GenPollText(
	foreground = current_theme[5],
	background = current_theme[2],
	update_interval= 30, 
	func=lambda: subprocess.check_output(os.path.expanduser("~/.config/qtile/scripts/gpu-stats.sh")).decode().strip(),
	mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('nvidia-settings')}
	)		
wdg_net = widget.Net(
	fontsize = 12,
	markup= True,
	interface = "enp0s31f6",
	format = '{down:} ↓↑ {up}',
	prefix= 'M',
	foreground = current_theme[5],
	background = current_theme[2],
	padding = 3,
	update_interval = 3,
	#mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' --hold -e ss -taunp')}
	)
wdg_df = widget.DF(
	fontsize=12,
	foreground = current_theme[5],
	background = current_theme[2],
	visible_on_warn = False,
	partition= '/home',
	format='/~ {uf}Gb ({r: .0f}%)',
	update_interval=300,
	mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn(myTerm + ' --hold -e df -h')}
	)
wdg_volicon = widget.TextBox(
	foreground = current_theme[5],
	fontsize = 16,
	text = "",
	mouse_callbacks = {'Button1': lambda: qtile.cmd_spawn('pavucontrol')}
	)		
wdg_volprct = widget.Volume(
	foreground = current_theme[5],
	background = current_theme[0],
	padding = 0
	)

# WIDGET DECORATORS
dec_sep = widget.Sep(
	linewidth = 0,
	padding = 8,
	background = current_theme[0],
	)
dec_fsep = widget.Sep(
	linewidth = 0,
	padding = 120,
	background = current_theme[0],
	)	
dec_angleopen = widget.TextBox(
	fontsize = 32,
	foreground = current_theme[2],
	background = current_theme[0],
	text = "",
	padding = 0
	)
dec_angleclose = widget.TextBox(
	fontsize = 32,
	foreground = current_theme[2],
	background = current_theme[0],
	text = "", 
	padding = 0
	)		
dec_cubeopen = widget.TextBox(
	fontsize = 32,
	foreground = current_theme[2],
	background = current_theme[0],
	text = "",
	padding = 0
	)		
dec_cubeclose = widget.TextBox(
	fontsize = 32,
	foreground = current_theme[2],
	background = current_theme[0],
	text = "",
	padding = 0
	)		
dec_vert = widget.TextBox(
	fontsize = 26,
	foreground = current_theme[9],
	background = current_theme[2],
	text = "",
	padding = 0
	)

# SCREEN 1  BAR COMPOSITION
def init_widgets_screen1():
    widgets_screen1 = [
		dec_sep,
		#wdg_menu,
		widget.CurrentLayoutIcon(
			foreground = current_theme[5],
			background = current_theme[0],
			scale = 0.6,
			padding = 0
			),
		dec_angleopen,
		wdg_updates,
		dec_angleclose,
		widget.GroupBox(
			font = "Noto Sans Bold",
			fontsize = 12,
			margin_y = 3,
			margin_x = 0,
			padding_y = 6,
			padding_x = 5,
			borderwidth = 5,
			disable_drag = True,
			rounded = False,
			highlight_method = "line",
			active = current_theme[8],
			inactive = current_theme[9],
			highlight_color = current_theme[4],
			this_current_screen_border = current_theme[6],
			other_current_screen_border = current_theme[7],
			this_screen_border = current_theme[6],
			other_screen_border = current_theme[7],
			foreground = current_theme[5],
			background = current_theme[0]
			),
		dec_angleopen,
		wdg_clock,
		dec_angleclose,
		widget.TaskList(
			max_title_width = 0,
			icon_size = None,
			center_aligned = True,
			# max_chars = 1,
			),
		dec_angleopen,
		# dec_cubeopen,
		wdg_cpuload,
		wdg_cputemp,
		dec_vert,
		wdg_ram,
		dec_vert,
		wdg_gpu,
		dec_vert,
		wdg_df,
		dec_vert,
		wdg_net,
		# dec_cubeclose,
		dec_angleclose,
		dec_sep,
		wdg_volicon,
		wdg_volprct,
		widget.Systray(
			background = current_theme[0],
			icon_size = 20,
			padding = 4
			),
		dec_sep,
		]
    return widgets_screen1

# SCREEN 2  BAR COMPOSITION
def init_widgets_screen2():
    widgets_screen2 = [	
		widget.CurrentLayoutIcon(
			foreground = current_theme[5],
			background = current_theme[0],
			scale = 0.6,
			padding = 0
			),
		dec_angleopen,
		wdg_miniclock,
		dec_angleclose,
		widget.GroupBox(
			fontsize = 12,
			margin_y = 3,
			margin_x = 0,
			padding_y = 6,
			padding_x = 5,
			borderwidth = 5,
			disable_drag = True,
			rounded = False,
			highlight_method = "line",
			active = current_theme[8],
			inactive = current_theme[9],
			highlight_color = current_theme[4],
			this_current_screen_border = current_theme[6],
			other_current_screen_border = current_theme[7],
			this_screen_border = current_theme[6],
			other_screen_border = current_theme[7],
			foreground = current_theme[5],
			background = current_theme[0]
			),
		#dec_angleopen,
		#wdg_clock,
		#dec_angleclose,
		#dec_sep,
		dec_angleopen,
		#dec_cubeopen,
		wdg_cpuload,
		wdg_cputemp,
		dec_vert,
		wdg_ram,
		dec_vert,
		wdg_gpu,
		dec_vert,
		wdg_net,
		dec_angleclose,
		dec_fsep,
		wdg_volicon,
		wdg_volprct,
		dec_fsep,
		]
    return widgets_screen2

# SCREEN INITIALIZATION
def init_screens():
    return [
	Screen(top=bar.Bar(widgets=init_widgets_screen1(), size=26)),
	Screen(top=bar.Bar(widgets=init_widgets_screen2(), size=26, opacity=1, margin=[0,0,0,0])),  # opacity default 1, margin [N,E,S,W]
	]
           
screens = init_screens()

# MOUSE CONFIGURATION
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size())
	]

dgroups_key_binder = None
dgroups_app_rules = []
main = None

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/scripts/autostart.sh'])

@hook.subscribe.startup
def start_always():
    # Set the cursor to something sane in X
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])

@hook.subscribe.client_new
def set_floating(window):
    if (window.window.get_wm_transient_for() or window.window.get_wm_type() in floating_types):
        window.floating = True

floating_types = ["notification", "toolbar", "splash", "dialog"]
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
# use xprop to get wm_class
floating_layout = layout.Floating(float_rules=[
	Match(wm_class = 'qalculate-gtk'),
    Match(wm_class = 'Galculator'),
    Match(wm_class = 'xfce4-terminal'),
    Match(wm_class = 'pavucontrol'),
    Match(title = 'P-Dal Capture'),
    Match(title = 'Save Document?'), # Libre Office
    Match(title = 'Torrent Options'), # Transmission 
    Match(title = 'Question'), # Geany
], border_focus = current_theme[6])

focus_on_window_activation = "focus" # or smart
wmname = "LG3D"
