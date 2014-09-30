# create device bindings for LIVE BCF2000
BCF_LIVE = [{(0, 81): ["state.zn",  '0',  "radius", (1.0, 1.0)],
             (0, 82): ["state.zn",  '2',  "radius", (1.0, 1.0)],
             (0, 83): ["state.zn",  '8',  "radius", (1.0, 1.0)],
             (0, 84): ["state.zn",  '9',  "radius", (1.0, 0.0)],
             (0, 85): ["state.zn",  '10', "radius", (1.0, 1.0)],
             (0, 86): ["state.zn",  '11', "radius", (1.0, 0.0)],
             (0, 87) : ["state.par", 'self.state.par_idx("_SEED_W")',  "val",    (1.0, 0.0)],
             (0, 88) : ["state.par", 'self.state.par_idx("_COLOR_A")',  "val",    (0.6, 0.4)],
             (0, 1) : ["state.par", 'self.state.par_idx("_COLOR_PHI1")',  "val",    (1.0, 0.0)],
             (0, 2) : ["state.par", 'self.state.par_idx("_COLOR_PSI1")',  "val",    (1.0, 0.0)],
             (0, 3) : ["state.par", 'self.state.par_idx("_COLOR_BASE_PHI")',  "val",    (1.0, 0.0)],
             (0, 4) : ["state.par", 'self.state.par_idx("_COLOR_BASE_PSI")',  "val",    (1.0, 0.0)],
             (0, 5) : ["state.par", 'self.state.par_idx("_SEED_W_MIN")',  "val",    (0.5, 0.0)],
             (0, 6) : ["state.par", 'self.state.par_idx("_COLOR_S")',  "val",    (1.0, 0.0)],
             (0, 7) : ["state.zn",  '8',  "th",     (3.14, 0.0)],
             (0, 8) : ["state.zn",  '10',  "th",     (3.14, 0.0)]
             }]


