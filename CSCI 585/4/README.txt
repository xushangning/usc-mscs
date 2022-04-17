# Answers

## Q1

The linear regression equation is

class =

     -0.1084 * CRIM +
      0.0458 * ZN +
      2.7187 * CHAS=1 +
    -17.376  * NOX +
      3.8016 * RM +
     -1.4927 * DIS +
      0.2996 * RAD +
     -0.0118 * TAX +
     -0.9465 * PTRATIO +
      0.0093 * B +
     -0.5226 * LSTAT +
     36.3411

There are only 11 terms in the equation, because Weka's linear regression by default performs feature selection with the M5 method. Setting attributeSelectionMethod to "No attribute selection" causes all 13 terms to appear in the equation. Another option eliminateColinearAttributes may also eliminate attributes in the final model but doesn't have effect in this case.

## Q2

The linear regression equation is

num_rings =

    -0.8249  * sex=l +
    0.0577   * sex=M +
    -0.4583  * length +
    11.0751  * diameter +
    10.7615  * height +
    8.9754   * whole_weight +
    -19.7869 * shucked_weight +
    -10.5818 * viscera +
    8.7418   * shell_weight +
    3.8946

## Q3

The linear regression equation is

num_rings =
    - 11.933 * length
    + 25.766 * diameter
    + 20.358 * height
    + 2.836
