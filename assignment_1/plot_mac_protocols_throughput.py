import math
import matplotlib.pyplot as plt


smooth_factor = 20  # to make the curve smooth

plt.figure(figsize=(16, 8))

offered_load_rate = [G / smooth_factor for G in range(10 * smooth_factor)]

slotted_aloha_success_rate = lambda G: G * math.e**-G
slotted_aloha_throughput = [
    slotted_aloha_success_rate(G) 
    for G in offered_load_rate
]

pure_aloha_success_rate = lambda G: G * math.e**(-2 * G)
pure_aloha_throughput = [
    pure_aloha_success_rate(G) 
    for G in offered_load_rate
]

plt.plot(offered_load_rate, slotted_aloha_throughput, label='slotted Aloha')
plt.plot(offered_load_rate, pure_aloha_throughput, label='pure Aloha')

plt.title(
    'Comparison of the channel utilization versus load '
    'for various random access protocols'
)
plt.xlabel('G (offered load rate)')
plt.ylabel('S (throughput)')

plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))

plt.show()
