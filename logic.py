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

    def __init__(self, opponents, player_federation):
        self.opponents = opponents
        self.player_federation = player_federation

    def get_federation_requirement_status(self):
        federations = []
        number_of_foreign_federations = 0
        number_of_players_from_same_federation = 0

        for opponent in self.opponents:
            if not opponent.federation in federations:
                federations.append(opponent.federation)
            if self.player_federation == opponent.federation:
                number_of_players_from_same_federation += 1
            else:
                number_of_foreign_federations += 1

        return len(federations) > 2 and number_of_players_from_same_federation <= math.floor(0.6 * len(self.opponents)) and number_of_foreign_federations <= math.floor(2*len(self.opponents)/3)

        # Funktion för att få fram det lägsta elo-talet av motståndarna.

    def get_minimum_opponent_rating(self):
        minimum = 3000
        for player in self.opponents:
            if player.rating < minimum:
                minimum = player.rating

        return minimum

    def compute_da(self, norm_type):
        rating_sum = 0
        min_rating = self.get_minimum_opponent_rating()

        replaced = False

        for player in self.opponents:
            if player.rating == min_rating and not replaced:
                replaced = True
                rating_sum += 2200 if norm_type == "GM" else 2050
            else:
                rating_sum += player.rating

        return rating_sum / len(self.opponents)

    def compute_norm_scores(self):
        da_im = self.compute_da("IM")
        da_gm = self.compute_da("GM")
        games = len(self.opponents)

        im_points = None
        gm_points = None

        if da_im >= 2230:
            for score, dp in self.dp_table:
                if da_im + dp >= 2450:
                    im_points = score * games
                else:
                    break  # viktigt: när det slutar uppfylla villkoret

        if da_gm >= 2380:
            for score, dp in self.dp_table:
                if da_gm + dp >= 2600:
                    gm_points = score * games
                else:
                    break

        def safe(x):
            return None if x is None else math.ceil(x * 2) / 2

        return safe(im_points), safe(gm_points)
