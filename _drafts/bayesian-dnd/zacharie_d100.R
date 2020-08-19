library(tibble)
library(dplyr)
library(ggplot2)
library(rmarkdown)


#d100_data <- data.frame(Rolls = round(runif(100000, 1, 100)))
d100_data <- data.frame(Rolls = c(
*** PASTE COMMA SEPARATED ROLL DATA HERE ***
))


# A copy of the bayesian dice analysis function
bayesian_dice_analysis <- function(roll_data, faces = 20, beta_prior_a = 1, beta_prior_b = 1) {
  
  faces_start <- 1
  faces_sep <- 1
  
  # Deal with the d100. It has 10 faces starting at 0 instead of 1 and increasing in increments of 10.
  #if (faces == 100) {
  #  roll_data <- as.numeric(roll_data)
  #  faces_start <- 0
  #  faces_sep <- 10
  #}
  
  # Check that no rolls are non-numeric
  if (sum(is.na(roll_data)) > 0) {
    stop("Non-numeric rolls were found in the data. Please ensure that the data is valid.")
  } 
  
  # Check that no rolls fall outside 1:faces
  if ((sum(roll_data > faces) + sum(roll_data < 0)) > 0) {
    stop(sprintf("Values outside the range 0 to %i were found in the data. Please ensure the faces parameter is correct and check that the data is valid.", faces))
  } 
  
  # Check that alpha and beta are non-negative
  if (beta_prior_a < 0 || beta_prior_b < 0) {
    stop("The alpha and beta priors must both be non-negtive. Please ensure the values specified are correct.") 
  }
  
  results_table <- tibble(face = seq(from = faces_start, to = faces_start + (faces - faces_sep), by = faces_sep))
  
  # Figure our the number of successes per face
  # Not sure how to do this inside a mutate function below
  successes <- c()
  for (i in results_table$face) {
    successes <- rbind(successes, sum(roll_data == i))
  }
  
  # Add columns for the count of binomial successes and failures
  results_table <- results_table %>% 
    mutate(successes = successes,
           failures = length(roll_data) - successes)
  
  # Add the values related to the posterior distribution
  results_table <- results_table %>%
    mutate(beta_post_a = beta_prior_a + successes,
           beta_post_b = beta_prior_b + failures,
           posterior_mean = beta_post_a / (beta_post_a + beta_post_b),
           posterior_median = qbeta(0.5, beta_post_a, beta_post_b),
           posterior_mode = (beta_post_a - 1) / (beta_post_a + beta_post_b - 2),
           ci_95_lower = qbeta(0.025, beta_post_a, beta_post_b),
           ci_95_upper = qbeta(0.975, beta_post_a, beta_post_b))
  
  return(results_table)
}

# Run the analysis on a true d100 from 1 to 
d100_result <- bayesian_dice_analysis(d100_data$Rolls, faces = 100, beta_prior_a = 1, beta_prior_b = 99)

ggplot(d100_result, aes(x = face, y = posterior_mean)) + 
  geom_point() +
  geom_errorbar(aes(ymin = ci_95_lower, ymax = ci_95_upper), colour = "black", width = 0.1) +
  geom_hline(aes(yintercept = 0.01, color = "red")) +
  scale_x_continuous(breaks = round(seq(from = 0, to = 100, by = 10))) +
  theme(legend.position = "none") +
  coord_flip() +
  ggtitle("Posterior Probablities for Each Roll of /roll in Star Wars: The Old Republic") +
  labs(x = "Value of the roll",
       y = "Posterior Probability Distribution")

d100_result %>% rmarkdown::paged_table()