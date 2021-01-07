**----------------------------------------------------------------------------
** Groups and Constraints                                                   --
**----------------------------------------------------------------------------
** PLATFORM INSTALLATIONS
*GROUP 'PLATFORM' *ATTACHTO 'FIELD'

** MANIFOLD INSTALLATIONS
*GROUP 'PRODUCTION' *ATTACHTO 'PLATFORM'
*GROUP 'INJECTION' *ATTACHTO 'PLATFORM'

** MANIFOLD PRODUCTION CONSTRAINTS
*GCONP 'PRODUCTION'
	*MAX *STO 28617.7 *CONT	**180,000.00 bbl
	*MAX *STW 19078.5 *CONT **120,000.00 bbl
	*MAX *STL 28617.7 *CONT **180,000.00 bbl
	*GTARGET *STG 450000.0 ** Restricted to allowed burden limit
  ** *MAX *STG 8000000.0 *CONT

** MANIFOLD INJECTION CONSTRAINTS
*GCONI 'INJECTION'
	*MAX *STW 38157.0 *CONT **240,000.00 bbl
	** *MAX *STG 8000000.0 *CONT

** ALL GAS PRODUCED IS REINJECTED
*GCONI 'PLATFORM'
	*RECYCLE GAS 1.0

** GROUP INJECTION RATES
*GCONI 'PLATFORM'
	*PMAINT *WATER *PMTARG 450.0 ** Maintenance off hydrocarbon volume weighted average pressure at 450 kgf/cm^2

**----------------------------------------------------------------------------
** INGUIDE                                                                  --
**----------------------------------------------------------------------------
*APPOR-METHOD *PROD 'PLATFORM'   *IP
*APPOR-METHOD *WATI 'PLATFORM'   *IP
*APPOR-METHOD *GASI 'PLATFORM'   *IP
*APPOR-METHOD *PROD 'PRODUCTION' *IP
*APPOR-METHOD *WATI 'INJECTION'  *IP
*APPOR-METHOD *GASI 'INJECTION'  *IP

**----------------------------------------------------------------------------
** Time Availability                                                        --
**----------------------------------------------------------------------------
** PLATFORM EFFICIENCY
*ON-TIME 'PLATFORM'
1

** MANIFOLD EFFICIENCY
*ON-TIME 'PRODUCTION'
0.91

*ON-TIME 'INJECTION'
0.91
