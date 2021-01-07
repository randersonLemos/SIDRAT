RESULTS SIMULATOR IMEX 201210

********************************************************************************
** I/O CONTROL SECTION                                                       **
********************************************************************************
TITLE1 'Campo de Namorado - com falhas'
**                ========================
TITLE2 ' Otimiza MR3 - well location'

*INUNIT *MODSI             **  SISTEMA INTER. COM PRESSAO EM KGF/CM2    UTPUT.
*OUTUNIT *MODSI

*XDR *ON
*NOLIST

*WPRN *WELL   0
*WPRN *GRID   0
*WPRN *SECTOR 0
*WPRN *ITER   *NONE

*OUTPRN *WELL        *BRIEF
*OUTPRN *GRID        *NONE
*OUTPRN *TABLES      *NONE
*OUTPRN *RES         *NONE
*OUTPRN *WELL-SECTOR *NONE

*WSRF *WELL   *TIME
*WSRF *GRID   *NEVER
*WSRF *SECTOR *TIME

*OUTSRF *WELL *LAYER *NONE
*OUTSRF *GRID *NONE

*INCLUDE 'includes/ionorm.inc'

********************************************************************************
** RESERVOIR DESCRIPTION SECTION                                             **
********************************************************************************
**RESULTS XOFFSET      352000.0000
**RESULTS YOFFSET     7520500.0000
**RESULTS ROTATION        -25.0000  **  (DEGREES)
**  Distance units: m

INTERRUPT RESTART-STOP
DIM MDPTCN 60000

** ****************************************************************************
** Definition of fundamental cartesian grid
** ****************************************************************************
GRID VARI 51 28 6
KDIR DOWN
*INCLUDE 'includes/grid_blococ.inc'

*INCLUDE 'includes/null.inc'

*INCLUDE 'includes/imgC87.inc'

*INCLUDE 'includes/trans.inc'

*INCLUDE 'includes/sectorarray.inc'

PRPOR 1.
CPOR 0.00005

*INCLUDE 'includes/pv.inc'

*INCLUDE  'includes/kr.inc'

*INCLUDE 'includes/rtype.inc'


*INITIAL
*******************************************************************************
** SECAO DAS CONDICOES INICIAIS                                              **
*******************************************************************************
*VERTICAL *ON                      **  USE VERTICAL EQUILIBRIUM CALCULATION.
*PB *CON       210.03              **  BUBLE POINT PRESSURE
*DATUMDEPTH   3000.                **  GIVE A DATUM DEPTH
*REFDEPTH     3000. 3000. 3000.    **  GIVE A REFERENCE DEPTH
*REFPRES       327 327 327         **  ASSOCIATED PRESSURE.

*DWOC
*****************************************************************************
**Contato agua-oleo e um atributo incerto
3100.0
*****************************************************************************

*DWOC
*****************************************************************************
**Contato agua-oleo e um atributo incerto
3100.0
*****************************************************************************

*DWOC
*****************************************************************************
**Contato agua-oleo e um atributo incerto
3100.0
*****************************************************************************

*DGOC       1000.          **  DEPTH TO GAS-OIL CONTTACT
*DGOC       1000.
*DGOC       1000.

*NUMERICAL
********************************************************************************
** SECAO DE CONTROLE NUMERICO                                                **
********************************************************************************
*DTMAX          30.        **  MAXIMUM TIME STEP SIZE
*MAXSTEPS     9000         **  MAXIMUM NUMBER OF TIME STEPS
*NORM *PRESS     4.0       **  NORMAL MAXIMUM CHANGES PER TIME STEP
*NORM *SATUR     0.20

*NCUTS 6
**  USE THRESH HOLD SWITCHING CRITERIA
*AIM  *THRESH    0.25 .25

********************************************************************************
** SECAO DOS DADOS DE POCOS                                                  **
********************************************************************************
*RUN

*DATE 2009 5 31

*DTWELL  1.0    **  TAMANHO DO PRIMEIRO TS

*INCLUDE 'includes/wellhist1.inc'

************** End of Production History Data t1 ************** 

${strategy}

*STOP
