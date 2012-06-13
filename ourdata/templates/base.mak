<!DOCTYPE HTML>
<html>

<head>
  <title><%block name="title" /></title>
  <meta name="description" content="website description" />
  <meta name="keywords" content="website keywords, website keywords" />
  <meta http-equiv="content-type" content="text/html; charset=UTF-8" />
  <link rel="stylesheet" type="text/css" href="/static/css/style.css" />
  <!-- modernizr enables HTML5 elements and feature detects -->
  <script type="text/javascript" src="js/modernizr-1.5.min.js"></script>
  <%block name="extra_head" />

</head>

<body>
  <div id="main">

    <header>
      <div id="logo">
        <div id="logo_text">
          <!-- class="logo_colour", allows you to change the colour of the text -->
          <h1><a href="/">Our<span class="logo_colour">Data</span></a></h1>
          <h2>Open Source Data Management Platform</h2>
        </div>
      </div><!--id:logo-->
    
    <%block name="navigation">
      <nav>
        <ul class="sf-menu" id="nav">
          <li><a href="/">Home</a></li>
          <li><a href="/signup">Signup</a></li>
          <li><a href="/about">About</a></li>
          <li><a href="/contact">Contact Us</a></li>
          <li><a href="https://github.com/dm03514/OurData.git">Github</a></li>
        </ul>
      </nav>
    </%block>

    </header>

    <div id="site_content">
        <div class="content">
            <%block name="content" />
        </div>
        <div class="sidebar_container">
            <div class="sidebar">
                <%block name="sidebar" />
            </div>
        </div>
    </div>

    <footer>
      <p>Copyright &copy; CSS3_photo_two | <a href="http://www.css3templates.co.uk">design from css3templates.co.uk</a></p>
    </footer>
  </div>

</body>
</html>
