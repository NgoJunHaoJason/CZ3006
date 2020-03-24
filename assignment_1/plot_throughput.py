import math
import matplotlib.pyplot as plt


from mac_protocols_throughput import slotted_aloha_throughput, pure_aloha_throughput, \
    non_persistent_csma_throughput, one_persistent_csma_throughput


smooth_factor = 20  # to make the curve smooth
a = 0.01  # normalised_propagation_delay; for CSMA

plt.figure(figsize=(16, 8))

offered_load_rate = [G / smooth_factor for G in range(10 * smooth_factor)]

# reference: Kleinrock-Tobagi paper
mac_protocols = {
    'slotted ALOHA': slotted_aloha_throughput,
    'pure ALOHA': pure_aloha_throughput,
    'non-persistent CSMA': (lambda G: non_persistent_csma_throughput(G, a)),
    '1-persistent CSMA': (lambda G: one_persistent_csma_throughput(G, a)),
}

for mac_protocol in mac_protocols:
    throughput = [
        mac_protocols[mac_protocol](G) 
        for G in offered_load_rate
    ]

    plt.plot(offered_load_rate, throughput, label=mac_protocol)

plt.title(
    'Comparison of the channel utilization versus load '
    'for various random access protocols'
)
plt.xlabel('G (offered load rate)')
plt.ylabel('S (throughput)')

plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

plt.show()
