from odoo import Command, fields

from odoo.addons.base.tests.common import BaseCommon


class TestCrmTeamInvoiced(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.journal = cls.env["account.journal"].create(
            {"name": "Journal Test", "code": "test", "type": "sale"}
        )
        cls.account = cls.env["account.account"].search(
            [("account_type", "=", "income"), ("company_ids", "=", cls.env.company.id)],
            limit=1,
        )
        cls.team = cls.env["crm.team"].create({"name": "Test Team"})
        cls.team2 = cls.env["crm.team"].create({"name": "Test Team 2"})
        cls.partner_id = cls.env["res.partner"].create({"name": "Test Partner"})

    def create_account_move(self, team_id, payment_state_code, amount):
        move = self.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "team_id": team_id.id,
                "date": fields.Date.context_today(self.env.user),
                "amount_untaxed_signed": amount,
                "partner_id": self.partner_id.id,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": "Test Line",
                            "quantity": 1,
                            "price_unit": amount,
                            "account_id": self.account.id,
                        }
                    )
                ],
            }
        )
        move.action_post()
        move.payment_state = payment_state_code
        return move

    def test_compute_invoiced_multiple_teams_with_all_payment_states(self):
        payment_states = ["not_paid", "in_payment", "paid", "partial", "reversed"]
        self.env.company.sales_team_invoiced_domain = str(
            [("payment_state", "in", payment_states)]
        )
        for state in payment_states:
            self.create_account_move(self.team, state, 100)
            self.create_account_move(self.team2, state, 50)
        (self.team + self.team2)._compute_invoiced()
        self.assertEqual(self.team.invoiced, 500.0)
        self.assertEqual(self.team2.invoiced, 250.0)

    def test_compute_invoiced_empty_domain(self):
        self.env.company.sales_team_invoiced_domain = "[]"
        self.create_account_move(self.team, "paid", 100)
        self.create_account_move(self.team2, "not_paid", 150)
        (self.team + self.team2)._compute_invoiced()
        self.assertEqual(self.team.invoiced, 100)
        self.assertEqual(self.team2.invoiced, 0)

    def test_compute_invoiced_invalid_domain(self):
        self.env.company.sales_team_invoiced_domain = "invalid domain"
        with self.assertRaises(SyntaxError):
            (self.team + self.team2)._compute_invoiced()
