<?php
session_start();
include 'db_connect.php';

$message = '';

// Function to process the checkout
function processCheckout($link, $customerId) {
    if (!isset($_SESSION['cart']) || empty($_SESSION['cart'])) {
        return "Your cart is empty.";
    }

    // Check if the customer ID exists in the database
    $customerCheckQuery = "SELECT * FROM Customers WHERE customer_id = $customerId";
    $customerCheckResult = mysqli_query($link, $customerCheckQuery);
    if (mysqli_num_rows($customerCheckResult) == 0) {
        return "Invalid Customer ID. Please check your Customer ID and try again.";
    }

    // Check stock availability for each product
    foreach ($_SESSION['cart'] as $productId => $quantity) {
        $stockQuery = "SELECT stock_quantity FROM Products WHERE product_id = $productId";
        $stockResult = mysqli_query($link, $stockQuery);
        if ($stockRow = mysqli_fetch_assoc($stockResult)) {
            if ($quantity > $stockRow['stock_quantity']) {
                return "Not enough stock for product ID $productId. Only " . $stockRow['stock_quantity'] . " left.";
            }
        } else {
            return "Product ID $productId not found.";
        }
    }

    // Create a new order
    $query = "INSERT INTO Orders (customer_id, order_date, status) VALUES ($customerId, NOW(), 'Processing')";
    mysqli_query($link, $query);
    $orderId = mysqli_insert_id($link);

    // Add items to order_items table and decrement stock quantity
    foreach ($_SESSION['cart'] as $productId => $quantity) {
        $query = "INSERT INTO OrderItems (order_id, product_id, quantity) VALUES ($orderId, $productId, $quantity)";
        mysqli_query($link, $query);

        // Decrement the stock quantity in the Products table
        $updateStockQuery = "UPDATE Products SET stock_quantity = stock_quantity - $quantity WHERE product_id = $productId";
        mysqli_query($link, $updateStockQuery);
    }

    // Clear the cart
    $_SESSION['cart'] = [];

    return "Thank you for your order. Your order number is " . $orderId . ".";
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $customerId = isset($_POST['customer_id']) ? $_POST['customer_id'] : 0;
    $message = processCheckout($link, $customerId);
}

// Display the message
if ($message) {
    echo $message;
}
?>



<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Checkout</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f4f4f4;
            color: #333;
        }

        .header {
            background-color: #007bff;
            color: #fff;
            padding: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            width: 100%;
        }

        .cart-button, .checkout-button {
            padding: 10px 20px;
            background-color: orange;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            transition: background-color 0.3s;
            margin-left: auto;
            margin-right: 20px;
        }

        .cart-button:hover, .checkout-button:hover {
            background-color: darkorange;
        }

		.message {
        background-color: #f2f2f2; /* Light gray background */
        border: 1px solid #ddd; /* Light border */
        padding: 10px;
        margin: 20px auto;
        width: 80%;
        text-align: center;
        border-radius: 5px;
		}

        form {
            width: 80%;
            margin: 20px auto;
        }

        input[type="submit"] {
            background-color: #28a745;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
        }

        input[type="submit"]:hover {
            background-color: #218838;
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Checkout</h1>
        <div>
            <a href="index.php" class="cart-button">Back to Shop</a>
            <a href="view_cart.php" class="cart-button">Back to Cart</a>
        </div>
    </div>

	<?php if ($message): ?>
		<div class="message">
			<?php echo $message; ?>
		</div>
	<?php endif; ?>

    <form method="post" style="text-align: center;">
        <label for="customer_id">Enter Your Customer ID:</label>
        <input type="number" id="customer_id" name="customer_id" required>
        <input type="submit" value="Place Order" class="checkout-button">
    </form>

    <p style="text-align: center;">Are you a new customer? <a href="registration.php">Then register here</a></p>
    
    <p style="text-align: center;">Forgot your customer ID? Call us at: [1-800-FORGOTID]</p>
</body>
</html>
