/* Copyright 2019 Tecnativa - Ernesto Tejeda
 * License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
 */
odoo.define('sale_layout_category_hide_detail.sale_layout_category_hide_detail', function (require) {
    "use strict";

    var fieldRegistry = require('web.field_registry');
    var section_and_note_one2many = fieldRegistry.get('section_and_note_one2many');

    var SectionAndNoteListRenderer = {
        _renderBodyCell: function (record, node, index, options) {
            var $cell = this._super.apply(this, arguments);

            var field_info = this.state.fieldsInfo.list[node.attrs.name];
            var show_in_line_section = field_info && field_info.options.show_in_line_section;

            var isSection = record.data.display_type === 'line_section';
            var isNote = record.data.display_type === 'line_note';
            if (isSection || isNote) {
                if (show_in_line_section) {
                    return $cell.removeClass('o_hidden');
                } else if (node.attrs.name === "name") {
                    var nbrColumns = this._getNumberOfCols();
                    if (this.handleField) {
                        nbrColumns--;
                    }
                    if (this.addTrashIcon) {
                        nbrColumns--;
                    }
                    nbrColumns -= this._getNumberOfLineSectionFields();
                    $cell.attr('colspan', nbrColumns);
                }
            }
            return $cell;
        },
        _getNumberOfLineSectionFields: function () {
            var section_fields_count = 0;
            var self = this;
            this.columns.forEach(function(elem) {
                var field_info = self.state.fieldsInfo.list[elem.attrs.name];
                if (field_info && field_info.options.show_in_line_section)
                    section_fields_count ++;
            });
            return section_fields_count;
        },
        _renderHeaderCell: function (node) {
            var $th = this._super.apply(this, arguments);
            var field_info = this.state.fieldsInfo.list[node.attrs.name];
            if (field_info && field_info.options.show_in_line_section)
                $th.text("").removeClass('o_column_sortable');
            return $th
        },
    };

    section_and_note_one2many.include({
        _getRenderer: function () {
            var result = this._super.apply(this, arguments);
            if (this.view.arch.tag === 'tree') {
                result.include(SectionAndNoteListRenderer)
            }
            return result
        },
    });
});
