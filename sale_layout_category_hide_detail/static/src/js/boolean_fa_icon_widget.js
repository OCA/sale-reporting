/* Copyright 2019 Tecnativa - Ernesto Tejeda
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */
odoo.define('sale_layout_category_hide_detail.boolean_fa_icon_widget', function (require) {
    "use strict";

    var core = require('web.core');
    var AbstractField = require('web.AbstractField');
    var registry = require('web.field_registry');

    var _t = core._t;

    var BooleanFaIconWidget = AbstractField.extend({
        className: 'o_boolean_fa_icon_widget',
        events: {
            'click': '_toggleValue'
        },
        supportedFieldTypes: ['boolean'],

        //--------------------------------------------------------------------------
        // Public
        //--------------------------------------------------------------------------

        /**
         * A boolean field is always set since false is a valid value.
         *
         * @override
         */
        isSet: function () {
            return true;
        },

        //--------------------------------------------------------------------------
        // Private
        //--------------------------------------------------------------------------

        /**
         * Render font-awesome icon based on state
         *
         * @override
         * @private
         */
        _render: function () {
            //set icon class
            var fa_icons = this.attrs.options.fa_icons;
            var icon_true = fa_icons && fa_icons.icon_true || 'fa-check-square-o';
            var icon_false = fa_icons && fa_icons.icon_false || 'fa-square-o';
            var fa_class = this.value ? icon_true : icon_false;
            //set tip message
            var terminology = this.attrs.options.terminology;
            var hover_true = terminology && _t(terminology.hover_true) || _t('Click to uncheck');
            var hover_false = terminology && _t(terminology.hover_false) || _t('Click to check');
            var tip = this.value ? hover_true : hover_false;
            //set template and add it to $el
            var template = "<span class='fa %s' title='%s' aria-label='%s'></span>";
            this.$el.empty().append(_.str.sprintf(template, fa_class, tip))
        },

        //--------------------------------------------------------------------------
        // Handlers
        //--------------------------------------------------------------------------

        /**
         * Toggle value
         *
         * @private
         * @param {MouseEvent} event
         */
        _toggleValue: function (event) {
            event.preventDefault();
            event.stopPropagation();
            this._setValue(!this.value);
        },
    });

    registry.add('boolean_fa_icon', BooleanFaIconWidget);
    return BooleanFaIconWidget;
});
