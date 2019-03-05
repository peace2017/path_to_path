# from path_to_path.path_calculation import path_calculation as path_calc
# import matplotlib.pyplot as plt
# from matplotlib import dates

# # file to open
# AGI0_file = '/media/smironenko/423661C53661BA95/TOPCON/Research/AGI-2/Report/2019_01_08_egnos_kinematic/AGI_0/1_agi0_egnos_dion.tps'
# AGI2_file = '/media/smironenko/423661C53661BA95/TOPCON/Research/AGI-2/Report/2019_01_08_egnos_kinematic/AGI-2/1_agi2_egnos_dion.tps'
# AGI4_file = '/media/smironenko/423661C53661BA95/TOPCON/Research/AGI-2/Report/2019_01_08_egnos_kinematic/AGI-4/1_agi4_egnos_dion.tps'
# SGR1_file = '/media/smironenko/423661C53661BA95/TOPCON/Research/AGI-2/Report/2019_01_08_egnos_kinematic/SGR-1/1_sgr1_egnos_dion.tps'

# """Reference point A in ECEF"""
# # point_A = {'X': 4440694.7519,
# #            'Y': 863805.2863,
# #            'Z': 4481084.0216,
# #            'System': 'ECEF'}

# # or reference point A in BLH
# AGI_0_point_A = {'X': 44,9198160966666667,
#                  'Y': 11,007728795,
#                  'Z': 58,0493,
#                  'System': 'BLH'}
# AGI_2_point_A = {'X': 44.91977540833333,
#                  'Y': 11.00770264833333,
#                  'Z': 58.0533,
#                  'System': 'BLH'}
# AGI_4_point_A = {'X': 44.91980596833333,
#                  'Y': 11.007725075,
#                  'Z': 58.0718,
#                  'System': 'BLH'}
# SGR1_point_A = {'X': 44.91975698,
#                 'Y': 11.007692985,
#                 'Z': 58.0212,
#                 'System': 'BLH'}

# """reference point B in ECEF"""
# # point_B = {'X': 4440641.5515,
# #            'Y': 863830.7878,
# #            'Z': 4481131.7792,
# #            'System': 'ECEF'}

# # or reference point B in BLH

# AGI_0_point_B = {'X': 44,920421265,
#                  'Y': 11,0081744883333333,
#                  'Z': 58,2422,
#                  'System': 'BLH'}
# AGI_2_point_B = {'X': 44.92046749333333,
#                  'Y': 11.00821197166667,
#                  'Z': 58.3056,
#                  'System': 'BLH'}
# AGI_4_point_B = {'X': 44.92042890333333,
#                  'Y': 11.00818372,
#                  'Z': 58.2713,
#                  'System': 'BLH'}
# SGR1_point_B = {'X': 44.92044915833333,
#                 'Y': 11.00820211166667,
#                 'Z': 58.2663,
#                 'System': 'BLH'}

# '''calculation based on NMEA GGA then message = GGA or
#  based on PV then message = PV'''
# messages = 'GGA'

# p2p_AGI0 = path_calc.PathCalc(AGI0_file,
#                               AGI_0_point_A,
#                               AGI_0_point_B,
#                               messages)
# # p2p_AGI2 = path_calc.PathCalc(AGI2_file,
# #                               AGI_2_point_A,
# #                               AGI_2_point_B,
# #                               messages)
# # p2p_AGI4 = path_calc.PathCalc(AGI4_file,
# #                               AGI_4_point_A,
# #                               AGI_4_point_B,
# #                               messages)
# # p2p_SGR1 = path_calc.PathCalc(SGR1_file,
# #                               SGR1_point_A,
# #                               SGR1_point_B,
# #                               messages)


# fig, ax = plt.subplots()
# ax_plot1, = ax.plot(p2p_AGI0.time_AB, p2p_AGI0.xtrack_AB, c='b', label='AGI-0')
# # ax_plot2, = ax.plot(p2p_AGI2.time_AB, p2p_AGI2.xtrack_AB, c='r', label='AGI-2')
# # ax_plot3, = ax.plot(p2p_AGI4.time_AB, p2p_AGI4.xtrack_AB, c='y', label='AGI-4')
# # ax_plot4, = ax.plot(p2p_SGR1.time_AB, p2p_SGR1.xtrack_AB, c='g', label='SGR-1')
# ax.set_title("Xtrack AB-line")
# ax.set_xlabel('Time')
# ax.set_ylabel('Xtrack, meters')
# ax.legend()
# plt.grid(True)
# plt.gcf().autofmt_xdate()
# myFmt = dates.DateFormatter('%H:%M:%S')
# plt.gca().xaxis.set_major_formatter(myFmt)

# fig, ax1 = plt.subplots()
# ax1_plot1, = ax1.plot(p2p_AGI0.time_AB[:-900], p2p_AGI0.p2p, c='b', label='AGI-0')
# # # ax1_plot2, = ax1.plot(p2p_AGI2.time_AB[:-900], p2p_AGI2.p2p, c='r', label='AGI-2')
# # # ax1_plot3, = ax1.plot(p2p_AGI4.time_AB[:-900], p2p_AGI4.p2p, c='y', label='AGI-4')
# # # ax1_plot4, = ax1.plot(p2p_SGR1.time_AB[:-900], p2p_SGR1.p2p, c='g', label='SGR-1')

# ax1.set_title("Path-to-path AB-line")
# ax1.set_xlabel('Time')
# ax1.set_ylabel('P2P, meters')
# ax1.legend()
# plt.grid(True)
# plt.gcf().autofmt_xdate()
# myFmt = dates.DateFormatter('%H:%M:%S')
# plt.gca().xaxis.set_major_formatter(myFmt)

# plt.show()
