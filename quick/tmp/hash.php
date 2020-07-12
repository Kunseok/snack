<?php
  $target = 'e626d51f8fbfd1124fdea88396c35d05';
  $fullfilename = "/home/kali/wordlists/rockyou.txt";
  $myfile = fopen($fullfilename, "r") or die("Unable to open file!");

  while (($password = fgets($myfile)) !== false) {
    $temp = trim($password, " \n.");
    $hash = md5(crypt($temp,'fa'));
    if($hash == $target){
      echo $password;
      break;
    }
  }

  fclose($myfile);
?>

