

```python
import tsfresh
```

# 准备数据

- timeseries
- y


```python
from tsfresh.examples.robot_execution_failures import download_robot_execution_failures, load_robot_execution_failures
download_robot_execution_failures()
timeseries, y = load_robot_execution_failures()
```

- There are six different time series (a-f) for the different sensors. The different robots are denoted by the ids column.


```python
timeseries.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>time</th>
      <th>F_x</th>
      <th>F_y</th>
      <th>F_z</th>
      <th>T_x</th>
      <th>T_y</th>
      <th>T_z</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>0</td>
      <td>-1</td>
      <td>-1</td>
      <td>63</td>
      <td>-3</td>
      <td>-1</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>1</td>
      <td>0</td>
      <td>0</td>
      <td>62</td>
      <td>-3</td>
      <td>-1</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>1</td>
      <td>2</td>
      <td>-1</td>
      <td>-1</td>
      <td>61</td>
      <td>-3</td>
      <td>0</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>1</td>
      <td>3</td>
      <td>-1</td>
      <td>-1</td>
      <td>63</td>
      <td>-2</td>
      <td>-1</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>1</td>
      <td>4</td>
      <td>-1</td>
      <td>-1</td>
      <td>63</td>
      <td>-3</td>
      <td>-1</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>



- `y` contains the information which robot id reported a failure and which not


```python
y.head()
```




    1    True
    2    True
    3    True
    4    True
    5    True
    dtype: bool



# extract

- Tsfresh allows us to automatically extract over 1200 features from those six different time series for each robot.

- For extracting all features, we use `extract_features`
- 参数
    - column_id: The name of the id column to group by. type: str
    - column_sort: The name of the sort column. type: str


```python
from tsfresh import extract_features
extracted_features = extract_features(timeseries, column_id="id", column_sort="time")
```

    Feature Extraction: 100%|██████████| 10/10 [00:29<00:00,  2.46s/it]



```python
extracted_features.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>variable</th>
      <th>F_x__abs_energy</th>
      <th>F_x__absolute_sum_of_changes</th>
      <th>F_x__agg_autocorrelation__f_agg_"mean"__maxlag_40</th>
      <th>F_x__agg_autocorrelation__f_agg_"median"__maxlag_40</th>
      <th>F_x__agg_autocorrelation__f_agg_"var"__maxlag_40</th>
      <th>F_x__agg_linear_trend__f_agg_"max"__chunk_len_10__attr_"intercept"</th>
      <th>F_x__agg_linear_trend__f_agg_"max"__chunk_len_10__attr_"rvalue"</th>
      <th>F_x__agg_linear_trend__f_agg_"max"__chunk_len_10__attr_"slope"</th>
      <th>F_x__agg_linear_trend__f_agg_"max"__chunk_len_10__attr_"stderr"</th>
      <th>F_x__agg_linear_trend__f_agg_"max"__chunk_len_50__attr_"intercept"</th>
      <th>...</th>
      <th>T_z__symmetry_looking__r_0.9</th>
      <th>T_z__symmetry_looking__r_0.9500000000000001</th>
      <th>T_z__time_reversal_asymmetry_statistic__lag_1</th>
      <th>T_z__time_reversal_asymmetry_statistic__lag_2</th>
      <th>T_z__time_reversal_asymmetry_statistic__lag_3</th>
      <th>T_z__value_count__value_-1</th>
      <th>T_z__value_count__value_0</th>
      <th>T_z__value_count__value_1</th>
      <th>T_z__variance</th>
      <th>T_z__variance_larger_than_standard_deviation</th>
    </tr>
    <tr>
      <th>id</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>14.0</td>
      <td>2.0</td>
      <td>-0.106351</td>
      <td>-7.206633e-02</td>
      <td>0.016879</td>
      <td>0.0</td>
      <td>-1.0</td>
      <td>-1.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.0</td>
      <td>15.0</td>
      <td>0.0</td>
      <td>0.000000</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>25.0</td>
      <td>14.0</td>
      <td>-0.039098</td>
      <td>-4.935275e-02</td>
      <td>0.088790</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>...</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>4.0</td>
      <td>11.0</td>
      <td>0.0</td>
      <td>0.195556</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>12.0</td>
      <td>10.0</td>
      <td>-0.029815</td>
      <td>3.035766e-17</td>
      <td>0.105435</td>
      <td>1.0</td>
      <td>-1.0</td>
      <td>-2.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>...</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>0.000000</td>
      <td>-0.090909</td>
      <td>0.000000</td>
      <td>4.0</td>
      <td>11.0</td>
      <td>0.0</td>
      <td>0.195556</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>16.0</td>
      <td>17.0</td>
      <td>-0.049773</td>
      <td>-6.417112e-02</td>
      <td>0.143580</td>
      <td>1.0</td>
      <td>-1.0</td>
      <td>-1.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>...</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>0.000000</td>
      <td>-0.181818</td>
      <td>0.000000</td>
      <td>6.0</td>
      <td>8.0</td>
      <td>1.0</td>
      <td>0.355556</td>
      <td>0.0</td>
    </tr>
    <tr>
      <th>5</th>
      <td>17.0</td>
      <td>13.0</td>
      <td>-0.061467</td>
      <td>-5.172414e-02</td>
      <td>0.052642</td>
      <td>2.0</td>
      <td>-1.0</td>
      <td>-2.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>...</td>
      <td>1.0</td>
      <td>1.0</td>
      <td>-0.076923</td>
      <td>-0.090909</td>
      <td>-0.222222</td>
      <td>4.0</td>
      <td>9.0</td>
      <td>2.0</td>
      <td>0.382222</td>
      <td>0.0</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 4764 columns</p>