# create device bindings for BCF2000
BCF_VJ   = [{(0, 83): ["state.zn",  '0',  "radius", (1.0, 1.0)],
             (0, 84): ["state.zn",  '2',  "radius", (1.0, 1.0)],
             (0, 85): ["state.zn",  '8',  "radius", (1.0, 1.0)],
             (0, 86): ["state.zn",  '9',  "radius", (1.0, 0.0)],
             (0, 87): ["state.zn",  '10', "radius", (1.0, 1.0)],
             (0, 88): ["state.zn",  '11', "radius", (1.0, 0.0)],
             (0, 1) : ["state.par", 'self.state.par_idx("_SEED_W")',  "val",    (1.0, 0.0)],
             (0, 2) : ["state.par", 'self.state.par_idx("_COLOR_PHI1")',  "val",    (1.0, 0.0)],
             (0, 3) : ["state.par", 'self.state.par_idx("_COLOR_PSI1")',  "val",    (1.0, 0.0)],
             (0, 4) : ["state.par", 'self.state.par_idx("_COLOR_BASE_PHI")',  "val",    (1.0, 0.0)],
             (0, 5) : ["state.par", 'self.state.par_idx("_COLOR_BASE_PSI")',  "val",    (1.0, 0.0)],
             (0, 6) : ["state.par", 'self.state.par_idx("_COLOR_A")',  "val",    (0.6, 0.4)],
             (0, 7) : ["state.par", 'self.state.par_idx("_SEED_W_MIN")',  "val",    (0.5, 0.0)],
             (0, 8) : ["state.zn",  '8',  "th",     (3.14, 0.0)]

             },
            {(0, 83): ["state.par", 'self.state.par_idx("_COLOR_DHUE")',  "val",    (1.0, 0.0)],
             (0, 84): ["state.par", 'self.state.par_idx("_COLOR_I")',  "val",    (1.0, 0.0)],
             (0, 85): ["state.par", 'self.state.par_idx("_COLOR_BASE_I")',  "val",    (1.0, 0.0)],
             (0, 86): ["state.par", 'self.state.par_idx("_HSLS_RESET_Z")',  "val",    (1.0, 0.0)],
             (0, 87): ["state.par", 'self.state.par_idx("_COLOR_LEN_SC")',  "val",    (1.0, 0.0)],
             (0, 88): ["state.par", 'self.state.par_idx("_COLOR_S")',  "val",    (1.0, 0.0)],
             (0, 1) : ["state.par", 'self.state.par_idx("_COLOR_PHI1")',  "val",    (1.0, 0.0)],
             (0, 2) : ["state.par", 'self.state.par_idx("_COLOR_PSI1")',  "val",    (1.0, 0.0)],
             (0, 3) : ["state.par", 'self.state.par_idx("_COLOR_PHI2")',  "val",    (1.0, 0.0)],
             (0, 4) : ["state.par", 'self.state.par_idx("_COLOR_PSI2")',  "val",    (1.0, 0.0)],
             (0, 5) : ["state.par", 'self.state.par_idx("_COLOR_BASE_PHI")',  "val",    (1.0, 0.0)],
             (0, 6) : ["state.par", 'self.state.par_idx("_COLOR_BASE_PSI")',  "val",    (1.0, 0.0)],
             (0, 7) : ["state.par", 'self.state.par_idx("_COLOR_KILL")', "val",    (1.0, 0.0)],
             },
            {(0, 83): ["state.zn",  '0',  "radius", (5.0, 0.0)],
             (0, 84): ["state.zn",  '1',  "radius", (1.0, 0.0)],
             (0, 85): ["state.zn",  '2',  "radius", (5.0, 0.0)],
             (0, 86): ["state.zn",  '3',  "radius", (1.0, 0.0)],
             (0, 3) : ["state.zn",  '0',  "th",     (3.14, 0.0)],
             (0, 4) : ["state.zn",  '1',  "th",     (3.14, 0.0)],
             (0, 5) : ["state.zn",  '2',  "th",     (3.14, 0.0)],
             (0, 6) : ["state.zn",  '3',  "th",     (3.14, 0.0)]},
            {(0, 83): ["state.zn",  '8',  "radius", (5.0, 0.0)],
             (0, 84): ["state.zn",  '9',  "radius", (1.0, 0.0)],
             (0, 85): ["state.zn",  '10', "radius", (5.0, 0.0)],
             (0, 86): ["state.zn",  '11', "radius", (1.0, 0.0)],
             (0, 3) : ["state.zn",  '8',  "th",     (3.14, 0.0)],
             (0, 4) : ["state.zn",  '9',  "th",     (3.14, 0.0)],
             (0, 5) : ["state.zn",  '10', "th",     (3.14, 0.0)],
             (0, 6) : ["state.zn",  '11', "th",     (3.14, 0.0)]}
             ]


# create advanced device bindings for BCF2000
BCF_FULL = [{(0, 81): ["state.zn", '0', "radius", (4.0, 0.0)],
             (0, 82): ["state.zn", '1', "radius", (4.0, 0.0)],
             (0, 83): ["state.zn", '2', "radius", (4.0, 0.0)],
             (0, 84): ["state.zn", '3', "radius", (4.0, 0.0)],
             (0, 85): ["state.zn", '4', "radius", (4.0, 0.0)],
             (0, 86): ["state.zn", '5', "radius", (4.0, 0.0)],
             (0, 87): ["state.zn", '6', "radius", (4.0, 0.0)],
             (0, 88): ["state.zn", '7', "radius", (4.0, 0.0)]}]
BCF_FULL[0].update(dict([((0, 1 + i), ["state.zn", str(i), "th", (2.0 * 3.14159, 0.0)]) for i in xrange(8)]))

BCF_FULL.append({(0, 81): ["state.zn", '8',  "radius", (4.0, 0.0)],
                 (0, 82): ["state.zn", '9',  "radius", (1.0, 0.0)],
                 (0, 83): ["state.zn", '10', "radius", (4.0, 0.0)],
                 (0, 84): ["state.zn", '11', "radius", (1.0, 0.0)],
                 (0, 85): ["state.zn", '12', "radius", (1.0, 0.0)],
                 (0, 86): ["state.zn", '13', "radius", (1.0, 0.0)],
                 (0, 87): ["state.zn", '14', "radius", (1.0, 0.0)],
                 (0, 88): ["state.zn", '15', "radius", (1.0, 0.0)]})
BCF_FULL[1].update(dict([((0, 1 + i), ["state.zn", str(8 + i), "th", (2.0 * 3.14159, 0.0)]) for i in xrange(8)]))

