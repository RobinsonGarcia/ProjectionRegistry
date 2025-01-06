# FORMULAS FOR THE SPHERE

The forward formulas for both Eckert IV and Eckert VI require iteration. 
Given \( R, \lambda_0, \phi, \) and \( \lambda \), to find \( x \) and \( y \) (see p. 368 for numerical examples):

## Eckert IV:

\[
x = \frac{2}{[\pi(4 + \pi)]^{1/2}} R (\lambda - \lambda_0)(1 + \cos \theta) \tag{32-1}
\]

\[
x = 0.4222382 \, R (\lambda - \lambda_0) (1 + \cos \theta) \tag{32-1a}
\]

\[
y = \frac{2}{[\pi/(4 + \pi)]^{1/2}} R \sin \theta \tag{32-2}
\]

\[
y = 1.3265004 \, R \sin \theta \tag{32-2a}
\]

where

\[
\theta + \sin \theta \cos \theta + 2 \sin \theta = \left(2 + \frac{\pi}{2}\right) \sin \phi \tag{32-3}
\]

The \( X \) axis coincides with the Equator, \( x \) increasing easterly, and the \( Y \) axis 
coincides with the central meridian, \( y \) increasing northerly. Angle \( \theta \) is a parametric angle, 
not a polar coordinate. Equation (32-3) may be solved with rapid convergence 
(but slow at the poles) using a Newton-Raphson iteration consisting of the following instead of (32-3):

\[
\Delta\theta = - \frac{\left[\theta + \sin\theta\cos\theta + 2\sin\theta - \left(2 + \frac{\pi}{2}\right)\sin\phi\right]}{[2\cos\theta(1+\cos\theta)]} \tag{32-4}
\]

With \((\phi/2)\) as the first trial \(\theta\), \(\Delta\theta\) is calculated from (32-4). This value is added to the preceding \(\theta\) to obtain the next trial \(\theta\), and the calculation is repeated with (32-4) until \(\Delta\theta\) is less than a predetermined convergence value. Note that all these formulas are in terms of radians.

## Eckert VI:

\[
x = R (\lambda - \lambda_0) \frac{(1 + \cos\theta)}{(2 + \pi)^{1/2}} \tag{32-5}
\]

\[
y = \frac{2R\theta}{(2 + \pi)^{1/2}} \tag{32-6}
\]

where

\[
\theta + \sin\theta = \left(1 + \frac{\pi}{2}\right)\sin\phi \tag{32-7}
\]

Axes are as described above for Eckert IV; \(\theta\) is parametric, but not the same as \(\theta\) for Eckert IV. Equation (32-7) may be replaced with the following Newton-Raphson iteration, treated in the same manner as equation (32-4) for Eckert IV, but with \(\phi\) as the first trial \(\theta\):

\[
\Delta\theta = - \frac{\left[\theta + \sin\theta - \left(1 + \frac{\pi}{2}\right)\sin\phi\right]}{(1 + \cos\theta)} \tag{32-8}
\]



For the *inverse* formulas, given \( R, \lambda_0, x, \) and \( y \), to find \( \phi \) and \( \lambda \), no iteration is required (see p. 368 for numerical examples):

## Eckert IV:

\[
\theta = \arcsin\left[y \frac{(4 + \pi)^{1/2}}{(2\pi^{1/2}R)}\right] \tag{32-9}
\]

\[
\theta = \arcsin\left[\frac{y}{1.3265004R}\right] \tag{32-9a}
\]

\[
\phi = \arcsin\left[\frac{\theta + \sin\theta \cos\theta + 2 \sin\theta}{\left(2 + \frac{\pi}{2}\right)}\right] \tag{32-10}
\]

\[
\lambda = \lambda_0 + \frac{[\pi(4 + \pi)]^{1/2}x}{[2R(1 + \cos\theta)]} \tag{32-11}
\]

\[
\lambda = \lambda_0 + \frac{x}{[0.4222382R(1 + \cos\theta)]} \tag{32-11a}
\]

## Eckert VI:

\[
\theta = \frac{(2 + \pi)^{1/2}y}{2R} \tag{32-12}
\]

\[
\phi = \arcsin\left[\frac{\theta + \sin\theta}{(1 + \frac{\pi}{2})}\right] \tag{32-13}
\]

\[
\lambda = \lambda_0 + \frac{(2 + \pi)^{1/2}x}{[R(1 + \cos\theta)]} \tag{32-14}
\]

Table 43 lists the rectangular coordinates of the 90th meridian for a sphere of radius \([(4 + \pi)^{1/2}/(2\pi^{1/2})]\) for Eckert IV and radius \([(2 + \pi)^{1/2}/\pi^{1/2}]\) for Eckert VI, to make maximum values equal to 1.0. The \( x \) coordinates for other meridians are proportional, and \( y \) coordinates are constant for a given latitude.