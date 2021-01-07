** cp=0
** ff=1
** img=80
** kr=1
** ogr=0.91
** oiw=0.98
** opl=1
** opw=1
** pvt=0

******************************************************************************
**                                UNISIM-II-D-BO                            **
**                                                                          **
**           Production Optimization - Black Oil Simulation Model           **
**                                                                          **
******************************************************************************

******************************************************************************
** I/O Control Section                                                      **
******************************************************************************
**CHECKONLY
*NOLIST
*INCLUDE './includes/iocontrol.inc'

******************************************************************************
** Reservoir Description Section                                            **
******************************************************************************
*GRID *CORNER 46 69 30
*CORNERS
*INCLUDE './includes/reservoir/grid.inc'
*DUALPERM
*SHAPE *GK
*POR *MATRIX *ALL
*INCLUDE './includes/reservoir/POR80.inc'
*POR *FRACTURE *ALL
*INCLUDE './includes/reservoir/PFR80.inc'
*PERMI *MATRIX *ALL
*INCLUDE './includes/reservoir/KX80.inc'
*PERMI *FRACTURE *ALL
*INCLUDE './includes/reservoir/KFX80.inc'
*PERMJ *MATRIX *ALL
*INCLUDE './includes/reservoir/KY80.inc'
*PERMJ *FRACTURE *ALL
*INCLUDE './includes/reservoir/KFY80.inc'
*PERMK *MATRIX *ALL
*INCLUDE './includes/reservoir/KZ80.inc'
*PERMK *FRACTURE *ALL
*INCLUDE './includes/reservoir/KFZ80.inc'
*DIFRAC *ALL
*INCLUDE './includes/reservoir/SGX80.inc'
*DJFRAC *ALL
*INCLUDE './includes/reservoir/SGY80.inc'
*DKFRAC *ALL
*INCLUDE './includes/reservoir/SGZ80.inc'
*NETGROSS *MATRIX *ALL
*INCLUDE './includes/reservoir/NTG80.inc'
*NULL *MATRIX *ALL
*INCLUDE './includes/reservoir/null_mtrx.inc'
*NULL *FRACTURE *ALL
*INCLUDE './includes/reservoir/null_frac.inc'
*INCLUDE './includes/reservoir/fltrans.inc'
*INCLUDE './includes/reservoir/pinc.inc'
*TRANSFER 0

******************************************************************************
** Component Properties Section                                             **
******************************************************************************
*PRPOR *MATRIX   450.0
*PRPOR *FRACTURE 450.0
*CPOR *MATRIX
*INCLUDE './includes/petrophysics/CP0.inc'
*CPOR *FRACTURE
*INCLUDE './includes/petrophysics/CP0.inc'
*INCLUDE './includes/petrophysics/PVT0.inc'
*PTYPE *MATRIX   *CON 1
*PTYPE *FRACTURE *CON 1

******************************************************************************
** Rock-Fluid Properties Section                                            **
******************************************************************************
*ROCKFLUID
*INCLUDE './includes/petrophysics/KR1.inc'
*RTYPE *MATRIX *ALL
*INCLUDE './includes/petrophysics/RTP80.inc'
*RTYPE *FRACTURE *CON 2

******************************************************************************
** Initial Conditions Section                                               **
******************************************************************************
*INITIAL
*VERTICAL *Block_Center *WATER_OIL
*REFDEPTH 4850
*REFPRES   450
*DWOC     9999
*PB *MATRIX *CON
*INCLUDE './includes/petrophysics/PB0.inc'
*PB *FRACTURE *CON
*INCLUDE './includes/petrophysics/PB0.inc'

******************************************************************************
** Numerical Control Section                                                **
******************************************************************************
*INCLUDE './includes/numerical.inc'

******************************************************************************
** Wells and Recurrent Section                                              **
******************************************************************************
*RUN
*DATE 2016 9 30.00000
*AIMSET *FRACTURE *CON 1
*DTWELL 1

**----------------------------------------------------------------------------
** Wildcat and History Match                                                --
** From 2016 10 01 (TIME 1) until 2018 02 28 (TIME 516)                     --
** Wildcat well defined and history match performed                         --
**----------------------------------------------------------------------------
*INCLUDE './includes/recurrent/history-match-wildcat.inc'
*INCLUDE './includes/recurrent/00001-00516-history-match.inc'

**----------------------------------------------------------------------------
** Period to set up exploitation strategy                                   --
** From 2018 03 01 (TIME 517) until 2020 02 28 (TIME 1246)                  --
** Nothing done. The time just passes.                                      --
**----------------------------------------------------------------------------
*INCLUDE './includes/recurrent/00517-01246-development-drilling.inc'

**----------------------------------------------------------------------------
** Production Unit                                                          --
** Groups, groups constraints, inguide approach, and available time         --
**----------------------------------------------------------------------------
*INCLUDE './includes/recurrent/facilities.inc'

