
document.addEventListener("DOMContentLoaded", function() {
    // Assuming your data is ready and the table is populated at this point
    // Show the table but keep the tbody content hidden initially
    var searchList = document.getElementById('search_list');
    searchList.style.display = "table"; // Make the table itself visible

    // Add the fade-in class to the table body to start the animation
    var tbody = searchList.getElementsByTagName('tbody')[0];
    tbody.classList.add("fade-in");
});
