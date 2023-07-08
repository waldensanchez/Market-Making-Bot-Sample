
"""
# -- --------------------------------------------------------------------------------------------------- -- #
# -- project: A SHORT DESCRIPTION OF THE PROJECT                                                         -- #
# -- script: functions.py : python script with general functions                                         -- #
# -- author: YOUR GITHUB USER NAME                                                                       -- #
# -- license: THE LICENSE TYPE AS STATED IN THE REPOSITORY                                               -- #
# -- repository: YOUR REPOSITORY URL                                                                     -- #
# -- --------------------------------------------------------------------------------------------------- -- #
"""
# Importa libraries
import scipy.stats as stats

# Functions
def price_crypto(sqrt_price, dec_token_1, dec_token_2):
    return int( dec_token_1/dec_token_2 )*( 1/( sqrt_price/(2**96) )**2 )

def test_statistical_zero(data):
    # Perform one-sample t-test
    t_statistic, p_value = stats.ttest_1samp(data, 0)

    # Set the significance level
    alpha = 0.05

    if p_value < alpha:
        print("The values in the list are statistically zero.")
        
    else:
        print("The values in the list are statistically different from zero.")