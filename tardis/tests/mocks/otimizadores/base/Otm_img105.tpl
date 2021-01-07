RESULTS SIMULATOR IMEX 201610

**********************************************************************************
**                                      UNISIM-I-D                              **
**                                                                              **
**         Production Optimization - Simulation Model Generated at t1 (SMT1)    **
**                                                                              **
**                      Available Data: 4 years of production history (t1)      **
**********************************************************************************

*****************************************************************************
** I/O Control Section
*****************************************************************************
*TITLE1
'UNISIM-I Simulation Model in t1 (IMG105)'

*TITLE2
'Production Strategy Optimization'
**------------------------------------------------------------------------

*TITLE3
'UNISIM GROUP'

**------------------------------------------------------------------------

*INUNIT  MODSI
*OUTUNIT MODSI

*XDR *ON
*NOLIST
**SRFORMAT SR3_IMRF
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
*WSRF *GRID   0
*WSRF *SECTOR *TIME

*OUTSRF *WELL *LAYER *NONE
** *OUTSRF *GRID *SO *SG *SW *PRES

*INCLUDE '../base/includes/normPersonalizada.txt'


**  Distance units: m
RESULTS XOFFSET            0.0000
RESULTS YOFFSET            0.0000
RESULTS ROTATION           0.0000  **  (DEGREES)
RESULTS AXES-DIRECTIONS 1.0 1.0 1.0


*****************************************************************************
** Reservoir Section
*****************************************************************************

GRID CORNER 81 58 20

*INCLUDE '../base/includes/corners.inc'

** Bloco Leste eh um atributo incerto
** *INCLUDE '../base/includes/bl0.inc'
*INCLUDE '../base/includes/bl0.inc'
***MAI_INCLUDE 'bl'


**$ Transmissibilidade da falha C
*INCLUDE '../base/includes/tc0.inc'


**$ Transmissibilidade da falha D e um atributo incerto
** *INCLUDE '../base/includes/td0.inc'
*INCLUDE '../base/includes/td0.inc'
***MAI_INCLUDE 'td'


*INCLUDE '../base/includes/pinchoutarray.inc'
*INCLUDE '../base/includes/sectorarray.inc'


**$ Cenario e um atributo incerto
**$ Cenario esta incluso: POR, PERM I, PERM J, PERM K, NTG e Facies.
** *INCLUDE '../base/includes/img0.inc'
*INCLUDE '../base/includes/img105.inc'
***MAI_INCLUDE 'img'


**$ Permeabilidade vertical e um atributo incerto
** *INCLUDE '../base/includes/kz0.inc'
*INCLUDE '../base/includes/kz1.inc'
***MAI_INCLUDE 'kz'


*********************************************************************************
** Component Properties Section
*********************************************************************************

PRPOR 322.0

**$ Compressibilidade eh um atributo incerto
CPOR
** ** *INCLUDE '../base/includes/cp0.inc'
*INCLUDE '../base/includes/cp1.inc'
***MAI_INCLUDE 'cp'


PVCUTOFF 80

MODEL BLACKOIL

TRES 80

PVT BG 1
**$     PVT1
**$     p               Rs              Bo              Bg              viso    visg            co
35.49   31.80   1.198   0.0346  2.05    0.0109  1.62E-04
41.82   34.66   1.200   0.0291  1.99    0.0113  1.62E-04
49.20   38.02   1.210   0.0245  1.91    0.0117  1.62E-04
59.75   42.83   1.230   0.0199  1.81    0.0123  1.62E-04
68.54   46.85   1.240   0.0172  1.73    0.0128  1.62E-04
80.85   52.51   1.250   0.0144  1.62    0.0134  1.62E-04
93.86   58.51   1.270   0.0123  1.52    0.0142  1.62E-04
105.81  64.06   1.280   0.0108  1.43    0.0148  1.62E-04
121.98  71.60   1.300   0.0093  1.32    0.0157  1.62E-04
133.94  77.20   1.320   0.0084  1.25    0.0164  1.62E-04
148.00  83.83   1.330   0.0076  1.17    0.0172  1.62E-04
166.29  92.49   1.350   0.0067  1.09    0.0182  1.62E-04
193.36  105.42  1.390   0.0058  1.00    0.0197  1.62E-04
213.26  115.01  1.410   0.0053  0.96    0.0208  1.62E-04
219.38  117.64  1.420   0.0051  0.94    0.0211  1.62E-04
229.50  122.19  1.430   0.0049  0.91    0.0217  1.62E-04
248.00  130.84  1.450   0.0045  0.85    0.0227  1.62E-04
283.02  147.22  1.500   0.0040  0.75    0.0246  1.62E-04
316.91  163.08  1.540   0.0035  0.65    0.0265  1.62E-04
352.63  179.79  1.580   0.0032  0.54    0.0285  1.62E-04
360.00  183.24  1.590   0.0031  0.52    0.0289  1.62E-04

BWI 1.0210
CVO 1.14E-03
CVW 0.0
CW 47.64E-06
DENSITY OIL 0.866E3
DENSITY WATER 1.010E03
REFPW 1.0
VWI 0.3
GRAVITY GAS 0.745


