---
title: Hockey Modeling - Less Code, More Math! (Part 1)
description: The mathematics that make my updated hockey model work. Incorporating win/loss data using probability theory and calculus.
author: "Everett Robinson"
date: "August 11, 2020"
output: html_document
layout: post
---

## Using win/loss information for better inference

While a hockey game can certainly end with a tie in regulation time, the NHL wont have any of that, and they have a system to ensure a victor and a loser either in overtime or in a shoot out. This means that an ordinary Poisson based model on final scores isn't appropriate. The Poisson parameter $\lambda$ that we are estimating is a rate; it's fundamentally tied to the duration over which the observation is taken from and needs to remain fixed!

Overtime in an NHL game is sudden death. The first team to score wins. Let us ignore the complications of shootouts, and consider a playoff game where overtime is played indefinitely until a goal occurs. From a mathematical perspective the probability of the home team winning is the probability that they score before the visiting team. This means we're considering the time until the next event, which isn't a Poisson random variable (RV) at all. Luckily for us however, this sounds like an exponential RV and there happens to be a very special relationship between a Poisson RV and an exponential RV! The time between events in the Poisson RV with rate parameter $\lambda$ is an exponential RV also described by $\lambda$!

How do we link the probability back to the rates? With calculus! Before we get there we need to remind ourselves about a few key formulas from probability theory.

### Exponential distribution crash course

The PDF of an exponential RV is:

$$ \lambda e^{-\lambda t} $$

The probability that an event occurs at or before time $T$ is given by:

$$ \int_0^T \lambda e^{-\lambda t} dt = 1 - e^{-\lambda t}$$

This is also known as the Cumulative Density Function (CDF).

For an exponential RV the rate parameter is meaningful for any value from 0 to $\infty$. We have two of these parameters, one for each team. Let us assume these are independent; that is a team's chance of scoring has nothing to do with the current scores, or the other team's latent chance score. There are lots of reasons one can argue against this, from player psychology to the effects of plain old puck possession. All of those are valid counter arguments that may in fact be real effects. But for simplicity I ignore them.

Now with two random exponential variables $\lambda_H$ and $\lambda_A$, we need to consider the marginal probability of the home team scoring before the away team. Under the assumption of independence, we can consider the probability of the away team scoring a goal within a certain time without consideration of the home team chances. To keep these times separate, lets refer to the time of the first home goal as $T_h$ and the time of the first away goal as $T_a$. Let us also separate the integrand of time for each team so that $t$ becomes $a$ for the away team and $h$ for the home team. This give us:

$$ \int_0^{T_A} \lambda_A e^{-\lambda_A a} da $$

Now the probability of the home tea scoring before a given 