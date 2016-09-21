# expertoption_test

Random Data
--------------------

expertoption_test=# select count(id) from expertoption_deal;
count
11909810
(1 row)

expertoption_test=# select count(id) from expertoption_transaction;
11909810
(1 row)

expertoption_test=# select count(id) from expertoption_trader;
20100
(1 row)


 Table Screenshot
-------------------
![Alt text](/images/table1.png?raw=true "Table")

 Load Page Time
---------------------
2016-08-28 12:20:11,031 DEBUG app.utils _get_history_deals_data 0.017056941986083984 (sec)

2016-08-28 12:20:11,046 DEBUG app.utils _get_history_deposit_data 0.01406407356262207 (sec)

2016-08-28 08:00:50,236 DEBUG app.utils view 2.395364046096802 (sec)

