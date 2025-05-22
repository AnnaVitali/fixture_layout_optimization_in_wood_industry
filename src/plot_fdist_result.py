from utility.result_displayer import ResultDisplayer

WIDTH = 698
HEIGHT = 380
AREA = 175769

VERTEX_A = (665, 394)
VERTEX_B = (20, 262)
VERTEX_C = (20, 135)
VERTEX_D = (665, 4)
VERTEX_E = (689, 17)
VERTEX_F = (689, 380)

file_path = '../resources/results_fdist_obj_mzn.json'

vertices = [VERTEX_A, VERTEX_B, VERTEX_C, VERTEX_D, VERTEX_E, VERTEX_F, VERTEX_A]

solution_displayer = ResultDisplayer(
    workpiece_vertices=[(x, y) for x, y in vertices])
solution_displayer.show_results(file_path)
