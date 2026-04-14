// (function () {

// 	let observerAttached = false;

// 	function hidefilter() {

// 		if (
// 			frappe.get_route()[0] === 'List' &&
// 			frappe.get_route()[1] === 'Course' &&
// 			frappe.get_route()[2] === 'Calendar'
// 		) {
// 			console.log("🔥 Calendar View Loaded");

// 			if (!frappe.user.has_role('Course Attendance')) return;

// 			const hideFilters = () => {
// 				let el = document.querySelector('.filter-section');
// 				console.log("Trying to hide:", el);

// 				if (el) {
// 					el.style.display = 'none';
// 					console.log("✅ Hidden");
// 				}
// 			};

// 			// Initial attempts
// 			setTimeout(hideFilters, 500);
// 			setTimeout(hideFilters, 1500);

// 			// Attach observer ONLY ONCE
// 			if (!observerAttached) {
// 				const observer = new MutationObserver(() => {
// 					hideFilters();
// 				});

// 				observer.observe(document.body, {
// 					childList: true,
// 					subtree: true
// 				});

// 				observerAttached = true;
// 				console.log("👀 Observer attached");
// 			}
// 		}
// 	}

// 	// Run periodically (lightweight)
// 	setInterval(hidefilter, 1000);

// })();

(function () {

  function HideSections() {
    try {
      // ✅ Use Frappe route (NOT window.location)
      const route = frappe.get_route_str();
      console.log("Current route:", route);

      // Check route
      if (!route || !route.includes("facilitator-dashboard")) {
        return;
      }

      console.log("On facilitator dashboard");

      // Check role
      if (!frappe.user.has_role('Course Attendance')) {
        console.log("User does NOT have role");
        return;
      }

      console.log("User has role → hide actions");

      // Target action bar
      const actionBar = document.querySelector(".page-actions");

      if (actionBar) {
        actionBar.style.display = "none";
        console.log("✅ Page actions hidden");
      } else {
        console.log("❌ .page-actions not found");
      }

    } catch (e) {
      console.error("Error in HideSections:", e);
    }
  }

  // ✅ Run when page is fully ready
  frappe.after_ajax(() => {
    setTimeout(HideSections, 300);
  });

  // ✅ Run on route change (SPA safe)
  if (frappe.router) {
    frappe.router.on("change", () => {
      setTimeout(HideSections, 300);
    });
  }

})();