
********************************************************************************
** SECAO DOS DADOS DE POCOS                                                  **
********************************************************************************
*RUN

*DATE 2009 5 31

*DTWELL  1.0    **  TAMANHO DO PRIMEIRO TS



*TIME 1.000000

*TIME 31.000000
*TIME 62.000000
*TIME 93.000000
*TIME 123.000000
*TIME 154.000000
*TIME 184.000000

*TIME 215.000000
*TIME 246.000000
*TIME 274.000000
*TIME 305.000000
*TIME 335.000000
*TIME 366.000000

*TIME 396.000000
*TIME 427.000000
*TIME 458.000000
*TIME 488.000000
*TIME 519.000000
*TIME 549.000000

*TIME 580.000000
*TIME 611.000000
*TIME 639.000000
*TIME 670.000000
*TIME 700.000000
*TIME 731.000000

*TIME 761.000000
*TIME 792.000000
*TIME 823.000000
*TIME 853.000000
*TIME 884.000000
*TIME 914.000000

*TIME 945.000000
*TIME 976.000000
*TIME 1005.000000
*TIME 1036.000000
*TIME 1066.000000
*TIME 1097.000000

*TIME 1127.000000
*TIME 1158.000000
*TIME 1189.000000
*TIME 1219.000000
*TIME 1250.000000
*TIME 1280.000000

*TIME 1311.000000
*TIME 1342.000000
*TIME 1370.000000
*TIME 1401.000000
*TIME 1431.000000
*TIME 1462.000000

*TIME 1492.000000
*TIME 1523.000000
*TIME 1554.000000
*TIME 1584.000000
*TIME 1615.000000
*TIME 1645.000000

*TIME 1676.000000
*TIME 1707.000000
*TIME 1735.000000
*TIME 1766.000000
*TIME 1796.000000
*TIME 1827.000000

*TIME 1857.000000
*TIME 1888.000000
*TIME 1919.000000
*TIME 1949.000000

*TIME 1980.000000

************** End of Production History Data t1 ************** 


** STRATEGY_BEGIN

*TIME 2010.0    ** DATE 2014 12 01

*TIME 2041.0    ** DATE 2015 01 01

*TIME 2072.0    ** DATE 2015 02 01

*TIME 2100.0    ** DATE 2015 03 01

*TIME 2131.0    ** DATE 2015 04 01

*TIME 2161.0    ** DATE 2015 05 01

*TIME 2192.0    ** DATE 2015 06 01

*TIME 2222.0    ** DATE 2015 07 01

*TIME 2253.0    ** DATE 2015 08 01

*TIME 2284.0    ** DATE 2015 09 01

*TIME 2314.0    ** DATE 2015 10 01

*TIME 2344.0    ** DATE 2015 10 31
** PLATFORM INSTALLATIONS
GROUP 'Plataforma' ATTACHTO 'Field'
** MANIFOLD INSTALLATIONS
GROUP 'Producao' ATTACHTO 'Plataforma'
GROUP 'Injecao' ATTACHTO 'Plataforma'

** WELL COMPLETIONS

*WELL 'PP-00'
**        dir rad    geofac wfac skin
**i  j   k  ff  status connection
**$          rad  geofac  wfrac  skin
GEOMETRY  I  0.0762  0.37  1.  0.
PERF  GEOA  'PP-00'
**$ UBA      ff  Status  Connection  
    18 18 1  1.  OPEN    FLOW-TO  'SURFACE'  REFLAYER
    17 18 1  1.  OPEN    FLOW-TO  1

*WELL 'PP-01'
**        dir rad    geofac wfac skin
**i  j   k  ff  status connection
**$          rad  geofac  wfrac  skin
GEOMETRY  I  0.0762  0.37  1.  0.
PERF  GEOA  'PP-01'
**$ UBA      ff  Status  Connection  
    13 18 1  1.  OPEN    FLOW-TO  'SURFACE'  REFLAYER
    12 18 1  1.  OPEN    FLOW-TO  1

*WELL 'PP-02'
**        dir rad    geofac wfac skin
**i  j   k  ff  status connection
**$          rad  geofac  wfrac  skin
GEOMETRY  I  0.0762  0.37  1.  0.
PERF  GEOA  'PP-02'
**$ UBA      ff  Status  Connection  
    26 12 2  1.  OPEN    FLOW-TO  'SURFACE'  REFLAYER
    25 12 2  1.  OPEN    FLOW-TO  1

