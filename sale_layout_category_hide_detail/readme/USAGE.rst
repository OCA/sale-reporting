To use this module, you need to:

#. Go to *Sales -> Orders -> Quotations* and create a new *Quotation*.
#. In *Order lines* tab add a section line.
#. Add some product lines.
#. Add another section line, but this time, click on the *plus-circle*
   icon |plus-circle-icon| on your right. That icon will be replaced by
   *minus-circle* icon |minus-circle-icon|. That mean *Show subtotal* field is
   set to False.
#. Add some product lines.
#. Add another section line and click on the *eye* icon |eye-icon| on your
   right. That icon will be replaced by *eye-slash* icon |eye-slash-icon|.
   That mean *Show details* field is set to False.
#. Add some product lines.
#. Print a *Quotation / Order* report for this quotation.

After following the steps described above, in the report you will see the
following:

  * The first 'line section' and its product order lines will be shown in
    a normal way.
  * The second 'line section' and its product order lines will be shown in
    a normal way, but the subtotal won't be shown. That is because in this
    section line *Show subtotal* field was set to False.
  * The third 'line section' will show the name on the left and the
    subtotal on the right. Besides, its product order lines won't be shown.
    That is because in this line *Show details* field was set to False.

The behavior described before is the same for Quotations and Invoices.

.. |eye-icon| image:: sale_layout_category_hide_detail/static/description/readme-icons/eye.png
   :alt: plus-circle icon
   :width: 12 px

.. |eye-slash-icon| image:: sale_layout_category_hide_detail/static/description/readme-icons/eye-slash.png
   :alt: minus-circle icon
   :width: 12 px

.. |plus-circle-icon| image:: sale_layout_category_hide_detail/static/description/readme-icons/plus-circle.png
   :alt: plus-circle icon
   :width: 12 px

.. |minus-circle-icon| image:: sale_layout_category_hide_detail/static/description/readme-icons/minus-circle.png
   :alt: minus-circle icon
   :width: 12 px
