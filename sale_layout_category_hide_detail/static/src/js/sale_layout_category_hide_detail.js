/* eslint-disable init-declarations */
/* Copyright 2019 Tecnativa - Ernesto Tejeda
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */
odoo.define(
    "sale_layout_category_hide_detail.sale_layout_category_hide_detail",
    function (require) {
        "use strict";

        var sectionAndNoteListRenderer = require("account.section_and_note_backend");

        var SectionAndNoteListRenderer = {
            _renderBodyCell: function (record, node, index, options) {
                var $cell = this._super.apply(this, arguments);

                var options;
                var show_in_line_section;

                var isSection = record.data.display_type === "line_section";
                var isNote = record.data.display_type === "line_note";
                if (isSection || isNote) {
                    if (node.attrs.name in this.state.fieldsInfo.list) {
                        options = this.state.fieldsInfo.list[node.attrs.name].options;
                        show_in_line_section = options.show_in_line_section;
                    } else {
                        show_in_line_section = false;
                    }

                    if (show_in_line_section) {
                        return $cell.removeClass("o_hidden");
                    } else if (node.attrs.name === "name") {
                        var nbrColumns = this._getNumberOfCols();
                        if (this.handleField) {
                            nbrColumns--;
                        }
                        if (this.addTrashIcon) {
                            nbrColumns--;
                        }
                        nbrColumns -= this._getNumberOfLineSectionFields();
                        $cell.attr("colspan", nbrColumns);
                    }
                }
                return $cell;
            },
            _getNumberOfLineSectionFields: function () {
                var section_fields_count = 0;
                var self = this;
                this.columns.forEach(function (elem) {
                    var options;

                    if (elem.attrs.name in self.state.fieldsInfo.list) {
                        options = self.state.fieldsInfo.list[elem.attrs.name].options;
                        if (options.show_in_line_section) section_fields_count++;
                    }
                });
                return section_fields_count;
            },
            _renderHeaderCell: function (node) {
                var $th = this._super.apply(this, arguments);
                var options;
                var show_in_line_section;

                if (!(node.attrs.name in this.state.fieldsInfo.list)) {
                    return $th;
                }
                options = this.state.fieldsInfo.list[node.attrs.name].options;
                show_in_line_section = options.show_in_line_section;
                if (show_in_line_section) $th.text("").removeClass("o_column_sortable");
                return $th;
            },
        };

        sectionAndNoteListRenderer.include(SectionAndNoteListRenderer);
    }
);