*WELL 'PP-03'
**        dir rad    geofac wfac skin
**i  j   k  ff  status connection
**$          rad  geofac  wfrac  skin
GEOMETRY  J  0.0762  0.37  1.  0.
PERF  GEOA  'PP-03'
**$ UBA     ff  Status  Connection  
    35 7 2  1.  OPEN    FLOW-TO  'SURFACE'  REFLAYER
    35 6 2  1.  OPEN    FLOW-TO  1

*WELL 'PP-04'
**        dir rad    geofac wfac skin
**i  j   k  ff  status connection
**$          rad  geofac  wfrac  skin
GEOMETRY  J  0.0762  0.37  1.  0.
PERF  GEOA  'PP-04'
**$ UBA      ff  Status  Connection  
    41 21 1  1.  OPEN    FLOW-TO  'SURFACE'  REFLAYER
    41 20 1  1.  OPEN    FLOW-TO  1

*WELL 'PP-05'
**        dir rad    geofac wfac skin
**i  j   k  ff  status connection
**$          rad  geofac  wfrac  skin
GEOMETRY  J  0.0762  0.37  1.  0.
PERF  GEOA  'PP-05'
**$ UBA      ff  Status  Connection  
    34 17 2  1.  OPEN    FLOW-TO  'SURFACE'  REFLAYER
    34 16 2  1.  OPEN    FLOW-TO  1

*WELL 'PP-06'
**        dir rad    geofac wfac skin
**i  j   k  ff  status connection
**$          rad  geofac  wfrac  skin
GEOMETRY  J  0.0762  0.37  1.  0.
PERF  GEOA  'PP-06'
**$ UBA      ff  Status  Connection  
    33 12 1  1.  OPEN    FLOW-TO  'SURFACE'  REFLAYER
    33 11 1  1.  OPEN    FLOW-TO  1

*WELL 'PP-07'
**        dir rad    geofac wfac skin
**i  j   k  ff  status connection
**$          rad  geofac  wfrac  skin
GEOMETRY  J  0.0762  0.37  1.  0.
PERF  GEOA  'PP-07'
**$ UBA      ff  Status  Connection  
    36 19 2  1.  OPEN    FLOW-TO  'SURFACE'  REFLAYER
    36 18 2  1.  OPEN    FLOW-TO  1

*WELL 'PP-08'
**        dir rad    geofac wfac skin
**i  j   k  ff  status connection
**$          rad  geofac  wfrac  skin
GEOMETRY  I  0.0762  0.37  1.  0.
PERF  GEOA  'PP-08'
**$ UBA      ff  Status  Connection  
    16 13 1  1.  OPEN    FLOW-TO  'SURFACE'  REFLAYER
    17 13 1  1.  OPEN    FLOW-TO  1

*WELL 'PP-09'
**        dir rad    geofac wfac skin
**i  j   k  ff  status connection
**$          rad  geofac  wfrac  skin
GEOMETRY  I  0.0762  0.37  1.  0.
PERF  GEOA  'PP-09'
**$ UBA      ff  Status  Connection  
    25 15 1  1.  OPEN    FLOW-TO  'SURFACE'  REFLAYER
    26 15 1  1.  OPEN    FLOW-TO  1

*WELL 'PI-10'
**        dir rad    geofac wfac skin
**i  j   k  ff  status connection
**$          rad  geofac  wfrac  skin
GEOMETRY  I  0.0762  0.37  1.  0.
PERF  GEOA  'PI-10'
**$ UBA     ff  Status  Connection  
    18 6 5  1.  OPEN    FLOW-TO  'SURFACE'  REFLAYER
    19 6 5  1.  OPEN    FLOW-TO  1

*WELL 'PI-11'
**        dir rad    geofac wfac skin
**i  j   k  ff  status connection
**$          rad  geofac  wfrac  skin
GEOMETRY  I  0.0762  0.37  1.  0.
PERF  GEOA  'PI-11'
**$ UBA      ff  Status  Connection  
    18 24 5  1.  OPEN    FLOW-TO  'SURFACE'  REFLAYER
    19 24 5  1.  OPEN    FLOW-TO  1

*WELL 'PI-12'
**        dir rad    geofac wfac skin
**i  j   k  ff  status connection
**$          rad  geofac  wfrac  skin
GEOMETRY  I  0.0762  0.37  1.  0.
PERF  GEOA  'PI-12'
**$ UBA     ff  Status  Connection  
    26 6 4  1.  OPEN    FLOW-TO  'SURFACE'  REFLAYER
    27 6 4  1.  OPEN    FLOW-TO  1

