<?php

error_reporting(0);

$output = null;

if (isset($_GET['dir'])) {
  $files = scandir($_GET['dir']);
  $output = ($files === false) ? "Error" : count($files)." files";
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
    <p><?= htmlspecialchars($output) ?></p>
  </body>
</html>
