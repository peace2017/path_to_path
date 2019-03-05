from asic_processing import parser_asic
from asic_processing import structurizer
from convertor_coordinates import ilocal as lc
import math
import numpy as np
import datetime


class PathCalc:

    def __init__(self, desc):
        self.file = desc['Name']
        self.point_A_global = desc['Points']['A']
        self.point_B_global = desc['Points']['B']
        self.messages = desc['Message']
        self.system = desc['System']
        self.GGA = []
        self.PV = []

        self.point_A_enu = {'E': 0.0,
                            'N': 0.0,
                            'U': 0.0}

        self.point_B_enu = {'E': 0.0,
                            'N': 0.0,
                            'U': 0.0}

        self.heading_AB = 0

        self.xtrack_AB = []
        self.time_AB = []
        self.p2p_AB = []

        self.xt_rms = 0.0
        self.xt_mean = 0.0
        self.ptp_rms = 0.0
        self.ptp_mean = 0.0

        self.structurizer = structurizer.Structirizer(self.data_storage)
        self.parser_asic = parser_asic.ParserAsic(
            self.structurizer.to_structurize)

        max_size = 256
        with open(self.file, mode='rb') as self.file:
            while True:
                fileContent = self.file.read(max_size)
                if not fileContent:
                    break
                self.parser_asic.write_data(fileContent)

        self.set_local_system()
        self.analyse()
        self.statistic()

    def data_storage(self, key, data):
        if key == 'GGA':
            self.GGA.append(data)
        elif key == 'PV':
            self.PV.append(data)

    def set_local_system(self):
        if (self.system == 'Lat. Lon. Alt - BLH'):
            temp_A = np.array([math.radians(self.point_A_global['X_lat']),
                               math.radians(self.point_A_global['Y_lon']),
                               math.radians(self.point_A_global['Z_alt'])])

            local_centre = lc.Geodetic2ECEF(temp_A)

            lc.InitENUNED(local_centre)

            temp_B_ecef = lc.Geodetic2ECEF(
                np.array([math.radians(self.point_B_global['X_lat']),
                          math.radians(self.point_B_global['Y_lon']),
                          math.radians(self.point_B_global['Z_alt'])]))

            temp_B = lc.PosECEF2ENU(
                np.array([temp_B_ecef[0],
                          temp_B_ecef[1],
                          temp_B_ecef[2]]))

            self.point_B_enu = {'E': temp_B[0],
                                'N': temp_B[1],
                                'U': temp_B[2]}

        if (self.system == 'XYZ - ECEF'):

            local_centre = {'X': self.point_A_global['X_lat'],
                            'Y': self.point_A_global['Y_lon'],
                            'Z': self.point_A_global['Z_alt']}

            lc.InitENUNED(local_centre)

            temp_B = lc.PosECEF2ENU(
                np.array([self.point_B_global['X_lat'],
                          self.point_B_global['Y_lon'],
                          self.point_B_global['Z_alt']]))

            self.point_B_enu = {'E': temp_B[0],
                                'N': temp_B[1],
                                'U': temp_B[2]}

        self.heading_AB = math.atan2(
            self.point_A_enu['N'] - self.point_B_enu['N'],
            self.point_A_enu['E'] - self.point_B_enu['E'])

        self.heading_AB = math.degrees(self.heading_AB)

    def analyse(self):
        pos_ant = []  # antenna position ENU
        pos_ant_AB = []  # antenna position ENU on AB-line
        pos_ant_hor = []  # antenna position ENU aligned in horizon

        if self.messages == 'nmea GGA':
            lat = [math.radians(
                lat['lat']) for lat in self.GGA if 'lat' in lat]
            lon = [math.radians(
                lon['lon']) for lon in self.GGA if 'lat' in lon]
            alt = [alt['alt'] for alt in self.GGA if 'alt' in alt]
            time = [time['time'] for time in self.GGA if 'time' in time]

            for b, l, h, t in zip(lat, lon, alt, time):
                xyz = lc.Geodetic2ECEF(np.array([b, l, h]))
                enu = lc.PosECEF2ENU(xyz)

                pos_ant.append([enu[0],
                                enu[1],
                                enu[2],
                                t])

            pos_ant = np.array(pos_ant)

            for pos in pos_ant:
                if(pos[0] >= self.point_A_enu['E'] and
                   pos[0] <= self.point_B_enu['E'] and
                   pos[1] >= self.point_A_enu['N'] and
                   pos[1] <= self.point_B_enu['N']):
                    pos_ant_AB.append(pos)

            pos_ant_AB = np.array(pos_ant_AB)

            alfa = -math.radians(self.heading_AB)
            cos_ = math.cos(alfa)
            sin_ = math.sin(alfa)

            rotation_matrix_AB = np.array([
                [cos_, -sin_, self.point_A_enu['E']],
                [sin_, cos_, self.point_A_enu['N']],
                [0, 0, 1]
            ])

            for _ in pos_ant_AB:
                temp = np.array([_[0] - self.point_A_enu['E'],
                                 _[1] - self.point_A_enu['N'],
                                 1])

                rot = rotation_matrix_AB.dot(temp)

                pos_ant_hor.append([rot[0],
                                    rot[1],
                                    rot[2]])

            pos_ant_hor = np.array(pos_ant_hor)
            for time in pos_ant_AB[:, 3]:
                hours = int(str(time)[:2])
                minutes = int(str(time)[2:4])
                sec = int(str(time)[4:6])
                msec = int(str(time)[7:])
                self.time_AB.append(
                    datetime.datetime(1970, 1, 1, hours, minutes, sec, msec))

            self.xtrack_AB = \
                [_[1] - self.point_A_enu['N'] for _ in pos_ant_hor]

            for i in range(len(self.xtrack_AB) - 900):
                self.p2p_AB.append(self.xtrack_AB[i] - self.xtrack_AB[i + 900])

        elif self.messages == 'binary PV':
            pass

    def statistic(self):
        if self.xtrack_AB:
            self.xt_rms = ("{0:.4f}".format(np.std(self.xtrack_AB)))
            self.xt_mean = ("{0:.4f}".format(np.mean(self.xtrack_AB)))

        if self.p2p_AB:
            self.ptp_rms = ("{0:.4f}".format(np.std(self.p2p_AB)))
            self.ptp_mean = ("{0:.4f}".format(np.mean(self.p2p_AB)))
