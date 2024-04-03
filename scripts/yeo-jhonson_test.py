from scipy.stats import yeojohnson, shapiro
from scipy.special import inv_boxcox
import numpy as np
from scipy.stats import norm

# Generate some non-normal data
data = np.random.exponential(scale=2, size=100)

# Apply Yeo-Johnson transformation
transformed_data, lambda_param = yeojohnson(data)
original_data = inv_boxcox(transformed_data, lambda_param)

statistic, p_value = shapiro(transformed_data)
if data.all() == original_data.all():
    print("Inverse equals original")
print("Shapiro-Wilk Test p-value:", p_value)