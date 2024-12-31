## Formulas for the Sphere (Gnomonic Projection)

A point at a given angular distance from the chosen center point on the sphere is plotted on the Gnomonic projection at a distance from the center proportional to the trigonometric tangent of that angular distance, and at its true azimuth. Symbolically:

$$
\rho = R \,\tan c 
\quad (22\text{-}1)
$$

$$
\theta = \pi \;-\; Az \;=\; 180^\circ \;-\; Az 
\quad (20\text{-}2)
$$

$$
h' = \frac{1}{\cos^2 c}
\quad (22\text{-}2)
$$

$$
k' = \frac{1}{\cos c}
\quad (22\text{-}3)
$$

where \(c\) is the angular distance of the given point from the center of projection, and \(Az\) is the azimuth measured east of north (whereas \(\theta\) is often treated as the polar coordinate measured east of south). The term \(k'\) is the scale factor in a direction perpendicular to the radius from the center of the map (not along a parallel except in the polar aspect). The scale factor \(h'\) is measured along the radius.

Combining these definitions with standard equations, the **rectangular coordinates** \((x,y)\) of the oblique Gnomonic projection can be expressed as follows. Given \(R\), \(\phi_1\), \(\lambda_0\), \(\phi\), and \(\lambda\), to find \(x\) and \(y\) (see p. 319 for numerical examples):

$$
x 
= R\,k' \,\cos \phi \,\sin\bigl(\lambda - \lambda_0\bigr)
\quad (22\text{-}4)
$$

$$
y 
= R\,k' 
  \Bigl[
    \cos \phi_1 \,\sin \phi
    \;-\;
    \sin \phi_1 \,\cos \phi \,\cos\bigl(\lambda - \lambda_0\bigr)
  \Bigr]
\quad (22\text{-}5)
$$

where \(k'\) is found from \((22\text{-}3)\) above. The **angular distance** \(c\) satisfies:

$$
\cos c
= \sin \phi_1 \,\sin \phi 
  + \cos \phi_1 \,\cos \phi \,\cos\bigl(\lambda - \lambda_0\bigr)
\quad (5\text{-}3)
$$

Here, \((\phi_1, \lambda_0)\) are the latitude and longitude of the projection center. By convention, the \(y\)-axis coincides with the central meridian \(\lambda_0\) (positive northward), and the meridians are arranged accordingly.


## Gnomonic Projection Variations

### North Polar Gnomonic
Let \(\phi_1 = 90^\circ\). Then the **north polar** gnomonic equations become:

$$
x = R \,\cot \phi \,\sin\bigl(\lambda - \lambda_0\bigr)
\quad (22\text{-}6)
$$

$$
y = -\,R \,\cot \phi \,\cos\bigl(\lambda - \lambda_0\bigr)
\quad (22\text{-}7)
$$

In **polar coordinates** (centered at \(\phi_1 = 90^\circ\)):

$$
\rho = R \,\cot \phi
\quad (22\text{-}8)
$$

$$
\theta = \lambda - \lambda_0
\quad (22\text{-}9)
$$

---

### South Polar Gnomonic
Let \(\phi_1 = -\,90^\circ\). The **south polar** gnomonic equations become:

$$
x = -\,R \,\cot \phi \,\sin\bigl(\lambda - \lambda_0\bigr)
\quad (22\text{-}10)
$$

$$
y = R \,\cot \phi \,\cos\bigl(\lambda - \lambda_0\bigr)
\quad (22\text{-}11)
$$

In **polar coordinates** (centered at \(\phi_1 = -\,90^\circ\)):

$$
\rho = -\,R \,\cot \phi
\quad (22\text{-}12)
$$

$$
\theta = \pi - \lambda + \lambda_0
\quad (22\text{-}13)
$$

---

### Equatorial Gnomonic
Let \(\phi_1 = 0^\circ\). The **equatorial** gnomonic equations become:

$$
x = R \,\tan \phi \,\sin\bigl(\lambda - \lambda_0\bigr)
\quad (22\text{-}14)
$$

$$
y = R \,\tan \phi \,\cos\bigl(\lambda - \lambda_0\bigr)
\quad (22\text{-}15)
$$

---

### Automatically Computing a General Gnomonic Map
In practice, to ensure the projection remains valid, one checks \(\cos c\) from equation \((5\text{-}3)\):

$$
\cos c 
= \sin \phi_1 \,\sin \phi 
  + \cos \phi_1 \,\cos \phi \,\cos\bigl(\lambda - \lambda_0\bigr).
$$

- If \(\cos c \le 0\), the point is generally **rejected** (it lies beyond 90° from the center).  
- If \(\cos c > 0\), the point **may** be plotted, depending on desired map limits.

---

## Inverse Formulas for the Sphere
To find \(\phi\) and \(\lambda\) from given \(R\), \(\phi_1\), \(\lambda_0\), \(x\), and \(y\), use:

1. **Distance** \(\rho\) in the plane (equations \((20\text{-}14)\) and \((20\text{-}15)\) context):

   $$
   \rho = \sqrt{x^2 + y^2}
   \quad (20\text{-}18)
   $$

2. **Central angle** \(c\) on the sphere:

   $$
   c = \arctan\!\bigl(\tfrac{\rho}{R}\bigr)
   \quad (22\text{-}16)
   $$

3. **Latitude** \(\phi\):

   $$
   \phi 
   = \arcsin\!\Bigl[
       \cos c \,\sin \phi_1 
       \;+\;
       \bigl(\tfrac{y}{\rho}\bigr)\,\sin c \,\cos \phi_1
     \Bigr]
   \quad (20\text{-}14)
   $$

4. **Longitude** \(\lambda\), depending on \(\phi_1\):
   - If \(\phi_1\) is not \(\pm 90^\circ\):
     $$
     \lambda
     = \lambda_0 
       \;+\;
       \arctan\!\Bigl[
         \frac{x \,\sin c}
              {\rho \,\cos \phi_1 \,\cos c \;-\; y \,\sin \phi_1 \,\sin c}
       \Bigr]
     \quad (20\text{-}15)
     $$
   - If \(\phi_1 = 90^\circ\):
     $$
     \lambda
     = \lambda_0 \;+\;
       \arctan\!\Bigl[\tfrac{x}{-\,y}\Bigr]
     \quad (20\text{-}16)
     $$
   - If \(\phi_1 = -\,90^\circ\):
     $$
     \lambda
     = \lambda_0 \;+\;
       \arctan\!\Bigl[\tfrac{x}{y}\Bigr]
     \quad (20\text{-}17)
     $$

These relationships complete the **inverse formulas**, allowing conversion back from Cartesian \((x,y)\) on the gnomonic plane to spherical coordinates \((\phi,\lambda)\). 

*Note: The specific form of each \(\arctan\) function may be adjusted (for quadrant considerations) so that the resulting \(\lambda\) is placed in the correct range.*