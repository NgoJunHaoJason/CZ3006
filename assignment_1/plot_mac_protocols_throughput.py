"""
Run this script to plot figure for CZ3006 assignment 1.

dependencies:
- Python: 3.7.4
- matplotlib: 3.2.1
"""
import math
import matplotlib.pyplot as plt


# reference: Kleinrock-Tobagi paper

# equation 2
slotted_aloha_throughput = lambda G: G * math.e**-G


# equation 1
pure_aloha_throughput = lambda G: G * math.e**(-2 * G)


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


# equation A1
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

    # refer to proof in Appendix A for the following formulas

    # store value in variable to avoid recomputation
    pi_0_exp_p_minus_pi_0 = pi_0**p - pi_0

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

    # store value in variable to avoid recomputation
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
    
    # store value in variable to avoid recomputation
    one_minus_e_exp_neg_a_G = 1 - math.e**(-a * G)

    numerator = one_minus_e_exp_neg_a_G * (
        P_s_hat_prime * pi_0 + P_s_hat * (1 - pi_0)
    )

    denominator = one_minus_e_exp_neg_a_G * (
        a * t_bar_hat_prime * pi_0 + a * t_bar_hat * (1 - pi_0) + 1 + a
    ) + a * pi_0

    return numerator / denominator


def plot_mac_protocols_throughput():
    # to make the curve smooth
    # bigger number -> interpolate between more points -> smoother surve
    smooth_factor = 100

    a = 0.02  # normalised_propagation_delay; for CSMA

    offered_load_rate = [G / smooth_factor for G in range(1, 100 * smooth_factor)]

    mac_protocols = {
        'slotted ALOHA': slotted_aloha_throughput,
        'pure ALOHA': pure_aloha_throughput,
        '1-persistent CSMA': (lambda G: one_persistent_csma_throughput(G, a)),
        '0.07-persistent CSMA': (lambda G: approximate_p_persistent_csma_throughput(G, 0.07, a)),
    }

    plt.figure(figsize=(16, 8))

    for mac_protocol in mac_protocols:
        throughput = [
            mac_protocols[mac_protocol](G) 
            for G in offered_load_rate
        ]

        plt.plot(offered_load_rate, throughput, label=mac_protocol)

    plt.title(
        'Comparison of the channel utilization versus load for various ' 
        f'random access protocols (normalised propagation delay = {a})'
    )
    plt.xlabel('G (offered load rate)')
    plt.ylabel('S (throughput)')

    plt.xscale('log')

    plt.legend()

    plt.savefig('assignment_1/mac_protocols_throughput.png')
    plt.show()


if __name__ == '__main__':
    plot_mac_protocols_throughput()
