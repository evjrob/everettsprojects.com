+++
title = "Hockey Modeling - Less Code, More Math! (Part 4)"
description = "The mathematics that make my updated hockey model work. Predicting if a win is in shootout or overtime from the model variables."
date = "2020-08-24"
authors = [ "Everett Robinson",]
aliases = ["/2020/08/24/hockey-modeling-less-code-more-math-4.html"]

[extra]
layout = "post"
output = "html_document"
+++

This post is part of a series exploring the math behind my hockey model:

1. [Incorporating win/loss data for inference](/2020/08/20/hockey-modeling-less-code-more-math-1.html)
2. [Predicting regulation score probabilities](/2020/08/22/hockey-modeling-less-code-more-math-2.html)
3. [Predicting the winner in overtime/shootout](/2020/08/23/hockey-modeling-less-code-more-math-3.html)
4. [Differentiating overtime wins from shootout wins](/2020/08/24/hockey-modeling-less-code-more-math-4.html)

With Bayesian posterior distributions for the model parameters, we need to account for the full range of each when we go to estimate things like scores and win probabilities. We turn to probability theory and calculus to figure this out! Here we will see how to find the probability that a non-regulation time win was in overtime rather than a shootout.

### Computing game outcome probabilities from the model variables.

With the previous two blog posts [1](/2020/08/22/hockey-modeling-less-code-more-math-2.html) and [2](/2020/08/23/hockey-modeling-less-code-more-math-3.html), we almost have everything in place to make predictions for future games. The only part missing is a means by which to separate an overtime win from a shoot out win during non-playoff games. This is almost not worth doing, because I currently make no distinction in my visualizations, and the difference doesn't actually impact the points awarded during regular season play. It *could*  play a deciding role in which team makes the playoff cut in the event of a tie in points. The tie-breaking procedure for the 2020 playoff season is:

*Points percentage in games through March 11 was used to determine the field for the 2020 Stanley Cup Qualifiers. If two teams were tied in points percentage, the standing of the clubs was determined in the following order:*

1. *The greater number of games won, excluding games won in Overtime or by Shootout (i.e., "Regulation Wins"). This figure is reflected in the RW column.*
2. *The greater number of games won, excluding games won by Shootout. This figure is reflected in the ROW column.*
3. *The greater number of games won by the Club in any manner (i.e, "Total Wins"). This figure is reflected in the W column.*

To ensure the model has the flexibility to predict a team's chances of making the playoff in the future, we cannot neglect this detail! To account for it we need to find the probability that at least one of the two teams playing would have scored their next goal within five minutes to decide if the win was in overtime or shootout. This is the same as one minus the probability of both teams requiring more than five minutes to score the first goal:

$$Pr(OT_{Win}) = 1 - Pr(HG \gt 5mins \land AG \gt 5 mins) $$

We turn to the exponential distribution again to solve this one. The Cumulative Density Function (CDF) function for the exponential distribution describes the probability that the random variable (RV) takes on a value less than or equal to $T$. It is:

$$Pr(x \leq T) =  1 - e^{-\lambda T} $$

The probability that the time required for the next event to occur is greater than $T$ is simply:

$$Pr(x \gt T) = 1 - 1 - e^{-\lambda T} = - e^{-\lambda T} $$

We are interested in the intersection of this probability for both teams in each game. Under the assumption of independence we know that the probability of each occurring simultaneously is simply the product of the two independent RVs. So the probability that both teams require more than $T$ minutes to score their next goal is:

$$ Pr(HG \gt T \land AG \gt T) = e^{-\lambda_H T} e^{-\lambda_A T} = e^{-(\lambda_H + \lambda_A)T} $$

Therefore the probability of the win occurring in a shoot out is: 

$$Pr(OT_{Win}) = 1 - e^{-(\lambda_H + \lambda_A)T} $$

Where $T = \frac{5}{60}$ given the exponential rate parameters $\lambda$ being tied to the 60 minutes of play in regulation time.

We once again need to account for the Bayesian nature of $\lambda_H$ and $\lambda_A$. This requires another double integral [similar to the one seen in the last post](/2020/08/23/hockey-modeling-less-code-more-math-3.html):

$$Pr(OT_{Win}|\lambda_A, \lambda_H) = \int_{-\infty}^{\infty} \int_{-\infty}^{\infty} (1 - e^{-(\lambda_H + \lambda_A)T}) \Phi(x, \mu_H, \sigma_H) \Phi(y, \mu_A, \sigma_A) dx dy $$

With:

$$ \Phi(x, \mu_H, \sigma_H) = \frac{1}{\sigma_H \sqrt{ 2\pi}} exp \left(-\frac{1}{2} (\frac{x - \mu_H}{\sigma_H})^2 \right) $$

$$ \Phi(y, \mu_A, \sigma_A) = \frac{1}{\sigma_A \sqrt{ 2\pi}} exp \left(-\frac{1}{2} (\frac{y - \mu_A}{\sigma_A})^2 \right) $$

Numerical integration returns as our trusty technique to solve this integral, again using [SciPy's implementation of dblquad](https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.dblquad.html):

```python

def bayesian_goal_within_time(t, log_λₕ_μ, log_λₕ_σ, log_λₐ_μ, log_λₐ_σ):
    def dblintegrand(y, x, log_λₕ_μ, log_λₕ_σ, log_λₐ_μ, log_λₐ_σ):
        normₕ = np.exp(-0.5*((x-log_λₕ_μ)/log_λₕ_σ)**2)/(log_λₕ_σ * sqrt(2*pi))
        normₐ = np.exp(-0.5*((y-log_λₐ_μ)/log_λₐ_σ)**2)/(log_λₐ_σ * sqrt(2*pi))
        λₕ = np.exp(x)
        λₐ = np.exp(y)
        p = normₐ*normₕ*(1 - np.exp(-1*(λₕ*t + λₐ*t)))
        return p

    lwr = -3.0
    upr = 5.0

    I = dblquad(dblintegrand, lwr, upr, lwr, upr, args=(log_λₕ_μ, log_λₕ_σ, log_λₐ_μ, log_λₐ_σ))
    p = I[0]

    return p

```

With that, we now have the ability to predict the probability that a non regulation time win is going to be in overtime or in a shootout. This rounds out all the required pieces for predicting game outcomes using the new posteriors from the [latest version of my hockey model](http://everettsprojects.com/2020/08/18/modeling-the-nhl-better.html). All of the techniques discussed in the last four blog posts are [live in the model now](https://github.com/evjrob/bayes-bet), and play a role in [the visualizations and results shown in the web-app](https://bayesbet.everettsprojects.com).