** PVT eh um atributo incerto
** *INCLUDE '../base/includes/pv0.inc'
*INCLUDE '../base/includes/pv0.inc'
***MAI_INCLUDE 'pv'


*INCLUDE '../base/includes/ptype.inc'

*******************************************************************************************************************************
** Rock-Fluid Properties Section
*******************************************************************************************************************************

*ROCKFLUID

RPT 1


** Permeabilidade relativa eh um atributo incerto
** *INCLUDE '../base/includes/kr0.inc'
*INCLUDE '../base/includes/kr1.inc'
***MAI_INCLUDE 'kr'


*********************************************************************************
** Initial Conditions Section
*********************************************************************************

*INITIAL
*VERTICAL *BLOCK_CENTER *WATER_OIL

** GIVE A REFERENCE DEPTH, ASSOCIATED PRESSURE and WATER-OIL CONTACT
** Regions       1        2
REFDEPTH        3000.0  3000.0
REFPRES         327.0   327.0


** Contato agua-oleo eh um atributo incerto
** *INCLUDE '../base/includes/wo0.inc'
*INCLUDE '../base/includes/wo3.inc'
***MAI_INCLUDE 'wo'


*PB *CON     210.03

***************************************************************************************
** Numerical Control Section
***************************************************************************************

*NUMERICAL
*NCUTS 20
** *MAXSTEPS 100000

**************************************************
******* Palavras que orientam a simulacao paralela
*** DPLANES
*** SOLVER *PARASOL
*** PPATERN *AUTOPSLAB 12
*** PNTHRDS 12

****************************************************************************************
** Wells and Recurrent Section
****************************************************************************************

*RUN

*DATE 2013 5 31
*DTWELL  1.0    ** TAMANHO DO PRIMEIRO TS

WELL  'NA1A'
PRODUCER 'NA1A'
OPERATE  MAX  STL  3000.  CONT
OPERATE  MIN  BHP  36.  CONT
**          rad  geofac  wfrac  skin
GEOMETRY  K  0.156 0.37  1.  0.
PERF  GEO  'NA1A'
** UBA       ff  Status  Connection
38 36 1   1.  OPEN    FLOW-TO  'SURFACE'  REFLAYER
38 36 2   1.  OPEN    FLOW-TO  1
38 36 3   1.  OPEN    FLOW-TO  2
38 36 6   1.  OPEN    FLOW-TO  3
38 36 7   1.  OPEN    FLOW-TO  4
38 36 8   1.  OPEN    FLOW-TO  5
38 36 9   1.  OPEN    FLOW-TO  6
38 36 10  1.  OPEN    FLOW-TO  7
38 36 11  1.  OPEN    FLOW-TO  8
38 36 12  1.  OPEN    FLOW-TO  9
38 36 13  1.  OPEN    FLOW-TO  10
38 36 15  1.  OPEN    FLOW-TO  11
38 36 16  1.  OPEN    FLOW-TO  12
38 36 17  1.  OPEN    FLOW-TO  13
38 36 18  1.  OPEN    FLOW-TO  14
38 36 19  1.  OPEN    FLOW-TO  15
SHUTIN 'NA1A'


WELL  'NA2'
PRODUCER 'NA2'
OPERATE  MAX  STL  3000.  CONT
OPERATE  MIN  BHP  36.  CONT
**          rad  geofac  wfrac  skin
GEOMETRY  K  0.156 0.37  1.  0.
PERF  GEO  'NA2'
** UBA       ff  Status  Connection
21 36 1   1.  OPEN    FLOW-TO  'SURFACE'  REFLAYER
21 36 2   1.  OPEN    FLOW-TO  1
21 36 3   1.  OPEN    FLOW-TO  2
21 36 6   1.  OPEN    FLOW-TO  3
21 36 7   1.  OPEN    FLOW-TO  4
21 36 8   1.  OPEN    FLOW-TO  5
21 36 9   1.  OPEN    FLOW-TO  6
21 36 10  1.  OPEN    FLOW-TO  7
21 36 11  1.  OPEN    FLOW-TO  8
21 36 12  1.  OPEN    FLOW-TO  9
SHUTIN 'NA2'


WELL  'NA3D'
PRODUCER 'NA3D'
OPERATE  MAX  STL  3000.  CONT
OPERATE  MIN  BHP  36.  CONT
**          rad  geofac  wfrac  skin
GEOMETRY  K  0.156 0.37  1.  0.
PERF  GEO  'NA3D'
** UBA       ff  Status  Connection
44 43 1   1.  OPEN    FLOW-TO  'SURFACE'  REFLAYER
44 43 2   1.  OPEN    FLOW-TO  1
44 43 3   1.  OPEN    FLOW-TO  2
44 43 6   1.  OPEN    FLOW-TO  3
44 43 7   1.  OPEN    FLOW-TO  4
44 43 8   1.  OPEN    FLOW-TO  5
44 43 9   1.  OPEN    FLOW-TO  6
44 43 10  1.  OPEN    FLOW-TO  7
44 43 11  1.  OPEN    FLOW-TO  8
SHUTIN 'NA3D'


