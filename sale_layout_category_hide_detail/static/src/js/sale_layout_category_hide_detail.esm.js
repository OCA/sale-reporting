/** @odoo-module **/
/* Copyright 2019 Tecnativa - Ernesto Tejeda
/* Copyright 2022 Tecnativa - Víctor Martínez
/* Copyright 2023 Tecnativa - Yadier Quesada
/* License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).*/

import {SectionAndNoteListRenderer} from "@account/components/section_and_note_fields_backend/section_and_note_fields_backend";
import {patch} from "@web/core/utils/patch";

patch(SectionAndNoteListRenderer.prototype, "new_widgets_buttons_patch", {
    getSectionColumns(columns) {
        var sectionCols = this._super.apply(this, arguments);
        const widgetCols = columns.filter((col) => col.widget === "boolean_fa_icon");
        const sectionWidget = widgetCols.map((col) => {
            return {...col, colspan: 1};
        });
        sectionCols.forEach(function (item) {
            if (item.colspan > 1) {
                item.colspan -= widgetCols.length;
            }
        });
        return sectionCols.concat(sectionWidget);
    },

    getCellClass(column) {
        var classNames = this._super.apply(this, arguments);
        if (column.widget === "boolean_fa_icon") {
            classNames = classNames.replace("o_hidden", "");
        }
        return classNames;
    },

    getColumnClass(column) {
        if (column.widget === "boolean_fa_icon") {
            column.hasLabel = false;
        }
        return this._super.apply(this, arguments);
    },
    /**
     * @override method from ListRenderer.isSortable
     * @param {Object} column - The column to render
     */
    isSortable(column) {
        if (column.widget === "boolean_fa_icon") {
            return false;
        }
        return this._super.apply(this, arguments);
    },
    /**
     * @override method from ListRenderer.calculateColumnWidth
     * @param {Object} column - The column to render
     */
    calculateColumnWidth(column) {
        if (column.widget === "boolean_fa_icon") {
            return {type: "absolute", value: "20px"};
        }
        return this._super.apply(this, arguments);
    },
});
