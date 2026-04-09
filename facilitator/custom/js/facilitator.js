(function () {

	let observerAttached = false;

	function hidefilter() {

		if (
			frappe.get_route()[0] === 'List' &&
			frappe.get_route()[1] === 'Course' &&
			frappe.get_route()[2] === 'Calendar'
		) {
			console.log("🔥 Calendar View Loaded");

			if (!frappe.user.has_role('Course Attendance')) return;

			const hideFilters = () => {
				let el = document.querySelector('.filter-section');
				console.log("Trying to hide:", el);

				if (el) {
					el.style.display = 'none';
					console.log("✅ Hidden");
				}
			};

			// Initial attempts
			setTimeout(hideFilters, 500);
			setTimeout(hideFilters, 1500);

			// Attach observer ONLY ONCE
			if (!observerAttached) {
				const observer = new MutationObserver(() => {
					hideFilters();
				});

				observer.observe(document.body, {
					childList: true,
					subtree: true
				});

				observerAttached = true;
				console.log("👀 Observer attached");
			}
		}
	}

	// Run periodically (lightweight)
	setInterval(hidefilter, 1000);

})();