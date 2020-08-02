<?php
// initiate the memcached instance
$m = new Memcached();
$m->setOption(Memcached::OPT_BINARY_PROTOCOL, true);
$m->setSaslAuthData("felamos", "zxcvbnm");
$m->addServer('10.10.10.190', 11211);
print_r( $m->getOption() );
?>
