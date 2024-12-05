
// Function that is used to add modules list/ input group to the form in course tab
function addModuleField() {
    const container = document.getElementById('module_container');
    const div = document.createElement('div');
    div.className = 'row mb-2';
    div.innerHTML = `
    <div class="col-md  m-auto p-1">
        <input type="text" name="module_name[]" class=" form-control" required placeholder="Module name">
    </div>
    <div class="col-md-8  m-auto p-1">
        <input type="text" name="module_desc[]" class=" form-control" required placeholder="Module description">
    </div>
    <div class="col-md  m-auto p-1">
        <button class="btn btn-danger" onclick="removeModuleField(this)">Remove</button>
    </div>
    `;
    container.appendChild(div);
}

function removeModuleField(button) {
    button.closest('.row').remove();
}


// Function that is used to switch between tabs  Main sidebar tabs.
function openTab(tabName, element) {
    // Hide all tab content
    var tabContents = document.getElementsByClassName("tab_content_main_sidebar");
    for (var i = 0; i < tabContents.length; i++) {
      tabContents[i].style.display = "none";
    }
  
    // Remove 'active' class from all tabs
    var tabs = document.getElementsByClassName("nav_link_main_sidebar");
    for (var i = 0; i < tabs.length; i++) {
      tabs[i].classList.remove("active");
    }
  
    // Show the selected tab content and mark its tab as active
    document.getElementById(tabName).style.display = "block";
    element.classList.add("active");
  }
  
  // Ensure the first tab is always displayed initially
  document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("Dashboard").style.display = "block";
  });


  // Function that is used to switch between tabs in user manager
function openTab_userManage_page(tabName, element) {
  // Hide all tab content
  var tabContents = document.getElementsByClassName("tab_content_manage");
  for (var i = 0; i < tabContents.length; i++) {
    tabContents[i].style.display = "none";
  }

  // Remove 'active' class from all tabs
  var tabs = document.getElementsByClassName("nav_link_user_manage");
  for (var i = 0; i < tabs.length; i++) {
    tabs[i].classList.remove("active");
  }

  // Show the selected tab content and mark its tab as active
  document.getElementById(tabName).style.display = "block";
  element.classList.add("active");
}

// Ensure the first tab is always displayed initially
document.addEventListener("DOMContentLoaded", function() {
  document.getElementById("Add_course").style.display = "block";
});

