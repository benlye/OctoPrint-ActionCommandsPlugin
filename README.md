# OctoPrint ActionCommands Plugin
Adds handling for custom action commands to OctoPrint.  Action commands are sent from the RepRap machine in the form `//action:command`.  

The plugin allows OctoPrint to execute a system command or send G-code to the printer in response to an action command.

## Installation
Install via the OctoPrint plugin manager.

## Use
As of the latest Marlin bugfix-1.1.x version, the command `M118` can be used to echo output to serial, meaning that `M118 //action:dostuff` would cause this plugin to try to handle the `dostuff` command when `//action:dostuff` was echoed back on the serial console.

A future application of the plugin would be to add actions in the RepRap machine's firmware so that hosts could respond.  For example, when Marlin is killed because something is wrong it would echo `//action:poweroff` and the attached OctoPrint instance could use this action command to trigger the printer's power outlet to switch off.

## References
* [OctoPrint Documentation](http://docs.octoprint.org/en/master/features/action_commands.html)
* [RepRap Wiki](http://reprap.org/wiki/Gcode#Replies_from_the_RepRap_machine_to_the_host_computer)

## Screenshot
![Settings](images/settings.png?raw=true)
