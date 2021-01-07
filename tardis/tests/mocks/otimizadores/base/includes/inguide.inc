****************************************************************************
**INGUIDE utilizado no UNISIM-I-D 

*APPOR-METHOD *PROD  'Producao'   *INGUIDE
*PRIOR-FORM   *PROD  'Producao' 
              ** FREQ  tcr_min   tcr_max
    *PRIOR-CTRL   30.    0.0      1.0
**               const   STO   STG  STW  STS  STL   BHF
    *PRIOR-NUMER    0.   1.0   0.0  0.0  0.0  0.0   0.0            
    *PRIOR-DENOM   10.   0.0   0.0  1.0  0.0  0.0   0.0 

*APPOR-METHOD *WATI  'Injecao'   *INGUIDE
*PRIOR-FORM   *WATI  'Injecao'        
    *PRIOR-RATE  *BHP 480.0 
**              FREQ  tcr_min   tcr_max
    *PRIOR-CTRL   30.    0.0      1.0