BCF_FULL.append(dict([((0, 81 + i), ["state.par", str(i),      "val", (1.0, 0.0)]) for i in xrange(8)]))
BCF_FULL.append(dict([((0, 81 + i), ["state.par", str(i + 8),  "val", (1.0, 0.0)]) for i in xrange(8)]))
BCF_FULL.append(dict([((0, 81 + i), ["state.par", str(i + 16), "val", (1.0, 0.0)]) for i in xrange(8)]))
BCF_FULL.append(dict([((0, 81 + i), ["state.par", str(i + 24), "val", (1.0, 0.0)]) for i in xrange(8)]))
BCF_FULL.append(dict([((0, 81 + i), ["state.par", str(i + 32), "val", (1.0, 0.0)]) for i in xrange(8)]))


# create device bindings for UC-33
UC = [{(0, 7): ["state.zn",  '0',  "radius", (1.0, 1.0)],
       (1, 7): ["state.zn",  '1',  "radius", (1.0, 0.0)],
       (2, 7): ["state.zn",  '2',  "radius", (1.0, 1.0)],
       (3, 7): ["state.zn",  '3',  "radius", (1.0, 0.0)],
       (4, 7): ["state.zn",  '8',  "radius", (1.0, 1.0)],
       (5, 7): ["state.zn",  '9',  "radius", (1.0, 0.0)],
       (6, 7): ["state.zn",  '10', "radius", (1.0, 1.0)],
       (7, 7): ["state.zn",  '11', "radius", (1.0, 0.0)],
       (0, 10) : ["state.par", 'self.state.par_idx("_SEED_W")',  "val",    (0.4, 0.2)],
       (1, 10) : ["state.par", 'self.state.par_idx("_COLOR_PHI")',  "val",    (1.0, 0.0)],
       (2, 10) : ["state.par", 'self.state.par_idx("_COLOR_PSI")',  "val",    (1.0, 0.0)],
       (3, 10) : ["state.par", 'self.state.par_idx("_COLOR_A")',  "val",    (0.6, 0.4)],
       (4, 10) : ["state.par", 'self.state.par_idx("_COLOR_S")',  "val",    (0.8, 0.2)],
       (5, 10) : ["state.zn",  '8',  "th",     (3.14, 0.0)],
       (6, 10) : ["state.par", 'self.state.par_idx("_SEED_W_THRESH")',  "val",    (0.6, 0.0)],
       (7, 10) : ["state.par", 'self.state.par_idx("_COLOR_DHUE")', "val",    (1.0, 0.0)],
       (0, 12) : ["state.par", 'self.state.par_idx("_SEED_W")',  "val",    (0.4, 0.2)],
       (1, 12) : ["state.par", 'self.state.par_idx("_COLOR_PHI")',  "val",    (1.0, 0.0)],
       (2, 12) : ["state.par", 'self.state.par_idx("_COLOR_PSI")',  "val",    (1.0, 0.0)],
       (3, 12) : ["state.par", 'self.state.par_idx("_COLOR_A")',  "val",    (0.6, 0.4)],
       (4, 12) : ["state.par", 'self.state.par_idx("_COLOR_S")',  "val",    (0.8, 0.2)],
       (5, 12) : ["state.zn",  '8',  "th",     (3.14, 0.0)],
       (6, 12) : ["state.par", 'self.state.par_idx("_SEED_W_THRESH")',  "val",    (0.6, 0.0)],
       (7, 12) : ["state.par", 'self.state.par_idx("_COLOR_DHUE")', "val",    (1.0, 0.0)],
       }]


nanoKONTROL = [{(0,2): ["state.zn", '0', "radius", (0.7, 0.7)],
                (0,3): ["state.zn", '2', "radius", (0.7, 0.7)],
                (0,4): ["state.zn", '16', "radius", (0.7, 0.7)],
                (0,5): ["state.zn", '18', "radius", (0.7, 0.7)],
                (0,6): ["state.zn", '17', "radius", (1.0, 0.0)],
                (0,8): ["state.zn", '19', "radius", (1.0, 0.0)],
                (0,16): ["state.zn", '16', "th",     (3.14, 0.0)]

            }]
