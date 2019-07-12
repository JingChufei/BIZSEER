# Gaussian Processes

## Introduction

- allow us to make predictions about our data by incorporating prior knowledge.
- Regression:  *fitting* a function to the data
- For a given set of training points, there are potentially infinitely many functions that fit the data. Gaussian processes assign a **probability** to each of these functions. The mean of this probability distribution then represents the most probable characterization of the data. Furthermore, using a probabilistic approach allows us to incorporate the confidence of the prediction into the regression result.



## Multivariate Gaussian distribution

- the Gaussian distribution (which is often also referred to as *normal* distribution) is the basic building block of Gaussian processes. we are interested in multivariate case of this distribution, where **each random variable is distributed normally and their joint distribution is also Gaussian**.
- The **multivariate Gaussian distribution** is defined by a mean vector *μ* and a covariance matrix Σ. 
  - The mean vector *μ* describes the expected value of the distribution. Each of its components describes the mean of the corresponding dimension. 
  - Σ models the variance along each dimension and determines how the different random variables are correlated. Always symmetric and postitive semi-definite. Σ describes the shape of the distribution.
    - Diagonal of Σ consists of the variance of the *i*-th random variable
    - Off-diagonal elements describe the correlation between the *i*-th and *j*-th random variable.



### Marginalization and Conditioning

![image-20190712110909351](/Users/jingchufei/Library/Application Support/typora-user-images/image-20190712110909351.png)

- *Marginalization*
  - Through *marginalization* we can extract partial information from multivariate probability distributions.
  - *Marginalization* can be seen as integrating along one of the dimensions of the Gaussian distribution, which is in line with the general definition of the marginal distribution.
  - ![image-20190712110840058](/Users/jingchufei/Library/Application Support/typora-user-images/image-20190712110840058.png)
    - each partition *X* and *Y* only depends on its corresponding entries in *μ* and Σ.
  - ![image-20190712110810366](/Users/jingchufei/Library/Application Support/typora-user-images/image-20190712110810366.png)
    - if we are interested in the probability density of *X*=*x*, we need to consider all possible outcomes of *Y* that can jointly lead to the result.
- *Conditioning*
  - It is used to determine the probability of one variable depending on another variable. Similar to marginalization, this operation is also closed and yields a modified Gaussian distribution. This operation is the cornerstone of Gaussian processes since it allows Bayesian inference.
  - *Conditioning* also has a nice geometric interpretation — we can imagine it as making a cut through the multivariate distribution, yielding a new Gaussian distribution with fewer dimensions.
  - ![image-20190712110612542](/Users/jingchufei/Library/Application Support/typora-user-images/image-20190712110612542.png)



## Gaussian Processes

- move from the continuous view to the **discrete** representation of a function: rather than finding an implicit function, we are interested in predicting the function values at concrete points, which we call *test points* *X*.
- the goal of Gaussian processes is to **learn underlying distribution from *training data***. Respective to the test data *X*, we will denote the training data as *Y*. As we have mentioned before, the key idea of Gaussian processes is to model the underlying distribution of *X* together with *Y* as a multivariate normal distribution. That means that the joint probability distribution spans the space of possible function values for the function that we want to predict. Please note that this joint distribution of test and training data has ∣*X*∣+∣*Y*∣ dimensions.
- In order to perform regression on the training data, we will treat this problem as ***Bayesian inference***. The essential idea of Bayesian inference is to **update the current hypothesis as new information becomes available**. In the case of Gaussian processes, **this information is the training data**. Thus, we are interested in the **conditional probability** *P* *(* *X*∣*Y* *)*. Finally, we recall that Gaussian distributions are closed under conditioning — so *P* *(* *X*∣*Y* *)* is also distributed normally.
- In Gaussian processes we **treat each test point as a random variable**. A multivariate Gaussian distribution has the same number of dimensions as the number of random variables. Since we want to predict the function values at ∣*X*∣=*N* test points, the corresponding multivariate Gaussian distribution is also *N* -dimensional. **Making a prediction using a Gaussian process ultimately boils down to drawing samples from this distribution**. We then interpret the *i*-th component of the resulting vector as the function value corresponding to the *i*-th test point.



