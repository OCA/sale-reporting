# Copyright 2023 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

from odoo import fields, models


class DisplayLineMixin(models.AbstractModel):
    _name = "display.line.mixin"
    _description = """This model intends to ease the propagation and generation
of sections and notes to any model in relation with a sale order line"""
    _order = "sequence ASC, id ASC"

    sequence = fields.Integer()
    previous_line_id = fields.Many2one("sale.order.line")
    next_line_id = fields.Many2one("sale.order.line")
    display_type = fields.Char(store=False)

    def get_section_or_note_class(self):
        """Return the class names depending of the display type

        Classes come from sale sections scss configuration
        """
        if self.is_section():
            return "bg-200 font-weight-bold o_line_section"
        elif self.is_note():
            return "font-italic o_line_note"
        return ""

    def is_section(self):
        """Quick method helper"""
        self.ensure_one()
        return self.display_type == "line_section"

    def is_note(self):
        """Quick method helper"""
        self.ensure_one()
        return self.display_type == "line_note"

    def is_section_or_note(self):
        """Quick method helper"""
        self.ensure_one()
        return self.is_section() or self.is_note()

    def has_section(self):
        """Quick method helper"""
        return bool(self.get_section())

    def has_note(self):
        """Quick method helper"""
        return bool(self.get_note())

    def get_section(self):
        """Returns the section of the current line"""
        if not self.is_section():
            previous_record = self.previous_line_id
            while previous_record:
                if previous_record.is_section():
                    return previous_record
                previous_record = previous_record.previous_line_id

    def get_note(self):
        """Return the note positioned after an order line even if a section"""
        if not self.is_note():
            if self.next_line_id.is_note():
                return self.next_line_id

    def get_section_subtotal(self, fields=None):
        """Return the sum of each individual provided fields
        :param fields: a list of fields to sum
        :returns: a dict as {field: sum values}
        """
        self.ensure_one()
        if self.is_section():
            if not fields:
                fields = []
            return {
                field: sum(self._get_section_lines(with_notes=False).mapped(field))
                for field in fields
            }

    def _get_section_lines(self, with_notes=True):
        """Get all order lines in a section.
        :param with_notes: Include note lines
        """
        self.ensure_one()
        if self.is_section():
            result = self.env[self._name]
            next_record = self.next_line_id
            while next_record:
                if next_record.is_section():
                    break
                result |= next_record
                next_record = next_record.next_line_id
            notes = result.filtered(lambda r: r.is_note())
            return result if with_notes else result - notes

    def prepare_section_or_note_values(self, order_line):
        """This method is intended to be used to `convert` a display line to
        the current model

        It is mainly used for display lines injection to delivery reports

        :param order_line: a sale.order.line record
        """
        self.ensure_one()
        raise NotImplementedError

    def inject_sections_and_notes(self):
        """This method inject all related display lines to the right position
        for the inheriting model

        See sale.order::compute_order_lines_dependency for further explanations
        """
        model_name = self._name

        def add_section_or_note(record, display_line):
            values = record.prepare_section_or_note_values(display_line)
            return self.new(values)

        result = self.env[model_name]
        # Avoid repeating display lines over hierarchy
        done_record = self.env["sale.order.line"]
        total_records = len(self)
        for index, record in enumerate(self.sorted("sequence")):

            # We parse all previous lines to retrieve every section or notes
            previous_lines = self.env[model_name]
            previous_record = record.previous_line_id
            while previous_record:
                if previous_record in done_record:
                    break
                elif previous_record.is_section_or_note():
                    previous_lines |= add_section_or_note(record, previous_record)
                done_record |= previous_record
                previous_record = previous_record.previous_line_id
            # As we parsed backwards, we need to sort back the lines ^^
            if previous_lines:
                result |= previous_lines.sorted("sequence")

            # Then of course we add our current line
            result |= record

            # Manage last lines if sections or notes
            if (index + 1) >= total_records and record.next_line_id:
                next_record = record.next_line_id
                while next_record:
                    if next_record in done_record:
                        break
                    elif next_record.is_section_or_note():
                        result |= add_section_or_note(record, next_record)
                    done_record |= next_record
                    next_record = next_record.next_line_id

        return result
