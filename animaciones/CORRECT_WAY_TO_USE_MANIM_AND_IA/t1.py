from manim import *


class SplineLineIntersector:
    """
    Detects intersections between a straight line and a spline using
    the Sederberg-Nishita fat line clipping algorithm.
    """
    
    def __init__(self, tolerance=1e-6, max_iterations=100):
        self.tolerance = tolerance
        self.max_iterations = max_iterations
    
    def find_intersections(self, spline, line):
        """
        Find all intersection points between a spline (VMobject) and a line.
        
        Args:
            spline: A Manim VMobject (e.g., Circle, Arc, ParametricFunction)
            line: A Manim Line object
        
        Returns:
            List of intersection points as numpy arrays
        """
        intersections = []
        
        # Get line endpoints
        line_start = line.get_start()
        line_end = line.get_end()
        
        # Get all cubic Bézier segments from the spline
        bezier_segments = self._extract_bezier_segments(spline)
        
        # Find intersections with each segment
        for segment in bezier_segments:
            segment_intersections = self._intersect_line_bezier(
                segment, line_start, line_end
            )
            intersections.extend(segment_intersections)
        
        # Remove duplicate points
        intersections = self._remove_duplicates(intersections)
        
        return intersections
    
    def _extract_bezier_segments(self, vmobject):
        """Extract cubic Bézier curve segments from a VMobject."""
        segments = []
        points = vmobject.get_all_points()
        
        # Manim stores cubic Bézier curves as sequences of 4 points
        # [anchor1, handle1, handle2, anchor2, ...]
        for i in range(0, len(points), 4):
            if i + 3 < len(points):
                segment = points[i:i+4]
                segments.append(segment)
        
        return segments
    
    def _intersect_line_bezier(self, bezier, line_start, line_end):
        """
        Find intersections between a line segment and a cubic Bézier curve
        using the Sederberg-Nishita algorithm.
        """
        return self._clip_recursive(bezier, line_start, line_end, 0)
    
    def _clip_recursive(self, bezier, line_start, line_end, depth):
        """Recursive fat line clipping."""
        if depth > self.max_iterations:
            return []
        
        # Check if bezier is small enough to be considered a point
        bbox_size = self._bbox_size(bezier)
        if bbox_size < self.tolerance:
            # Return the midpoint of the curve
            t = 0.5
            point = self._evaluate_bezier(bezier, t)
            return [point]
        
        # Compute distance from bezier control points to the line
        distances = self._compute_distances_to_line(bezier, line_start, line_end)
        
        # Compute the fat line (convex hull in distance space)
        d_min, d_max = self._compute_fat_line(distances)
        
        # Clip the parameter range [0, 1] using the fat line
        t_min, t_max = self._clip_parameter_range(bezier, line_start, line_end, 
                                                    d_min, d_max)
        
        if t_min is None or t_max is None:
            # No intersection
            return []
        
        if t_max - t_min < self.tolerance:
            # Parameter range is small enough
            t = (t_min + t_max) / 2
            point = self._evaluate_bezier(bezier, t)
            
            # Verify the point is actually on the line segment
            if self._point_on_line_segment(point, line_start, line_end):
                return [point]
            return []
        
        # Subdivide the curve and recurse
        mid_t = (t_min + t_max) / 2
        left_bezier = self._subdivide_bezier(bezier, t_min, mid_t)
        right_bezier = self._subdivide_bezier(bezier, mid_t, t_max)
        
        left_intersections = self._clip_recursive(left_bezier, line_start, 
                                                   line_end, depth + 1)
        right_intersections = self._clip_recursive(right_bezier, line_start, 
                                                    line_end, depth + 1)
        
        return left_intersections + right_intersections
    
    def _bbox_size(self, bezier):
        """Compute the size of the bounding box of the bezier curve."""
        min_coords = np.min(bezier, axis=0)
        max_coords = np.max(bezier, axis=0)
        return np.linalg.norm(max_coords - min_coords)
    
    def _compute_distances_to_line(self, bezier, line_start, line_end):
        """Compute signed distances from bezier points to the line."""
        # Line direction vector
        line_vec = line_end - line_start
        line_len = np.linalg.norm(line_vec[:2])  # Use only x, y
        
        if line_len < 1e-10:
            return np.zeros(len(bezier))
        
        # Normal to the line (perpendicular)
        normal = np.array([-line_vec[1], line_vec[0], 0])
        normal = normal / np.linalg.norm(normal[:2])
        
        # Compute signed distances
        distances = []
        for point in bezier:
            vec = point - line_start
            dist = np.dot(vec, normal)
            distances.append(dist)
        
        return np.array(distances)
    
    def _compute_fat_line(self, distances):
        """Compute the fat line bounds (convex hull of distance function)."""
        d_min = np.min(distances)
        d_max = np.max(distances)
        
        # For cubic Bézier, we use a simple convex hull
        # The fat line is defined by the min and max distances
        return d_min, d_max
    
    def _clip_parameter_range(self, bezier, line_start, line_end, d_min, d_max):
        """
        Clip the parameter range based on the fat line.
        Returns the clipped t_min and t_max, or (None, None) if no intersection.
        """
        # Check if the curve's distance range overlaps with zero
        # (i.e., the line passes through the fat line)
        if d_min > self.tolerance or d_max < -self.tolerance:
            return None, None
        
        # For simplicity, return full range if there's potential intersection
        # A more sophisticated implementation would compute exact clipping bounds
        return 0.0, 1.0
    
    def _evaluate_bezier(self, bezier, t):
        """Evaluate a cubic Bézier curve at parameter t using De Casteljau."""
        p0, p1, p2, p3 = bezier
        
        u = 1 - t
        tt = t * t
        uu = u * u
        uuu = uu * u
        ttt = tt * t
        
        point = uuu * p0
        point += 3 * uu * t * p1
        point += 3 * u * tt * p2
        point += ttt * p3
        
        return point
    
    def _subdivide_bezier(self, bezier, t_start, t_end):
        """Extract a portion of a Bézier curve between t_start and t_end."""
        # First, extract curve from 0 to t_end
        if t_end < 1.0:
            bezier = self._split_bezier_at_t(bezier, t_end)[0]
        
        # Then extract from t_start to t_end
        if t_start > 0.0:
            adjusted_t = t_start / t_end if t_end > 0 else 0
            bezier = self._split_bezier_at_t(bezier, adjusted_t)[1]
        
        return bezier
    
    def _split_bezier_at_t(self, bezier, t):
        """Split a Bézier curve at parameter t using De Casteljau algorithm."""
        p0, p1, p2, p3 = bezier
        
        # De Casteljau's algorithm for subdivision
        p01 = (1 - t) * p0 + t * p1
        p12 = (1 - t) * p1 + t * p2
        p23 = (1 - t) * p2 + t * p3
        
        p012 = (1 - t) * p01 + t * p12
        p123 = (1 - t) * p12 + t * p23
        
        p0123 = (1 - t) * p012 + t * p123
        
        left = np.array([p0, p01, p012, p0123])
        right = np.array([p0123, p123, p23, p3])
        
        return left, right
    
    def _point_on_line_segment(self, point, line_start, line_end):
        """Check if a point lies on the line segment."""
        vec = line_end - line_start
        line_len_sq = np.dot(vec[:2], vec[:2])
        
        if line_len_sq < 1e-10:
            return np.linalg.norm(point[:2] - line_start[:2]) < self.tolerance
        
        # Project point onto line
        t = np.dot(point[:2] - line_start[:2], vec[:2]) / line_len_sq
        
        # Check if projection is within segment bounds
        if t < -self.tolerance or t > 1 + self.tolerance:
            return False
        
        # Check distance to line
        projection = line_start + t * vec
        dist = np.linalg.norm(point[:2] - projection[:2])
        
        return dist < self.tolerance
    
    def _remove_duplicates(self, points):
        """Remove duplicate points from the list."""
        if not points:
            return []
        
        unique = [points[0]]
        for point in points[1:]:
            is_duplicate = False
            for existing in unique:
                if np.linalg.norm(point[:2] - existing[:2]) < self.tolerance:
                    is_duplicate = True
                    break
            if not is_duplicate:
                unique.append(point)
        
        return unique


# Example usage in a Manim scene
class IntersectionDemo(Scene):
    def construct(self):
        # Create a circle
        circle = Star(color=BLUE).scale(2.5)
        
        # Create a line that intersects the circle
        line = Line(start=LEFT * 3, end=RIGHT * 3, color=YELLOW)
        
        # Find intersections
        intersector = SplineLineIntersector(tolerance=1e-4)
        intersection_points = intersector.find_intersections(circle, line)
        
        # Create dots at intersection points
        dots = VGroup(*[
            Dot(point, color=RED, radius=0.1)
            for point in intersection_points
        ])
        
        # Display
        self.play(Create(circle), Create(line))
        self.play(FadeIn(dots))
        self.wait(2)
        
        # Try another line
        line2 = Line(start=UP * 3, end=DOWN * 3 + RIGHT * 2, color=GREEN)
        intersection_points2 = intersector.find_intersections(circle, line2)
        dots2 = VGroup(*[
            Dot(point, color=PURPLE, radius=0.1)
            for point in intersection_points2
        ])
        
        self.play(Create(line2))
        self.play(FadeIn(dots2))
        self.wait(2)