*WELL 'PI-13'
**        dir rad    geofac wfac skin
**i  j   k  ff  status connection
**$          rad  geofac  wfrac  skin
GEOMETRY  I  0.0762  0.37  1.  0.
PERF  GEOA  'PI-13'
**$ UBA     ff  Status  Connection  
    7 11 5  1.  OPEN    FLOW-TO  'SURFACE'  REFLAYER
    8 11 5  1.  OPEN    FLOW-TO  1

*WELL 'PI-14'
**        dir rad    geofac wfac skin
**i  j   k  ff  status connection
**$          rad  geofac  wfrac  skin
GEOMETRY  J  0.0762  0.37  1.  0.
PERF  GEOA  'PI-14'
**$ UBA      ff  Status  Connection  
    38 13 6  1.  OPEN    FLOW-TO  'SURFACE'  REFLAYER
    38 14 6  1.  OPEN    FLOW-TO  1

*WELL 'PI-15'
**        dir rad    geofac wfac skin
**i  j   k  ff  status connection
**$          rad  geofac  wfrac  skin
GEOMETRY  I  0.0762  0.37  1.  0.
PERF  GEOA  'PI-15'
**$ UBA      ff  Status  Connection  
    29 23 5  1.  OPEN    FLOW-TO  'SURFACE'  REFLAYER
    28 23 5  1.  OPEN    FLOW-TO  1

*WELL 'PI-16'
**        dir rad    geofac wfac skin
**i  j   k  ff  status connection
**$          rad  geofac  wfrac  skin
GEOMETRY  J  0.0762  0.37  1.  0.
PERF  GEOA  'PI-16'
**$ UBA      ff  Status  Connection  
    36 24 5  1.  OPEN    FLOW-TO  'SURFACE'  REFLAYER
    36 25 5  1.  OPEN    FLOW-TO  1

*WELL 'PI-17'
**        dir rad    geofac wfac skin
**i  j   k  ff  status connection
**$          rad  geofac  wfrac  skin
GEOMETRY  J  0.0762  0.37  1.  0.
PERF  GEOA  'PI-17'
**$ UBA      ff  Status  Connection  
    31 15 6  1.  OPEN    FLOW-TO  'SURFACE'  REFLAYER
    31 14 6  1.  OPEN    FLOW-TO  1

** MANIFOLD PRODUCTION CONSTRAINTS

*GCONP 'Producao'
*MAX *STO 15900.0 *CONT
*MAX *STW 12879.2 *CONT
*MAX *STL 15900.0 *CONT

** MANIFOLD INJECTION CONSTRAINTS

*GCONI 'Injecao'
*MAX *STW 22260.0 *CONT

** WELL PRODUCTION CONSTRAINTS

*PRODUCER 'PP-00'
*OPERATE *MAX *STL 2500.0 *CONT *REPEAT
*OPERATE *MIN *BHP 190.0 *CONT *REPEAT
*MONITOR *MIN *STO 20.0 *SHUTIN
*MONITOR *WCUT 0.95 *SHUTIN
*MONITOR *GOR 400.0 *SHUTIN
*SHUTIN 'PP-00'

*PRODUCER 'PP-01'
*OPERATE *MAX *STL 2500.0 *CONT *REPEAT
*OPERATE *MIN *BHP 190.0 *CONT *REPEAT
*MONITOR *MIN *STO 20.0 *SHUTIN
*MONITOR *WCUT 0.95 *SHUTIN
*MONITOR *GOR 400.0 *SHUTIN
*SHUTIN 'PP-01'

*PRODUCER 'PP-02'
*OPERATE *MAX *STL 2500.0 *CONT *REPEAT
*OPERATE *MIN *BHP 190.0 *CONT *REPEAT
*MONITOR *MIN *STO 20.0 *SHUTIN
*MONITOR *WCUT 0.95 *SHUTIN
*MONITOR *GOR 400.0 *SHUTIN
*SHUTIN 'PP-02'

*PRODUCER 'PP-03'
*OPERATE *MAX *STL 2500.0 *CONT *REPEAT
*OPERATE *MIN *BHP 190.0 *CONT *REPEAT
*MONITOR *MIN *STO 20.0 *SHUTIN
*MONITOR *WCUT 0.95 *SHUTIN
*MONITOR *GOR 400.0 *SHUTIN
*SHUTIN 'PP-03'

*PRODUCER 'PP-04'
*OPERATE *MAX *STL 2500.0 *CONT *REPEAT
*OPERATE *MIN *BHP 190.0 *CONT *REPEAT
*MONITOR *MIN *STO 20.0 *SHUTIN
*MONITOR *WCUT 0.95 *SHUTIN
*MONITOR *GOR 400.0 *SHUTIN
*SHUTIN 'PP-04'

