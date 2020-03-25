"""
This file contains functions for calculating throughput for various MAC protocols.
All functions take G as their only parameter,
where G is the offered load rate
"""
import math

# reference: Kleinrock-Tobagi paper

# equation 2
slotted_aloha_throughput = lambda G: G * math.e**-G


# equation 1
pure_aloha_throughput = lambda G: G * math.e**(-2 * G)


# equation 3
def non_persistent_csma_throughput(G, a):
    """
    params:
    - G (float): offered load rate
    - a (float): normalised propagation delay

    return:
    (float) non-persistent CSMA throughput
    """
    # time during a cycle that the channel is used without conflicts
    U_bar = math.e**(-a * G)

    numerator = G * U_bar
    denominator = G * (1 + 2*a) + U_bar

    return numerator / denominator


# equation 10
def one_persistent_csma_throughput(G, a):
    """
    params:
    - G (float): offered load rate
    - a (float): normalised propagation delay

    return:
    (float) 1-persistent CSMA throughput
    """
    numerator = G * (1 + G + a*G*(1 + G + a*G/2)) * math.e**(-G * (1 + 2*a))
    denominator = G * (1 + 2*a) - (1 - math.e**(-a*G)) + (1 + a*G) * math.e**(-G * (1 + a))

    return numerator / denominator


def approximate_p_persistent_csma_throughput(G, p, a):
    """
    params:
    - G (float): offered load rate
    - p (float): transmission probability, with value < 0.1
    - a (float): normalised propagation delay

    return:
    (float) p-persistent CSMA throughput
    """
    g = a * G  # average arrival rate of new and rescheduled packets during a (mini) slot

    # pi_n = ((1 + a) * G)**n / math.factorial(n) * math.exp(-(1 + a) * G)
    pi_0 = math.exp(-(1 + a) * G)

    q = 1 - p

    # refer to proof in Appendix A

    pi_0_exp_p_minus_pi_0 = pi_0**p - pi_0  # no need recalculate later

    t_bar_hat = pi_0_exp_p_minus_pi_0 / (
        1 - pi_0 - pi_0_exp_p_minus_pi_0 * math.e**(-p * g)
    )

    P_s_hat_first_term = pi_0_exp_p_minus_pi_0 / (q * (1 - pi_0))

    P_s_hat_second_term = (
        1 - math.exp(-g * p)
    ) * (
        pi_0**(1 - q**2) - pi_0
    ) / (
        q * (1 - pi_0) - q * math.exp(-2 * g * p) * pi_0_exp_p_minus_pi_0
    )

    P_s_hat = P_s_hat_first_term - P_s_hat_second_term

    # no need to recalculate later
    e_exp_neg_g_exp_p_minus_e_exp_neg_g = (math.e**-g)**p - math.e**-g

    t_bar_hat_prime = e_exp_neg_g_exp_p_minus_e_exp_neg_g / (
        1 - math.e**-g - e_exp_neg_g_exp_p_minus_e_exp_neg_g * math.e**(-p * g)
    )

    P_s_hat_prime_first_term = e_exp_neg_g_exp_p_minus_e_exp_neg_g  / (q * (1 - math.e**-g))

    P_s_hat_prime_second_term = (
        1 - math.exp(-g * p)
    ) * (
        (math.e**-g)**(1 - q**2) - math.e**-g
    ) / (
        q * (1 - math.e**-g) - q * math.exp(-2 * g * p) * e_exp_neg_g_exp_p_minus_e_exp_neg_g
    )

    P_s_hat_prime = P_s_hat_prime_first_term - P_s_hat_prime_second_term
    
    one_minus_e_exp_neg_a_G = 1 - math.e**(-a * G)  # no need recalculate later

    numerator = one_minus_e_exp_neg_a_G * (
        P_s_hat_prime * pi_0 + P_s_hat * (1 - pi_0)
    )

    denominator = one_minus_e_exp_neg_a_G * (
        a * t_bar_hat_prime * pi_0 + a * t_bar_hat * (1 - pi_0) + 1 + a
    ) + a * pi_0

    return numerator / denominator
