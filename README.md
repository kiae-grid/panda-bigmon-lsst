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

 * 'time_profiler_output': base filename for time profiler output.
   Used to construct file name which will be concatenated with
   the corresponding extension (.csv/.txt) and timings will be
   put there.  By-default, file name is based on the query parameters
   and is rather long: that is not convinient in some cases.
