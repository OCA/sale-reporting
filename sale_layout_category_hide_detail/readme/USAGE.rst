To use this module, you need to:

#. Go to *Sales -> Configuration -> Sales Orders -> Report Layout Categories*.
#. Create a new *Report Layout Category* with *Hide details* field on *True*
   and create another one with *Hide details* field on *False*.
#. Notice when you check *Hide details*, *Add subtotal* is hidden. There's no
   sense to not put subtotal when hiding details, so it doesn't matter if you
   check the *Add subtotal* or not.
#. Go to *Sales -> Orders -> Quotations* and create a new *Quotation*.
#. Add to the *Quotation* some lines associated with the first
   *Report Layout Category* created before and add other lines associated with
   the second *Report Layout Category* created.
#. Print this Quotation. In the PDF report the section with *Hide details*
   field on *True* will be shown without its lines and with the subtotal.
#. Go to the Quotation in the customer portal. The section with *Hide details*
   field on *True* will be shown without its lines and with the subtotal.

The behavior described before is the same for Quotations and Invoices.
