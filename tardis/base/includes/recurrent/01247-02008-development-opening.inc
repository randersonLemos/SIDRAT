*WSRF GRID TNEXT

*TIME 1247.0 ** DATE 2020 02 29

*OPEN 'PRK085'

*TIME 1278.0 ** DATE 2020 03 31

**----------------------------------------------------------------------------
*GCONP 'PRODUCTION'
	*GTARGET *STG 3000000. **limitado à máxima vazão de injeção de 1 poço IG
*GCONI 'PLATFORM'
	*RECYCLE *GAS  1.0
**----------------------------------------------------------------------------

*OPEN 'IRK063-G'

*TIME 1308.0 ** DATE 2020 04 30

*OPEN 'PRK084'

*TIME 1339.0 ** DATE 2020 05 31

**----------------------------------------------------------------------------
*GCONP 'PRODUCTION'
	*GTARGET *STG 6000000. **limitado à máxima vazão de injeção de 2 poço IG
*GCONI 'PLATFORM'
	*RECYCLE *GAS  1.0
**----------------------------------------------------------------------------

*OPEN 'IRK056-G'

*TIME 1369.0 ** DATE 2020 06 30

*OPEN 'PRK045'

*TIME 1400.0 ** DATE 2020 07 31

*OPEN 'IRK029-W'

*TIME 1431.0 ** DATE 2020 08 31

*OPEN 'PRK083'

*TIME 1461.0 ** DATE 2020 09 30

*OPEN 'IRK050-W'

*TIME 1492.0 ** DATE 2020 10 31

*OPEN 'PRK060'

*TIME 1522.0 ** DATE 2020 11 30

**----------------------------------------------------------------------------
*GCONP 'PRODUCTION'
	*MAX *STG 8000000. **limitado à capacidade máxima da plataforma
*GCONI 'PLATFORM'
	*RECYCLE *GAS  1.0
**----------------------------------------------------------------------------

*OPEN 'IRK049-G'

*TIME 1553.0 ** DATE 2020 12 31

*OPEN 'Wildcat'

*TIME 1584.0 ** DATE 2021 01 31

*OPEN 'IRK036-G'

*TIME 1612.0 ** DATE 2021 02 28

*OPEN 'PRK028'

*TIME 1643.0 ** DATE 2021 03 31

*OPEN 'IRK028-W'

*TIME 1673.0 ** DATE 2021 04 30

*OPEN 'PRK061'

*TIME 1704.0 ** DATE 2021 05 31

*OPEN 'PRK014'

*TIME 1734.0 ** DATE 2021 06 30

*OPEN 'IRK004-W'

*TIME 1765.0 ** DATE 2021 07 31

*OPEN 'PRK052'

*TIME 1796.0 ** DATE 2021 08 31

*TIME 1826.0 ** DATE 2021 09 30

*TIME 1857.0 ** DATE 2021 10 31

*TIME 1887.0 ** DATE 2021 11 30

*TIME 1918.0 ** DATE 2021 12 31

*TRIGGER 'WAG-A' *ON_ELAPSED 'TIME' *TRELTD > 0 *APPLY_TIMES 100 *INCREMENT 366

*SHUTIN 'IRK063-G'
*SHUTIN 'IRK056-G'
*SHUTIN 'IRK029-W'
*SHUTIN 'IRK050-W'
*SHUTIN 'IRK049-G'
*SHUTIN 'IRK036-G'
*SHUTIN 'IRK028-W'
*SHUTIN 'IRK004-W'

*OPEN 'IRK063-W'
*OPEN 'IRK056-W'
*OPEN 'IRK029-G'
*OPEN 'IRK050-G'
*OPEN 'IRK049-W'
*OPEN 'IRK036-W'
*OPEN 'IRK028-G'
*OPEN 'IRK004-G'

*TRIGGER 'WAG-B' *ON_ELAPSED 'TIME' *TRELTD > 180 *APPLY_TIMES 100 *INCREMENT 366

*OPEN 'IRK063-G'
*OPEN 'IRK056-G'
*OPEN 'IRK029-W'
*OPEN 'IRK050-W'
*OPEN 'IRK049-G'
*OPEN 'IRK036-G'
*OPEN 'IRK028-W'
*OPEN 'IRK004-W'

*SHUTIN 'IRK063-W'
*SHUTIN 'IRK056-W'
*SHUTIN 'IRK029-G'
*SHUTIN 'IRK050-G'
*SHUTIN 'IRK049-W'
*SHUTIN 'IRK036-W'
*SHUTIN 'IRK028-G'
*SHUTIN 'IRK004-G'

*END_TRIGGER

*END_TRIGGER
*TIME 1949.0 ** DATE 2022 01 31

*TIME 1977.0 ** DATE 2022 02 28

*TIME 2008.0 ** DATE 2022 03 31
