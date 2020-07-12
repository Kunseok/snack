<?xml version="1.0" encoding="iso-8859-1"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:j="http://xml.apache.org/xalan/java" xmlns:bufferedreader="xalan://java.io.BufferedReader" xmlns:inputstreamreader="xalan://java.io.InputStreamReader" xmlns:process="xalan://java.lang.Process" xmlns:runtime="xalan://java.lang.Runtime" xmlns:loop="http://informatik.hu-berlin.de/loop" exclude-result-prefixes="j" version="1.0">

  <xsl:output method="xml" omit-xml-declaration="yes"/>

  <xsl:template match="/">
    <xsl:call-template name="bloop">
    </xsl:call-template>
  </xsl:template>

  <!-- recursive named template -->
  <!-- recursive named template -->
  <xsl:template name="bloop">

    <xsl:variable name="VALUE">
      0
    </xsl:variable>
      trash
    <xsl:if test="$VALUE=0">
      <xsl:call-template name="bloop"/>
    </xsl:if>
  </xsl:template>
  <!-- recursive named template -->
  <!-- recursive named template -->

</xsl:stylesheet>