*PRODUCER 'PP-05'
*OPERATE *MAX *STL 2500.0 *CONT *REPEAT
*OPERATE *MIN *BHP 190.0 *CONT *REPEAT
*MONITOR *MIN *STO 20.0 *SHUTIN
*MONITOR *WCUT 0.95 *SHUTIN
*MONITOR *GOR 400.0 *SHUTIN
*SHUTIN 'PP-05'

*PRODUCER 'PP-06'
*OPERATE *MAX *STL 2500.0 *CONT *REPEAT
*OPERATE *MIN *BHP 190.0 *CONT *REPEAT
*MONITOR *MIN *STO 20.0 *SHUTIN
*MONITOR *WCUT 0.95 *SHUTIN
*MONITOR *GOR 400.0 *SHUTIN
*SHUTIN 'PP-06'

*PRODUCER 'PP-07'
*OPERATE *MAX *STL 2500.0 *CONT *REPEAT
*OPERATE *MIN *BHP 190.0 *CONT *REPEAT
*MONITOR *MIN *STO 20.0 *SHUTIN
*MONITOR *WCUT 0.95 *SHUTIN
*MONITOR *GOR 400.0 *SHUTIN
*SHUTIN 'PP-07'

*PRODUCER 'PP-08'
*OPERATE *MAX *STL 2500.0 *CONT *REPEAT
*OPERATE *MIN *BHP 190.0 *CONT *REPEAT
*MONITOR *MIN *STO 20.0 *SHUTIN
*MONITOR *WCUT 0.95 *SHUTIN
*MONITOR *GOR 400.0 *SHUTIN
*SHUTIN 'PP-08'

*PRODUCER 'PP-09'
*OPERATE *MAX *STL 2500.0 *CONT *REPEAT
*OPERATE *MIN *BHP 190.0 *CONT *REPEAT
*MONITOR *MIN *STO 20.0 *SHUTIN
*MONITOR *WCUT 0.95 *SHUTIN
*MONITOR *GOR 400.0 *SHUTIN
*SHUTIN 'PP-09'

** WELL INJECTION CONSTRAINTS

*INJECTOR 'PI-10'
*INCOMP *WATER
*OPERATE *MAX *STW 5000.0 *CONT *REPEAT
*OPERATE *MAX *BHP 350.0 *CONT *REPEAT
*SHUTIN 'PI-10'

*INJECTOR 'PI-11'
*INCOMP *WATER
*OPERATE *MAX *STW 5000.0 *CONT *REPEAT
*OPERATE *MAX *BHP 350.0 *CONT *REPEAT
*SHUTIN 'PI-11'

*INJECTOR 'PI-12'
*INCOMP *WATER
*OPERATE *MAX *STW 5000.0 *CONT *REPEAT
*OPERATE *MAX *BHP 350.0 *CONT *REPEAT
*SHUTIN 'PI-12'

*INJECTOR 'PI-13'
*INCOMP *WATER
*OPERATE *MAX *STW 5000.0 *CONT *REPEAT
*OPERATE *MAX *BHP 350.0 *CONT *REPEAT
*SHUTIN 'PI-13'

*INJECTOR 'PI-14'
*INCOMP *WATER
*OPERATE *MAX *STW 5000.0 *CONT *REPEAT
*OPERATE *MAX *BHP 350.0 *CONT *REPEAT
*SHUTIN 'PI-14'

*INJECTOR 'PI-15'
*INCOMP *WATER
*OPERATE *MAX *STW 5000.0 *CONT *REPEAT
*OPERATE *MAX *BHP 350.0 *CONT *REPEAT
*SHUTIN 'PI-15'

*INJECTOR 'PI-16'
*INCOMP *WATER
*OPERATE *MAX *STW 5000.0 *CONT *REPEAT
*OPERATE *MAX *BHP 350.0 *CONT *REPEAT
*SHUTIN 'PI-16'

*INJECTOR 'PI-17'
*INCOMP *WATER
*OPERATE *MAX *STW 5000.0 *CONT *REPEAT
*OPERATE *MAX *BHP 350.0 *CONT *REPEAT
*SHUTIN 'PI-17'

** PLATFORM EFFICIENCY

*ON-TIME 'Plataforma'
1.0

** MANIFOLD EFFICIENCY

*ON-TIME 'Producao'
1.0

*ON-TIME 'Injecao'
1.0

** WELL EFFICIENCY

*ON-TIME 'PP-00'
1.0

*ON-TIME 'PP-01'
1.0

