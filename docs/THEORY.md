# Theory reference

The equations implemented in `fluidmech`, module by module. All quantities are in SI units.

## Fluid properties — `properties`

| Property | Model |
|---|---|
| Water density | Tanaka et al. (2001): $\rho = 1000\left[1 - \frac{(T+288.9414)(T-3.9863)^2}{508929.2\,(T+68.12963)}\right]$ |
| Water viscosity | Vogel equation: $\mu = 2.414\times10^{-5}\cdot 10^{\,247.8/(T_K-140)}$ |
| Water vapour pressure | Antoine: $\log_{10} p_v[\text{mmHg}] = 8.07131 - \dfrac{1730.63}{233.426+T}$ |
| Water surface tension | IAPWS: $\sigma = 0.2358\,\tau^{1.256}(1-0.625\tau)$, $\tau = 1 - T_K/647.096$ |
| Air density | Ideal gas: $\rho = p/(R T_K)$, $R = 287.05$ J/(kg K) |
| Air viscosity | Sutherland: $\mu = \mu_0 \left(\frac{T}{T_0}\right)^{3/2}\frac{T_0+S}{T+S}$ |

## Hydrostatics — `hydrostatics`

$$p = p_0 + \rho g h, \qquad F = \rho g h_c A, \qquad y_{cp} = y_c + \frac{I_{xc}}{y_c A}$$

Buoyancy: $F_B = \rho g V_{displaced}$. Manometer: $\Delta p = (\rho_m - \rho_f) g h$.

## Bernoulli equation — `bernoulli`

$$\frac{p_1}{\rho g} + \frac{V_1^2}{2g} + z_1 = \frac{p_2}{\rho g} + \frac{V_2^2}{2g} + z_2$$

| Device | Equation |
|---|---|
| Torricelli | $V = \sqrt{2gh}$ |
| Pitot tube | $V = \sqrt{2\Delta p/\rho}$ |
| Venturi / orifice meter | $Q = C_d A_2\sqrt{\dfrac{2\Delta p}{\rho(1-\beta^4)}}$ |
| Tank draining | $t = \dfrac{2A_t}{C_d A_o\sqrt{2g}}\left(\sqrt{h_1}-\sqrt{h_2}\right)$ |

## Pipe flow — `pipe_flow`

Darcy–Weisbach and minor losses:

$$h_L = f\frac{L}{D}\frac{V^2}{2g} + \sum K \frac{V^2}{2g}$$

Friction factor: laminar $f = 64/Re$ for $Re < 2300$; turbulent from Colebrook (1939)

$$\frac{1}{\sqrt f} = -2\log_{10}\left(\frac{\varepsilon/D}{3.7} + \frac{2.51}{Re\sqrt f}\right)$$

or the explicit approximations of Swamee–Jain (1976) and Haaland (1983). Type 2 and Type 3
problems are solved by bracketed root finding on the Type 1 relation.

## Pipe networks — `networks`

For link flows $\mathbf Q$ and junction heads $\mathbf H$, the energy and continuity equations

$$h_i(Q_i) = H_{start} - H_{end}, \qquad \sum Q_{in} - \sum Q_{out} = q_{demand}$$

are solved simultaneously by Newton's method (global gradient algorithm, Todini & Pilati 1988):

$$\left(\mathbf A_{21}\mathbf D^{-1}\mathbf A_{12}\right)\Delta\mathbf H = \mathbf C - \mathbf A_{21}\mathbf D^{-1}\mathbf E,
\qquad \Delta\mathbf Q = -\mathbf D^{-1}\left(\mathbf E + \mathbf A_{12}\Delta\mathbf H\right)$$

where $\mathbf A_{12}$ is the link–node incidence matrix, $\mathbf D = \mathrm{diag}(dh/dQ)$,
$\mathbf E$ the energy residuals and $\mathbf C$ the continuity residuals. Pumps are links with
head loss $-H_{pump}(Q)$.

## Pumps — `pumps`

Pump curve $H = h_0 + h_1Q + h_2Q^2$, efficiency $\eta = e_0 + e_1Q + e_2Q^2$ (least-squares fits).

