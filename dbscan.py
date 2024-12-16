class Coordinate:
    def __init__(self, x, y, label):
        self.x = x
        self.y = y
        self.label = label
        self.cluster = None
        self.visited = False
        self.is_core = False
        self.is_border = False
        self.is_noise = False

def dbscan_clustering(entities, epsilon, min_samples):
    cluster = 1
    for entity in entities:
        if not entity.visited:
            if grow_cluster(entity, entities, epsilon, min_samples, cluster):
                cluster += 1

def grow_cluster(start_point, all_points, eps, min_pts, cluster_id):
    neighbor_points = find_neighbors(start_point, all_points, eps)
    if len(neighbor_points) < min_pts:
        start_point.visited = True
        start_point.is_noise = True
        return False
    else:
        start_point.visited = True
        start_point.is_core = True
        start_point.cluster = cluster_id
        seeds = neighbor_points[:]
        while seeds:
            current_point = seeds.pop()
            neighbors = find_neighbors(current_point, all_points, eps)
            if len(neighbors) < min_pts:
                current_point.is_border = True
                current_point.visited = True
                current_point.cluster = cluster_id
            else:
                current_point.is_core = True
                current_point.visited = True
                current_point.cluster = cluster_id
                for neighbor in neighbors:
                    if neighbor.cluster is None:
                        if neighbor not in seeds:
                            seeds.append(neighbor)
        return True

def compute_distance(point1, point2):
    return abs(point1.x - point2.x) + abs(point1.y - point2.y)

def find_neighbors(core_point, points, eps):
    neighbors = []
    for point in points:
        if compute_distance(core_point, point) <= eps:
            neighbors.append(point)
    return neighbors

points = [
    Coordinate(1, 1, "A"), Coordinate(2, 1, "B"), Coordinate(1, 2, "C"), Coordinate(2, 2, "D"),
    Coordinate(3, 5, "E"), Coordinate(3, 9, "F"), Coordinate(3, 10, "G"), Coordinate(4, 10, "H"),
    Coordinate(4, 11, "I"), Coordinate(5, 10, "J"), Coordinate(7, 10, "K"), Coordinate(10, 9, "L"),
    Coordinate(10, 6, "M"), Coordinate(9, 5, "N"), Coordinate(10, 5, "O"), Coordinate(11, 5, "P"),
    Coordinate(9, 4, "Q"), Coordinate(10, 4, "R"), Coordinate(11, 4, "S"), Coordinate(10, 3, "T")
]

dbscan_clustering(points, 1.1, 3)

core_points = [pt.label for pt in points if pt.is_core]
border_points = [pt.label for pt in points if pt.is_border]
noise_points = [pt.label for pt in points if pt.is_noise]

print("Core Points:", core_points)
print("Border Points:", border_points)
print("Noise Points:", noise_points)
