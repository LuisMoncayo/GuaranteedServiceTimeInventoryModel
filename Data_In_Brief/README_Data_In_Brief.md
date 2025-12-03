# Compute the Safety Stock Cost in Table 1

In the file **main.py**, the user selects which supply chain instances to analyse. In this example, all 38 instances are evaluated simultaneously.


```{python}
list_instances = ['01','02','03','04','05','06','07','08','09','10',
                  '11','12','13','14','15','16','17','18','19','20',
                  '21','22','23','24','25','26','27','28','29','30',
                  '31','32','33','34','35','36','37','38']
```
The service level $\alpha$ and the guaranteed service time $\Phi$ are set based on the data from the file **file_name = "MSOM-06-038-R2 Data Set in Excel.xls"**. The reader has to set the holding cost $I$ that by default is 20%/year.

In line 266 of the file **main.py**, the user must set the time $T$ in which the algorithm must stop if the Gurobi B&C Algorithm does not find a better solution. In the below figure, the time is set to 10 minutes (or 60*10 second).

```{python}
# Terminate if objective has not improved in 20s
if time.time() - model._time > 60*10:
  model.terminate()
```