*ON-TIME 'PP-02'
1.0

*ON-TIME 'PP-03'
1.0

*ON-TIME 'PP-04'
1.0

*ON-TIME 'PP-05'
1.0

*ON-TIME 'PP-06'
1.0

*ON-TIME 'PP-07'
1.0

*ON-TIME 'PP-08'
1.0

*ON-TIME 'PP-09'
1.0

*ON-TIME 'PI-10'
1.0

*ON-TIME 'PI-11'
1.0

*ON-TIME 'PI-12'
1.0

*ON-TIME 'PI-13'
1.0

*ON-TIME 'PI-14'
1.0

*ON-TIME 'PI-15'
1.0

*ON-TIME 'PI-16'
1.0

*ON-TIME 'PI-17'
1.0

*TIME 2345.0    ** DATE 2015 11 01

*OPEN 'PP-02'
GUIDEI  STW  'PI-10'
    5000.
*OPEN 'PI-10'

*TIME 2375.0    ** DATE 2015 12 01

*OPEN 'PP-03'
GUIDEI  STW  'PI-14'
    5000.
*OPEN 'PI-14'

*TIME 2406.0    ** DATE 2016 01 01

*OPEN 'PP-05'
GUIDEI  STW  'PI-16'
    5000.
*OPEN 'PI-16'

*TIME 2437.0    ** DATE 2016 02 01

*OPEN 'PP-00'
GUIDEI  STW  'PI-11'
    5000.
*OPEN 'PI-11'

*TIME 2466.0    ** DATE 2016 03 01

*OPEN 'PP-08'
GUIDEI  STW  'PI-13'
    5000.
*OPEN 'PI-13'

*TIME 2497.0    ** DATE 2016 04 01

*OPEN 'PP-04'
GUIDEI  STW  'PI-15'
    5000.
*OPEN 'PI-15'

*TIME 2527.0    ** DATE 2016 05 01

*OPEN 'PP-09'
GUIDEI  STW  'PI-17'
    5000.
*OPEN 'PI-17'

*TIME 2558.0    ** DATE 2016 06 01

*OPEN 'PP-06'
GUIDEI  STW  'PI-12'
    5000.
*OPEN 'PI-12'

*TIME 2588.0    ** DATE 2016 07 01

*OPEN 'PP-01'

*OPEN 'PP-07'

*TIME 2619.0    ** DATE 2016 08 01

*TIME 2650.0    ** DATE 2016 09 01

*TIME 2680.0    ** DATE 2016 10 01

*TIME 2711.0    ** DATE 2016 11 01

*TIME 2741.0    ** DATE 2016 12 01

*TIME 2772.0    ** DATE 2017 01 01

*TIME 2803.0    ** DATE 2017 02 01

*TIME 2831.0    ** DATE 2017 03 01

*TIME 2862.0    ** DATE 2017 04 01

*TIME 2892.0    ** DATE 2017 05 01

*TIME 2923.0    ** DATE 2017 06 01

*TIME 2953.0    ** DATE 2017 07 01

*TIME 2984.0    ** DATE 2017 08 01

*TIME 3015.0    ** DATE 2017 09 01

*TIME 3045.0    ** DATE 2017 10 01

*TIME 3076.0    ** DATE 2017 11 01

*TIME 3106.0    ** DATE 2017 12 01

*TIME 3137.0    ** DATE 2018 01 01

*TIME 3168.0    ** DATE 2018 02 01

*TIME 3196.0    ** DATE 2018 03 01

*TIME 3227.0    ** DATE 2018 04 01

*TIME 3257.0    ** DATE 2018 05 01

*TIME 3288.0    ** DATE 2018 06 01

*TIME 3318.0    ** DATE 2018 07 01

*TIME 3349.0    ** DATE 2018 08 01

*TIME 3380.0    ** DATE 2018 09 01

*TIME 3410.0    ** DATE 2018 10 01

*TIME 3441.0    ** DATE 2018 11 01

*TIME 3471.0    ** DATE 2018 12 01

*TIME 3502.0    ** DATE 2019 01 01

*TIME 3533.0    ** DATE 2019 02 01

*TIME 3561.0    ** DATE 2019 03 01

*TIME 3592.0    ** DATE 2019 04 01

*TIME 3622.0    ** DATE 2019 05 01

*TIME 3653.0    ** DATE 2019 06 01

*TIME 3683.0    ** DATE 2019 07 01

*TIME 3714.0    ** DATE 2019 08 01

*TIME 3745.0    ** DATE 2019 09 01

*TIME 3775.0    ** DATE 2019 10 01

