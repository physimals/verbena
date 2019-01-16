#!/usr/bin/env python
"""
Verbena: Perfusion quantification from DSC-MRI using the Vascular Model

Michael Chappell, QuBIc & FMRIB Image Analysis Group

Copyright (c) 2012-19 University of Oxford
"""

import sys
from optparse import OptionParser, OptionGroup

import numpy as np

from fsl.data.image import Image
import fsl.wrappers as fsl

from fabber import Fabber
from oxasl import Workspace
from oxasl.wrappers import fabber

from verbena._version import __version__

if __name__ == "__main__":
    main()

def main():
    """
    Command line tool entry point
    """
    parser = OptionParser(usage="verbena -i <DSC input file> [options...]", version=__version__)
    parser.add_option("--data", "-i", help="DSC input file")
    parser.add_option("--aif", "-a", help="Voxelwise AIF image file")
    parser.add_option("--output", "-o", help="Output directory")
    parser.add_option("--mask", "-m", help="Mask image")
    parser.add_option("--time-delt", "--tr", help="Time resolution (s)", type="float", default=1.5)
    parser.add_option("--te", help="Sequence TE (s)", type="float", default=0.065)
    adv = OptionGroup(parser, "Additional options")
    adv.add_option("--aifconc", action="store_true", help="Indicates that the AIF is a concentration-time curve", default=False)
    adv.add_option("--mv", action="store_true", help="Add a macrovascular component", default=False)
    adv.add_option("--sigadd", action="store_true", help="Combine macrovascular and tissue components by summing the signals (rather than concentrations)", default=False)
    adv.add_option("--modelfree", action="store_true", help="Run a 'model free' SVD analysis", default=False)
    adv.add_option("--modelfreeinit", action="store_true", help="Run a 'model free' SVD analysis as initialisation to the VB modelling", default=False)
    adv.add_option("--debug", action="store_true", help="Output debug information", default=False)
    parser.add_option_group(adv)

    options, _ = parser.parse_args()
    if not options.output:
        options.output = "verbena_out"

    if not options.data:
        sys.stderr.write("Input data file not specified\n")
        parser.print_help()
        sys.exit(1)

    wsp = Workspace(savedir=options.output, **vars(options))
    wsp.log.write("Verbena %s\n" % __version__)
    wsp.dscdata = Image(wsp.data)
    
    get_mask(wsp)
    get_aifconc(wsp)
    
    if wsp.modelfree or wsp.modelfreeinit:
        do_modelfree(wsp)

    if not wsp.modelfree:
        do_vascular_model(wsp)

    wsp.log.write("\nVerbena DONE\n")

def get_mask(wsp):
    """
    Generate the mask to use - if it has not been provided by the user
    """
    if wsp.mask is None:
        wsp.datamean = Image(np.mean(wsp.dscdata.data, axis=-1), header=wsp.dscdata.header)
        bet_result = fsl.bet(wsp.datamean, seg=False, mask=True, output=fsl.LOAD, log=wsp.fsllog)
        wsp.mask = bet_result["output_mask"]

def get_aifconc(wsp):
    """ 
    If the AIF is signal timeseries convert to concentration 
    """
    if wsp.aifconc:
        wsp.aifconc = wsp.aif
    else:
        wsp.aifconc = sig_to_conc(wsp, wsp.aif)

def sig_to_conc(wsp, img):
    """
    Convert a DSC signal to a concentration curve
    """
    nzero = 1 # number of time points to use from start of data to calculate S0
    sig0 = np.mean(img.data[..., :nzero], axis=-1)
    concdata = -np.log(img.data / sig0) / wsp.te
    return Image(concdata, header=img.header)

def do_modelfree(wsp):
    """
    Do the SVD model-free analysis. This may be used as the output itself or as
    an initialisation for the Fabber modelling
    """
    wsp.log.write("\nBegin model-free analysis\n")
    
    # do deconvolution
    #$asl_mfree --data=concdata --mask=mask --out=modfree --aif=concaif --dt=$tr
    
    # ASL_MFREE can produce nans if the mask is poor
    #fslmaths modfree_magntiude -nan modfree_magnitude_nonans
    #fslmaths modfree_residuals -nan modfree_residuals_nonans

    #calculate cbv
    #fslmaths concdata -Tmean -mul `fslnvols concdata` concsum
    #fslmaths concaif -Tmean -mul `fslnvols concaif` aifsum
    #fslmaths concsum -div aifsum cbv
    
    # calcualte MTT
    #fslmaths cbv -div modfree_magnitude_nonans mtt
    
    #copy results to output directory
    #cd "$stdir"
    #mkdir $outdir/modelfree
    #fslmaths $tempdir/modfree_magnitude_nonans $outdir/modelfree/rcbf
    #fslmaths $tempdir/cbv $outdir/modelfree/cbv
    #fslmaths $tempdir/mtt $outdir/modelfree/mtt
    #cd $tempdir

