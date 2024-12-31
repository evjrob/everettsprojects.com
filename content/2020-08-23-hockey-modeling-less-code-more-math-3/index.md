+++
title = "Hockey Modeling - Less Code, More Math! (Part 3)"
description = "The mathematics that make my updated hockey model work. Predicting the home team win probability in overtime or shootout from model variables."
date = "2020-08-23"
authors = [ "Everett Robinson",]
aliases = ["/2020/08/23/hockey-modeling-less-code-more-math-3.html"]

[taxonomies]
tags = ["Data Science", "Python", "Statistics", "Bayesian Statistics", "Hockey", "NHL", "Sports"]

[extra]
layout = "post"
output = "html_document"
+++

This post is part of a series exploring the math behind my hockey model:

1. [Incorporating win/loss data for inference](/2020/08/20/hockey-modeling-less-code-more-math-1.html)
2. [Predicting regulation score probabilities](/2020/08/22/hockey-modeling-less-code-more-math-2.html)
3. [Predicting the winner in overtime/shootout](/2020/08/23/hockey-modeling-less-code-more-math-3.html)
4. [Differentiating overtime wins from shootout wins](/2020/08/24/hockey-modeling-less-code-more-math-4.html)
   
With Bayesian posterior distributions for the model parameters, we need to account for the full range of each when we go to estimate things like scores and win probabilities. We turn to probability theory and calculus to figure this out! Here we will determine the probability of the home team ultimately winning the game in overtime or shootout.

### The Bernoulli probability of a home win

Recall from [an earlier post](http://everettsprojects.com/2020/08/20/hockey-modeling-less-code-more-math-1.html) that the Bernoulli PMF of the home team winning in overtime is:

$$ Pr(HG \leq AG) = \frac{\lambda_H}{\lambda_A + \lambda_H} $$

Where:

$$ \lambda_{H,t} = exp(log\lambda_{H,t})$$

$$ \lambda_{A,t} = exp(log\lambda_{A,t})$$

Meaning that:

$$ Pr(HG \leq AG) = \frac{exp(log\lambda_H)}{exp(log\lambda_A) + exp(log\lambda_H)} $$

We also saw in [the previous post](http://everettsprojects.com/2020/08/22/hockey-modeling-less-code-more-math-2.html) that:

$$log\lambda_{H,t} \sim Normal(\mu_i + \mu_h + \mu_{o_{j,t}} - \mu_{d_{k,t}}, \sigma^2_i + \sigma^2_h + \sigma^2_{o_{j,t}} + \sigma^2_{d_{k,t}})$$

$$log\lambda_{A,t} \sim Normal(\mu_i + \mu_{o_{k,t}} - \mu_{d_{j,t}}, \sigma^2_i + \sigma^2_{o_{k,t}} +\sigma^2_{d_{j,t}})$$

Like the earlier analyses, this all rests on the assumption of independence between $log\lambda_{H,t}$ and $log\lambda_{A,t}$. It should come as no surprise then that the trick to combining our posteriors for each $log\lambda$ and the Bernoulli PMF is to take the integral over the product of the three. The key difference between this integral and the one we saw in the last post is that we now have two rate parameters $log\lambda_{H,t}$ and $log\lambda_{A,t}$. A single integral will not suffice; we need a double integral:

$$ Pr(HW|\lambda_A, \lambda_H) = \int_{\infty}^{-\infty} \int_{\infty}^{-\infty} \frac{exp(x)}{exp(y) + exp(x)} \Phi(x, \mu_H, \sigma_H) \Phi(y, \mu_A, \sigma_A) dx dy$$

Where:

$$ \Phi(x, \mu_H, \sigma_H) = \frac{1}{\sigma_H \sqrt{ 2\pi}} exp \left(-\frac{1}{2} (\frac{x - \mu_H}{\sigma_H})^2 \right) $$

$$ \Phi(y, \mu_A, \sigma_A) = \frac{1}{\sigma_A \sqrt{ 2\pi}} exp \left(-\frac{1}{2} (\frac{y - \mu_A}{\sigma_A})^2 \right) $$

This is a tricky integral with no obvious analytical solution, so we will again solve it numerically. This time we use [SciPy's double Quadrature implementation dblquad](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.dblquad.html).

```python

def bayesian_bernoulli_win_pdf(log_λₕ_μ, log_λₕ_σ, log_λₐ_μ, log_λₐ_σ):
    def dblintegrand(y, x, log_λₕ_μ, log_λₕ_σ, log_λₐ_μ, log_λₐ_σ):
        normₕ = np.exp(-0.5*((x-log_λₕ_μ)/log_λₕ_σ)**2)/(log_λₕ_σ * sqrt(2*pi))
        normₐ = np.exp(-0.5*((y-log_λₐ_μ)/log_λₐ_σ)**2)/(log_λₐ_σ * sqrt(2*pi))
        λₕ = np.exp(x)
        λₐ = np.exp(y)
        p_dydx = normₐ*normₕ*λₕ/(λₕ + λₐ)
        return p_dydx

    lwr = -3.0
    upr = 5.0

    I = dblquad(dblintegrand, lwr, upr, lwr, upr, args=(log_λₕ_μ, log_λₕ_σ, log_λₐ_μ, log_λₐ_σ))
    p = I[0]

    return p

```

Now we have the value $p_{HW}$ for the probability of the home team winning in either over time or shoot out. For non playoff games we can be essentially 100% certain this is an overtime win and do not need to do anything further. For regular and preseason games we still have one more step to do: Predicting if the game will end within the 5 minute overtime period or not. Stay tuned for my next post where I will address how we do that.