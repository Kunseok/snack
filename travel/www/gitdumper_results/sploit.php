<?php
class TemplateHelper
{
  private $file;
  private $data;
  private function init(string $file, string $data)
  {    	
    $this->file= $file;
    $this->data= $data;
    /*
    $this->file[0]= $file;
    $this->file[1]= $file;
    $this->data[0]= $data;
    $this->data[1]= $data;
    #file_put_contents(__DIR__.'/logs/'.$this->file, $this->data);
     */
  }
}

$obj = new TemplateHelper('kun','kun');
echo serialize($obj);
echo "\n";
?>
