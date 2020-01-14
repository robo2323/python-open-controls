const changeH2Casing = () => {
	const moduleNameRegex = /(qctrl)|\./gi;
	const h2elements = document.querySelectorAll("h2");
	const h2ModuleTitles = [...h2elements].filter(element => {
		const elText = element.innerText;
		return moduleNameRegex.test(elText);
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

document.addEventListener("DOMContentLoaded", () => {
	changeH2Casing();
	changeBreadcrumbsSeparator();
});