| Relation | Equation |
|---|---|
| Affinity laws (speed $N$) | $Q \propto N$, $H \propto N^2$, $P \propto N^3$ |
| Impeller trim (diameter $D$) | $Q \propto D$, $H \propto D^2$ |
| Shaft power | $P = \rho g Q H/\eta$ |
| NPSH available | $\mathrm{NPSH}_a = \dfrac{p_{atm}-p_v}{\rho g} + z_s - h_{L,s}$ |
| Specific speed | $\Omega_s = \omega Q^{1/2}/(gH)^{3/4}$ |

## Open channels — `open_channel`

| Relation | Equation |
|---|---|
| Manning (SI) | $Q = \dfrac1n A R^{2/3} S_0^{1/2}$ |
| Critical flow | $\dfrac{Q^2 T}{g A^3} = 1$ |
| Froude number | $Fr = V/\sqrt{g D_h}$, $D_h = A/T$ |
| Specific energy | $E = y + \dfrac{Q^2}{2gA^2}$ |
| Hydraulic jump | $\dfrac{y_2}{y_1} = \tfrac12\left(\sqrt{1+8Fr_1^2}-1\right)$, $\Delta E = \dfrac{(y_2-y_1)^3}{4y_1y_2}$ |
| Gradually varied flow (direct step) | $\Delta x = \dfrac{E_2-E_1}{S_0-\bar S_f}$, $S_f = \dfrac{n^2V^2}{R^{4/3}}$ |
| Sharp-crested weir | $Q = C_d\,\tfrac23\sqrt{2g}\,L H^{3/2}$ |
| V-notch weir | $Q = C_d\,\tfrac{8}{15}\sqrt{2g}\tan\tfrac\theta2\, H^{5/2}$ |
| Broad-crested weir | $Q = C_d\, b\sqrt g\,(2H/3)^{3/2}$ |
| Sluice gate | $Q = C_d\, b\, a\sqrt{2 g y_1}$ |

## Compressible flow — `compressible`

$$\frac{T_0}{T} = 1 + \frac{k-1}{2}M^2, \qquad \frac{p_0}{p} = \left(\frac{T_0}{T}\right)^{\frac{k}{k-1}}, \qquad
\frac{A}{A^*} = \frac1M\left[\frac{2}{k+1}\left(1+\frac{k-1}{2}M^2\right)\right]^{\frac{k+1}{2(k-1)}}$$

Normal shock (Rankine–Hugoniot):

$$M_2^2 = \frac{1 + \frac{k-1}{2}M_1^2}{kM_1^2 - \frac{k-1}{2}}, \qquad
\frac{p_2}{p_1} = 1 + \frac{2k}{k+1}\left(M_1^2-1\right), \qquad
\frac{\rho_2}{\rho_1} = \frac{(k+1)M_1^2}{(k-1)M_1^2+2}$$

Choked mass flow: $\dot m = A^* p_0 \sqrt{\dfrac{k}{R T_0}}\left(\dfrac{2}{k+1}\right)^{\frac{k+1}{2(k-1)}}$

## External flow — `drag`

| Relation | Equation |
|---|---|
| Drag force | $F_D = C_D\,\tfrac12\rho V^2 A$ |
| Sphere (Brown & Lawler 2003) | $C_D = \dfrac{24}{Re}\left(1+0.150\,Re^{0.681}\right) + \dfrac{0.407}{1+8710/Re}$ |
| Cylinder (White) | $C_D = 1 + 10\,Re^{-2/3}$ |
| Flat plate, laminar (Blasius) | $C_f = 1.328/\sqrt{Re_L}$, $\delta = 4.91x/\sqrt{Re_x}$ |
| Flat plate, turbulent | $C_f = 0.074/Re_L^{1/5}$, $\delta = 0.37x/Re_x^{1/5}$ |
| Prandtl–Schlichting | $C_f = 0.455/(\log_{10}Re_L)^{2.58}$ (minus $1700/Re_L$ for a laminar leading edge) |

## Water hammer — `transients`

$$c = \sqrt{\frac{K/\rho}{1 + \frac{K D}{E e}}}, \qquad \Delta p = \rho c \Delta V \ (t_c \le 2L/c),
\qquad \Delta p \approx \frac{2\rho L V}{t_c} \ (t_c > 2L/c)$$


## Rheology — `rheology`

