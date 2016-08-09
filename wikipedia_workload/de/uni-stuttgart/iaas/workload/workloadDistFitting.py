import warnings
import numpy as np
import pandas as pd
import scipy.stats as st
import statsmodels as sm
import matplotlib
import matplotlib.pyplot as plt
import datetime


from workload import constants as cs
from workload import WorkloadSummary as ws


matplotlib.rcParams['figure.figsize'] = (16.0, 12.0)
matplotlib.style.use('ggplot')

# Create models from data
def best_fit_distribution(data, bins=200, ax=None):
    """Model data by finding best fit distribution to data"""
    # Get histogram of original data
    y, x = np.histogram(data, bins=bins, normed=True)
    x = (x + np.roll(x, -1))[:-1] / 2.0

    # Distributions to check
    DISTRIBUTIONS = [
        st.alpha,st.anglit,st.arcsine,st.beta,st.betaprime,st.bradford,st.burr,st.cauchy,st.chi,st.chi2,st.cosine,
        st.dgamma,st.dweibull,st.erlang,st.expon,st.exponnorm,st.exponweib,st.exponpow,st.f,st.fatiguelife,st.fisk,
        st.foldcauchy,st.foldnorm,st.frechet_r,st.frechet_l,st.genlogistic,st.genpareto,st.gennorm,st.genexpon,
        st.genextreme,st.gausshyper,st.gamma,st.gengamma,st.genhalflogistic,st.gilbrat,st.gompertz,st.gumbel_r,
        st.gumbel_l,st.halfcauchy,st.halflogistic,st.halfnorm,st.halfgennorm,st.hypsecant,st.invgamma,st.invgauss,
        st.invweibull,st.johnsonsb,st.johnsonsu,st.ksone,st.kstwobign,st.laplace,st.levy,st.levy_l,st.levy_stable,
        st.logistic,st.loggamma,st.loglaplace,st.lognorm,st.lomax,st.maxwell,st.mielke,st.nakagami,st.ncx2,st.ncf,
        st.nct,st.norm,st.pareto,st.pearson3,st.powerlaw,st.powerlognorm,st.powernorm,st.rdist,st.reciprocal,
        st.rayleigh,st.rice,st.recipinvgauss,st.semicircular,st.t,st.triang,st.truncexpon,st.truncnorm,st.tukeylambda,
        st.uniform,st.vonmises,st.vonmises_line,st.wald,st.weibull_min,st.weibull_max,st.wrapcauchy
    ]

    # Best holders
    best_distribution = st.norm
    best_params = (0.0, 1.0)
    best_sse = np.inf

    # Estimate distribution parameters from data
    for distribution in DISTRIBUTIONS:

        # Try to fit the distribution
        try:
            # Ignore warnings from data that can't be fit
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')

                # fit dist to data
                params = distribution.fit(data)

                # Separate parts of parameters
                arg = params[:-2]
                loc = params[-2]
                scale = params[-1]

                # Calculate fitted PDF and error with fit in distribution
                pdf = distribution.pdf(x, loc=loc, scale=scale, *arg)
                sse = np.sum(np.power(y - pdf, 2.0))

                # if axis pass in add to plot
                try:
                    if ax:
                        pd.Series(pdf, x).plot(ax=ax)
                    #end
                except Exception:
                    pass

                # identify if this distribution is better
                if best_sse > sse > 0:
                    best_distribution = distribution
                    best_params = params
                    best_sse = sse

        except Exception:
            pass

    return (best_distribution.name, best_params)

def make_pdf(dist, params, size=10000):
    """Generate distributions's Propbability Distribution Function """

    # Separate parts of parameters
    arg = params[:-2]
    loc = params[-2]
    scale = params[-1]

    # Get sane start and end points of distribution
    start = dist.ppf(0.01, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.01, loc=loc, scale=scale)
    end = dist.ppf(0.99, *arg, loc=loc, scale=scale) if arg else dist.ppf(0.99, loc=loc, scale=scale)

    # Build PDF and turn into pandas Series
    x = np.linspace(start, end, size)
    y = dist.pdf(x, loc=loc, scale=scale, *arg)
    pdf = pd.Series(y, x)

    return pdf





