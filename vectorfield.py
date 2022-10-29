from manim import *
from math import *
import numpy as np
class BasicUsage(Scene):
    dt = 0.01
    total_time = 12
    def spiral(self,pos):
        x, y = pos[0], pos[1]
        dxdt =  3*y
        dydt = -x-0.5*y
        return np.array([dxdt, dydt, 0])
    ode = spiral

    def construct(self):
        plane = NumberPlane().set_opacity(0.5)
        #self.add(stream_lines)
        self.add(plane)
        self.add(ArrowVectorField(self.ode, opacity = 0.5))
        stream_lines = StreamLines(self.ode, stroke_width=2, max_anchors_per_line=10)
        def MoveAlongPaths(a, b):
            return [MoveAlongPath(a[i], b[i]) for i in range(len(a))]
        def draw_traj(xs, ys):
            points = VGroup()
            trajectory = VGroup()
            traj = VGroup()
            for i in range(len(xs)):
                points.add(Dot(point = [xs[i], ys[i], 0], radius=DEFAULT_DOT_RADIUS/2, color = BLUE))
                trajectory.add(VMobject())
                trajectory[i].start_new_path(points[i].get_center())
                traj.add(VMobject())
            
            
            nums = range(len(xs)) #[0,1]
            
            def addUpdater(m, point):
                def func(t):
                    
                    if(np.linalg.norm(t.points[-1]-point.get_center()) >= 0.01):
                        return t.add_smooth_curve_to(point.get_center())
                    return t
                m.add_updater(func)
            for j in nums:
                print(j)
                traj[j].append_points([points[j].get_center()])
                point = points[j]
                print(point)
                addUpdater(traj[j], point)
            
            a = range(len(trajectory))
            for _ in range(round(self.total_time/self.dt)):
                for i in a :
                    p = trajectory[i].points[-1]
                    dp_dt = self.ode(p)
                    x = p[0] + dp_dt[0] * self.dt
                    y = p[1] + dp_dt[1]*self.dt
                    trajectory[i].add_smooth_curve_to(np.array([x, y, 0]))

            self.add(points, traj)
            self.play(
                *MoveAlongPaths(points, trajectory),
                run_time= self.total_time,
                rate_func=bezier([0, 0, 1, 1]),
            )
        
        draw_traj([2,3,-4], [1,-2.5,-1],)


        