| Model | Constitutive equation |
|---|---|
| Newtonian | $\tau = \mu\dot\gamma$ |
| Power law | $\tau = K\dot\gamma^n$, apparent viscosity $\mu_{app} = K\dot\gamma^{n-1}$ |
| Bingham plastic | $\tau = \tau_y + \mu_p\dot\gamma$ for $\tau > \tau_y$ |
| Herschel–Bulkley | $\tau = \tau_y + K\dot\gamma^n$ |
| Carreau | $\mu = \mu_\infty + (\mu_0-\mu_\infty)\left[1+(\lambda\dot\gamma)^2\right]^{(n-1)/2}$ |
| Andrade (liquids) | $\mu = A\,e^{B/T}$ |

## Hydrostatics in rigid-body motion — `hydrostatics`

Linear acceleration: free-surface slope $dz/dx = -a_x/(g+a_z)$. Rotation: $z = z_0 + \omega^2 r^2/(2g)$,
with the centre falling and the wall rising by $\omega^2R^2/(4g)$ each (volume conservation).

## Exact viscous solutions — `laminar`

With $G = -dp/dx$:

| Flow | Velocity | Flow rate |
|---|---|---|
| Couette–Poiseuille (gap $h$) | $u = \dfrac{Uy}{h} + \dfrac{G}{2\mu}y(h-y)$ | $q = \dfrac{Uh}{2} + \dfrac{Gh^3}{12\mu}$ |
| Hagen–Poiseuille | $u = \dfrac{G}{4\mu}(R^2-r^2)$ | $Q = \dfrac{\pi G R^4}{8\mu}$ |
| Annulus ($\kappa = R_i/R$) | $u = \dfrac{GR^2}{4\mu}\left[1-\dfrac{r^2}{R^2}+\dfrac{1-\kappa^2}{\ln(1/\kappa)}\ln\dfrac rR\right]$ | $Q = \dfrac{\pi GR^4}{8\mu}\left[1-\kappa^4-\dfrac{(1-\kappa^2)^2}{\ln(1/\kappa)}\right]$ |
| Falling film | $u = \dfrac{\rho g\sin\beta}{\mu}\left(\delta y - \dfrac{y^2}{2}\right)$ | $\delta = \left(\dfrac{3\mu\Gamma}{\rho^2 g\sin\beta}\right)^{1/3}$ |
| Power-law pipe | $u = \dfrac{n}{n+1}\left(\dfrac{G}{2K}\right)^{1/n}\left(R^{\frac{n+1}{n}} - r^{\frac{n+1}{n}}\right)$ | $Q = \dfrac{\pi n}{3n+1}\left(\dfrac{G}{2K}\right)^{1/n}R^{\frac{3n+1}{n}}$ |
| Bingham pipe (Buckingham–Reiner) | plug for $r < 2\tau_y/G$ | $Q = \dfrac{\pi R^4G}{8\mu_p}\left[1-\tfrac43\phi+\tfrac13\phi^4\right]$, $\phi = \tau_y/\tau_w$ |
| Stokes' first problem | $u = U\,\mathrm{erfc}\left(\dfrac{y}{2\sqrt{\nu t}}\right)$ | |
| Stokes' second problem | $u = Ue^{-ky}\cos(\omega t - ky)$, $k = \sqrt{\omega/2\nu}$ | |

Laminar $f\,Re$ for rectangular ducts: Shah & London (1978) polynomial; for annuli the exact result above.

## Potential flow — `potential_flow`

Uniform stream $\psi = Uy$; source $\psi = \dfrac{m}{2\pi}\theta$; vortex $\psi = -\dfrac{\Gamma}{2\pi}\ln r$;
doublet $\psi = -\dfrac{\kappa}{2\pi}\dfrac{\sin\theta}{r}$. Pressure from Bernoulli, $C_p = 1-(V/U)^2$.
Lift per unit span $L' = \rho U\Gamma$ (Kutta–Joukowski); drag zero (d'Alembert).

## Turbulent wall flows — `turbulence`

$u^+ = u/u_\tau$, $y^+ = yu_\tau/\nu$, $u_\tau = \sqrt{\tau_w/\rho}$. Log law $u^+ = \frac{1}{0.41}\ln y^+ + 5.0$;
Spalding's inner-layer formula
$y^+ = u^+ + e^{-\kappa B}\left[e^{\kappa u^+} - 1 - \kappa u^+ - \frac{(\kappa u^+)^2}{2} - \frac{(\kappa u^+)^3}{6}\right]$.
Entrance length $L_e/D = 0.06\,Re$ (laminar), $4.4\,Re^{1/6}$ (turbulent). Kolmogorov scales
$\eta = (\nu^3/\varepsilon)^{1/4}$, $\tau_\eta = (\nu/\varepsilon)^{1/2}$.

