$(function() {
    function ActionCommandsViewModel(parameters) {
        var self = this;

        self.global_settings = parameters[0];

        self.command_definitions = ko.observableArray();

        self.addCommandDefinition = function() {
            self.command_definitions.push({action:"", type:"", command:"", enabled: true});
        };

        self.removeCommandDefinition = function(definition) {
            self.command_definitions.remove(definition);
        };

        self.onBeforeBinding = function () {
            self.settings = self.global_settings.settings.plugins.actioncommands;
            self.command_definitions(self.settings.command_definitions.slice(0));
        };

        self.onSettingsBeforeSave = function () {
            self.global_settings.settings.plugins.actioncommands.command_definitions(self.command_definitions.slice(0));
        }
    }

    ADDITIONAL_VIEWMODELS.push([
        ActionCommandsViewModel,
        ["settingsViewModel"],
        ["#settings_plugin_actioncommands"]
    ]);
});