### Kernel

- In Gaussian processes it is often assumed that *μ*=0, which simplifies the necessary equations for conditioning. We can always assume such a distribution, even if *μ*≠0, and add *μ* back to the resulting function values after the prediction step. This process is also called *centering* of the data.

- The covariance matrix Σ will not only describe the **shape of our distribution**, but ultimately determines the **characteristics of the function** that we want to predict. We generate the covariance matrix by evaluating the **kernel** *k*, which is often also called ***covariance function***, pairwise on all the points. The kernel receives two points as an input and returns a **similarity measure** between those points in the form of a scalar
- ![image-20190712113219402](/Users/jingchufei/Library/Application Support/typora-user-images/image-20190712113219402.png)
- **The entry Σ*i* *j* describes how much influence the *i*-th and *j*-th point have on each other**. This follows from the definition of the multivariate Gaussian distribution, which states that Σ*i* *j* defines the correlation between the *i*-th and the *j*-th random variable. Since the kernel describes the similarity between the values of our function, it controls the possible shape that a fitted function can adopt. Note that when we choose a kernel, we need to make sure that the resulting matrix adheres to the properties of a covariance matrix.
- Kernels are widely used in machine learning, for example in *support vector machines*. The reason for this is that **kernels allow similarity measures that go far beyond the standard euclidean distance**. Many of these kernels conceptually **embed the input points into a higher dimensional space in which they then measure the similarity**.
- ![image-20190712113815017](/Users/jingchufei/Library/Application Support/typora-user-images/image-20190712113815017.png)
- Kernels can be separated into ***stationary*** and ***non-stationary*** kernels. 
  - *Stationary* kernels, such as the RBF kernel, are functions invariant to translations, and the covariance of two points is only dependent on their **relative position**. A special case here would be the periodic kernel, which is only invariant to translations equal to the period of its respective function. 
    - The stationary nature of the **RBF kernel** can be observed in the banding around the diagonal of its covariance matrix. Increasing the length parameter increases the banding, as points further away from each other become more correlated. 
    - For the **periodic kernel**, we have an additional parameter P*P* that determines the periodicity, which controls the distance between each repetition of the function.
  - *Non-stationary* kernels, such as the linear kernel, do not have this constraint and depend on an **absolute location**. 
    -  the parameter *C* of the **linear kernel** allows us to change the point on which all functions hinge.
