Whenever the taxes are in the same group for the whole order the column won't be
displayed.

The module performs the following validation:
    - It checks that all order lines have the same tax group.
    - It does not validate if the taxes within the same line are different.

**Result:**
    - If all tax groups are the same, the Taxes column is hidden in the printed or sent quotation.
    - If at least one line has a different tax group, the Taxes column is displayed as usual.