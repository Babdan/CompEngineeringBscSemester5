<?php
session_start();

include 'db_connect.php';  // Include your database connection

// Function to fetch categories from the database
function fetchCategories($link) {
    $query = "SELECT * FROM Category";
    $result = mysqli_query($link, $query);

    $categories = [];
    while ($row = mysqli_fetch_assoc($result)) {
        $categories[] = $row;
    }
    return $categories;
}

// Function to fetch products from the database by category, including all product type attributes and sorting
function fetchProductsByCategory($link, $categoryId, $sortBy) {
    $orderBy = "model"; // Default order (adjusted to any default column)
    switch ($sortBy) {
        case 'price_asc':
            $orderBy = "price ASC";
            break;
        case 'price_desc':
            $orderBy = "price DESC";
            break;
        case 'name':
            $orderBy = "model";
            break;
    }

    $query = "SELECT p.*, g.core_count AS gpu_core_count, g.base_clock AS gpu_base_clock, g.boost_clock AS gpu_boost_clock, g.vram_size, 
                     c.core_count AS cpu_core_count, c.thread_count, c.base_clock AS cpu_base_clock, c.boost_clock AS cpu_boost_clock,
                     m.ram_slots, m.pcie_slots, 
                     r.capacity AS ram_capacity, r.speed AS ram_speed,
                     s.capacity AS storage_capacity 
              FROM Products p 
              LEFT JOIN GPU g ON p.product_id = g.product_id 
              LEFT JOIN CPU c ON p.product_id = c.product_id
              LEFT JOIN Motherboard m ON p.product_id = m.product_id
              LEFT JOIN RAM r ON p.product_id = r.product_id
              LEFT JOIN Storage s ON p.product_id = s.product_id
              WHERE p.category_id = " . intval($categoryId) . 
              " ORDER BY " . $orderBy;
    $result = mysqli_query($link, $query);
    
    $products = [];
    while ($row = mysqli_fetch_assoc($result)) {
        $products[] = $row;
    }
    return $products;
}

$categories = fetchCategories($link);  // Fetch categories

if (empty($categories)) {
    echo "No categories found.";
    exit;
}

// Handling the selected category and sort option
$selectedCategory = isset($_GET['category']) ? $_GET['category'] : $categories[0]['category_id'];
$sortBy = isset($_GET['sort']) ? $_GET['sort'] : 'name'; // Default to sorting by name if not specified

