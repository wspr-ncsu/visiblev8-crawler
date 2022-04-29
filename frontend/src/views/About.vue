<script>
	import ElementPlus from 'element-plus'
</script>

<template>
  <div>
	<div class="aboutInfo">
    	<h1>About</h1>
		<br>
		<h2>What is VisibleV8?</h2>
		<p>VisibleV8 (VV8) is a dynamic analysis framework created by Dr. Alexandros Kapravelos and Dr. Jordan
			Jueckstock. Hosted inside V8, the JS engine of the Chrome Browser, this framework logs native fuctions
			during JS execution. The VisibleV8 web application aims to make these logs user friendly and easy to
			understand. Please take a look at the links below for more information about the VisibleV8 project.</p>

		<br>
		<h2>What is VV8Web?</h2>
		<p>VV8Web is a web application dedicated to solving VV8's two biggest weaknesses: accessibility and results
			 legibility. This simple web application provides an easy to use access point to request VV8 jobs
			 without needing to install VV8 on your own device. Simply input a URL into the home page and follow
			 the prompts. It will then direct you to a results page where you can utilize our various visualization
			 tools to understand what VV8 has provided.</p>

		<br>
		<h2>Who made VV8Web?</h2>
		<img src="../assets/team_photo.jpg" />
		<p>VV8Web was developed by John Fagan, Ryan Rice, Quentin Davidson, Richardo Ma, and Scott Burnett as part
			of the North Carolina State University Senior Design Center.</p>

		<br>
		<h2>Sponsor Background</h2>
		
		<img src="../assets/DrK.jpg" />
		<p>Dr. Alexandros Kapravelos is an Assistant Professor in the Department of Computer Science at NC State
			University. He is a member of the Wolfpack Security and Privacy Research (WSPR) Lab and the faculty mentor
			of HackPack. He received his PhD in Computer Science from University of California, Santa Barbara in 2015.
			His research interests span the areas of systems and software security. Currently, he studies how the web
			changes on the client side via browser extensions and how we can protect the browser from malicious
			client-side attacks. He is also interested in Internet privacy and browser fingerprinting specifically,
			where he is working on making Internet users less distinctive while they browse the web. He is the lead
			developer of VisibleV8.</p>
		<br>
		<img src="../assets/LASLogo.png" />
		<p>LAS is a mission-oriented translational research lab focused on the development of new analytic technology
			and analysis tradecraft. The new technologies will help us understand the underlying scientific principles
			and analytics required to meet the complex and dynamic challenges presented by “Big Data.” The new
			tradecraft will help us discover, understand, and enhance critical aspects of intelligence analysis. These
			new technologies and tradecraft will be brought together through the development of user experiences that
			allow engagement with the data, tools, and techniques to achieve mission outcomes.</p>

		<br>
		<h2>Links</h2>
		<br>
		<p>If you are interested in how the backend of this project works, please take a look at the following links!</p>
		<br>
		<ul class="noBullets">
			<li><a href="https://kapravelos.com/publications/vv8-imc19.pdf">VisibleV8 Paper</a></li>
			<li><a href="https://github.com/wspr-ncsu/visiblev8">VisibleV8 GitHub</a></li>
			<li><a href="https://kapravelos.com/projects/vv8">VisibleV8 Website</a></li>
		</ul>
	</div>
  </div>
</template>

<style>
.aboutInfo{
	text-align: center;
	margin-left: 5%;
	margin-right: 5%;
}
.noBullets{
	list-style-type: none;
}
img{
	width: 30%;
}

</style>