def do_vascular_model(wsp):
    """
    Do vascular modelling using Fabber
    """
    wsp.log.write("\nBegin VM analysis\n")
    wsp.sub("vm")

    options = {
        "data" : wsp.dscdata,
        "suppdata" : wsp.aif,
        "mask" : wsp.mask,
        "model" : "dsc",
        "te" : wsp.te,
        "delt" : wsp.time_delt,
        "inferdelay" : True,
        "infermtt" : True,
        "inferlambda" : True,
        "method" : "spatialvb",
        "param-spatial-priors" : "N+M",
        "noise" : "white",
        "max-iterations" : 20,
    }
    if wsp.aifconc:
        options["--aifconc"] = True
    else:
        options["--aifsig"] = True

    if wsp.modelfreeinit:
        raise NotImplementedError("modelfree")
        # make inital parameter estimates from model-free analysis
        # run fabber to get the right sized MVN
	    #rm -r init*
	    #$fabber --data=data --data-order=singlefile --output=init --suppdata=aif --method=vb --max-iterations=1 -@ core_options.txt
        
        # assemble the intial MVN for fabber
        #$mvntool --input=init/finalMVN --output=init_MVN --param=1 --valim=modfree_magnitude_nonans --var=100 --mask=mask --write
        #fslmaths mtt -thr 0.0001 -log mtt_log
        #$mvntool --input=init_MVN --output=init_MVN --param=2 --valim=mtt_log --var=10 --mask=mask --write
        #$mvntool --input=init_MVN --output=init_MVN --param=3 --val=2 --var=1 --mask=mask --write
        #$mvntool --input=init_MVN --output=init_MVN --param=4 --val=5 --var=1 --mask=mask --write
        #$mvntool --input=init_MVN --output=init_MVN --param=5 --valim=szero --var=1 --mask=mask --write
        
        #echo "--continue-from-mvn=init_MVN --continue-fwd-only" >> options.txt

    #result = fab.run(options)
    print(options)
    result = fabber(options, output=fsl.LOAD, progress_log=wsp.log, log=wsp.fsllog)
    for key, value in result.items():
        print("Data", key)
        setattr(wsp.vm, key, value)
    if wsp.vm.logfile is not None:
        wsp.vm.set_item("logfile", step_wsp.logfile, save_fn=str)
    
    # Macrovascular component
    if wsp.mv:
        wsp.log.write(" - Begin VM + MV analysis\n")
        raise NotImplementedError("MV component")
        #calculate cbv - used for intitalisation (this is just a model-free calculation)
        #fslmaths concdata -Tmean -mul `fslnvols concdata` concsum
        #fslmaths concaif -Tmean -mul `fslnvols concaif` aifsum
        #fslmaths concdata -div aifsum cbv
        
        # sort out intial MVN
        #$mvntool --input=vm/finalMVN.nii.gz --param=1 --output=init_cbf --val --mask=mask
        #fslmaths init_cbf -div 10 init_cbf
        #$mvntool --input=vm/finalMVN.nii.gz --param=1 --output=tempmvn --valim=init_cbf --write --mask=mask
        #$mvntool --input=tempmvn --param=6 --output=tempmvn --valim=cbv --var=0.1 --new --mask=mask
        #$mvntool --input=tempmvn.nii.gz --param=7 --output=tempmvn --val=5 --var=1 --new --mask=mask
        
        #echo "#Verneba analysis options (VM+MV)" > mvoptions.txt
        #cat core_options.txt >> mvoptions.txt
        #echo "--method=spatialvb" >> mvoptions.txt
        #echo "--param-spatial-priors=MNNNMAN" >> mvoptions.txt
        #echo "--max-iterations=20" >> mvoptions.txt 
        #echo "--inferart" >> mvoptions.txt
        #if [ ! -z $sigadd ]; then
        #echo "--artoption" >> mvoptions.txt
        #fi
        
        #rm -r vm_mv*
        #$fabber --data=data --data-order=singlefile --suppdata=aif --output=vm_mv --continue-from-mvn=tempmvn -@ mvoptions.txt
        
        #copy results to output directory
        #cd "$stdir"
        #mkdir $outdir/vm_mv
        #fslmaths $tempdir/vm_mv/mean_cbf -thr 0 $outdir/vm_mv/rcbf
        #fslmaths $tempdir/vm_mv/mean_transitm -mas $tempdir/mask $outdir/vm_mv/mtt
        #fslmaths $tempdir/vm_mv/mean_lambda -mas $tempdir/mask $outdir/vm_mv/lambda
        #fslmaths $tempdir/vm_mv/mean_abv -thr 0 $outdir/vm_mv/rabv
        #cd $tempdir
        #fi
