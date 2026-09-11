import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import sys
import termios
import tty
import threading

class ArrowKeyTwistPublisher(Node):
    def __init__(self):
        super().__init__('arrow_key_twist_publisher')
        self.publisher_ = self.create_publisher(Twist, '/cmd_vel', 10)
        self.linear_x = 0.0
        self.angular_z = 0.0
        self.linear_step = 0.1
        self.angular_step = 5
        self.running = True
        self.get_logger().info('Use arrow keys to control the robot. Press q to quit.')
        thread = threading.Thread(target=self.keyboard_loop)
        thread.daemon = True
        thread.start()
        self.timer = self.create_timer(0.1, self.publish_twist)

    def get_key(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch1 = sys.stdin.read(1)
            if ch1 == '\x1b':
                ch2 = sys.stdin.read(1)
                if ch2 == '[':
                    ch3 = sys.stdin.read(1)
                    return ch1 + ch2 + ch3
            return ch1
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

    def keyboard_loop(self):
        while self.running:
            key = self.get_key()
            if key == '\x1b[A':  # Up arrow
                self.linear_x += self.linear_step
            elif key == '\x1b[B':  # Down arrow
                self.linear_x -= self.linear_step
            elif key == '\x1b[C':  # Right arrow
                self.angular_z -= self.angular_step
            elif key == '\x1b[D':  # Left arrow
                self.angular_z += self.angular_step
            elif key == 'q':
                self.running = False
                rclpy.shutdown()
            self.linear_x = max(-2.0, min(2.0, self.linear_x))
            self.angular_z = max(-15.0, min(15.0, self.angular_z))

    def publish_twist(self):
        if not self.running:
            return
        msg = Twist()
        msg.linear.x = self.linear_x
        msg.angular.z = self.angular_z
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = ArrowKeyTwistPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.running = False
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()