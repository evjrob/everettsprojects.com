---
title: Hockey Modeling - Less Code, More Math! (Part 1)
description: The mathematics that make my updated hockey model work. Incorporating win/loss data using probability theory and calculus.
author: "Everett Robinson"
date: "August 20, 2020"
output: html_document
layout: post
---

### Using win/loss information for better inference

While a hockey game can certainly end with a tie in regulation time, the NHL wont have any of that. In all games they ensure there's a victor and a loser either in overtime or in a shoot out. This means that an ordinary Poisson based model on final scores isn't appropriate. The Poisson parameter $$\lambda$$ that we are estimating is a rate; it's fundamentally tied to the duration over which the observation is taken from and that duration needs to remain fixed!

Overtime in an NHL game is sudden death. The first team to score wins. Let us ignore the complications of shootouts, and consider a playoff game where overtime is played indefinitely until a goal occurs. From a mathematical perspective the probability of the home team winning is the probability that they score before the visiting team. This means we're considering the time until the next event, which isn't a Poisson random variable (RV) at all. Luckily for us however, this sounds like an exponential RV and there happens to be [a very special relationship between the Poisson and an exponential distributions](https://en.wikipedia.org/wiki/Exponential_distribution)! The time between events in the Poisson RV with rate parameter $$\lambda$$ is an exponentially distributed RV also characterized by $$\lambda$$!

Great, but how do we get the probability of one team winning from these rates? With calculus! Let's take a look at the formulas from probability theory we need to work with.

### Exponential distribution equations

The Probability Density Function (PDF) of an exponential RV is:

$$ \lambda e^{-\lambda t} $$

The probability that an event occurs at or before time $$T$$ is given by:

$$ \int_0^T \lambda e^{-\lambda t} dt = 1 - e^{-\lambda T}$$

This is also known as the Cumulative Density Function (CDF).

### The calculus

For an exponential RV the rate parameter is meaningful for any value from 0 to $$\infty$$. We have two of these parameters, one for each team. Let us assume these are independent; that is a team's chance of scoring has nothing to do with the current scores, or the other team's latent chance to score. There are lots of reasons one can argue against this, from player psychology to the both teams can't possess the puck at the same time. All of those are valid counter arguments to the assumption, and they may be worth modeling. For the sake of simplicity I have chosen to ignore them.

Now with two random exponential variables $$\lambda_H$$ and $$\lambda_A$$, we need to consider the marginal probability of the home team scoring before the away team. Under the assumption of independence, we can treat these times to next goal as separate. Let us also separate the integrand of time for each team so that $$t$$ becomes $$a$$ for the away team and $$h$$ for the home team. The probability of the home team scoring before the away team then is:

$$ Pr(HG \leq AG) = \int^\infty_0 \int^a_0 p(h,a) dh da $$

Where the assumption of independence gives us:

$$ p(h,a) = \lambda_H \lambda_A e^{-(\lambda_H h + \lambda_A a)} $$

So:

$$ Pr(HG \leq AG) = \int^\infty_0 \int^a_0 \lambda_H \lambda_A e^{-(\lambda_H h + \lambda_A a)} dh da $$

We can rearrange the integral:

$$ Pr(HG \leq AG) = \int^\infty_0 \lambda_A e^{-\lambda_A a} \int^a_0  \lambda_H e^{-\lambda_H h} dh da $$

Notice that $$\int^a_0  \lambda_H e^{-\lambda_H h} dh $$ is the cdf, so the integral becomes:

$$ Pr(HG \leq AG) = \int^\infty_0 \lambda_A e^{-\lambda_A a} (1 - e^{-\lambda_H a}) da $$

$$ Pr(HG \leq AG) = \int^\infty_0 \lambda_A e^{-\lambda_A a} da - \int^\infty_0  \lambda_A e^{-(\lambda_A a + \lambda_H a)} da $$

The first term is the cdf of time until the first away team goal from 0 to infinity, so it is equal to one:

$$ Pr(HG \leq AG) = 1 - \int^\infty_0  \lambda_A e^{-(\lambda_A a + \lambda_H a)} da $$

The integral for the second term needs a bit more work, but is still straightforward:

$$ Pr(HG \leq AG) = 1 + \frac{\lambda_A}{\lambda_A + \lambda_H} e^{-(\lambda_A a + \lambda_H a)} |^\infty_0 $$

Now through a little algebra we can simplify the expression:

$$ Pr(HG \leq AG) = 1 + \frac{\lambda_A}{\lambda_A + \lambda_H} (0 - 1) $$

$$ Pr(HG \leq AG) = 1 - \frac{\lambda_A}{\lambda_A + \lambda_H} $$

$$ Pr(HG \leq AG) = \frac{\lambda_A + \lambda_H - \lambda_A}{\lambda_A + \lambda_H} $$

$$ Pr(HG \leq AG) = \frac{\lambda_H}{\lambda_A + \lambda_H} $$

This is the probability that the home team scores the next goal and wins in overtime. We can create a deterministic variable in PyMC3 to capture this, and use it along side the Poisson distributed regulation time score. We no longer need to worry about ruining the poisson rate inference by directly using the final scores, but still get to include the extra bit of information about which team is better using the outcome of the game. It's the best of both worlds! I do exactly this in [my hockey model](https://bayesbet.everettsprojects.com).