WELL  'RJS19'
PRODUCER 'RJS19'
OPERATE  MAX  STL  3000.  CONT
OPERATE  MIN  BHP  36.  CONT
**          rad  geofac  wfrac  skin
GEOMETRY  K  0.156 0.37  1.  0.
PERF  GEO  'RJS19'
** UBA       ff  Status  Connection
31 27 1   1.  OPEN    FLOW-TO  'SURFACE'  REFLAYER
31 27 2   1.  OPEN    FLOW-TO  1
31 27 3   1.  OPEN    FLOW-TO  2
31 27 6   1.  OPEN    FLOW-TO  3
31 27 7   1.  OPEN    FLOW-TO  4
31 27 8   1.  OPEN    FLOW-TO  5
31 27 9   1.  OPEN    FLOW-TO  6
31 27 10  1.  OPEN    FLOW-TO  7
31 27 11  1.  OPEN    FLOW-TO  8
31 27 12  1.  OPEN    FLOW-TO  9
31 27 13  1.  OPEN    FLOW-TO  10
31 27 15  1.  OPEN    FLOW-TO  11
31 27 16  1.  OPEN    FLOW-TO  12
31 27 17  1.  OPEN    FLOW-TO  13
31 27 18  1.  OPEN    FLOW-TO  14
31 27 19  1.  OPEN    FLOW-TO  15
SHUTIN 'RJS19'


************** Start of Production History Data t0 **************

*TARGET  *STL   'NA1A'
0
*TIME   1
*TARGET  *STL   'NA1A'
0
*TIME   30
*TARGET  *STL   'NA1A'
1998
*TIME   61
*TARGET  *STL   'NA1A'
2015
*TIME   92
*TARGET  *STL   'NA1A'
1934
*TIME   122
*TARGET  *STL   'NA1A'
2014
*TIME   153
*TARGET  *STL   'NA1A'  'RJS19'
1975    0
*TIME   183
*TARGET  *STL   'NA1A'  'RJS19'
1992    1384
*TIME   214
*TARGET  *STL   'NA1A'  'RJS19'
1954    1269
*TIME   245
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'
2062    1192    0
*TIME   273
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'
1956    1203    1937
*TIME   304
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'
2039    1215    0
*TIME   334
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'  'NA2'
1944    1080    0       0
*TIME   365
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'  'NA2'
1988    1027    0       2077
*TIME   395
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'  'NA2'
2071    1000    0       1992
*TIME   426
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'  'NA2'
1991    919     1973    2065
*TIME   457
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'  'NA2'
2035    845     1732    2074
*TIME   487
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'  'NA2'
2059    816     1526    1987
*TIME   518
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'  'NA2'
0       0       0       0
*TIME   548
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'  'NA2'
0       0       0       0
*TIME   579
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'  'NA2'
0       0       0       0
*TIME   610
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'  'NA2'
0       0       0       0
*TIME   638
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'  'NA2'
1989    872     1408    2052
*TIME   669
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'  'NA2'
2056    670     1167    2007
*TIME   699
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'  'NA2'
1722    604     1090    2019
*TIME   730
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'  'NA2'
1608    571     914     2038
*TIME   760
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'  'NA2'
1401    458     817     2018
*TIME   791
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'  'NA2'
1251    415     794     1753
*TIME   822
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'  'NA2'
1134    357     707     1629
*TIME   852
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'  'NA2'
1059    352     645     1416
*TIME   883
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'  'NA2'
868     285     616     1270
*TIME   913
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'  'NA2'
880     305     575     1197
*TIME   944
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'  'NA2'
785     260     511     1043
*TIME   975
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'  'NA2'
693     247     475     940
*TIME   1004
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'  'NA2'
616     216     468     894
*TIME   1035
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'  'NA2'
643     200     408     936
*TIME   1065
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'  'NA2'
550     208     391     849
*TIME   1096
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'  'NA2'
566     171     356     832
*TIME   1126
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'  'NA2'
475     163     337     812
*TIME   1157
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'  'NA2'
504     174     368     770
*TIME   1188
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'  'NA2'
459     153     349     721
*TIME   1218
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'  'NA2'
432     162     331     695
*TIME   1249
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'  'NA2'
468     139     327     635
*TIME   1279
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'  'NA2'
442     140     321     627
*TIME   1310
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'  'NA2'
413     0       319     614
*TIME   1341
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'  'NA2'
422     0       272     595
*TIME   1369
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'  'NA2'
354     138     299     609
*TIME   1400
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'  'NA2'
358     136     298     603
*TIME   1430
*TARGET  *STL   'NA1A'  'RJS19' 'NA3D'  'NA2'
358     121     291     574
*TIME   1461

*SHUTIN  'NA1A'
*SHUTIN  'RJS19'
*SHUTIN  'NA3D'
*SHUTIN  'NA2'

************** End of Production History Data t1 **************
${strategy}
*STOP