import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
from scipy.stats import norm
from scipy.stats import poisson
from scipy.stats import gamma
import statistics
#--------------------------------
df=pd.read_csv('2009.tsv', sep='\t')
df.fillna(0,inplace=True)
df["log pop density"]=df["population density"].apply(lambda x:x+1).apply(math.log)
df["ratios"]=df["forest cover"]/df["log pop density"]
df.fillna(0,inplace=True)
print("="*33 + "DATASET" +"="*33)
print(df)
print("="*75)
#--------------------------------
print("working with log of population density")
print("Fitting a 'Normal Distribution' ...")
plt.hist(df["log pop density"])
mean = statistics.mean(df["log pop density"])
sd = statistics.stdev(df["log pop density"])
print("mean = ",mean," variance = " , sd*sd)
x_axis = np.arange(0, 10, 0.01) # to match binning
plt.plot(x_axis, norm.pdf(x_axis, mean, sd)*300, label="Gaussian Fit")
plt.xlabel("log of population density in person per sqm")
plt.ylabel("count")
plt.legend()
plt.title("distribution of log of population density")
plt.savefig("pop density.png")
plt.clf()
print("="*75)
#----------
print("working with extreme climate")
plt.hist(df["extreme climate"])
mean=statistics.mean(df["extreme climate"])
sd=statistics.stdev(df["extreme climate"])
print("mean = ",mean,"std dev = ", sd)
print("variance/mean = ",sd*sd/mean, " > 1 ⇒ not binomial or exponential")
print("let's try poisson")
print("Fitting Poisson ...")
l=(mean+sd*sd)/2
print("λ = ",l)
x_axis = np.arange(0, 10, 1) # to match binning
def poisson(k):
	global l
	return np.math.pow(l,k) * np.exp(-l) / np.math.factorial(k)
#y_axis=np.apply_along_axis(lambda x: k*np.exp(-k*x),-1,x_axis)
y_axis=[1000*poisson(i) for i in x_axis ]
plt.plot(x_axis, y_axis, label="Poisson Fit")
print("Fitting Gamma ...")
theta=sd*sd/mean
k=mean/theta
print("shape = ", k , " scale = " , theta)
x_axis = np.arange(0, 10, 0.01) # to match binning
plt.plot(x_axis, gamma.pdf(x_axis, a=k, scale=theta)*50, label="Gamma Fit" , color="r")
plt.xlabel("extreme climate per person")
plt.ylabel("count")
plt.legend()
plt.title("distribution of extreme climate")
plt.savefig("extreme climate.png")
plt.clf()
print("="*75)
#-----------
print("working on population density and forest cover")
print("printing scatter plot ...")
plt.ylabel("log of population density in person per sqm")
plt.xlabel("forest cover % of total land area")
plt.title("distribution of log of population density vs forest cover")
plt.scatter(df["forest cover"], df["log pop density"])
plt.savefig("ppdensity vs forest cover.png")
plt.clf()
#------------
print("correlation between population density and forest cover")
plt.hist(df["ratios"])
mean=statistics.mean(df["ratios"])
sd=statistics.stdev(df["ratios"])
print("mean = ",mean,"std dev = ", sd)
print("really close -- > exponential fit.")
print("Fitting a 'Exponential Distribution' ...")
k=2.0/(mean+sd)
print("k = ",k)
x_axis =range(60) # to match binning
y_axis=np.apply_along_axis(lambda x: k*np.exp(-k*x),-1,x_axis)
plt.plot(x_axis, y_axis*1000, label="Exponential Fit")
plt.legend()
plt.title("slope of log population density vs forest cover")
plt.savefig("ratios lppd vs fc.png")
plt.clf()
print("="*75)