"use strict";

document.documentElement.style.display = "none";

var loadCSS = function loadCSS() {
	// Check if we are at dev or prod docs url and load appropriate CSS
	var cssUrl = /dev/i.test(window.location.hostname)
		? "https://cdn.jsdelivr.net/gh/robo2323/python-open-controls@master/docs/_static/css/custom.css"
		: "https://cdn.jsdelivr.net/gh/robo2323/python-open-controls@master/docs/_static/css/custom.css";
	var head = document.getElementsByTagName("head")[0];
	var link = document.createElement("link");
	link.rel = "stylesheet";
	link.type = "text/css";
	link.href = cssUrl;
	link.media = "all";

	head.appendChild(link);
};

var changeH2Casing = function changeH2Casing() {
	var moduleNameRegex = /(qctrl)|\.|_/i;
	var h2elements = document.querySelectorAll("h2, h3");
	var h2ModuleTitles = [].concat(h2elements).filter(function(element) {
		var elText = element.innerText;
		return moduleNameRegex.test(elText);
	});
	h2ModuleTitles.forEach(function(element) {
		return (element.style.textTransform = "lowercase");
	});
};

var changeBreadcrumbsSeparator = function changeBreadcrumbsSeparator() {
	var breadCrumbsEl = document.querySelector(".wy-breadcrumbs");

	var newHTML = breadCrumbsEl.innerHTML
		.split("")
		.map(function(v) {
			return v === "»" ? ">" : v;
		})
		.join("");

	breadCrumbsEl.innerHTML = newHTML;
};

var fixNavHeader = function fixNavHeader() {
	var imageEl = document.querySelector(
		".wy-side-nav-search > a.icon img.logo"
	);
	var navHeaderEl = document.querySelector(".wy-side-nav-search > a");
	navHeaderEl.innerHTML = "";
	navHeaderEl.appendChild(imageEl);
};

var styleMobileNavHeader = function styleMobileNavHeader() {
	var navLogo = document.createElement("img");
	navLogo.src = "_static/logo.svg";
	navLogo.className = "logo";
	navLogo.alt = "Logo";
	var headerLinkEl = document.querySelector(".wy-nav-top a");
	headerLinkEl.innerHTML = "";
	headerLinkEl.appendChild(navLogo);
};

document.addEventListener("DOMContentLoaded", function() {
	loadCSS();
	changeH2Casing();
	changeBreadcrumbsSeparator();
	fixNavHeader();
	styleMobileNavHeader();
	document.documentElement.style.display = "block";
});
