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


def p_persistent_csma_throughput(G, p, a):
    """
    params:
    - G (float): offered load rate
    - p (float): TODO
    - a (float): normalised propagation delay

    return:
    (float) p-persistent CSMA throughput
    """
    pass  # TODO
