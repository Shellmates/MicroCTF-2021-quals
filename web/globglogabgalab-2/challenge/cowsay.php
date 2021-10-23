<?php

error_reporting(0);

$output = null;

if (isset($_GET['message']) && is_string($_GET['message'])) {
  $regex = "/^[0-9a-zA-Z\/_\.]+$/";
  $cowacter = (isset($_GET['cowacter']) && is_string($_GET['cowacter'])) ? $_GET['cowacter'] : "default";
  $message = $_GET['message'];

  if (!preg_match($regex, $cowacter)
      || !preg_match($regex, $message)) {
    $output = "No";
  } else {
    $output = shell_exec("/usr/games/cowsay -f ${cowacter} ${message}");
  }

} else {
  highlight_file(__FILE__);
  exit;
}

?>

<!DOCTYPE html>
<html>
  <head>
    <title>Globglogabgalab</title>
  </head>
  <body>
    <pre><?= htmlspecialchars($output) ?></pre>
  </body>
</html>
