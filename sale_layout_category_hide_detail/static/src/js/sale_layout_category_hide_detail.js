/* eslint-disable init-declarations */
/* Copyright 2019 Tecnativa - Ernesto Tejeda
/* Copyright 2022 Tecnativa - Víctor Martínez
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */
odoo.define(
    "sale_layout_category_hide_detail.sale_layout_category_hide_detail",
    function (require) {
        "use strict";

        var sectionAndNoteListRenderer = require("account.section_and_note_backend");

        var SectionAndNoteListRenderer = {
            _getOptionValueFromField: function (name, option) {
                if (name in this.state.fieldsInfo.list) {
                    return this.state.fieldsInfo.list[name].options[option];
                }
                return false;
            },
            _allowRemoveClassHidden: function (name) {
                return this._getOptionValueFromField(name, "show_in_line_section");
            },
            _getColspanSectionName: function () {
                var nbrColumns = this._getNumberOfCols();
                if (this.handleField) {
                    nbrColumns--;
                }
                if (this.addTrashIcon) {
                    nbrColumns--;
                }
                nbrColumns -= this._getNumberOfLineSectionFields();
                return nbrColumns;
            },
            _renderBodyCell: function (record, node) {
                var $cell = this._super.apply(this, arguments);
                var isSection = record.data.display_type === "line_section";
                var isNote = record.data.display_type === "line_note";
                if (isSection || isNote) {
                    if (this._allowRemoveClassHidden(node.attrs.name)) {
                        return $cell.removeClass("o_hidden");
                    } else if (node.attrs.name === "name") {
                        $cell.attr("colspan", this._getColspanSectionName());
                    }
                }
                return $cell;
            },
            _getNumberOfLineSectionFields: function () {
                var section_fields_count = 0;
                var self = this;
                this.columns.forEach(function (elem) {
                    if (
                        self._getOptionValueFromField(
                            elem.attrs.name,
                            "show_in_line_section"
                        )
                    ) {
                        section_fields_count++;
                    }
                });
                return section_fields_count;
            },
            _getColumnWidth: function (column) {
                var res = this._super.apply(this, arguments);
                if (column.attrs.widget === "boolean_fa_icon") res = "15px";
                return res;
            },
            _renderHeaderCell: function (node) {
                var $th = this._super.apply(this, arguments);
                if (!(node.attrs.name in this.state.fieldsInfo.list)) {
                    return $th;
                }
                if (
                    this._getOptionValueFromField(
                        node.attrs.name,
                        "show_in_line_section"
                    )
                ) {
                    $th.text("").removeClass("o_column_sortable");
                }
                return $th;
            },
        };

        sectionAndNoteListRenderer.include(SectionAndNoteListRenderer);
    }
);
