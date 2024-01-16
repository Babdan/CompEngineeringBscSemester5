<?php
include 'db_connect.php';

$message = '';
$orderDetails = '';

// Check if the form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['order_id'])) {
    $orderId = mysqli_real_escape_string($link, $_POST['order_id']);

    // SQL query to fetch the order status and order date
    $orderQuery = "SELECT status, order_date FROM Orders WHERE order_id = $orderId";
    $orderResult = mysqli_query($link, $orderQuery);

    if ($orderRow = mysqli_fetch_assoc($orderResult)) {
        // Include the order date in the output
        $orderDetails = "<strong>Order Status For Order ID " . $orderId . ": " . $orderRow['status'] . "</strong>";
        $orderDetails .= "<br>Order Date: " . $orderRow['order_date'];

        // Fetch order items
        $itemsQuery = "SELECT p.model, oi.quantity FROM OrderItems oi JOIN Products p ON oi.product_id = p.product_id WHERE oi.order_id = $orderId";
        $itemsResult = mysqli_query($link, $itemsQuery);

        $orderDetails .= "<ol>";
        while ($itemRow = mysqli_fetch_assoc($itemsResult)) {
            $orderDetails .= "<li>" . htmlspecialchars($itemRow['model']) . " - Quantity: " . $itemRow['quantity'] . "</li>";
        }
        $orderDetails .= "</ol>";
    } else {
        $message = "Order ID not found. Please check your Order ID and try again.";
    }
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Check Order Status</title>
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
        .form-container {
            width: 300px;
            margin: 20px auto;
            padding: 20px;
            background-color: #fff;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        label, input {
            display: block;
            width: 100%;
            margin-bottom: 10px;
        }

        input[type="submit"] {
            background-color: #28a745;
            color: white;
            border: none;
            padding: 10px;
            border-radius: 5px;
            cursor: pointer;
        }

        input[type="submit"]:hover {
            background-color: #218838;
        }

        .message, .status {
            text-align: center;
            margin-top: 20px;
        }
		.message, .status {
            background-color: #f2f2f2; /* Light gray background */
            border: 1px solid #ddd; /* Light border */
            padding: 10px;
            margin: 20px auto;
            width: 500px;
            text-align: center;
            border-radius: 5px;
        }
		.status ol li {
		border-top: 1px solid #ddd;
        border-bottom: 1px solid #ddd; /* Add a bottom border to each list item */
        padding-bottom: 5px; /* Add some padding at the bottom */
        margin-bottom: 5px; /* Add some space below each item */
		}
    </style>
</head>
<body>
    <div class="header">
        <h1>Check Order Status</h1>
        <div>
            <a href="index.php" class="cart-button">Back to Shop</a>
        </div>
    </div>

    <div class="form-container">
        <form method="post">
            <label for="order_id">Enter Your Order ID:</label>
            <input type="number" id="order_id" name="order_id" required>
            <input type="submit" value="Check Status">
        </form>
    </div>

    <?php if ($message): ?>
        <div class="message"><?php echo $message; ?></div>
    <?php endif; ?>

    <?php if ($orderDetails): ?>
        <div class="status"><?php echo $orderDetails; ?></div>
    <?php endif; ?>
</body>
</html>