## Porous media — `porous`

| Relation | Equation |
|---|---|
| Darcy's law | $u = \dfrac{k}{\mu}\dfrac{\Delta p}{L}$ |
| Kozeny–Carman | $\dfrac{\Delta p}{L} = \dfrac{180\,\mu u(1-\varepsilon)^2}{\varepsilon^3(\phi_s d_p)^2}$ |
| Ergun | $\dfrac{\Delta p}{L} = \dfrac{150\,\mu u(1-\varepsilon)^2}{\varepsilon^3(\phi_s d_p)^2} + \dfrac{1.75\,\rho u^2(1-\varepsilon)}{\varepsilon^3\phi_s d_p}$ |
| Minimum fluidisation | Ergun = $(1-\varepsilon_{mf})(\rho_p-\rho)g$; or Wen & Yu $Re_{mf} = \sqrt{33.7^2 + 0.0408\,Ar} - 33.7$ |
| Cake filtration (Ruth) | $\dfrac tV = \dfrac{\mu\alpha c}{2A^2\Delta p}V + \dfrac{\mu R_m}{A\Delta p}$ |
| Membranes | $J = \dfrac{\Delta p - \Delta\pi}{\mu(R_m + R_f)}$, $\pi = iCRT$ |

## Dimensional analysis — `dimensional`

For $n$ variables whose dimensional matrix has rank $r$, there are $n-r$ independent groups. For each
non-repeating variable $q$ the exponents $\mathbf a$ of the repeating variables solve
$\mathbf D_{rep}\,\mathbf a = -\mathbf d_q$ exactly in rational arithmetic.

## Mixing — `mixing`

Power $P = N_p\rho N^3D^5$, $N_p \approx K_p/Re + N_{p,turb}$, $Re = \rho ND^2/\mu$. Blend time
$N\theta_{95} = 5.20\,N_p^{-1/3}(T/D)^2$ (Grenville). Engulfment rate $E = 0.058(\varepsilon/\nu)^{1/2}$.
First-order conversions: CSTR $X = \dfrac{k\tau}{1+k\tau}$, PFR $X = 1-e^{-k\tau}$, $N$ tanks
$X = 1-(1+k\tau/N)^{-N}$, laminar tube with $E(t) = \dfrac{\tau^2}{2t^3}$ ($t \ge \tau/2$).

## Drops, bubbles and suspensions — `drag`

Hadamard–Rybczynski $U = U_{Stokes}\dfrac{3(1+\kappa)}{2+3\kappa}$; Mendelson $U = \sqrt{\dfrac{2\sigma}{\rho d} + \dfrac{gd}{2}}$;
Richardson–Zaki $U = U_t\varepsilon^n$ with Rowe's $n = \dfrac{4.7+0.41Re^{0.75}}{1+0.175Re^{0.75}}$.

## Advanced topics

