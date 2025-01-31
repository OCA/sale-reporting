/** @odoo-module **/
/* Copyright 2019 Tecnativa - Ernesto Tejeda
/* Copyright 2022 Tecnativa - Víctor Martínez
/* Copyright 2023 Tecnativa - Yadier Quesada
/* License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).*/

import {SectionAndNoteListRenderer} from "@account/components/section_and_note_fields_backend/section_and_note_fields_backend";
import {patch} from "@web/core/utils/patch";
import {ProductLabelSectionAndNoteListRender} from "@account/components/product_label_section_and_note_field/product_label_section_and_note_field";

patch(ProductLabelSectionAndNoteListRender.prototype, {
    getActiveColumns(list) {
        const activeColumns = super.getActiveColumns(list);
        // Remove widgets from list_renderer columns
        return activeColumns.filter((col) => col.widget !== "boolean_fa_icon");
    },
});

patch(SectionAndNoteListRenderer.prototype, {
    getSectionColumns(columns) {
        var sectionCols = super.getSectionColumns(columns);
        if (this.record.data.display_type !== "line_section") {
            // We do not want to display icons in notes, only in sections
            return sectionCols;
        }
        const widgetCols = this.allColumns.filter(
            (col) => col.widget === "boolean_fa_icon"
        );
        sectionCols.forEach(function (item) {
            // Adapt colspan of the name column, to make space for widget columns
            if (item.colspan > 1) {
                item.colspan -= widgetCols.length;
            }
        });
        // Add widget columns to section rows
        return sectionCols.concat(widgetCols);
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
