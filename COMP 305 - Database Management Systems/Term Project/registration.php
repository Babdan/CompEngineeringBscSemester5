<?php
include 'db_connect.php';

$message = '';

// Check if the form is submitted
if ($_SERVER["REQUEST_METHOD"] == "POST" && isset($_POST['shipping_address'])) {
    // Collect and sanitize input data
    $name = mysqli_real_escape_string($link, $_POST['name']);
    $surname = mysqli_real_escape_string($link, $_POST['surname']);  // Surname field
    $email = mysqli_real_escape_string($link, $_POST['email']);
    $shipping_address = mysqli_real_escape_string($link, $_POST['shipping_address']);
    $phone = mysqli_real_escape_string($link, $_POST['phone']);

    // SQL query to insert data into the Customers table
    $query = "INSERT INTO Customers (name, surname, email, shipping_address, phone_number) VALUES ('$name', '$surname', '$email', '$shipping_address', '$phone')";
    
    if (mysqli_query($link, $query)) {
        $customer_id = mysqli_insert_id($link);
        $message = "Registration successful. Your Customer ID is: $customer_id. Please write it down and do not forget it.";
    } else {
        $message = "Error: " . mysqli_error($link);
    }
}
?>


<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Customer Registration</title>
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
        }

        .cart-button {
            padding: 10px 20px;
            background-color: orange;
            color: white;
            text-decoration: none;
            border-radius: 5px;
            margin: 10px;
            display: inline-block;
        }

        .cart-button:hover {
            background-color: darkorange;
        }

        form {
            width: 300px;
            margin: 20px auto;
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
    </style>
</head>
<body>
	<div class="header">
        <h1>Customer Registration</h1>
        <div>
            <a href="index.php" class="cart-button">Back to Shop</a>
            <a href="view_cart.php" class="cart-button">Back to Cart</a>
        </div>
    </div>
    <div style="text-align: left;">
        <?php if ($message): ?>
            <p><?php echo $message; ?></p>
        <?php endif; ?>
        <form method="post">
            <label for="name">Name:</label>
            <input type="text" id="name" name="name" required>

            <label for="surname">Surname:</label>
            <input type="text" id="surname" name="surname" required>

            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required>

            <label for="shipping_address">Shipping Address:</label>
            <input type="text" id="shipping_address" name="shipping_address" required>

            <label for="phone">Phone Number:</label>
            <input type="text" id="phone" name="phone" required>

            <input type="submit" value="Register">
        </form>
    </div>
</body>
</html>
