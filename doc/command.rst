Running verbena
===============

For the full usage of VERBENA type ``verbena`` at the command line. A typical usage of VERBENA would be::

    verbena -i data.nii.gz -a aif.nii.gz -o output_directory -m mask.nii.gz

This would process the 4D DSC data in ``data.nii.gz`` using the AIFs supplied in ``aif.nii.gz`` 
and using the modified Vascular Model to estimate (relative) perfusion, commonly referred to as 
cerebral blood flow (``rCBF``), along with the mean transit time (``MTT``) and the transit time distribution 
parameter ``lambda``. 

Maps of these are placed in the output directory. Analysis is only performed within the
mask supplied (``mask.nii.gz``) which will normally have been derived from a brain extraction using 
BET or other equivalent tool.

AIFs
----

VERBENA takes as an input a 4D Nifti file containing the Arterial Input Functions (AIFs) this should 
have identical dimensions to the data and thus should have a single AIF time course for every single 
voxel (within the mask).

If the AIF is taken directly from the DSC data it will be in the form of a DSC signal. However if the
AIF has been preprocessed using some other tool, or a predefined 'population AIF' is being used, it may
take the form of a *concentration* time curve. In this case the option ``-aifconc`` should be given
to indicate this. Verbena will perform conversions between signal and concentration curves as required.

Often this will be a single global AIF replicated for every single voxel. 
However, VERBENA allows for different AIFs to be specified for individual brain regions should a 
local AIF be available. 

We do not currently include a tool for the selection or identification of 
the AIF. Often the AIF time course will be manually selected from the DSC data by the identification 
of a major artery, various automated methods have been developed in the literature and it may be 
possible to find tools that implement them online.

Acquisition parameters
----------------------

The ``-tr=TR`` option is used to specify the time resolution of the data in seconds, i.e. the time spacing 
between volumes. The ``-te=TE`` option specifies the assumed TE of tissue, used for conversion of 
concentration to signal

Macro vascular contamination
----------------------------

By adding the ``-mv`` option an additional component will be added to the model (based on the AIF) 
to account for macro vascular contamination contrast in large arteries, see Theory. When this 
option is included a further image will be produced in the output directory that maps the Arterial
Blood Volume (``rABV``) in relative units. 

By default the additional macro vascular component is added 
when the concentration time course of the voxel is calculated, optionally addition of the tissue 
and macro vascular component can be done as signal time courses using the ``-sigadd`` option.

'Model-Free' Analysis
---------------------

VERBENA takes a model-based approach to perfusion quantification. It is possible to use a more 
conventional Singular Value Decomposition deconvolution method by choosing the ``-modelfree`` 
option. 

This 'model-free' quantification can also be used to create initial estimates for the 
main model-based VERBENA analysis using the ``-modelfreeinit`` option, which may lead to more 
robust results in some cases.
