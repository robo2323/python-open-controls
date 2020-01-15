const changeH2Casing = () => {
	const moduleNameRegex = /(qctrl)|\./gi;
	const h2elements = document.querySelectorAll("h2");
	const h2ModuleTitles = [...h2elements].filter(element => {
		const elText = element.innerText;
		return !moduleNameRegex.test(elText);
	});

	h2ModuleTitles.forEach(
		element => (element.style.textTransform = "uppercase")
	);
};

const changeBreadcrumbsSeparator = () => {
	const breadCrumbsEl = document.querySelector(".wy-breadcrumbs");

	[...breadCrumbsEl.children].forEach(el => {
		const newHTML = el.innerHTML
			.split(" ")
			.map(v => (v === "»" ? ">" : v))
			.join(" ");

		el.innerHTML = newHTML;
	});
};

const fixNavHeader = () => {
	const imageEl = document.querySelector(
		".wy-side-nav-search > a.icon img.logo"
	);
	const navHeaderEl = document.querySelector(".wy-side-nav-search > a");
	navHeaderEl.innerHTML = "";
	navHeaderEl.appendChild(imageEl);
};

const styleMobileNavHeader = () => {
	const navLogo = document.createElement("img");
	navLogo.src = "_static/logo.svg";
	navLogo.className = "logo";
	navLogo.alt = "Logo";

	const headerLinkEl = document.querySelector(".wy-nav-top a");
	headerLinkEl.innerHTML = "";
	headerLinkEl.appendChild(navLogo);
};

document.addEventListener("DOMContentLoaded", () => {
	changeH2Casing();
	changeBreadcrumbsSeparator();
	fixNavHeader();
	styleMobileNavHeader();
});