**Blasius boundary layer** (`laminar.blasius`): with $\eta = y\sqrt{U/\nu x}$ and $u/U = f'(\eta)$,
$f''' + \tfrac12 f f'' = 0$, $f(0) = f'(0) = 0$, $f'(\infty) = 1$; solved by shooting on $f''(0)$
with RK4. Results: $f''(0) = 0.33206$, $\delta_{99} = 4.91\,x/\sqrt{Re_x}$.

**Method of characteristics** (`transients.moc_valve_closure`): with $B = c/(gA)$ and $R = f\Delta x/(2gDA^2)$,
along $dx/dt = \pm c$
$$H_P = C_P - B Q_P,\quad C_P = H_A + BQ_A - RQ_A|Q_A|;\qquad H_P = C_M + BQ_P,\quad C_M = H_B - BQ_B + RQ_B|Q_B|.$$
Valve: $Q_P = -BC_v + \sqrt{(BC_v)^2 + 2C_vC_P}$, $C_v = (\tau Q_0)^2 / (2H_0)$ (Wylie & Streeter; Chaudhry).

**Rayleigh–Plesset equation** (`cavitation`):
$$R\ddot R + \tfrac32\dot R^2 = \frac{1}{\rho}\left[p_v + p_{g0}\left(\frac{R_0}{R}\right)^{3\kappa} - \frac{2\sigma}{R} - \frac{4\mu\dot R}{R} - p_\infty\right],$$
empty-cavity collapse time $t_c = 0.9147\,R_0\sqrt{\rho/\Delta p}$ (Rayleigh 1917).

**Lid-driven cavity** (`cfd.lid_driven_cavity`): $\omega_t + u\omega_x + v\omega_y = Re^{-1}\nabla^2\omega$,
$\nabla^2\psi = -\omega$, $u = \psi_y$, $v = -\psi_x$; central differences, explicit time stepping,
sparse direct Poisson solve, Thom's wall vorticity $\omega_w = -2\psi_1/h^2 - 2U_w/h$.

**Lattice Boltzmann** (`cfd.lbm_cylinder`): D2Q9 lattice, BGK collision
$f_k \leftarrow f_k - (f_k - f_k^{eq})/\tau$, $\nu = (\tau - \tfrac12)/3$ in lattice units,
$f_k^{eq} = w_k\rho\,[1 + 3\mathbf c_k\cdot\mathbf u + \tfrac92(\mathbf c_k\cdot\mathbf u)^2 - \tfrac32 u^2]$,
bounce-back on the cylinder.

**Taylor dispersion** (`cfd.taylor_dispersion`): particles advected by $u = 2\bar U(1 - r^2/a^2)$ with
Brownian steps of variance $2D\,\Delta t$; theory $D_{eff} = D(1 + Pe^2/48)$, $Pe = \bar U a / D$
(Taylor 1953; Aris 1956).

## References

- Baldyga, J. & Bourne, J. R. (1999). *Turbulent Mixing and Chemical Reactions*. Wiley.
- Bird, R. B., Stewart, W. E. & Lightfoot, E. N. *Transport Phenomena*. Wiley.
- Aris, R. (1956). On the dispersion of a solute in a fluid flowing through a tube. *Proc. R. Soc. A* 235.
- Brown, P. P. & Lawler, D. F. (2003). Sphere drag and settling velocity revisited. *J. Environ. Eng.* 129(3).
- Çengel, Y. A. & Cimbala, J. M. *Fluid Mechanics: Fundamentals and Applications*. McGraw-Hill.
- Chow, V. T. (1959). *Open-Channel Hydraulics*. McGraw-Hill.
- Colebrook, C. F. (1939). Turbulent flow in pipes. *J. Inst. Civil Eng.* 11.
- Ergun, S. (1952). Fluid flow through packed columns. *Chem. Eng. Prog.* 48.
- Grenville, R. K. (1992). Blending of viscous Newtonian and pseudo-plastic fluids. PhD thesis, Cranfield.
- Ghia, U., Ghia, K. N. & Shin, C. T. (1982). High-Re solutions for incompressible flow using the Navier-Stokes equations and a multigrid method. *J. Comput. Phys.* 48.
- Haaland, S. E. (1983). Simple and explicit formulas for the friction factor. *J. Fluids Eng.* 105.
- McCabe, W. L., Smith, J. C. & Harriott, P. *Unit Operations of Chemical Engineering*. McGraw-Hill.
- NACA Report 1135 (1953). Equations, tables and charts for compressible flow.
- Rayleigh, Lord (1917). On the pressure developed in a liquid during the collapse of a spherical cavity. *Phil. Mag.* 34.
- Shah, R. K. & London, A. L. (1978). *Laminar Flow Forced Convection in Ducts*. Academic Press.
- Succi, S. (2001). *The Lattice Boltzmann Equation for Fluid Dynamics and Beyond*. Oxford University Press.
- Swamee, P. K. & Jain, A. K. (1976). Explicit equations for pipe-flow problems. *J. Hydraul. Div.* 102.
- Taylor, G. I. (1953). Dispersion of soluble matter in solvent flowing slowly through a tube. *Proc. R. Soc. A* 219.
- Todini, E. & Pilati, S. (1988). A gradient algorithm for the analysis of pipe networks.
- White, F. M. *Fluid Mechanics*. McGraw-Hill.
- Williamson, C. H. K. (1996). Vortex dynamics in the cylinder wake. *Annu. Rev. Fluid Mech.* 28.
- Wen, C. Y. & Yu, Y. H. (1966). A generalized method for predicting the minimum fluidization velocity. *AIChE J.* 12.
- Wylie, E. B. & Streeter, V. L. (1993). *Fluid Transients in Systems*. Prentice Hall.