**----------------------------------------------------------------------------
** Producers (9 + Wildcat)                                                  --
**----------------------------------------------------------------------------
*INCLUDE './includes/wells/PRK085.inc'
*INCLUDE './includes/wells/PRK084.inc'
*INCLUDE './includes/wells/PRK045.inc'
*INCLUDE './includes/wells/PRK083.inc'
*INCLUDE './includes/wells/PRK060.inc'
*INCLUDE './includes/wells/Wildcat.inc'
*INCLUDE './includes/wells/PRK028.inc'
*INCLUDE './includes/wells/PRK061.inc'
*INCLUDE './includes/wells/PRK014.inc'
*INCLUDE './includes/wells/PRK052.inc'

**----------------------------------------------------------------------------
** Injectors - WAG(8)                                                       --
**----------------------------------------------------------------------------
*INCLUDE './includes/wells/IRK004.inc'
*INCLUDE './includes/wells/IRK028.inc'
*INCLUDE './includes/wells/IRK029.inc'
*INCLUDE './includes/wells/IRK036.inc'
*INCLUDE './includes/wells/IRK049.inc'
*INCLUDE './includes/wells/IRK050.inc'
*INCLUDE './includes/wells/IRK056.inc'
*INCLUDE './includes/wells/IRK063.inc'

**----------------------------------------------------------------------------
** Well schedule                                                            --
** From 2020 02 29 (TIME 1247) until 2022 03 31 (TIME 2008)                 --
**----------------------------------------------------------------------------
**DTMAX 1.0
*INCLUDE './includes/recurrent/01247-02008-development-opening.inc'

**----------------------------------------------------------------------------
** ICV's control rules                                                      --
**----------------------------------------------------------------------------
*TRIGGER 'ICVs_PROD' *ON_ELAPSED 'TIME' *TRELTD > 0 *INCREMENT 183 *APPLY_TIMES 200

** *****PRK014*****
*TRIGGER 'ICV_PRK014_Z1' *ON_CTRLLUMP 'PRK014_Z1' *GOR > #PRK014_Z1_GOR# *TEST_TIMES 1
  *CLUMPSETTING 'PRK014_Z1' 0.0
*END_TRIGGER
*TRIGGER 'ICV_PRK014_Z2' *ON_CTRLLUMP 'PRK014_Z2' *GOR > #PRK014_Z2_GOR# *TEST_TIMES 1
  *CLUMPSETTING 'PRK014_Z2' 0.0
*END_TRIGGER
*TRIGGER 'ICV_PRK014_Z3' *ON_CTRLLUMP 'PRK014_Z3' *GOR > #PRK014_Z3_GOR# *TEST_TIMES 1
  *CLUMPSETTING 'PRK014_Z3' 0.0
*END_TRIGGER
** *****PRK028*****
*TRIGGER 'ICV_PRK028_Z1' *ON_CTRLLUMP 'PRK028_Z1' *GOR > #PRK028_Z1_GOR# *TEST_TIMES 1
  *CLUMPSETTING 'PRK028_Z1' 0.0
*END_TRIGGER
*TRIGGER 'ICV_PRK028_Z2' *ON_CTRLLUMP 'PRK028_Z2' *GOR > #PRK028_Z2_GOR# *TEST_TIMES 1
  *CLUMPSETTING 'PRK028_Z2' 0.0
*END_TRIGGER
*TRIGGER 'ICV_PRK028_Z3' *ON_CTRLLUMP 'PRK028_Z3' *GOR > #PRK028_Z3_GOR# *TEST_TIMES 1
  *CLUMPSETTING 'PRK028_Z3' 0.0
*END_TRIGGER
** *****PRK045*****
*TRIGGER 'ICV_PRK045_Z1' *ON_CTRLLUMP 'PRK045_Z1' *GOR > #PRK045_Z1_GOR# *TEST_TIMES 1
  *CLUMPSETTING 'PRK045_Z1' 0.0
*END_TRIGGER
*TRIGGER 'ICV_PRK045_Z2' *ON_CTRLLUMP 'PRK045_Z2' *GOR > #PRK045_Z2_GOR# *TEST_TIMES 1
  *CLUMPSETTING 'PRK045_Z2' 0.0
*END_TRIGGER
*TRIGGER 'ICV_PRK045_Z3' *ON_CTRLLUMP 'PRK045_Z3' *GOR > #PRK045_Z3_GOR# *TEST_TIMES 1
  *CLUMPSETTING 'PRK045_Z3' 0.0
*END_TRIGGER
** *****PRK052*****
*TRIGGER 'ICV_PRK052_Z1' *ON_CTRLLUMP 'PRK052_Z1' *GOR > #PRK052_Z1_GOR# *TEST_TIMES 1
  *CLUMPSETTING 'PRK052_Z1' 0.0
*END_TRIGGER
*TRIGGER 'ICV_PRK052_Z2' *ON_CTRLLUMP 'PRK052_Z2' *GOR > #PRK052_Z2_GOR# *TEST_TIMES 1
  *CLUMPSETTING 'PRK052_Z2' 0.0
