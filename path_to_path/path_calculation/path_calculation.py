from asic_processing import parser_asic
from asic_processing import structurizer
from convertor_coordinates import ilocal as lc
import math
import numpy as np
import datetime


class PathCalc:

    def __init__(self, file, point_A, point_B, messages):
        self.GGA = []
        self.PV = []
        self.file = file
        self.point_A_global = point_A
        self.point_B_global = point_B
        self.messages = messages

        self.point_A_enu = {'E': 0.0,
                            'N': 0.0,
                            'U': 0.0}

        self.point_B_enu = {'E': 0.0,
                            'N': 0.0,
                            'U': 0.0}

        self.heading_AB = 0

        self.xtrack_AB = []
        self.time_AB = []
        self.p2p = []

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

    def data_storage(self, key, data):
        if key == 'GGA':
            self.GGA.append(data)
        elif key == 'PV':
            self.PV.append(data)

    def set_local_system(self):
        if (self.point_A_global['System'] == 'BLH' and
                self.point_B_global['System'] == 'BLH'):

            temp_A = np.array([math.radians(self.point_A_global['X']),
                               math.radians(self.point_A_global['Y']),
                               math.radians(self.point_A_global['Z'])])

            local_centre = lc.Geodetic2ECEF(temp_A)

            lc.InitENUNED(local_centre)

            temp_B_ecef = lc.Geodetic2ECEF(
                np.array([math.radians(self.point_B_global['X']),
                          math.radians(self.point_B_global['Y']),
                          math.radians(self.point_B_global['Z'])]))

            temp_B = lc.PosECEF2ENU(
                np.array([temp_B_ecef[0],
                          temp_B_ecef[1],
                          temp_B_ecef[2]]))

            self.point_B_enu = {'E': temp_B[0],
                                'N': temp_B[1],
                                'U': temp_B[2]}

        if (self.point_A_global['System'] == 'ECEF' and
                self.point_B_global['System'] == 'ECEF'):

            local_centre = {'X': self.point_A_global['X'],
                            'Y': self.point_A_global['Y'],
                            'Z': self.point_A_global['Z']}

            lc.InitENUNED(local_centre)

            temp_B = lc.PosECEF2ENU(
                np.array([self.point_B_global['X'],
                          self.point_B_global['Y'],
                          self.point_B_global['Z']]))

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

        if self.messages == 'GGA':
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
                self.p2p.append(self.xtrack_AB[i] - self.xtrack_AB[i + 900])

        elif self.messages == 'PV':
            pass

    def statistic(self):
        if not self.xtrack_AB:
            xt_rms = np.std(self.xtrack_AB)
            xt_mean = np.mean(self.xtrack_AB)

        if not self.p2p:
            p2p_rms = np.std(self.p2p)
            p2p_mean = np.mean(self.p2p)