*TIME 3806.0    ** DATE 2019 11 01

*TIME 3836.0    ** DATE 2019 12 01

*TIME 3867.0    ** DATE 2020 01 01

*TIME 3898.0    ** DATE 2020 02 01

*TIME 3927.0    ** DATE 2020 03 01

*TIME 3958.0    ** DATE 2020 04 01

*TIME 3988.0    ** DATE 2020 05 01

*TIME 4019.0    ** DATE 2020 06 01

*TIME 4049.0    ** DATE 2020 07 01

*TIME 4080.0    ** DATE 2020 08 01

*TIME 4111.0    ** DATE 2020 09 01

*TIME 4141.0    ** DATE 2020 10 01

*TIME 4172.0    ** DATE 2020 11 01

*TIME 4202.0    ** DATE 2020 12 01

*TIME 4233.0    ** DATE 2021 01 01

*TIME 4264.0    ** DATE 2021 02 01

*TIME 4292.0    ** DATE 2021 03 01

*TIME 4323.0    ** DATE 2021 04 01

*TIME 4353.0    ** DATE 2021 05 01

*TIME 4384.0    ** DATE 2021 06 01

*TIME 4414.0    ** DATE 2021 07 01

*TIME 4445.0    ** DATE 2021 08 01

*TIME 4476.0    ** DATE 2021 09 01

*TIME 4506.0    ** DATE 2021 10 01

*TIME 4537.0    ** DATE 2021 11 01

*TIME 4567.0    ** DATE 2021 12 01

*TIME 4598.0    ** DATE 2022 01 01

*TIME 4629.0    ** DATE 2022 02 01

*TIME 4657.0    ** DATE 2022 03 01

*TIME 4688.0    ** DATE 2022 04 01

*TIME 4718.0    ** DATE 2022 05 01

*TIME 4749.0    ** DATE 2022 06 01

*TIME 4779.0    ** DATE 2022 07 01

*TIME 4810.0    ** DATE 2022 08 01

*TIME 4841.0    ** DATE 2022 09 01

*TIME 4871.0    ** DATE 2022 10 01

*TIME 4902.0    ** DATE 2022 11 01

*TIME 4932.0    ** DATE 2022 12 01

*TIME 4963.0    ** DATE 2023 01 01

*TIME 4994.0    ** DATE 2023 02 01

*TIME 5022.0    ** DATE 2023 03 01

*TIME 5053.0    ** DATE 2023 04 01

*TIME 5083.0    ** DATE 2023 05 01

*TIME 5114.0    ** DATE 2023 06 01

*TIME 5144.0    ** DATE 2023 07 01

*TIME 5175.0    ** DATE 2023 08 01

*TIME 5206.0    ** DATE 2023 09 01

*TIME 5236.0    ** DATE 2023 10 01

*TIME 5267.0    ** DATE 2023 11 01

*TIME 5297.0    ** DATE 2023 12 01

*TIME 5328.0    ** DATE 2024 01 01

*TIME 5359.0    ** DATE 2024 02 01

*TIME 5388.0    ** DATE 2024 03 01

*TIME 5419.0    ** DATE 2024 04 01

*TIME 5449.0    ** DATE 2024 05 01

*TIME 5480.0    ** DATE 2024 06 01

*TIME 5510.0    ** DATE 2024 07 01

*TIME 5541.0    ** DATE 2024 08 01

*TIME 5572.0    ** DATE 2024 09 01

*TIME 5602.0    ** DATE 2024 10 01

*TIME 5633.0    ** DATE 2024 11 01

*TIME 5663.0    ** DATE 2024 12 01

*TIME 5694.0    ** DATE 2025 01 01

*TIME 5725.0    ** DATE 2025 02 01

*TIME 5753.0    ** DATE 2025 03 01

*TIME 5784.0    ** DATE 2025 04 01

*TIME 5814.0    ** DATE 2025 05 01

*TIME 5845.0    ** DATE 2025 06 01

*TIME 5875.0    ** DATE 2025 07 01

*TIME 5906.0    ** DATE 2025 08 01

*TIME 5937.0    ** DATE 2025 09 01

*TIME 5967.0    ** DATE 2025 10 01

*TIME 5998.0    ** DATE 2025 11 01

*TIME 6028.0    ** DATE 2025 12 01

*TIME 6059.0    ** DATE 2026 01 01

*TIME 6090.0    ** DATE 2026 02 01

*TIME 6118.0    ** DATE 2026 03 01

*TIME 6149.0    ** DATE 2026 04 01

*TIME 6179.0    ** DATE 2026 05 01

