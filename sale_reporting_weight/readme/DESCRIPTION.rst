This module adds the measure "Weight" in the sales analysis view. This is
caught from 2 possible sources:

* If the UoM of the product is one of the category "Weight", the value is taken
  from the ordered quantity.
* If the UoM of the product is another, then the weight is taken from the
  weight field of the product multiply by the ordered quantity.
