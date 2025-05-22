import matplotlib.pyplot as plt
import matplotlib.patches as patches
from src.inertia_analysis.moments_of_inerta import InertiaAnalysis
from utility.fixtures_utiility import SQUARE_CUP_DIM, RECTANGULAR_CUP_DIM_X, RECTANGULAR_CUP_DIM_Y
import math
import json


class ResultDisplayer:
    """
    This class is responsible for displaying the results of the fixture analysis.
    """

    def __init__(self, workpiece_vertices):
        """
        Initializes the ResultDisplayer with the vertices of the workpiece.

        Args:
            workpiece_vertices (list of tuple): A list of tuples representing the vertices of the workpiece.
                                                Each tuple contains the x and y coordinates of a vertex.
        """
        self.workpiece_vertices = workpiece_vertices

    def show_results(self, file_path):
        """
        Displays the results of the fixture analysis by reading data from a JSON file and plotting the results.

        Args:
            file_path (str): The path to the JSON file containing the fixture analysis results.

        Raises:
            ValueError: If the total area of the fixtures is zero, making it impossible to compute the center of gravity.
        """
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)

        x = data["x"]
        y = data["y"]
        selected_fixtures = data["selected_fixture"]
        fixture_types = data["fixture_type"]
        fixtures_center_x = data["fixtures_center_x"]
        fixtures_center_y = data["fixtures_center_y"]
        x_g, y_g = self.__compute_center_of_gravity(
            selected_fixtures, fixture_types, fixtures_center_x, fixtures_center_y,
            {1: SQUARE_CUP_DIM, 2: SQUARE_CUP_DIM}, {1: RECTANGULAR_CUP_DIM_X, 2: RECTANGULAR_CUP_DIM_Y}
        )

        polygons = []
        distance_obj = 0

        for i in range(len(fixture_types)):
            if selected_fixtures[i] == 1:
                for j in range(i, len(fixture_types)):
                    if selected_fixtures[j] == 1:
                        distance_obj += (fixtures_center_x[j] - fixtures_center_x[i]) + (x[i] == x[j]) * (
                                fixtures_center_y[j] - fixtures_center_y[i])

        for idx in range(len(selected_fixtures)):
            if selected_fixtures[idx] == 1:
                if fixture_types[idx] == 1:
                    distance_obj += SQUARE_CUP_DIM + SQUARE_CUP_DIM
                elif fixture_types[idx] == 2:
                    distance_obj += RECTANGULAR_CUP_DIM_X + RECTANGULAR_CUP_DIM_Y

        for idx in range(len(fixture_types)):
            if selected_fixtures[idx] == 1:
                fixture_x, fixture_y = self.__create_fixture(fixture_types[idx], x[idx], y[idx])
                fixture_coords = list(zip(fixture_x, fixture_y))
                jx, jy, jxy = InertiaAnalysis.compute_absolute_moments_of_inertia(fixture_coords)

                fixture = {
                    "area": 21025 if fixture_types[idx] == 1 else 7975,
                    "absolute_moments_of_inertia": [jx, jy, jxy],
                    "barycenter": (fixtures_center_x[idx], fixtures_center_y[idx]),
                    "angle": 0,
                    "idx": idx
                }

                jxg, jyg, jxyg = InertiaAnalysis.compute_baricentric_moments_of_inertia(fixture)

                fixture["baricentric_moments_of_inertia"] = [jxg, jyg, jxyg]
                polygons.append(fixture)

        j_xg, j_yg = InertiaAnalysis.compute_combined_baricentric_moments_of_inertia(polygons, x_g, y_g)

        print("\n-------------Principal Moments of Inertia-------------\n")
        print(f"Principal Moment I: {j_xg:.5e}")
        print(f"Principal moment J: {j_yg:.5e}")
        print(f"I + J: {j_xg + j_yg:.5e}")

        plt.figure(figsize=(8, 6))
        x_workpiece, y_workpiece = zip(*self.workpiece_vertices)
        plt.plot(x_workpiece, y_workpiece, '-o', label="Polygon", linewidth=2)
        plt.scatter(*zip(*self.workpiece_vertices), color='red', zorder=5, label="Vertices")

        for idx, fixture in enumerate(polygons):
            fixture_coords = list(zip(*self.__create_fixture(fixture_types[fixture["idx"]], x[idx], y[idx])))
            patch = patches.Polygon(fixture_coords, closed=True, edgecolor='black', facecolor='none', hatch='/')
            plt.gca().add_patch(patch)
            barycenter_x, barycenter_y = fixture["barycenter"]
            plt.scatter(barycenter_x, barycenter_y, color='green', zorder=5)
            plt.text(barycenter_x + 5, barycenter_y + 5, f"c{idx + 1}", color="green", fontsize=10)

        manhattan_distance = 0

        for i in range(len(selected_fixtures)):
            if selected_fixtures[i] == 1:
                for j in range(i + 1, len(selected_fixtures)):
                    if selected_fixtures[j] == 1:
                        x1, y1 = fixtures_center_x[i], fixtures_center_y[i]
                        x2, y2 = fixtures_center_x[j], fixtures_center_y[j]

                        distance = abs((x2 - x1)) + abs(y2 - y1)
                        manhattan_distance += distance
                        plt.plot([x1, x2], [y1, y2], color='gray', linestyle='--', linewidth=0.8)

                        # Annotate the distance
                        mid_x, mid_y = (x1 + x2) / 2, (y1 + y2) / 2
                        plt.text(mid_x, mid_y, f"{distance:.2f}", color='purple', fontsize=10)

        print("\n----------Manhattan Distance between centers----------\n")
        print(f"Distance: {manhattan_distance}")

        plt.scatter(x_g, y_g, color='black', label="Overall center of gravity", zorder=5)
        plt.text(x_g + 5, y_g + 5, f"g({self.__truncate(x_g, 3)}, {self.__truncate(y_g, 3)})", color="black",
                 fontsize=10)

        plt.xlabel("X-coordinate")
        plt.ylabel("Y-coordinate")
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.gca().set_aspect('equal', adjustable='box')
        plt.show()

    def __square_suction_fixture(self, lb_x, lb_y):
        square_side = SQUARE_CUP_DIM

        square_coords = [
            (lb_x, lb_y),
            (lb_x, lb_y + square_side),
            (lb_x + square_side, lb_y + square_side),
            (lb_x + square_side, lb_y),
            (lb_x, lb_y),  # Close the square
        ]
        return zip(*square_coords)

    def __rectangle_suction_fixture(self, lb_x, lb_y):
        width = RECTANGULAR_CUP_DIM_X
        height = RECTANGULAR_CUP_DIM_Y

        rectangle_coords = [
            (lb_x, lb_y),
            (lb_x, lb_y + height),
            (lb_x + width, lb_y + height),
            (lb_x + width, lb_y),
            (lb_x, lb_y),  # Close the square
        ]
        return zip(*rectangle_coords)

    def __create_fixture(self, fixture_type, center_x, center_y):
        if fixture_type == 1:
            return list(self.__square_suction_fixture(center_x, center_y))
        elif fixture_type == 2:
            return list(self.__rectangle_suction_fixture(center_x, center_y))
        else:
            raise ValueError("Invalid fixture type: must be 1 (square) or 2 (rectangle)")

    def __truncate(self, f, n):
        return math.floor(f * 10 ** n) / 10 ** n

    def __compute_manhattan_distance(self, center_x, center_y, fixture_x, fixture_y):
        point1 = (center_x, center_y)
        point2 = (fixture_x, fixture_y)
        return abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])

    def __compute_center_of_gravity(self, selected_fixtures, fixture_types, fixtures_center_x, fixtures_center_y, w_fix,
                                    h_fix):
        total_area = 0
        weighted_sum_x = 0
        weighted_sum_y = 0

        for i in range(len(selected_fixtures)):
            if selected_fixtures[i] == 1:
                fixture_type = fixture_types[i]
                width = w_fix[fixture_type]
                height = h_fix[fixture_type]
                area = width * height

                total_area += area
                weighted_sum_x += area * fixtures_center_x[i]
                weighted_sum_y += area * fixtures_center_y[i]

        if total_area == 0:
            raise ValueError("Total area is zero, cannot compute center of gravity.")

        x_g = weighted_sum_x / total_area
        y_g = weighted_sum_y / total_area

        return x_g, y_g
