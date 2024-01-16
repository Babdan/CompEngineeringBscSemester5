<?php
ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

session_start();

if (isset($_POST['update']) && isset($_POST['product_id']) && isset($_POST['quantity'])) {
    $product_id = (int)$_POST['product_id'];
    $quantity = (int)$_POST['quantity'];
    $_SESSION['cart'][$product_id] = $quantity;
}

if (isset($_POST['remove']) && isset($_POST['product_id'])) {
    $product_id = (int)$_POST['product_id'];
    unset($_SESSION['cart'][$product_id]);
}

header('Location: view_cart.php');
exit();
?>