</div>



# impute and select

- end up with a DataFrame extracted_features with all more than 1200 different extracted features.
- now remove all NaN values and select only the relevant features
    - `impute`
        * -inf -> min
        * +inf -> max
        * NaN -> median
    - `select_features`
        - Check the significance of all features (columns) of feature matrix X and return a possibly reduced feature matrix
    only containing relevant features.
        - X 必须是 一列id 其余列feature


```python
from tsfresh import select_features
from tsfresh.utilities.dataframe_functions import impute

impute(extracted_features)
features_filtered = select_features(extracted_features, y)
```


```python
features_filtered.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th>variable</th>
      <th>F_x__value_count__value_-1</th>
      <th>F_x__abs_energy</th>
      <th>F_x__range_count__max_1__min_-1</th>
      <th>F_y__abs_energy</th>
      <th>T_y__standard_deviation</th>
      <th>T_y__variance</th>
      <th>F_x__fft_coefficient__coeff_1__attr_"abs"</th>
      <th>T_y__fft_coefficient__coeff_1__attr_"abs"</th>
      <th>T_y__abs_energy</th>
      <th>F_z__standard_deviation</th>
      <th>...</th>
      <th>T_z__large_standard_deviation__r_0.35000000000000003</th>
      <th>T_z__quantile__q_0.9</th>
      <th>F_z__agg_linear_trend__f_agg_"max"__chunk_len_5__attr_"intercept"</th>
      <th>T_x__agg_autocorrelation__f_agg_"mean"__maxlag_40</th>
      <th>F_y__change_quantiles__f_agg_"var"__isabs_False__qh_1.0__ql_0.8</th>
      <th>T_x__spkt_welch_density__coeff_5</th>
      <th>T_y__agg_linear_trend__f_agg_"min"__chunk_len_5__attr_"intercept"</th>
      <th>F_y__change_quantiles__f_agg_"var"__isabs_False__qh_0.6__ql_0.2</th>
      <th>F_z__agg_linear_trend__f_agg_"max"__chunk_len_10__attr_"intercept"</th>
      <th>F_z__change_quantiles__f_agg_"var"__isabs_False__qh_0.8__ql_0.4</th>
    </tr>
    <tr>
      <th>id</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>1</th>
      <td>14.0</td>
      <td>14.0</td>
      <td>15.0</td>
      <td>13.0</td>
      <td>0.471405</td>
      <td>0.222222</td>
      <td>1.000000</td>
      <td>1.165352</td>
      <td>10.0</td>
      <td>1.203698</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>62.833333</td>
      <td>-0.095589</td>
      <td>0.209184</td>
      <td>0.037795</td>
      <td>-1.000000</td>
      <td>0.000000</td>
      <td>63.0</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>2</th>
      <td>7.0</td>
      <td>25.0</td>
      <td>13.0</td>
      <td>76.0</td>
      <td>2.054805</td>
      <td>4.222222</td>
      <td>0.624118</td>
      <td>6.020261</td>
      <td>90.0</td>
      <td>4.333846</td>
      <td>...</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>64.666667</td>
      <td>-0.054604</td>
      <td>0.000000</td>
      <td>0.319311</td>
      <td>-1.000000</td>
      <td>0.222222</td>
      <td>70.0</td>
      <td>2.666667</td>
    </tr>
    <tr>
      <th>3</th>
      <td>11.0</td>
      <td>12.0</td>
      <td>14.0</td>
      <td>40.0</td>
      <td>1.768867</td>
      <td>3.128889</td>
      <td>2.203858</td>
      <td>8.235442</td>
      <td>103.0</td>
      <td>4.616877</td>
      <td>...</td>
      <td>1.0</td>
      <td>0.0</td>
      <td>67.333333</td>
      <td>-0.061050</td>
      <td>0.000000</td>
      <td>9.102780</td>
      <td>-3.000000</td>
      <td>0.250000</td>
      <td>68.0</td>
      <td>8.187500</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5.0</td>
      <td>16.0</td>
      <td>10.0</td>
      <td>60.0</td>
      <td>2.669998</td>
      <td>7.128889</td>
      <td>0.844394</td>
      <td>12.067855</td>
      <td>124.0</td>
      <td>3.833188</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>63.666667</td>
      <td>-0.133794</td>
      <td>1.555556</td>
      <td>56.910262</td>
      <td>-3.166667</td>
      <td>1.360000</td>
      <td>66.0</td>
      <td>1.000000</td>
    </tr>
    <tr>
      <th>5</th>
      <td>9.0</td>
      <td>17.0</td>
      <td>13.0</td>
      <td>46.0</td>
      <td>2.039608</td>
      <td>4.160000</td>
      <td>2.730599</td>
      <td>6.445330</td>
      <td>180.0</td>
      <td>4.841487</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.6</td>
      <td>64.333333</td>
      <td>-0.106108</td>
      <td>0.000000</td>
      <td>22.841805</td>
      <td>-4.166667</td>
      <td>1.040000</td>
      <td>67.0</td>
      <td>0.000000</td>
    </tr>
  </tbody>
</table>
<p>5 rows × 631 columns</p>
</div>



# extract, impute and select at the same time

- Further, you can even perform the extraction, imputing and filtering at the same time with the `tsfresh.extract_relevant_features()` function:


```python
from tsfresh import extract_relevant_features

features_filtered_direct = extract_relevant_features(timeseries, y,
                                                     column_id='id', column_sort='time')
```

- now use the features contained in the DataFrame features_filtered (which is equal to features_filtered_direct) in conjunction with y to train your classification model