*TIME 6210.0    ** DATE 2026 06 01

*TIME 6240.0    ** DATE 2026 07 01

*TIME 6271.0    ** DATE 2026 08 01

*TIME 6302.0    ** DATE 2026 09 01

*TIME 6332.0    ** DATE 2026 10 01

*TIME 6363.0    ** DATE 2026 11 01

*TIME 6393.0    ** DATE 2026 12 01

*TIME 6424.0    ** DATE 2027 01 01

*TIME 6455.0    ** DATE 2027 02 01

*TIME 6483.0    ** DATE 2027 03 01

*TIME 6514.0    ** DATE 2027 04 01

*TIME 6544.0    ** DATE 2027 05 01

*TIME 6575.0    ** DATE 2027 06 01

*TIME 6605.0    ** DATE 2027 07 01

*TIME 6636.0    ** DATE 2027 08 01

*TIME 6667.0    ** DATE 2027 09 01

*TIME 6697.0    ** DATE 2027 10 01

*TIME 6728.0    ** DATE 2027 11 01

*TIME 6758.0    ** DATE 2027 12 01

*TIME 6789.0    ** DATE 2028 01 01

*TIME 6820.0    ** DATE 2028 02 01

*TIME 6849.0    ** DATE 2028 03 01

*TIME 6880.0    ** DATE 2028 04 01

*TIME 6910.0    ** DATE 2028 05 01

*TIME 6941.0    ** DATE 2028 06 01

*TIME 6971.0    ** DATE 2028 07 01

*TIME 7002.0    ** DATE 2028 08 01

*TIME 7033.0    ** DATE 2028 09 01

*TIME 7063.0    ** DATE 2028 10 01

*TIME 7094.0    ** DATE 2028 11 01

*TIME 7124.0    ** DATE 2028 12 01

*TIME 7155.0    ** DATE 2029 01 01

*TIME 7186.0    ** DATE 2029 02 01

*TIME 7214.0    ** DATE 2029 03 01

*TIME 7245.0    ** DATE 2029 04 01

*TIME 7275.0    ** DATE 2029 05 01

*TIME 7306.0    ** DATE 2029 06 01

*TIME 7336.0    ** DATE 2029 07 01

*TIME 7367.0    ** DATE 2029 08 01

*TIME 7398.0    ** DATE 2029 09 01

*TIME 7428.0    ** DATE 2029 10 01

*TIME 7459.0    ** DATE 2029 11 01

*TIME 7489.0    ** DATE 2029 12 01

*TIME 7520.0    ** DATE 2030 01 01

*TIME 7551.0    ** DATE 2030 02 01

*TIME 7579.0    ** DATE 2030 03 01

*TIME 7610.0    ** DATE 2030 04 01

*TIME 7640.0    ** DATE 2030 05 01

*TIME 7671.0    ** DATE 2030 06 01

*TIME 7701.0    ** DATE 2030 07 01

*TIME 7732.0    ** DATE 2030 08 01

*TIME 7763.0    ** DATE 2030 09 01

*TIME 7793.0    ** DATE 2030 10 01

*TIME 7824.0    ** DATE 2030 11 01

*TIME 7854.0    ** DATE 2030 12 01

*TIME 7885.0    ** DATE 2031 01 01

*TIME 7916.0    ** DATE 2031 02 01

*TIME 7944.0    ** DATE 2031 03 01

*TIME 7975.0    ** DATE 2031 04 01

*TIME 8005.0    ** DATE 2031 05 01

*TIME 8036.0    ** DATE 2031 06 01

*TIME 8066.0    ** DATE 2031 07 01

*TIME 8097.0    ** DATE 2031 08 01

*TIME 8128.0    ** DATE 2031 09 01

*TIME 8158.0    ** DATE 2031 10 01

*TIME 8189.0    ** DATE 2031 11 01

*TIME 8219.0    ** DATE 2031 12 01

*TIME 8250.0    ** DATE 2032 01 01

*TIME 8281.0    ** DATE 2032 02 01

*TIME 8310.0    ** DATE 2032 03 01

*TIME 8341.0    ** DATE 2032 04 01

*TIME 8371.0    ** DATE 2032 05 01

*TIME 8402.0    ** DATE 2032 06 01

*TIME 8432.0    ** DATE 2032 07 01

*TIME 8463.0    ** DATE 2032 08 01

*TIME 8494.0    ** DATE 2032 09 01

*TIME 8524.0    ** DATE 2032 10 01

*TIME 8555.0    ** DATE 2032 11 01

*TIME 8585.0    ** DATE 2032 12 01