*END_TRIGGER
*TRIGGER 'ICV_PRK052_Z3' *ON_CTRLLUMP 'PRK052_Z3' *GOR > #PRK052_Z3_GOR# *TEST_TIMES 1
  *CLUMPSETTING 'PRK052_Z3' 0.0
*END_TRIGGER
** *****PRK060*****
*TRIGGER 'ICV_PRK060_Z1' *ON_CTRLLUMP 'PRK060_Z1' *GOR > #PRK060_Z1_GOR# *TEST_TIMES 1
  *CLUMPSETTING 'PRK060_Z1' 0.0
*END_TRIGGER
*TRIGGER 'ICV_PRK060_Z2' *ON_CTRLLUMP 'PRK060_Z2' *GOR > #PRK060_Z2_GOR# *TEST_TIMES 1
  *CLUMPSETTING 'PRK060_Z2' 0.0
*END_TRIGGER
*TRIGGER 'ICV_PRK060_Z3' *ON_CTRLLUMP 'PRK060_Z3' *GOR > #PRK060_Z3_GOR# *TEST_TIMES 1
  *CLUMPSETTING 'PRK060_Z3' 0.0
*END_TRIGGER
** *****PRK061*****
*TRIGGER 'ICV_PRK061_Z1' *ON_CTRLLUMP 'PRK061_Z1' *GOR > #PRK061_Z1_GOR# *TEST_TIMES 1
  *CLUMPSETTING 'PRK061_Z1' 0.0
*END_TRIGGER
*TRIGGER 'ICV_PRK061_Z2' *ON_CTRLLUMP 'PRK061_Z2' *GOR > #PRK061_Z2_GOR# *TEST_TIMES 1
  *CLUMPSETTING 'PRK061_Z2' 0.0
*END_TRIGGER
*TRIGGER 'ICV_PRK061_Z3' *ON_CTRLLUMP 'PRK061_Z3' *GOR > #PRK061_Z3_GOR# *TEST_TIMES 1
  *CLUMPSETTING 'PRK061_Z3' 0.0
*END_TRIGGER
** *****PRK083*****
*TRIGGER 'ICV_PRK083_Z1' *ON_CTRLLUMP 'PRK083_Z1' *GOR > #PRK083_Z1_GOR# *TEST_TIMES 1
  *CLUMPSETTING 'PRK083_Z1' 0.0
*END_TRIGGER
*TRIGGER 'ICV_PRK083_Z2' *ON_CTRLLUMP 'PRK083_Z2' *GOR > #PRK083_Z2_GOR# *TEST_TIMES 1
  *CLUMPSETTING 'PRK083_Z2' 0.0
*END_TRIGGER
*TRIGGER 'ICV_PRK083_Z3' *ON_CTRLLUMP 'PRK083_Z3' *GOR > #PRK083_Z3_GOR# *TEST_TIMES 1
  *CLUMPSETTING 'PRK083_Z3' 0.0
*END_TRIGGER
** *****PRK084*****
*TRIGGER 'ICV_PRK084_Z1' *ON_CTRLLUMP 'PRK084_Z1' *GOR > #PRK084_Z1_GOR# *TEST_TIMES 1
  *CLUMPSETTING 'PRK084_Z1' 0.0
*END_TRIGGER
*TRIGGER 'ICV_PRK084_Z2' *ON_CTRLLUMP 'PRK084_Z2' *GOR > #PRK084_Z2_GOR# *TEST_TIMES 1
  *CLUMPSETTING 'PRK084_Z2' 0.0
*END_TRIGGER
*TRIGGER 'ICV_PRK084_Z3' *ON_CTRLLUMP 'PRK084_Z3' *GOR > #PRK084_Z3_GOR# *TEST_TIMES 1
  *CLUMPSETTING 'PRK084_Z3' 0.0
*END_TRIGGER
** *****PRK085*****
*TRIGGER 'ICV_PRK085_Z1' *ON_CTRLLUMP 'PRK085_Z1' *GOR > #PRK085_Z1_GOR# *TEST_TIMES 1
  *CLUMPSETTING 'PRK085_Z1' 0.0
*END_TRIGGER
*TRIGGER 'ICV_PRK085_Z2' *ON_CTRLLUMP 'PRK085_Z2' *GOR > #PRK085_Z2_GOR# *TEST_TIMES 1
  *CLUMPSETTING 'PRK085_Z2' 0.0
*END_TRIGGER
*TRIGGER 'ICV_PRK085_Z3' *ON_CTRLLUMP 'PRK085_Z3' *GOR > #PRK085_Z3_GOR# *TEST_TIMES 1
  *CLUMPSETTING 'PRK085_Z3' 0.0
*END_TRIGGER

*END_TRIGGER

**----------------------------------------------------------------------------
** Field production - Opening Schedule and Management stage                 --
** From 2022 04 30 (TIME 2038) until the rest of simulation is field        --
** management stage                                                         --
**----------------------------------------------------------------------------
**DTMAX 15.0
*INCLUDE './includes/recurrent/02038-10957-management.inc'
*STOP
