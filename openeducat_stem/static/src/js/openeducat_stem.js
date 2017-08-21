odoo.define('web.html_field', function (require) {
    "use strict";

    var core = require('web.core');

    var Listview = require('web.ListView');

    var formats = require('web.formats');

    var list_widget_registry = core.list_widget_registry;

    var html = Listview.Column.extend({
        _format: function (row_data, options) {

            return formats.format_value(row_data[this.id].value, this, options.value_if_empty);
        }
    });

    list_widget_registry.add('field.html', html);
});