- [More kernels](https://www.cs.toronto.edu/~duvenaud/cookbook/)



### Prior Distribution

- Consider the case where we **have not yet observed any training data**. In the context of Bayesian inference, this is called the ***prior* distribution** *P* (*X*).
- The kernel is used to define the entries of the covariance matrix. Consequently, the covariance matrix determines which type of functions from the space of all possible functions are more probable. As the prior distribution does not yet contain any additional information, it is perfect to visualize **the influence of the kernel on the distribution of functions**.



### Posterior Distribution

- Bayesian inference states that we can **incorporate additional information (training data)** into our model, yielding the ***posterior* distribution** *P* (*X*∣*Y*).
- First, we **form the joint distribution *P* (*X*,*Y*) between the test points *X* and the training points *Y***. The result is a multivariate Gaussian distribution with dimensions ∣*Y*∣+∣*X*∣. We concatenate the training and the test points to compute the corresponding covariance matrix.
- Second, **Using *conditioning* we can find *P* (*X*∣*Y*) from *P* (*X*,*Y*)**. The dimensions of this new distribution matches the number of test points *N* and the distribution is also normal. The intuition behind this step is that the **training points constrain the set of functions to those that pass through the training points**.
  - But in real-world scenarios this is an unrealistic assumption, since most of our data is afflicted with measurement errors or uncertainty. Gaussian processes offer a simple solution to this problem by modeling the error of the measurements. For this, we need to add **an error term ϵ*∼N(0,*ψ*2)** to each of our training points
    - ![image-20190712115734098](/Users/jingchufei/Library/Application Support/typora-user-images/image-20190712115734098.png)
  - We do this by slightly modifying the setup of the joint distribution *P* (*X*,*Y*)
    - ![image-20190712120013653](/Users/jingchufei/Library/Application Support/typora-user-images/image-20190712120013653.png)
    - Again, we can use conditioning to derive the predictive distribution *P* (*X*∣*Y*).
    -  In this formulation, *ψ* is an additional parameter of our model.
- Third, **predict the value using conditioning mean and variance**. In contrast to the prior distribution, we set the mean to *μ*=0. But when we condition the joint distribution of the test and training data the resulting distribution will most likely have a non-zero mean *μ*′≠0. Extracting *μ*′ and *σ*′ does not only lead to a more **meaningful prediction**, it also allows us to make a statement about **the confidence of the prediction**.
- Case 
  - ![image-20190712130745638](/Users/jingchufei/Library/Application Support/typora-user-images/image-20190712130745638.png)
  - The **training points** lead to a constrained distribution. This change is reflected in the entries of the covariance matrix, and **leads to an adjustment of the mean and the standard deviation of the predicted function**. As we would expect, **the uncertainty of the prediction is small in regions close to the training data** and grows as we move further away from those points.
  - In the **constrained covariance matrix**, we can see that the correlation of neighbouring points is affected by the training data. If a predicted point lies on the training data, there is no correlation with other points. Therefore, the function must pass directly through it. Predicted values further away are also affected by the training data — proportional to their distance.



### Combining different kernels

- The power of Gaussian processes lies in the choice of the kernel function. This property allows experts to **introduce domain knowledge into the process** and lends Gaussian processes their flexibility to **capture trends in the training data**. For example, by choosing a suitable bandwidth for the RBF kernel, we can control how smooth the resulting function will be.
- A big benefit that **kernels** provide is that they **can be combined together**, resulting in a more **specialized kernel**. The decision **which kernel to use is highly dependent on prior knowledge about the data**, e.g. if certain characteristics are expected. Examples for this would be stationary nature, or global trends and patterns. 
- Remember that the covariance matrix of Gaussian processes has to be **positive semi-definite**. When choosing the optimal kernel combinations, all methods that preserve this property are allowed. The most common kernel combinations would be **addition** and **multiplication**. However, combinations are not limited to the above example, and there are more possibilities such as **concatenation** or **composition** with a function.
- Example
  - Let's consider two kernels, a linear kernel *k*lin and a periodic kernel *k*per, for example. This is how we would multiply the two
  - ![image-20190712132007172](/Users/jingchufei/Library/Application Support/typora-user-images/image-20190712132007172.png)
  - If we add a periodic and a linear kernel, the global trend of the linear kernel is incorporated into the combined kernel. The result is a periodic function that follows a linear trend. When combining the same kernels through multiplication instead, the result is a periodic function with a linearly growing amplitude away from linear kernel parameter *c*.
  - ![image-20190712132403578](/Users/jingchufei/Library/Application Support/typora-user-images/image-20190712132403578.png)



## Furture

- sometimes it might not be possible to describe the kernel in simple terms. To overcome this challenge, **learning specialized kernel functions from the underlying data**, for example **by using deep learning** is an area of ongoing research.
- Even though we mostly talk about Gaussian processes in the context of regression, they can be adapted for different purposes, e.g. *model-peeling* and hypothesis testing. 
- By comparing different kernels on the dataset, domain experts can introduce additional knowledge through appropriate combination and parameterization of the kernel.

## Reference 

https://www.jgoertler.com/visual-exploration-gaussian-processes/