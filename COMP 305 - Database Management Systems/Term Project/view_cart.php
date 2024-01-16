<?php
session_start();

include 'db_connect.php';

if (!isset($_SESSION['cart'])) {
    $_SESSION['cart'] = [];
}

echo "<!DOCTYPE html>";
echo "<html lang='en'>";
echo "<head>";
echo "    <meta charset='UTF-8'>";
echo "    <meta name='viewport' content='width=device-width, initial-scale=1.0'>";
echo "    <title>Simple Shopping Platform - Cart</title>";
echo "    <style>";
echo "        body {";
echo "            font-family: Arial, sans-serif;";
echo "            margin: 0;";
echo "            padding: 0;";
echo "            background-color: #f4f4f4;";
echo "            color: #333;";
echo "        }";
echo "        .header {";
echo "            background-color: #007bff;";
echo "            color: #fff;";
echo "            padding: 10px;";
echo "            display: flex;";
echo "            justify-content: space-between;";
echo "            align-items: center;";
echo "            width: 100%;";
echo "        }";
echo "        .cart-button {";
echo "            padding: 10px 20px;";
echo "            background-color: orange;";
echo "            color: white;";
echo "            text-decoration: none;";
echo "            border-radius: 5px;";
echo "            transition: background-color 0.3s;";
echo "            margin-left: auto;";
echo "            margin-right: 30px;";
echo "        }";
echo "        .cart-button:hover {";
echo "            background-color: darkorange;";
echo "        }";
echo "    		.message {";
echo "        background-color: #f2f2f2; /* Light gray background */";
echo "        border: 1px solid #ddd; /* Light border */";
echo "        padding: 10px;";
echo "        margin: 20px auto;";
echo "        width: 80%;";
echo "        text-align: center;";
echo "        border-radius: 5px;";
echo "    	}";
echo "        .cart-items {";
echo "            width: 80%;";
echo "            margin: 20px auto;";
echo "            list-style: decimal inside;"; // Numbered list style
echo "        }";
echo "        .cart-item {";
echo "            background-color: #fff;";
echo "            margin: 10px 0;";
echo "            padding: 15px;";
echo "            border-radius: 5px;";
echo "            box-shadow: 0 2px 5px rgba(0,0,0,0.1);";
echo "        }";
echo "        .checkout-button {";
echo "            display: block;";
echo "            width: fit-content;";
echo "            margin: 20px auto;";
echo "            padding: 10px 20px;";
echo "            background-color: #28a745;"; // Green background
echo "            color: white;";
echo "            text-decoration: none;";
echo "            border-radius: 5px;";
echo "            text-align: center;";
echo "            transition: background-color 0.3s;";
echo "        }";
echo "        .checkout-button:hover {";
echo "            background-color: #218838;"; // Darker green on hover
echo "        }";
echo "    </style>";
echo "</head>";
echo "<body>";
echo "    <div class='header'>";
echo "        <h1>Your Shopping Cart</h1>";
echo "        <a href='index.php' class='cart-button'>Back to Shop</a>";
echo "    </div>";

if (empty($_SESSION['cart'])) {
    echo "<div class='message'>";
    echo "    <p>Your cart is empty.</p>";
    echo "</div>";
} else {
    echo "<ol class='cart-items'>"; // Ordered list for cart items
    $itemNumber = 1;
    foreach ($_SESSION['cart'] as $product_id => $quantity) {
        // Fetch product details from database
        $query = "SELECT * FROM Products WHERE product_id = $product_id";
        $result = mysqli_query($link, $query);
        $product = mysqli_fetch_assoc($result);

        echo "<li class='cart-item'>";
        echo "<p><strong>Item $itemNumber:</strong> " . htmlspecialchars($product['model']) . " - Quantity: $quantity</p>";
        echo "<form action='update_cart.php' method='post'>";
        echo "<input type='hidden' name='product_id' value='$product_id'>";
        echo "<input type='number' name='quantity' value='$quantity' min='1'>";
        echo "<input type='submit' name='update' value='Update'>";
        echo "<input type='submit' name='remove' value='Remove'>";
        echo "</form>";
        echo "</li>";
        $itemNumber++;
    }
    echo "</ol>"; // Close the ordered list
    echo "<a href='checkout.php' class='checkout-button'>Proceed to Checkout</a>"; // Styled checkout button
}

echo "</body>";
echo "</html>";
?>