"""Implements Alphabet cuts."""

"""
alphabet size 对应的 数值字母对应表
    0周围切分密集 高斯分布
"""


import numpy as np


def cuts_for_asize(a_size):
    """Generate a set of alphabet cuts for its size."""
    """ Typically, we generate cuts in R as follows:
        get_cuts_for_num <- function(num) {
        cuts = c(-Inf)
        for (i in 1:(num-1)) {
            cuts = c(cuts, qnorm(i * 1/num))
            }
            cuts
        }
        get_cuts_for_num(3) """
    options = {
        2: np.array([-np.inf,  0.00]),
        3: np.array([-np.inf, -0.4307273, 0.4307273]),
        4: np.array([-np.inf, -0.6744898, 0, 0.6744898]),
        5: np.array([-np.inf, -0.841621233572914, -0.2533471031358,
                    0.2533471031358, 0.841621233572914]),
        6: np.array([-np.inf, -0.967421566101701, -0.430727299295457, 0,
                    0.430727299295457, 0.967421566101701]),
        7: np.array([-np.inf, -1.06757052387814, -0.565948821932863,
                    -0.180012369792705, 0.180012369792705, 0.565948821932863,
                    1.06757052387814]),
        8: np.array([-np.inf, -1.15034938037601, -0.674489750196082,
                    -0.318639363964375, 0, 0.318639363964375,
                    0.674489750196082, 1.15034938037601]),
        9: np.array([-np.inf, -1.22064034884735, -0.764709673786387,
                    -0.430727299295457, -0.139710298881862, 0.139710298881862,
                    0.430727299295457, 0.764709673786387, 1.22064034884735]),
        10: np.array([-np.inf, -1.2815515655446, -0.841621233572914,
                     -0.524400512708041, -0.2533471031358, 0, 0.2533471031358,
                     0.524400512708041, 0.841621233572914, 1.2815515655446]),
        11: np.array([-np.inf, -1.33517773611894, -0.908457868537385,
                     -0.604585346583237, -0.348755695517045,
                     -0.114185294321428, 0.114185294321428, 0.348755695517045,
                     0.604585346583237, 0.908457868537385, 1.33517773611894]),
        12: np.array([-np.inf, -1.38299412710064, -0.967421566101701,
                     -0.674489750196082, -0.430727299295457,
                     -0.210428394247925, 0, 0.210428394247925,
                     0.430727299295457, 0.674489750196082, 0.967421566101701,
                     1.38299412710064]),
        13: np.array([-np.inf, -1.42607687227285, -1.0200762327862,
                     -0.736315917376129, -0.502402223373355,
                     -0.293381232121193, -0.0965586152896391,
                     0.0965586152896394, 0.293381232121194, 0.502402223373355,
                     0.73631591737613, 1.0200762327862, 1.42607687227285]),
        14: np.array([-np.inf, -1.46523379268552, -1.06757052387814,
                     -0.791638607743375, -0.565948821932863, -0.36610635680057,
                     -0.180012369792705, 0, 0.180012369792705,
                     0.36610635680057, 0.565948821932863, 0.791638607743375,
                     1.06757052387814, 1.46523379268552]),
        15: np.array([-np.inf, -1.50108594604402, -1.11077161663679,
                     -0.841621233572914, -0.622925723210088,
                     -0.430727299295457, -0.2533471031358, -0.0836517339071291,
                     0.0836517339071291, 0.2533471031358, 0.430727299295457,
                     0.622925723210088, 0.841621233572914, 1.11077161663679,
                     1.50108594604402]),
        16: np.array([-np.inf, -1.53412054435255, -1.15034938037601,
                     -0.887146559018876, -0.674489750196082,
                     -0.488776411114669, -0.318639363964375,
                     -0.157310684610171, 0, 0.157310684610171,
                     0.318639363964375, 0.488776411114669, 0.674489750196082,
                     0.887146559018876, 1.15034938037601, 1.53412054435255]),
        17: np.array([-np.inf, -1.5647264713618, -1.18683143275582,
                     -0.928899491647271, -0.721522283982343,
                     -0.541395085129088, -0.377391943828554,
                     -0.223007830940367, -0.0737912738082727,
                     0.0737912738082727, 0.223007830940367, 0.377391943828554,
                     0.541395085129088, 0.721522283982343, 0.928899491647271,
                     1.18683143275582, 1.5647264713618]),
        18: np.array([-np.inf, -1.59321881802305, -1.22064034884735,
                     -0.967421566101701, -0.764709673786387,
                     -0.589455797849779, -0.430727299295457,
                     -0.282216147062508, -0.139710298881862, 0,
                     0.139710298881862, 0.282216147062508, 0.430727299295457,
                     0.589455797849779, 0.764709673786387, 0.967421566101701,
                     1.22064034884735, 1.59321881802305]),
        19: np.array([-np.inf, -1.61985625863827, -1.25211952026522,
                     -1.00314796766253, -0.8045963803603, -0.633640000779701,
                     -0.47950565333095, -0.336038140371823, -0.199201324789267,
                     -0.0660118123758407, 0.0660118123758406,
                     0.199201324789267, 0.336038140371823, 0.47950565333095,
                     0.633640000779701, 0.8045963803603, 1.00314796766253,
                     1.25211952026522, 1.61985625863827]),
        20: np.array([-np.inf, -1.64485362695147, -1.2815515655446,
                     -1.03643338949379, -0.841621233572914, -0.674489750196082,
                     -0.524400512708041, -0.385320466407568, -0.2533471031358,
                     -0.125661346855074, 0, 0.125661346855074, 0.2533471031358,
                     0.385320466407568, 0.524400512708041, 0.674489750196082,
                     0.841621233572914, 1.03643338949379, 1.2815515655446,
                     1.64485362695147]),
    }

    return options[a_size]
