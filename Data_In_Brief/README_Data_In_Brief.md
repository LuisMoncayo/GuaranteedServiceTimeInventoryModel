# Compute the Safety Stock Cost in Table 1

In the file **main.py**, teh user must select the supply chain instance to analyse. In this example, we evaluate all 38 supply chains simultaneously.

```{python}
list_instances = ['01','02','03','04','05','06','07','08','09','10',
                  '11','12','13','14','15','16','17','18','19','20',
                  '21','22','23','24','25','26','27','28','29','30',
                  '31','32','33','34','35','36','37','38']
```
The service level $\alpha$ and the guaranteed service time $\Phi$ are set based on the data from the file **file_name = "MSOM-06-038-R2 Data Set in Excel.xls"**. The reader has to set the holding cost $I$ that by default is 20%/year.

