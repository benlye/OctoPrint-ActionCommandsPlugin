# coding=utf-8
from __future__ import absolute_import

import logging
import time
import os
import sys

import octoprint.plugin
import octoprint.settings

__plugin_name__ = "Action Commands"
__plugin_version__ = "0.2"
__plugin_pythoncompat__ = ">=2.7,<4"

def __plugin_init__():
    global _plugin
    global __plugin_hooks__

    global __plugin_implementation__
    __plugin_implementation__ = ActionCommandsPlugin()
    
    __plugin_hooks__ = {
        "octoprint.comm.protocol.action": __plugin_implementation__.hook_actioncommands, 
        "octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
    }

class ActionCommandsPlugin(octoprint.plugin.TemplatePlugin,
              octoprint.plugin.AssetPlugin,
              octoprint.plugin.SettingsPlugin):
  
    def __init__(self):
        self.command_definitions = {}

    def on_settings_initialized(self):
        self.reload_command_definitions()

    def reload_command_definitions(self):
        self.command_definitions = {}

        command_definitions_tmp = self._settings.get(["command_definitions"])
        self._logger.debug("command_definitions: %s" % command_definitions_tmp)

        for definition in command_definitions_tmp:
            self.command_definitions[definition['action']] = dict(type=definition['type'], command=definition['command'], enabled=definition['enabled'])
            self._logger.info("Add command definition 'action:%s' = %s" % (definition['action'], definition['command']))

    def get_settings_defaults(self):
        return dict(
            command_definitions = []
        )

    def on_settings_save(self, data):
        octoprint.plugin.SettingsPlugin.on_settings_save(self, data)
        self.reload_command_definitions()

    def get_template_configs(self):
        return [
            dict(type="settings", name="Action Commands", custom_bindings=True)
        ]

    def get_assets(self):
        return {
            "js": ["js/actioncommands.js"]
        } 

    def get_update_information(self):
        return dict(
        actioncommands=dict(
        displayName="Action Commands",
        displayVersion=self._plugin_version,
        
        # version check: github repository
        type="github_release",
        user="benlye",
        repo="OctoPrint-ActionCommandsPlugin",
        current=self._plugin_version,
        
        # update method: pip w/ dependency links
        pip="https://github.com/benlye/OctoPrint-ActionCommandsPlugin/archive/{target_version}.zip"
        )
    )

    def hook_actioncommands(self, comm, line, command):
        self._logger.info("Command received: 'action:%s'" % (command))
        
        if command == None:
            return

        else:
            try:
                this_command = self.command_definitions[command]
                self._logger.info("Command found for 'action:%s'" % (command))
            except:
                self._logger.error("No command found for 'action:%s'" % command)
                return (None,)

        if this_command["enabled"] == True:
            self._logger.info("Command 'action:%s' is enabled" % command)
            
        else:
            self._logger.info("Command 'action:%s' is disabled" % command)
            return (None,)

        if this_command["type"] == "gcode":
            self._logger.info("Command 'action:%s' is type 'gcode'" % (command))
            self._logger.info("Executing printer command '%s'" % (this_command["command"]))
            self._printer.commands(this_command["command"].split(";"))

        elif this_command["type"] == "system":
            self._logger.info("Command 'action:%s' is type 'system'" % (command))
            self._logger.info("Executing system command '%s'" % (this_command["command"]))

            try:
                r = os.system(this_command["command"])
            except:
                e = sys.exc_info()[0]
                self._logger.exception("Error executing command '%s'" % (this_command["command"]))
                return (None,)
            
            self._logger.info("Command '%s' returned: %s" % (this_command["command"], r))
            
        else:
            self._logger.error("Command type not found or not known for 'action:%s'" % command)
            return (None,)