###### Loading and Fitting Data

def load_and_fit_data(fileName='', df=None, bins=200):

    if fileName != '':
        df = pd.read_csv(fileName, delimiter=' ')

        df.columns = [cs.WORKLOAD_SUMMARY_STAT_TIMESTAMP,
                       cs.WORKLOAD_SUMMARY_STAT_COUNT_REQ,
                       cs.WORKLOAD_SUMMARY_STAT_COUNT_BYTES,
                       cs.WORKLOAD_SUMMARY_STAT_MEAN_REQ,
                       cs.WORKLOAD_SUMMARY_STAT_MEAN_BYTES,
                       cs.WORKLOAD_SUMMARY_STAT_STD_REQ,
                       cs.WORKLOAD_SUMMARY_STAT_STD_BYTES,
                       cs.WORKLOAD_SUMMARY_STAT_MAX_REQ,
                       cs.WORKLOAD_SUMMARY_STAT_MAX_BYTES,
                        cs.WORKLOAD_SUMMARY_STAT_SUM_REQ,
                        cs.WORKLOAD_SUMMARY_STAT_SUM_BYTES]

        df = ws.WorkloadSummary.sortOccurrencesPerTimeStamp(df=df, timestampColName=cs.WORKLOAD_SUMMARY_STAT_TIMESTAMP)
        # Getting TimeStamp for X-Axis
        timeStamp_list = df[cs.WORKLOAD_SUMMARY_STAT_TIMESTAMP].tolist()
        date_list = []
        for i in timeStamp_list:
            date_list.append(datetime.datetime.fromtimestamp(i))
    else:
        timeStamp_list = range(1, 31)

    data = df[cs.WORKLOAD_SUMMARY_STAT_SUM_REQ]
    #data = df[cs.WORKLOAD_SUMMARY_STAT_SUM_BYTES]

    # Plot for comparison
    plt.figure(figsize=(12,8))
    #ax = data.plot(kind='hist', bins=50, normed=True, alpha=0.5, color=plt.rcParams['axes.color_cycle'][1])
    ax = data.plot(kind='hist', bins=bins, normed=True, alpha=0.5, color='black')
    # Save plot limits
    dataYLim = ax.get_ylim()

    # Find best fit distribution
    best_fit_name, best_fir_paramms = best_fit_distribution(data, bins, ax)
    best_dist = getattr(st, best_fit_name)

    # Update plots
    ax.set_ylim(dataYLim)
    ax.set_title(u'Bytes Number of Requests/Hour - All Distributions Fitting')
    ax.set_xlabel(u'Bytes per Request')
    ax.set_ylabel('Frequency')

    # Make PDF
    pdf = make_pdf(best_dist, best_fir_paramms)

    # Display
    plt.figure(figsize=(12,8))
    ax = pdf.plot(lw=2, label='PDF', legend=True)
    data.plot(kind='hist', bins=bins, normed=True, alpha=0.5, label='Data', legend=True, ax=ax, color='black')

    param_names = (best_dist.shapes + ', loc, scale').split(', ') if best_dist.shapes else ['loc', 'scale']
    param_str = ', '.join(['{}={:0.2f}'.format(k,v) for k,v in zip(param_names, best_fir_paramms)])
    dist_str = '{}({})'.format(best_fit_name, param_str)

    ax.set_title(u'Requests per Day - Best fit distribution \n' + dist_str)
    ax.set_xlabel(u'Number of Requests')
    ax.set_ylabel('Frequency')

    plt.show()



fileName = cs.DATA_LOCAL_PATH + "1-2016_1-2016_hourly_summary.csv"