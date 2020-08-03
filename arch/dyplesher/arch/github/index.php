<HTML>
<BODY>
<h1>Add key and value to memcache<h1>
<FORM METHOD="GET" NAME="test" ACTION="">
<INPUT TYPE="text" NAME="add">
<INPUT TYPE="text" NAME="val">
<INPUT TYPE="submit" VALUE="Send">
</FORM>

<pre>
<?php
if($_GET['add'] != $_GET['val']){
	$m = new Memcached();
	$m->setOption(Memcached::OPT_BINARY_PROTOCOL, true);
	$m->setSaslAuthData("felamos", "zxcvbnm");
	$m->addServer('127.0.0.1', 11211);
	$m->add($_GET['add'], $_GET['val']);
	echo "Done!";
}
else {
	echo "its equal";
}
?>
</pre>

</BODY>
</HTML>
