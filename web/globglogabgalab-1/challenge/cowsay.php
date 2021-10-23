<?php

error_reporting(0);

$output = null;

if (isset($_GET['message']) && is_string($_GET['message'])) {
  $cowacter = (isset($_GET['cowacter']) && is_string($_GET['cowacter'])) ? $_GET['cowacter'] : "default";
  $message = $_GET['message'];

  $output = shell_exec("/usr/games/cowsay -f ${cowacter} ${message}");
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
