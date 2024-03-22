To use this module, you need to:

1.  Go to *Sales -\> Orders -\> Quotations* and create a new
    *Quotation*.
2.  In *Order lines* tab add a section line.
3.  Add some product lines.
4.  Add another section line, but this time, click on the *plus-circle*
    icon
    ![plus-circle icon](../static/description/readme-icons/plus-circle.png)
    on your right. That icon will be replaced by *minus-circle* icon
    ![minus-circle icon](../static/description/readme-icons/minus-circle.png).
    That mean *Show subtotal* field is set to False.
5.  Add some product lines.
6.  Add another section line and click on the *eye* icon
    ![plus-circle icon](../static/description/readme-icons/eye.png) on
    your right. That icon will be replaced by *eye-slash* icon
    ![minus-circle icon](../static/description/readme-icons/eye-slash.png).
    That mean *Show details* field is set to False.
7.  Add some product lines.
8.  Print a *Quotation / Order* report for this quotation.

After following the steps described above, in the report you will see
the following:

> - The first 'line section' and its product order lines will be shown
>   in a normal way.
> - The second 'line section' and its product order lines will be shown
>   in a normal way, but the subtotal won't be shown. That is because in
>   this section line *Show subtotal* field was set to False.
> - The third 'line section' will show the name on the left and the
>   subtotal on the right. Besides, its product order lines won't be
>   shown. That is because in this line *Show details* field was set to
>   False.

The behavior described before is the same for Quotations and Invoices.
