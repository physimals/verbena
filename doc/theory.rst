Theory
======

The Vascular Model
------------------

The Vascular Model was originally proposed by Ostergaard et al [1]_. and was used for the analysis of DSC 
data (within a Bayesian like algorithm) by Mouridsen et al. 2006 [2]_. The basic principle follows all 
tracer kinetic studies and treats the concentration of contrast agent in the tissue as the convolution 
of an arterial input function (AIF) and a residue function. 

.. math::

    C(t) = CBF\int_0^t{C_a(\tau)R(t-\tau)d\tau}

Where :math:`C_a` is the arterial concentration as a function of time (AIF) which describes the 
supply of tracer by the blood and :math:`R(t)` is the *residue function* which describes the dissipation of the
tracer once it has arrived - for example how long a unit of contrast agent remains before it is removed to the venous 
vasculature. . :math:`CBF` is the cerebral blood flow which scales the concentration.

In the context of DSC-MRI the convolution model is applied to each voxel in turn and the 
residue function represents the residence of the agent within the tissue volume described by the voxel.
In the healthy brain the Gadolinium tracer that is used in DSC-MRI does not leave the vasculature and
thus the residue function encapsulates the transit of the contrast agent through the capillary bed. 
In fact the residue function is the integral of the distribution of transit times for blood passing 
through the voxel - a key parameter of which is the mean transit time (MTT), which is routinely used 
in DSC perfusion as a surrogate measure of perfusion (although it is often calculated without finding 
the transit distribution itself). 

The Vascular Model assumes that the transit time distribution can 
be modelled as series of parallel pathways of differing lengths that can be summered by a gamma
distribution of transit times. 

.. math::

    R(t) = \int_t^\infty{\frac{1}{\beta^\alpha\Gamma(\alpha)} t^{\alpha-1} e^{\frac{-t}{\alpha}}}

Here :math:`\alpha > 0` and :math:`\beta > 0` describe the shape and scale of the transport distribution.
:math:`\alpha\beta` is the mean of the distribution which can be identified as the mean transit time
(MTT) of the tracer.

In practice DSC measures the effect that this concentration of contrast agent has 
on the T2* of the voxel which is described by a non-linear transformation. 

.. math::

    S(t) = S_0e^{r_2C(t)TE}

Where :math:`S_0` is the baseline signal before the bolus arrives and :math:`r_2` is the T2 relaxivity 
of the contrast agent.

In VERBENA it is this final 
estimated signal that is compared to the data and used to find the optimal parameters using a Bayesian 
inference algorithm. Additionally the potential for a time delay between the supplied AIF (often 
measured at a remote location from the tissue) and the tissue signal is included in the model.

The Modified Vascular Model
---------------------------

VERBENA implements a modified version of the Vascular Model whereby the MTT is not pre-calculated 
from the data, but instead is a further parameter to be estimated as part of the inference applied 
to the data, see Chappell et al [3]_. This removes the risk of bias from the separate MTT calculation and 
also allows for a separate macro vascular component to be implemented within the model.

The other model parameter used by Verbena is named lambda and is identified with :math:`\alpha`.
in the residue function model. Hence in it's basic form the Verbena model contains three parameters: 
``CBF``, ``MTT`` and ``lambda``. An additional parameter ``delta`` can be used to model a delay in
the arrival of the arterial input.

Macro Vascular Contamination
----------------------------

VERBENA has the option to include a macro vascular component to the model. This combines the estimated 
concentration time curve from the (modified) vascular model with a scaled version of the AIF, where the 
AIF is representative of contrast that is still within the large arteries during imaging and the scaling 
is a (relative) measure of arterial blood volume. 

The component is subject to a 'shrinkage prior' that 
aims to provide a conservative estimate - so that this component is only included in voxels where the 
data supports its inclusion, recognising that macro vascular contamination will be be universally 
present within the brain, but only occur in voxels that contain large arteries. 

The combination of 
tissue and macro vascular contributions could be done in terms of the concentrations of contrast in the 
voxel. However, since in DSC it is the T2* effect of the concentration that is measured, the summation 
might be better done with the signals once their effect on T2* has been accounted for. VERBENA offers 
the option to do either, there is currently no clear evidence as to which is most physically accurate 
and it is likely that both are an incomplete representation of the reality, see Chappell et al [3]_.

The CPI model
-------------

The CPI model (Control Point Interpolation) is an alternative model for the residue function :math:`R(t)`.
Rather than base this function on physical assumptions, the CPI model simply defines a finite number
of 'control points' :math:`C_n` whose residue function values :math:`R(C_n)` are allowed to vary as 
model parameters. The full residue function is determined by fitting a natural spline curve to
these points with the constraint that :math:`R(0)` = 1 (no loss of contrast agent at time zero). 
In addition we expect :math:`R(t)` to be a decreasing function, hence the :math:`C_n` are modelled
by multiplicative factors each in the range :math:`[0, 1]` with :math:`R(C_{n+1}) = P_{n+1}R(C_n)`.

The CPI method allows great flexibility in the shape of the :math:`R(t)` however this is at the cost 
of larger numbers of model parameters.


References
----------

.. [1] *Ostergaard L, Chesler D, Weisskoff R, Sorensen A, Rosen B. Modeling Cerebral Blood Flow and Flow 
   Heterogeneity From Magnetic Resonance Residue Data. J Cereb Blood Flow Metab 1999;19:690–699.*

.. [2] *Mouridsen K, Friston K, Hjort N, Gyldensted L, Østergaard L, Kiebel S. Bayesian estimation of 
   cerebral perfusion using a physiological model of microvasculature. NeuroImage 2006;33:570–579. 
   doi: 10.1016/j.neuroimage.2006.06.015*

.. [3] *Chappell, M.A., Mehndiratta, A., Calamante F., "Correcting for large vessel contamination in DSC 
   perfusion MRI by extension to a physiological model of the vasculature", e-print ahead of publication. 
   doi: 10.1002/mrm.25390*
