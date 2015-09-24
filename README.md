panda-bigmon-lsst
=================

BigPanDA monitoring - LSST


NoSQL parameters
----------------

Query parameters that are relevant to the NoSQL part.

 * nosql: turns on NoSQL processing; supported values:
   - [LEGACY] 'day_site_errors_cnt': same as 'day_anything_errors_cnt'.
   - [LEGACY] 'day_user_errors_cnt': same as 'day_anything_errors_cnt'.
   - 'day_anything_errors_cnt': uses aggregated tables
     day_[site,user]_errors_cnt for table creation.
   - 'jobs': uses NoSQL jobs table for direct queries with no
     pre-aggregation.

 * 'nosql_interval': aggregation interval; supported values are
   '1m' (minute), '30m' (1/2 hour), '1d' (day), '10d' (10 days).
