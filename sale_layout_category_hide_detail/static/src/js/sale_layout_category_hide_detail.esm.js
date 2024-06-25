/** @odoo-module **/
/* Copyright 2019 Tecnativa - Ernesto Tejeda
/* Copyright 2022 Tecnativa - Víctor Martínez
/* Copyright 2023 Tecnativa - Yadier Quesada
/* License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).*/

import {SectionAndNoteListRenderer} from "@account/components/section_and_note_fields_backend/section_and_note_fields_backend";
import {patch} from "@web/core/utils/patch";

patch(SectionAndNoteListRenderer.prototype, {
    getColumns(record) {
        // Set record to use it in getSectionColumns()
        this.record = record;
        return super.getColumns(record);
    },
    getSectionColumns(columns) {
        // We do not want to display icons in notes, only in sections
        if (this.record.data.display_type !== "line_section") {
            return super.getSectionColumns(columns);
        }
        var sectionCols = super.getSectionColumns(columns);
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

    getCellClass(column, record) {
        let classNames = super.getCellClass(column, record);
        if (column.widget === "boolean_fa_icon") {
            classNames = classNames.replace("o_hidden", "");
        }
        return classNames;
    },

    getColumnClass(column) {
        if (column.widget === "boolean_fa_icon") {
            column.hasLabel = false;
        }
        return super.getColumnClass(column);
    },
    /**
     * @override method from ListRenderer.isSortable
     * @param {Object} column - The column to render
     */
    isSortable(column) {
        if (column.widget === "boolean_fa_icon") {
            return false;
        }
        return super.isSortable(column);
    },
    /**
     * @override method from ListRenderer.calculateColumnWidth
     * @param {Object} column - The column to render
     */
    calculateColumnWidth(column) {
        if (column.widget === "boolean_fa_icon") {
            return {type: "absolute", value: "20px"};
        }
        return super.calculateColumnWidth(column);
    },
});
