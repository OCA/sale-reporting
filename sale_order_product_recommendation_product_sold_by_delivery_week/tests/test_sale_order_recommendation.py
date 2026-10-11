from odoo.tests import TransactionCase


class TestSaleOrderRecommendation(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.partner = cls.env["res.partner"].create({"name": "Test Partner"})
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
                "type": "consu",
            }
        )
        cls.service_product = cls.env["product.product"].create(
            {
                "name": "Test Service",
                "type": "service",
            }
        )
        cls.order = cls.env["sale.order"].create({"partner_id": cls.partner.id})

    def test_weekly_sold_delivered_shown_compute(self):
        wizard = self.env["sale.order.recommendation"].create(
            {"order_id": self.order.id}
        )
        # Create recommendation lines
        line1 = self.env["sale.order.recommendation.line"].create(
            {
                "wizard_id": wizard.id,
                "product_id": self.product.id,
            }
        )
        line2 = self.env["sale.order.recommendation.line"].create(
            {
                "wizard_id": wizard.id,
                "product_id": self.service_product.id,
            }
        )
        self.assertTrue(isinstance(line1.weekly_sold_delivered_shown, str))
        self.assertFalse(line2.weekly_sold_delivered_shown)