*TIME 8616.0    ** DATE 2033 01 01

*TIME 8647.0    ** DATE 2033 02 01

*TIME 8675.0    ** DATE 2033 03 01

*TIME 8706.0    ** DATE 2033 04 01

*TIME 8736.0    ** DATE 2033 05 01

*TIME 8767.0    ** DATE 2033 06 01

*TIME 8797.0    ** DATE 2033 07 01

*TIME 8828.0    ** DATE 2033 08 01

*TIME 8859.0    ** DATE 2033 09 01

*TIME 8889.0    ** DATE 2033 10 01

*TIME 8920.0    ** DATE 2033 11 01

*TIME 8950.0    ** DATE 2033 12 01

*TIME 8981.0    ** DATE 2034 01 01

*TIME 9012.0    ** DATE 2034 02 01

*TIME 9040.0    ** DATE 2034 03 01

*TIME 9071.0    ** DATE 2034 04 01

*TIME 9101.0    ** DATE 2034 05 01

*TIME 9132.0    ** DATE 2034 06 01

*TIME 9162.0    ** DATE 2034 07 01

*TIME 9193.0    ** DATE 2034 08 01

*TIME 9224.0    ** DATE 2034 09 01

*TIME 9254.0    ** DATE 2034 10 01

*TIME 9285.0    ** DATE 2034 11 01

*TIME 9315.0    ** DATE 2034 12 01

*TIME 9346.0    ** DATE 2035 01 01

*TIME 9377.0    ** DATE 2035 02 01

*TIME 9405.0    ** DATE 2035 03 01

*TIME 9436.0    ** DATE 2035 04 01

*TIME 9466.0    ** DATE 2035 05 01

*TIME 9497.0    ** DATE 2035 06 01

*TIME 9527.0    ** DATE 2035 07 01

*TIME 9558.0    ** DATE 2035 08 01

*TIME 9589.0    ** DATE 2035 09 01

*TIME 9619.0    ** DATE 2035 10 01

*TIME 9650.0    ** DATE 2035 11 01

*TIME 9680.0    ** DATE 2035 12 01

*TIME 9711.0    ** DATE 2036 01 01

*TIME 9742.0    ** DATE 2036 02 01

*TIME 9771.0    ** DATE 2036 03 01

*TIME 9802.0    ** DATE 2036 04 01

*TIME 9832.0    ** DATE 2036 05 01

*TIME 9863.0    ** DATE 2036 06 01

*TIME 9893.0    ** DATE 2036 07 01

*TIME 9924.0    ** DATE 2036 08 01

*TIME 9955.0    ** DATE 2036 09 01

*TIME 9985.0    ** DATE 2036 10 01

*TIME 10016.0    ** DATE 2036 11 01

*TIME 10046.0    ** DATE 2036 12 01

*TIME 10077.0    ** DATE 2037 01 01

*TIME 10108.0    ** DATE 2037 02 01

*TIME 10136.0    ** DATE 2037 03 01

*TIME 10167.0    ** DATE 2037 04 01

*TIME 10197.0    ** DATE 2037 05 01

*TIME 10228.0    ** DATE 2037 06 01

*TIME 10258.0    ** DATE 2037 07 01

*TIME 10289.0    ** DATE 2037 08 01

*TIME 10320.0    ** DATE 2037 09 01

*TIME 10350.0    ** DATE 2037 10 01

*TIME 10381.0    ** DATE 2037 11 01

*TIME 10411.0    ** DATE 2037 12 01

*TIME 10442.0    ** DATE 2038 01 01

*TIME 10473.0    ** DATE 2038 02 01

*TIME 10501.0    ** DATE 2038 03 01

*TIME 10532.0    ** DATE 2038 04 01

*TIME 10562.0    ** DATE 2038 05 01

*TIME 10593.0    ** DATE 2038 06 01

*TIME 10623.0    ** DATE 2038 07 01

*TIME 10654.0    ** DATE 2038 08 01

*TIME 10685.0    ** DATE 2038 09 01

*TIME 10715.0    ** DATE 2038 10 01

*TIME 10746.0    ** DATE 2038 11 01

*TIME 10776.0    ** DATE 2038 12 01

*TIME 10807.0    ** DATE 2039 01 01

*TIME 10838.0    ** DATE 2039 02 01

*TIME 10866.0    ** DATE 2039 03 01

*TIME 10897.0    ** DATE 2039 04 01

*TIME 10927.0    ** DATE 2039 05 01

*TIME 10958.0    ** DATE 2039 06 01

** STRATEGY_END


*STOP

