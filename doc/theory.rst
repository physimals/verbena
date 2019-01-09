Theory
======

The Vascular Model
------------------

The Vascular Model was originally proposed by Ostergaard et al. and was used for the analysis of DSC 
data (within a Bayesian like algorithm) by Mouridsen et al. in 2006. The basic principle follows all 
tracer kinetic studies and treats the concentration of contrast agent in the tissue as the convolution 
of an arterial input function (AIF) and a residue function. The AIF describes the delivery of agent 
to the tissue region by in the blood, the residue function describes what happens to it once it has 
arrived - for example how long a unit of contrast agent remains before it is removed to the venous 
vasculature. 

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
distribution of transit times. This can be converted to the equivalent residue function by integration. 
Once this has been convolved with the residue function the concentration time curve in the tissue 
can be calculated. 

In practice DSC measures the effect that this concentration of contrast agent has 
on the T2* of the voxel which is described by a non-linear transformation. In VERBENA it is this final 
estimated signal that is compared to the data and used to find the optimal parameters using a Bayesian 
inference algorithm. Additionally the potential for a time delay between the supplied AIF (often 
measured at a remote location from the tissue) and the tissue signal is included in the model.

The Modified Vascular Model
---------------------------

VERBENA implements a modified version of the Vascular Model whereby the MTT is not pre-calcualted 
from the data, but instead is a further parameter to be estimated as part of the inference applied 
to the data, see Chappell et al.. This removes the risk of bias from the separate MTT calculation and 
also allows for a separate macro vascular component to be implemented within the model.

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
and it is likely that both are an incomplete representation of the reality, see Chappell et al.

References
----------

 - *Ostergaard L, Chesler D, Weisskoff R, Sorensen A, Rosen B. Modeling Cerebral Blood Flow and Flow 
   Heterogeneity From Magnetic Resonance Residue Data. J Cereb Blood Flow Metab 1999;19:690–699.*

 - *Mouridsen K, Friston K, Hjort N, Gyldensted L, Østergaard L, Kiebel S. Bayesian estimation of 
   cerebral perfusion using a physiological model of microvasculature. NeuroImage 2006;33:570–579. 
   doi: 10.1016/j.neuroimage.2006.06.015*

 - *Chappell, M.A., Mehndiratta, A., Calamante F., "Correcting for large vessel contamination in DSC 
   perfusion MRI by extension to a physiological model of the vasculature", e-print ahead of publication. 
   doi: 10.1002/mrm.25390*