// Fetch products for the selected category with sorting
$products = fetchProductsByCategory($link, $selectedCategory, $sortBy);
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple Shopping Platform</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
            color: #333;
        }

		/* Full-width header with flex layout */
        .header {
            background-color: #007bff;
            color: #fff;
            padding: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 100%; /* Ensure header spans full width */
        }
		
        /* Style for the cart button - now orange */
        .cart-button {
            padding: 10px 20px;
            background-color: orange; /* Orange color */
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: background-color 0.3s;
            margin-left: auto; /* Push button to the right */
			margin-right: 30px;
        }

        .cart-button:hover {
            background-color: darkorange; /* Darker orange on hover */
        }

        .categories {
            background-color: #eee;
            padding: 10px;
            text-align: center;
        }

        .category-tab {
            margin: 0 10px;
            padding: 5px 10px;
            display: inline-block;
            background-color: #007bff;
            color: #fff;
            text-decoration: none;
            border-radius: 5px;
            transition: background-color 0.3s;
        }

        .category-tab:hover {
            background-color: #0056b3;
        }

		        /* Styling for the sorting options form */
        .sort-options {
            text-align: left;
            margin: 20px 10;
			padding-left: 20px;
        }

        .sort-options select {
            padding: 5px 10px;
            margin-right: 10px;
            border-radius: 5px;
            border: 1px solid #ddd;
            background-color: #f8f8f8;
            cursor: pointer;
        }

        .sort-options select:hover {
            background-color: #eaeaea;
        }

        .products {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            padding: 20px;
        }

        .product {
            background-color: #fff;
            border: 1px solid #ddd;
            margin: 10px;
            padding: 15px;
            width: 200px;
            text-align: center;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        .product h3 {
            margin: 0 0 10px 0;
        }

        form {
            margin-top: 10px;
        }

        input[type="number"] {
            width: 60px;
            padding: 5px;
        }

        input[type="submit"] {
            background-color: #28a745;
            color: #fff;
            border: none;
            padding: 5px 10px;
            border-radius: 5px;
            cursor: pointer;
        }

        input[type="submit"]:hover {
            background-color: #218838;
        }

        .out-of-stock {
            color: red;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Welcome to Our Simple Shopping Platform</h1>
        <div>
            <a href="order_status.php" class="cart-button">Order Tracking</a>
            <a href="view_cart.php" class="cart-button">View Cart</a>
        </div>
    </div>
    <div class="categories">
        <?php foreach ($categories as $category): ?>
            <a class="category-tab" href="?category=<?php echo $category['category_id']; ?>">
                <?php echo htmlspecialchars($category['name']); ?>
            </a>
        <?php endforeach; ?>
    </div>
	    <!-- Sorting options -->
    <div class="sort-options">
    <form action="" method="get">
        <select name="sort" onchange="this.form.submit()">
            <option value="name" <?php echo $sortBy == 'name' ? 'selected' : ''; ?>>Sort by Name</option>
            <option value="price_asc" <?php echo $sortBy == 'price_asc' ? 'selected' : ''; ?>>Price Low to High</option>
            <option value="price_desc" <?php echo $sortBy == 'price_desc' ? 'selected' : ''; ?>>Price High to Low</option>
        </select>
        <input type="hidden" name="category" value="<?php echo $selectedCategory; ?>">
    </form>
	</div>

    <h2 style="text-align:center;">Products in <?php echo htmlspecialchars($categories[array_search($selectedCategory, array_column($categories, 'category_id'))]['name']); ?></h2>
    <div class="products">
        <?php foreach ($products as $product): ?>
            <div class="product">
                <h3><?php echo htmlspecialchars($product['model']); ?></h3>
                <p>Price: $<?php echo htmlspecialchars($product['price']); ?></p>
                <p>Available in Stock: <?php echo htmlspecialchars($product['stock_quantity']); ?></p>

                <!-- Display GPU-specific attributes if available -->
                <?php if (isset($product['gpu_core_count'])): ?>
                    <p>Core Count: <?php echo htmlspecialchars($product['gpu_core_count']); ?></p>
                    <p>Base Clock: <?php echo htmlspecialchars($product['gpu_base_clock']); ?> GHz</p>
                    <p>Boost Clock: <?php echo htmlspecialchars($product['gpu_boost_clock']); ?> GHz</p>
                    <p>VRAM: <?php echo htmlspecialchars($product['vram_size']); ?> GB</p>
                <?php endif; ?>

                <!-- Display CPU-specific attributes if available -->
                <?php if (isset($product['cpu_core_count'])): ?>
                    <p>Core Count: <?php echo htmlspecialchars($product['cpu_core_count']); ?></p>
                    <p>Thread Count: <?php echo htmlspecialchars($product['thread_count']); ?></p>
                    <p>Base Clock: <?php echo htmlspecialchars($product['cpu_base_clock']); ?> GHz</p>
                    <p>Boost Clock: <?php echo htmlspecialchars($product['cpu_boost_clock']); ?> GHz</p>
                <?php endif; ?>

                <!-- Display Motherboard-specific attributes if available -->
                <?php if (isset($product['ram_slots'])): ?>
                    <p>RAM Slots: <?php echo htmlspecialchars($product['ram_slots']); ?></p>
                    <p>PCIe Slots: <?php echo htmlspecialchars($product['pcie_slots']); ?></p>
                <?php endif; ?>

                <!-- Display RAM-specific attributes if available -->
                <?php if (isset($product['ram_capacity'])): ?>
                    <p>Capacity: <?php echo htmlspecialchars($product['ram_capacity']); ?> GB</p>
                    <p>Speed: <?php echo htmlspecialchars($product['ram_speed']); ?> MHz</p>
                <?php endif; ?>

                <!-- Display Storage-specific attributes if available -->
                <?php if (isset($product['storage_capacity'])): ?>
                    <p>Capacity: <?php echo htmlspecialchars($product['storage_capacity']); ?> GB</p>
                <?php endif; ?>

                <?php if ($product['stock_quantity'] > 0): ?>
                    <form action="cart.php" method="post">
                        <input type="hidden" name="product_id" value="<?php echo $product['product_id']; ?>">
                        <input type="number" name="quantity" value="1" min="1" max="<?php echo $product['stock_quantity']; ?>">
                        <input type="submit" value="Add to Cart">
                    </form>
                <?php else: ?>
                    <p class="out-of-stock">Out of Stock</p>
                <?php endif; ?>
            </div>
        <?php endforeach; ?>
    </div>
</body>
</html>
