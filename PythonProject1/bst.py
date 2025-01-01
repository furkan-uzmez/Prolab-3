from PIL import Image, ImageDraw, ImageFont
import io


class AvlNode:
    def __init__(self, data):
        self.data = data[0]
        self.priority = data[1]
        self.left = None
        self.right = None
        self.height = 1


class AVLTree:
    def __init__(self):
        self.root = None

    def Height(self, node):
        if not node:
            return 0
        return node.height

    def Balance(self, node):
        if not node:
            return 0
        return self.Height(node.left) - self.Height(node.right)

    def UpdateHeight(self, node):
        if not node:
            return
        node.height = max(self.Height(node.left), self.Height(node.right)) + 1

    def RightRotate(self, y):
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        self.UpdateHeight(y)
        self.UpdateHeight(x)

        return x

    def LeftRotate(self, x):
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        self.UpdateHeight(x)
        self.UpdateHeight(y)

        return y

    def Insert(self, root, data):
        if not root:
            return AvlNode(data)

        if data[1] <= root.priority:
            root.left = self.Insert(root.left, data)
        else:
            root.right = self.Insert(root.right, data)

        self.UpdateHeight(root)

        balance = self.Balance(root)

        # LL
        if balance > 1 and data[1] <= root.left.priority:
            return self.RightRotate(root)

        # RR
        if balance < -1 and data[1] > root.right.priority:
            return self.LeftRotate(root)

        # LR
        if balance > 1 and data[1] > root.left.priority:
            root.left = self.LeftRotate(root.left)
            return self.RightRotate(root)

        # RL
        if balance < -1 and data[1] <= root.right.priority:
            root.right = self.RightRotate(root.right)
            return self.LeftRotate(root)

        return root

    def FindMinNode(self, root):
        if not root or not root.left:
            return root
        return self.FindMinNode(root.left)

    def Remove(self, root, priority):
        if not root:
            return root

        if priority < root.priority:
            root.left = self.Remove(root.left, priority)
        elif priority > root.priority:
            root.right = self.Remove(root.right, priority)
        else:
            if not root.left or not root.right:
                temp = root.left if root.left else root.right
                if not temp:
                    temp = root
                    root = None
                else:
                    root = temp
            else:
                temp = self.FindMinNode(root.right)
                root.data = temp.data
                root.priority = temp.priority
                root.right = self.Remove(root.right, temp.data)

        if not root:
            return root

        self.UpdateHeight(root)

        balance = self.Balance(root)

        # LL
        if balance > 1 and self.Balance(root.left) >= 0:
            return self.RightRotate(root)

        # LR
        if balance > 1 and self.Balance(root.left) < 0:
            root.left = self.LeftRotate(root.left)
            return self.RightRotate(root)

        # RR
        if balance < -1 and self.Balance(root.right) <= 0:
            return self.LeftRotate(root)

        # RL
        if balance < -1 and self.Balance(root.right) > 0:
            root.right = self.RightRotate(root.right)
            return self.LeftRotate(root)

        return root

    def Print(self, root):
        if not root:
            return
        self.Print(root.left)
        print(root.data, end=' ')
        self.Print(root.right)

class BSTVisualizer:
    def __init__(self, width=800, height=800, node_radius=30, vertical_spacing=200, spacing_factor=4):
        self.width = width
        self.height = height
        self.node_radius = node_radius
        self.vertical_spacing = vertical_spacing
        self.spacing_factor = spacing_factor
        self.node_color = (226, 232, 240)  # Light gray
        self.line_color = (148, 163, 184)  # Slate gray
        self.text_color = (30, 41, 59)  # Dark blue/gray

    def _calculate_tree_dimensions(self, root, level=0):
        if root is None:
            return 0, level

        left_width, left_depth = self._calculate_tree_dimensions(root.left, level + 1)
        right_width, right_depth = self._calculate_tree_dimensions(root.right, level + 1)

        return max(left_width, right_width) * 2 + 1, max(left_depth, right_depth)

    def _draw_node(self, draw, x, y, value, priority, font):
        # Draw circle
        draw.ellipse([x - self.node_radius, y - self.node_radius,
                      x + self.node_radius, y + self.node_radius],
                     fill=self.node_color, outline=self.line_color, width=2)

        # Draw text (value and priority)
        text = f"{value}\n({priority})"
        text_bbox = font.getbbox(text)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # Draw each line of text separately for better spacing
        lines = text.split('\n')
        y_offset = -text_height / 4
        for line in lines:
            line_bbox = font.getbbox(line)
            line_width = line_bbox[2] - line_bbox[0]
            draw.text((x - line_width / 2, y + y_offset), line,
                      fill=self.text_color, font=font)
            y_offset += text_height / 2

    def _draw_tree(self, draw, root, x, y, dx, font):
        if root is None:
            return

        # Draw connections first
        if root.left:
            child_x = x - dx
            child_y = y + self.vertical_spacing
            draw.line([x, y, child_x, child_y], fill=self.line_color, width=2)
            self._draw_tree(draw, root.left, child_x, child_y, dx / 2, font)

        if root.right:
            child_x = x + dx
            child_y = y + self.vertical_spacing
            draw.line([x, y, child_x, child_y], fill=self.line_color, width=2)
            self._draw_tree(draw, root.right, child_x, child_y, dx / 2, font)

        # Draw current node
        self._draw_node(draw, x, y, root.data, root.priority, font)

    def visualize_to_png(self, bst):
        # Create image with white background
        img = Image.new('RGB', (self.width, self.height), 'white')
        draw = ImageDraw.Draw(img)

        try:
            font = ImageFont.truetype("arial.ttf", 14)
        except:
            font = ImageFont.load_default()

        # Calculate initial spacing
        total_width, _ = self._calculate_tree_dimensions(bst.root)
        dx = self.width / (total_width + 2) * self.spacing_factor  # Apply spacing factor

        # Draw the tree
        self._draw_tree(draw, bst.root, self.width / 2, 50, dx, font)

        # Convert to PNG
        img_byte_array = io.BytesIO()
        img.save(img_byte_array, format='PNG')
        img_byte_array.seek(0)
        return img_byte_array



def convert_bst_to_json(root):
    """Convert BST to JSON-serializable format"""
    if root is None:
        return None
    return {
        'value': root.data,
        'priority': root.priority,
        'left': convert_bst_to_json(root.left),
        'right': convert_bst_to_json(root.right)
    }