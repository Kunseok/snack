<?php

/**
 Todo: finish logging implementation via TemplateHelper
*/

function safe($url)
{
	return $url;
}

function url_get_contents ($url) {
  $url = safe($url);
	$url = escapeshellarg($url);
	$pl = "curl ".$url;
  $output = shell_exec($pl);
  return $output;
}


class TemplateHelper
{

    private $file;
    private $data;

    public function __construct(string $file, string $data)
    {
    	$this->init($file, $data);
    }

    public function __wakeup()
    {
    	$this->init($this->file, $this->data);
    }

    private function init(string $file, string $data)
    {    	
        $this->file = $file;
        $this->data = $data;
        file_put_contents(__DIR__.'/logs/'.$this->file, $this->data);
    }
}
