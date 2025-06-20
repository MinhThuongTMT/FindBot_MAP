# Updated Supermarket layout - 5 rows x 4 columns = 20 shelves
# 0 = walkway (black), 1 = product shelf, 9 = entrance/exit

# Product categories mapping - 20 shelves arranged in 5 rows x 4 columns
# Each shelf is 5 cells long x 3 cells wide
PRODUCT_CATEGORIES = {
    'sua_nuoc': {
        'name': 'Sua/Nuoc uong',
        'key': '1',
        'shelf_id': 1,
        'positions': [(3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7)],
        'color': (0, 255, 255),  # Cyan
        'description': 'Ke 1: Sua tuoi, sua hop, nuoc uong cac loai'
    },
    'gao_muoi': {
        'name': 'Gao/Muoi/Duong',
        'key': '2',
        'shelf_id': 2,
        'positions': [(3, 11), (3, 12), (3, 13), (3, 14), (3, 15), (4, 11), (4, 12), (4, 13), (4, 14), (4, 15), (5, 11), (5, 12), (5, 13), (5, 14), (5, 15)],
        'color': (255, 255, 0),  # Yellow
        'description': 'Ke 2: Gao, muoi, duong, gia vi'
    },
    'banh_keo': {
        'name': 'Banh keo',
        'key': '3',
        'shelf_id': 3,
        'positions': [(3, 19), (3, 20), (3, 21), (3, 22), (3, 23), (4, 19), (4, 20), (4, 21), (4, 22), (4, 23), (5, 19), (5, 20), (5, 21), (5, 22), (5, 23)],
        'color': (255, 192, 203),  # Pink
        'description': 'Ke 3: Banh keo, snack, do an vat'
    },
    'mi_tom': {
        'name': 'Mi tom',
        'key': '4',
        'shelf_id': 4,
        'positions': [(3, 27), (3, 28), (3, 29), (3, 30), (3, 31), (4, 27), (4, 28), (4, 29), (4, 30), (4, 31), (5, 27), (5, 28), (5, 29), (5, 30), (5, 31)],
        'color': (255, 165, 0),  # Orange
        'description': 'Ke 4: Mi tom, mi goi, do an lien'
    },
    'rau_cu': {
        'name': 'Rau cu/Trai cay',
        'key': '5',
        'shelf_id': 5,
        'positions': [(8, 3), (8, 4), (8, 5), (8, 6), (8, 7), (9, 3), (9, 4), (9, 5), (9, 6), (9, 7), (10, 3), (10, 4), (10, 5), (10, 6), (10, 7)],
        'color': (0, 255, 0),  # Green
        'description': 'Ke 5: Rau cu tuoi, trai cay'
    },
    'thit_ca': {
        'name': 'Thit ca',
        'key': '6',
        'shelf_id': 6,
        'positions': [(8, 11), (8, 12), (8, 13), (8, 14), (8, 15), (9, 11), (9, 12), (9, 13), (9, 14), (9, 15), (10, 11), (10, 12), (10, 13), (10, 14), (10, 15)],
        'color': (255, 0, 0),  # Red
        'description': 'Ke 6: Thit tuoi, ca, hai san'
    },
    'do_uong': {
        'name': 'Do uong co con',
        'key': '7',
        'shelf_id': 7,
        'positions': [(8, 19), (8, 20), (8, 21), (8, 22), (8, 23), (9, 19), (9, 20), (9, 21), (9, 22), (9, 23), (10, 19), (10, 20), (10, 21), (10, 22), (10, 23)],
        'color': (0, 0, 255),  # Blue
        'description': 'Ke 7: Bia, ruou, do uong co con'
    },
    'dong_lanh': {
        'name': 'Thuc pham dong lanh',
        'key': '8',
        'shelf_id': 8,
        'positions': [(8, 27), (8, 28), (8, 29), (8, 30), (8, 31), (9, 27), (9, 28), (9, 29), (9, 30), (9, 31), (10, 27), (10, 28), (10, 29), (10, 30), (10, 31)],
        'color': (173, 216, 230),  # Light Blue
        'description': 'Ke 8: Thuc pham dong lanh'
    },
    'gia_dung': {
        'name': 'Do gia dung',
        'key': '9',
        'shelf_id': 9,
        'positions': [(13, 3), (13, 4), (13, 5), (13, 6), (13, 7), (14, 3), (14, 4), (14, 5), (14, 6), (14, 7), (15, 3), (15, 4), (15, 5), (15, 6), (15, 7)],
        'color': (128, 0, 128),  # Purple
        'description': 'Ke 9: Do gia dung, dung cu nha bep'
    },
    'my_pham': {
        'name': 'My pham',
        'key': '0',
        'shelf_id': 10,
        'positions': [(13, 11), (13, 12), (13, 13), (13, 14), (13, 15), (14, 11), (14, 12), (14, 13), (14, 14), (14, 15), (15, 11), (15, 12), (15, 13), (15, 14), (15, 15)],
        'color': (255, 20, 147),  # Deep Pink
        'description': 'Ke 10: My pham, cham soc da'
    },
    'thuoc_yte': {
        'name': 'Thuoc/Y te',
        'key': 'q',
        'shelf_id': 11,
        'positions': [(13, 19), (13, 20), (13, 21), (13, 22), (13, 23), (14, 19), (14, 20), (14, 21), (14, 22), (14, 23), (15, 19), (15, 20), (15, 21), (15, 22), (15, 23)],
        'color': (255, 255, 255),  # White
        'description': 'Ke 11: Thuoc, dung cu y te'
    },
    'em_be': {
        'name': 'Do em be',
        'key': 'w',
        'shelf_id': 12,
        'positions': [(13, 27), (13, 28), (13, 29), (13, 30), (13, 31), (14, 27), (14, 28), (14, 29), (14, 30), (14, 31), (15, 27), (15, 28), (15, 29), (15, 30), (15, 31)],
        'color': (255, 182, 193),  # Light Pink
        'description': 'Ke 12: Do dung cho em be'
    },
    've_sinh': {
        'name': 'Ve sinh/Tay rua',
        'key': 'e',
        'shelf_id': 13,
        'positions': [(18, 3), (18, 4), (18, 5), (18, 6), (18, 7), (19, 3), (19, 4), (19, 5), (19, 6), (19, 7), (20, 3), (20, 4), (20, 5), (20, 6), (20, 7)],
        'color': (0, 255, 127),  # Spring Green
        'description': 'Ke 13: Chat tay rua, ve sinh'
    },
    'thu_cung': {
        'name': 'Thu cung',
        'key': 'r',
        'shelf_id': 14,
        'positions': [(18, 11), (18, 12), (18, 13), (18, 14), (18, 15), (19, 11), (19, 12), (19, 13), (19, 14), (19, 15), (20, 11), (20, 12), (20, 13), (20, 14), (20, 15)],
        'color': (210, 180, 140),  # Tan
        'description': 'Ke 14: Thuc an, do dung thu cung'
    },
    'dien_tu': {
        'name': 'Dien tu',
        'key': 't',
        'shelf_id': 15,
        'positions': [(18, 19), (18, 20), (18, 21), (18, 22), (18, 23), (19, 19), (19, 20), (19, 21), (19, 22), (19, 23), (20, 19), (20, 20), (20, 21), (20, 22), (20, 23)],
        'color': (64, 64, 64),  # Dark Gray
        'description': 'Ke 15: Dien tu, phu kien'
    },
    'sach_vpham': {
        'name': 'Sach/Van phong pham',
        'key': 'y',
        'shelf_id': 16,
        'positions': [(18, 27), (18, 28), (18, 29), (18, 30), (18, 31), (19, 27), (19, 28), (19, 29), (19, 30), (19, 31), (20, 27), (20, 28), (20, 29), (20, 30), (20, 31)],
        'color': (160, 82, 45),  # Saddle Brown
        'description': 'Ke 16: Sach, van phong pham'
    },
    'do_choi': {
        'name': 'Do choi',
        'key': 'u',
        'shelf_id': 17,
        'positions': [(23, 3), (23, 4), (23, 5), (23, 6), (23, 7), (24, 3), (24, 4), (24, 5), (24, 6), (24, 7), (25, 3), (25, 4), (25, 5), (25, 6), (25, 7)],
        'color': (255, 69, 0),  # Red Orange
        'description': 'Ke 17: Do choi tre em'
    },
    'the_thao': {
        'name': 'The thao',
        'key': 'i',
        'shelf_id': 18,
        'positions': [(23, 11), (23, 12), (23, 13), (23, 14), (23, 15), (24, 11), (24, 12), (24, 13), (24, 14), (24, 15), (25, 11), (25, 12), (25, 13), (25, 14), (25, 15)],
        'color': (34, 139, 34),  # Forest Green
        'description': 'Ke 18: Dung cu the thao'
    },
    'hang_mua': {
        'name': 'Hang theo mua',
        'key': 'o',
        'shelf_id': 19,
        'positions': [(23, 19), (23, 20), (23, 21), (23, 22), (23, 23), (24, 19), (24, 20), (24, 21), (24, 22), (24, 23), (25, 19), (25, 20), (25, 21), (25, 22), (25, 23)],
        'color': (255, 215, 0),  # Gold
        'description': 'Ke 19: Hang theo mua, le hoi'
    },
    'banh_mi': {
        'name': 'Banh mi',
        'key': 'p',
        'shelf_id': 20,
        'positions': [(23, 27), (23, 28), (23, 29), (23, 30), (23, 31), (24, 27), (24, 28), (24, 29), (24, 30), (24, 31), (25, 27), (25, 28), (25, 29), (25, 30), (25, 31)],
        'color': (139, 69, 19),  # Brown
        'description': 'Ke 20: Banh mi, banh ngot'
    }
}

