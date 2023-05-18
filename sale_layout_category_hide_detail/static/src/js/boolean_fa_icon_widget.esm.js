/** @odoo-module **/
/* Copyright 2019 Tecnativa - Ernesto Tejeda
/* Copyright 2022 Tecnativa - Víctor Martínez
/* Copyright 2023 Tecnativa - Yadier Quesada
/* License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).*/

const {useState} = owl;
import {BooleanField} from "@web/views/fields/boolean/boolean_field";
import {_lt} from "@web/core/l10n/translation";
import {registry} from "@web/core/registry";

const iconTrue = "fa-check-square-o";
const iconFalse = "fa-square-o";
const tooltipTrue = "Switch to hidden";
const tooltipFalse = "Switch to show";

export class BooleanFaIconWidget extends BooleanField {
    setup() {
        super.setup();
        this.state = useState({
            fa_class: this.faIconClass(this.props.value),
            text_tooltip: this.textTooltip(this.props.value),
        });
    }
    // --------------------------------------------------------------------------
    // Public
    // --------------------------------------------------------------------------
    faIconClass(currentValue) {
        var fa_icons = this.props.fa_icons;
        var icon_true = fa_icons.icon_true || iconTrue;
        var icon_false = fa_icons.icon_false || iconFalse;
        return currentValue ? icon_true : icon_false;
    }
    // --------------------------------------------------------------------------
    // Public
    // --------------------------------------------------------------------------
    textTooltip(currentValue) {
        var show_tooltip = this.props.terminology;
        var tooltip_true = show_tooltip.hover_true || tooltipTrue;
        var tooltip_false = show_tooltip.hover_false || tooltipFalse;
        return currentValue ? _lt(tooltip_true) : _lt(tooltip_false);
    }
    /**
     * Check the 'draft' state in sale order or invoices
     * Only the order in this state are allowed to edit the value for the widget
     * @param {Object} column - The column to render
     * @returns {Boolean}
     */
    isAllowEdit() {
        var resModel = this.props.record.resModel;
        var state = this.props.record.data.state;
        if (typeof state === "undefined" || state === null) {
            state = this.props.record.data.parent_state;
        }
        if (
            ["account.move.line", "sale.order.line"].includes(resModel) &&
            state !== "draft"
        ) {
            this.props.allow = false;
        }
        return this.props.allow;
    }
    /**
     * @override from BooleanField.isReadonly
     * We need to get readonly attribute from field
     * and allow to edit inline without the need of focus
     */
    get isReadonly() {
        return this.props.record.isReadonly(this.props.name);
    }
    /**
     * @returns {Boolean} allow
     */
    get allow() {
        return this.props.allow;
    }
    /**
     * @returns {String} fa_icons
     */
    get fa_icons() {
        return this.props.fa_icons;
    }
    /**
     * @returns {String} terminology
     */
    get terminology() {
        return this.props.terminology;
    }
    /**
     * This method change the value for record, fa-icon class and text for tooltip.
     * @event click - triggered when widget element is clicked
     */
    onClickButton(ev) {
        ev.stopPropagation();
        if (this.isReadonly || !this.isAllowEdit()) {
            return;
        }
        const newValue = !this.props.value;
        this.props.update(newValue);
        this.state.fa_class = this.faIconClass(newValue);
        this.state.text_tooltip = this.textTooltip(newValue);
    }
}

BooleanFaIconWidget.template = "sale_layout_category.BooleanFaIconWidget";
BooleanFaIconWidget.displayName = _lt("Toggle");

BooleanFaIconWidget.defaultProps = {
    fa_icons: {
        icon_true: "fa-check-square-o",
        icon_false: "fa-square-o",
    },
    terminology: {
        hover_true: _lt("Switch to: details hidden"),
        hover_false: _lt("Switch to: details shown"),
    },
    allow: true,
};

BooleanFaIconWidget.props = {
    ...BooleanField.props,
    fa_icons: {type: Object, optional: true},
    terminology: {type: Object, optional: true},
    allow: {type: Boolean, optional: true},
};

// Extract props from the attributes
BooleanFaIconWidget.extractProps = ({attrs}) => {
    return {
        fa_icons: attrs.options.fa_icons,
        terminology: attrs.options.terminology,
    };
};

registry.category("fields").add("boolean_fa_icon", BooleanFaIconWidget);
