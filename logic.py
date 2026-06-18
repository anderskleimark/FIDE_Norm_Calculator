import math


class Logic:

    dp_table = [(1.0, 800), (0.99, 677), (0.98, 589), (0.97, 538), (0.96, 501), (0.95, 470),
                (0.94, 444), (0.93, 422), (0.92,
                                           401), (0.91, 383), (0.90, 366), (0.89, 351),
                (0.88, 336), (0.87, 322), (0.86,
                                           309), (0.85, 296), (0.84, 284), (0.83, 273),
                (0.82, 262), (0.81, 251), (0.80,
                                           240), (0.79, 230), (0.78, 220), (0.77, 211),
                (0.76, 202), (0.75, 193), (0.74,
                                           184), (0.73, 175), (0.72, 166), (0.71, 158),
                (0.70, 149), (0.69, 141), (0.68,
                                           133), (0.67, 125), (0.66, 117), (0.65, 110),
                (0.64, 102), (0.63, 95), (0.62,
                                          87), (0.61, 80), (0.60, 72), (0.59, 65), (0.58, 57),
                (0.57, 50), (0.56, 43), (0.55, 36), (0.54,
                                                     29), (0.53, 21), (0.52, 14), (0.51, 7),
                (0.50, 0), (0.49, -7), (0.48, -14), (0.47, -
                                                     21), (0.46, -27), (0.45, -36), (0.44, -43),
                (0.43, -50), (0.42, -57), (0.41, -65), (0.40, -72),
                (0.39, -80), (0.38, -87), (0.37, -
                                           95), (0.36, -102), (0.35, -110)

                ]

    def __init__(self, chessplayers):
        self.chessplayers = chessplayers

    # Funktion för att få fram det lägsta elo-talet av motståndarna.
    def get_minimum_opponent_rating(self):
        minimum = 3000
        for player in self.chessplayers:
            if player.rating < minimum:
                minimum = player.rating

        return minimum

    def compute_da(self, norm_type):
        rating_sum = 0
        for player in self.chessplayers:
            if self.get_minimum_opponent_rating() == player.rating:
                if norm_type == "GM":
                    rating += 2200
                elif norm_type == "IM":
                    rating += 2050
            else:
                rating_sum += player.rating

        return rating_sum / len(self.chessplayers)

    def compute_norm_scores(self):
        da_gm = self.compute_da("GM")
        da_im = self.compute_da("IM")
        games = len(self.chessplayers)

        im_points = None
        gm_points = None

        # IM-norm
        if da_im >= 2230:
            for score, dp in self.dp_table:
                if da_im + dp >= 2450:
                    im_points = score * games

        # GM-norm
        if da_gm >= 2380:
            for score, dp in self.dp_table:
                if da_gm + dp >= 2600:
                    gm_points = score * games

        return math.ceil(im_points * 2) / 2, math.ceil(gm_points * 2) / 2