# New supermarket layout - 35 columns x 28 rows
# Layout: 5 rows of shelves, each row has 4 shelves
# Each shelf: 5 cells long x 3 cells wide
# Main walkway in center: 3 cells wide
# Entrance at bottom center
supermarket_layout = [
    # Top border
    [6, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 5],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    
    # First row of shelves (Shelves 1-4)
    [3, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 3],
    [3, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 3],
    [3, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 3],
    
    # Walkway between first and second row
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    
    # Second row of shelves (Shelves 5-8)
    [3, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 3],
    [3, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 3],
    [3, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 3],
    
    # Main central walkway (3 cells wide)
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    
    # Third row of shelves (Shelves 9-12)
    [3, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 3],
    [3, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 3],
    [3, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 3],
    
    # Walkway between third and fourth row
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    
    # Fourth row of shelves (Shelves 13-16)
    [3, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 3],
    [3, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 3],
    [3, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 3],
    
    # Walkway between fourth and fifth row
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],
    
    # Fifth row of shelves (Shelves 17-20)
    [3, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 3],
    [3, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 3],
    [3, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 3],
    
    # Bottom walkway with entrance
    [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3],  # Entrance
    [7, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 9, 9, 9, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 8]   # Bottom border with entrance
]

# Helper function to get category by key
def get_category_by_key(key):
    for category, info in PRODUCT_CATEGORIES.items():
        if info['key'] == key:
            return category
    return None

# Helper function to get shelf center position
def get_shelf_center(shelf_id):
    """Get the center position of a shelf for pathfinding target"""
    for category, info in PRODUCT_CATEGORIES.items():
        if info['shelf_id'] == shelf_id:
            positions = info['positions']
            if positions:
                # Return center of the shelf (middle position)
                center_idx = len(positions) // 2
                return positions[center_idx]
    return None
